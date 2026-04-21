import os
import shlex
import subprocess
from pathlib import Path
from shutil import which


class ArchInstallError(RuntimeError):
    pass


def detect_disks() -> list[dict]:
    try:
        result = subprocess.run(
            ["lsblk", "-dpno", "NAME,SIZE,MODEL,TYPE"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []

    disks: list[dict] = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 3 or parts[-1] != "disk":
            continue
        name = parts[0]
        size = parts[1]
        model = " ".join(parts[2:-1]) or "Disco"
        disks.append(
            {
                "path": name,
                "size": size,
                "model": model,
                "label": f"{name} - {size} - {model}",
            }
        )
    return disks


class ArchInstaller:
    DESKTOP_PACKAGES = {
        "gnome": ["gnome", "gdm"],
        "kde": ["plasma", "sddm"],
        "xfce": ["xfce4", "xfce4-goodies", "lightdm", "lightdm-gtk-greeter"],
        "mate": ["mate", "mate-extra", "lightdm", "lightdm-gtk-greeter"],
        "cinnamon": ["cinnamon", "lightdm", "lightdm-gtk-greeter"],
        "cli": [],
    }

    DISPLAY_SERVICES = {
        "gnome": "gdm",
        "kde": "sddm",
        "xfce": "lightdm",
        "mate": "lightdm",
        "cinnamon": "lightdm",
    }

    VIDEO_PACKAGES = {
        "auto": ["mesa", "xf86-video-vesa"],
        "intel": ["mesa", "xf86-video-intel"],
        "amd": ["mesa", "xf86-video-amdgpu"],
        "nvidia": ["nvidia", "nvidia-utils"],
        "vm": ["xf86-video-vmware", "open-vm-tools"],
    }

    LOCALE_MAP = {
        "pt_BR": ("pt_BR.UTF-8 UTF-8", "pt_BR.UTF-8"),
        "pt_PT": ("pt_PT.UTF-8 UTF-8", "pt_PT.UTF-8"),
        "en_US": ("en_US.UTF-8 UTF-8", "en_US.UTF-8"),
        "es_ES": ("es_ES.UTF-8 UTF-8", "es_ES.UTF-8"),
    }

    def __init__(self, config: dict):
        self.config = config
        self.progress = 0
        self.status = "Por iniciar"
        self.logs: list[str] = []
        self.error: str | None = None
        self.finished = False
        self.success = False
        self.mountpoint = Path("/mnt")

    def log(self, message: str) -> None:
        self.logs.append(message)

    def set_status(self, message: str, progress: int) -> None:
        self.status = message
        self.progress = progress
        self.log(message)

    def run(self) -> None:
        try:
            self._validate()
            self._prepare_partition_layout()
            self._partition_disk()
            self._format_and_mount()
            self._install_base_system()
            self._generate_fstab()
            self._configure_system()
            self._install_bootloader()
            self._finalize()
            self.status = "Instalacao concluida com sucesso."
            self.progress = 100
            self.success = True
            self.log("Instalacao concluida com sucesso.")
        except Exception as exc:
            self.error = str(exc)
            self.status = f"Erro: {exc}"
            self.log(self.status)
        finally:
            self.finished = True

    def _validate(self) -> None:
        self.set_status("A validar ambiente liveboot...", 5)
        geteuid = getattr(os, "geteuid", None)
        if geteuid is None or geteuid() != 0:
            raise ArchInstallError("A instalacao real precisa de correr como root.")
        if not Path("/run/archiso").exists():
            raise ArchInstallError("Instalacao real permitida apenas no liveboot do Arch.")
        if self.config.get("partition_method") != "auto":
            raise ArchInstallError("So o particionamento automatico esta implementado.")
        if not self.config.get("disk"):
            raise ArchInstallError("Nenhum disco foi selecionado.")
        for command in ("sgdisk", "wipefs", "mkfs.fat", "mkfs.ext4", "mount", "pacstrap", "arch-chroot"):
            if not self._command_exists(command):
                raise ArchInstallError(f"Comando obrigatorio em falta: {command}")
        if not self._is_disk_device(self.config["disk"]):
            raise ArchInstallError("O disco selecionado nao e valido.")

        if not self._is_uefi() and self.config.get("bootloader") != "grub":
            raise ArchInstallError("Em BIOS legacy apenas o GRUB esta suportado.")

    def _prepare_partition_layout(self) -> None:
        disk = self.config["disk"]
        suffix = "p" if disk.startswith("/dev/nvme") or disk.startswith("/dev/mmcblk") else ""
        if self._is_uefi():
            self.efi_partition = f"{disk}{suffix}1"
            self.root_partition = f"{disk}{suffix}2"
            self.partition_plan = "UEFI: EFI + raiz"
        else:
            self.bios_partition = f"{disk}{suffix}1"
            self.root_partition = f"{disk}{suffix}2"
            self.partition_plan = "BIOS: BIOS boot + raiz"
        self.log(f"Plano de particoes: {self.partition_plan}")

    def _partition_disk(self) -> None:
        disk = self.config["disk"]
        self.set_status(f"A particionar {disk}...", 15)
        self._run(["swapoff", "-a"], check=False)
        self._run(["umount", "-R", str(self.mountpoint)], check=False)
        self._run(["wipefs", "-af", disk])
        self._run(["sgdisk", "--zap-all", disk])
        if self._is_uefi():
            self._run(["sgdisk", "-n", "1:0:+512M", "-t", "1:ef00", "-c", "1:EFI", disk])
            self._run(["sgdisk", "-n", "2:0:0", "-t", "2:8300", "-c", "2:arch-root", disk])
        else:
            self._run(["sgdisk", "-n", "1:0:+1M", "-t", "1:ef02", "-c", "1:bios-boot", disk])
            self._run(["sgdisk", "-n", "2:0:0", "-t", "2:8300", "-c", "2:arch-root", disk])
        self._run(["partprobe", disk], check=False)

    def _format_and_mount(self) -> None:
        self.set_status("A formatar e montar particoes...", 30)
        self._run(["mkfs.ext4", "-F", self.root_partition])
        self.mountpoint.mkdir(parents=True, exist_ok=True)
        self._run(["mount", self.root_partition, str(self.mountpoint)])
        if self._is_uefi():
            self._run(["mkfs.fat", "-F32", self.efi_partition])
            boot_path = self.mountpoint / "boot"
            boot_path.mkdir(parents=True, exist_ok=True)
            self._run(["mount", self.efi_partition, str(boot_path)])

    def _install_base_system(self) -> None:
        self.set_status("A instalar sistema base com pacstrap...", 45)
        packages = []
        packages.extend(self.config.get("packages", []))
        packages.extend(self.config.get("extra_packages", []))
        packages.extend(self.DESKTOP_PACKAGES.get(self.config.get("desktop", "cli"), []))
        packages.extend(self.VIDEO_PACKAGES.get(self.config.get("video_driver", "auto"), []))
        packages.extend(self._bootloader_packages())
        packages.extend(["linux", "linux-firmware", "networkmanager", "sudo"])
        final_packages = self._unique(packages)
        self.log(f"Pacotes: {' '.join(final_packages)}")
        self._run(["pacstrap", str(self.mountpoint), *final_packages])

    def _generate_fstab(self) -> None:
        self.set_status("A gerar fstab...", 55)
        result = subprocess.run(
            ["genfstab", "-U", str(self.mountpoint)],
            check=True,
            capture_output=True,
            text=True,
        )
        fstab_path = self.mountpoint / "etc/fstab"
        with fstab_path.open("a", encoding="utf-8") as fstab_file:
            fstab_file.write(result.stdout)
        self.log("fstab gerado.")

    def _configure_system(self) -> None:
        self.set_status("A configurar sistema instalado...", 70)
        locale_gen, lang = self.LOCALE_MAP.get(
            self.config.get("language", "en_US"),
            self.LOCALE_MAP["en_US"],
        )
        hostname = self.config.get("hostname", "archlinux")
        keymap = self.config.get("keyboard", "us")
        username = self.config.get("username", "user")
        user_password = self.config.get("password", "")
        root_password = self.config.get("root_password", user_password)

        self._write_target_file(
            "/etc/locale.gen",
            self._replace_or_append(
                self._read_target_file("/etc/locale.gen"),
                f"#{locale_gen}",
                locale_gen,
            ),
        )
        self._write_target_file("/etc/locale.conf", f"LANG={lang}\n")
        self._write_target_file("/etc/vconsole.conf", f"KEYMAP={keymap}\n")
        self._write_target_file("/etc/hostname", f"{hostname}\n")
        self._write_target_file(
            "/etc/hosts",
            "\n".join(
                [
                    "127.0.0.1\tlocalhost",
                    "::1\tlocalhost",
                    f"127.0.1.1\t{hostname}.localdomain\t{hostname}",
                    "",
                ]
            ),
        )

        self._chroot("ln -sf /usr/share/zoneinfo/UTC /etc/localtime")
        self._chroot("hwclock --systohc")
        self._chroot("locale-gen")
        self._chroot("systemctl enable NetworkManager")

        if self.config.get("multilib", True):
            pacman_conf = self._read_target_file("/etc/pacman.conf")
            pacman_conf = pacman_conf.replace(
                "#[multilib]\n#Include = /etc/pacman.d/mirrorlist",
                "[multilib]\nInclude = /etc/pacman.d/mirrorlist",
            )
            self._write_target_file("/etc/pacman.conf", pacman_conf)

        self._chroot(f"useradd -m -G wheel -s /bin/bash {shlex.quote(username)}")
        if self.config.get("sudo"):
            sudoers_path = self.mountpoint / "etc/sudoers.d/10-wheel"
            sudoers_path.write_text("%wheel ALL=(ALL:ALL) ALL\n", encoding="utf-8")
        self._chroot("chpasswd", input_text=f"root:{root_password}\n")
        self._chroot("chpasswd", input_text=f"{username}:{user_password}\n")

        display_service = self.DISPLAY_SERVICES.get(self.config.get("desktop", "cli"))
        if display_service:
            self._chroot(f"systemctl enable {shlex.quote(display_service)}")

        if self.config.get("video_driver") == "vm":
            self._chroot("systemctl enable vmtoolsd", check=False)

    def _install_bootloader(self) -> None:
        self.set_status("A instalar bootloader...", 85)
        bootloader = self.config.get("bootloader", "grub")
        disk = self.config["disk"]
        if bootloader == "grub":
            if self._is_uefi():
                self._chroot("grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ArchTUI")
            else:
                self._chroot(f"grub-install --target=i386-pc {shlex.quote(disk)}")
            self._chroot("grub-mkconfig -o /boot/grub/grub.cfg")
            return

        if bootloader == "systemd-boot":
            root_uuid = self._get_blkid_value(self.root_partition, "UUID")
            self._chroot("bootctl --path=/boot install")
            self._write_target_file(
                "/boot/loader/loader.conf",
                "default arch.conf\ntimeout 3\neditor no\n",
            )
            self._write_target_file(
                "/boot/loader/entries/arch.conf",
                "\n".join(
                    [
                        "title   Arch Linux",
                        "linux   /vmlinuz-linux",
                        "initrd  /initramfs-linux.img",
                        f"options root=UUID={root_uuid} rw",
                        "",
                    ]
                ),
            )
            return

        if bootloader == "refind":
            self._chroot("refind-install")
            return

        raise ArchInstallError("Bootloader selecionado nao suportado.")

    def _finalize(self) -> None:
        self.set_status("A finalizar instalacao...", 95)
        self._run(["sync"])
        self.log("Podes sair, rever `/mnt` ou reiniciar quando quiseres.")

    def _run(self, command: list[str], check: bool = True, input_text: str | None = None) -> None:
        self.log(f"$ {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, input=input_text)
        if result.stdout:
            for line in result.stdout.splitlines():
                self.log(line)
        if result.stderr:
            for line in result.stderr.splitlines():
                self.log(line)
        if check and result.returncode != 0:
            raise ArchInstallError(f"Falhou comando: {' '.join(command)}")

    def _chroot(self, command: str, check: bool = True, input_text: str | None = None) -> None:
        if input_text is not None:
            self._run(["arch-chroot", str(self.mountpoint), command], check=check, input_text=input_text)
            return
        self._run(["arch-chroot", str(self.mountpoint), "/bin/bash", "-lc", command], check=check)

    def _bootloader_packages(self) -> list[str]:
        bootloader = self.config.get("bootloader", "grub")
        if bootloader == "grub":
            return ["grub", "efibootmgr"] if self._is_uefi() else ["grub"]
        if bootloader == "systemd-boot":
            return ["efibootmgr"]
        if bootloader == "refind":
            return ["refind", "efibootmgr"]
        return []

    def _command_exists(self, command: str) -> bool:
        return which(command) is not None

    def _is_uefi(self) -> bool:
        return Path("/sys/firmware/efi").exists()

    def _is_disk_device(self, path: str) -> bool:
        return any(disk["path"] == path for disk in detect_disks())

    def _get_blkid_value(self, device: str, key: str) -> str:
        result = subprocess.run(
            ["blkid", "-s", key, "-o", "value", device],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def _read_target_file(self, relative_path: str) -> str:
        path = self.mountpoint / relative_path.lstrip("/")
        return path.read_text(encoding="utf-8")

    def _write_target_file(self, relative_path: str, content: str) -> None:
        path = self.mountpoint / relative_path.lstrip("/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _replace_or_append(self, content: str, old: str, new: str) -> str:
        if old in content:
            return content.replace(old, new)
        if new in content:
            return content
        return f"{content.rstrip()}\n{new}\n"

    def _unique(self, items: list[str]) -> list[str]:
        seen = set()
        unique_items = []
        for item in items:
            if not item or item in seen:
                continue
            seen.add(item)
            unique_items.append(item)
        return unique_items
