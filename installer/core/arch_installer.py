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
        "budgie": ["budgie-desktop", "budgie-desktop-view", "gnome-terminal", "lightdm", "lightdm-gtk-greeter"],
        "lxqt": ["lxqt", "breeze-icons", "sddm"],
        "deepin": ["deepin", "deepin-extra", "lightdm", "lightdm-gtk-greeter"],
        "i3": ["i3-wm", "i3status", "i3lock", "dmenu", "alacritty", "xorg-xinit"],
        "sway": ["sway", "swaylock", "swayidle", "waybar", "wofi", "alacritty"],
        "hyprland": ["hyprland", "waybar", "wofi", "alacritty", "xdg-desktop-portal-hyprland"],
        "cli": [],
    }

    DISPLAY_SERVICES = {
        "gnome": "gdm",
        "kde": "sddm",
        "xfce": "lightdm",
        "mate": "lightdm",
        "cinnamon": "lightdm",
        "budgie": "lightdm",
        "lxqt": "sddm",
        "deepin": "lightdm",
    }

    # WMs que arrancam via .bash_profile (sem display manager)
    WM_LAUNCH_COMMANDS = {
        "i3": "exec startx",
        "sway": "exec sway",
        "hyprland": "exec Hyprland",
    }

    VIDEO_PACKAGES = {
        "auto": ["mesa", "xf86-video-vesa"],
        "intel": ["mesa", "xf86-video-intel"],
        "amd": ["mesa", "xf86-video-amdgpu"],
        "nvidia": ["nvidia", "nvidia-utils"],
        "nouveau": ["mesa", "xf86-video-nouveau"],
        "vm": ["xf86-video-vmware", "open-vm-tools"],
    }

    LOCALE_MAP = {
        "pt_BR": ("pt_BR.UTF-8 UTF-8", "pt_BR.UTF-8"),
        "pt_PT": ("pt_PT.UTF-8 UTF-8", "pt_PT.UTF-8"),
        "en_US": ("en_US.UTF-8 UTF-8", "en_US.UTF-8"),
        "en_GB": ("en_GB.UTF-8 UTF-8", "en_GB.UTF-8"),
        "es_ES": ("es_ES.UTF-8 UTF-8", "es_ES.UTF-8"),
        "es_MX": ("es_MX.UTF-8 UTF-8", "es_MX.UTF-8"),
        "es_AR": ("es_AR.UTF-8 UTF-8", "es_AR.UTF-8"),
        "fr_FR": ("fr_FR.UTF-8 UTF-8", "fr_FR.UTF-8"),
        "de_DE": ("de_DE.UTF-8 UTF-8", "de_DE.UTF-8"),
        "it_IT": ("it_IT.UTF-8 UTF-8", "it_IT.UTF-8"),
        "nl_NL": ("nl_NL.UTF-8 UTF-8", "nl_NL.UTF-8"),
        "ru_RU": ("ru_RU.UTF-8 UTF-8", "ru_RU.UTF-8"),
        "ja_JP": ("ja_JP.UTF-8 UTF-8", "ja_JP.UTF-8"),
        "zh_CN": ("zh_CN.UTF-8 UTF-8", "zh_CN.UTF-8"),
        "zh_TW": ("zh_TW.UTF-8 UTF-8", "zh_TW.UTF-8"),
        "ko_KR": ("ko_KR.UTF-8 UTF-8", "ko_KR.UTF-8"),
        "ar_EG": ("ar_EG.UTF-8 UTF-8", "ar_EG.UTF-8"),
        "pl_PL": ("pl_PL.UTF-8 UTF-8", "pl_PL.UTF-8"),
        "cs_CZ": ("cs_CZ.UTF-8 UTF-8", "cs_CZ.UTF-8"),
        "sv_SE": ("sv_SE.UTF-8 UTF-8", "sv_SE.UTF-8"),
        "nb_NO": ("nb_NO.UTF-8 UTF-8", "nb_NO.UTF-8"),
        "da_DK": ("da_DK.UTF-8 UTF-8", "da_DK.UTF-8"),
        "fi_FI": ("fi_FI.UTF-8 UTF-8", "fi_FI.UTF-8"),
        "hu_HU": ("hu_HU.UTF-8 UTF-8", "hu_HU.UTF-8"),
        "ro_RO": ("ro_RO.UTF-8 UTF-8", "ro_RO.UTF-8"),
        "tr_TR": ("tr_TR.UTF-8 UTF-8", "tr_TR.UTF-8"),
        "el_GR": ("el_GR.UTF-8 UTF-8", "el_GR.UTF-8"),
        "uk_UA": ("uk_UA.UTF-8 UTF-8", "uk_UA.UTF-8"),
        "ca_ES": ("ca_ES.UTF-8 UTF-8", "ca_ES.UTF-8"),
        "gl_ES": ("gl_ES.UTF-8 UTF-8", "gl_ES.UTF-8"),
        "eu_ES": ("eu_ES.UTF-8 UTF-8", "eu_ES.UTF-8"),
        "id_ID": ("id_ID.UTF-8 UTF-8", "id_ID.UTF-8"),
        "vi_VN": ("vi_VN.UTF-8 UTF-8", "vi_VN.UTF-8"),
        "th_TH": ("th_TH.UTF-8 UTF-8", "th_TH.UTF-8"),
        "hi_IN": ("hi_IN.UTF-8 UTF-8", "hi_IN.UTF-8"),
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
            self._create_swap()
            self._optimize_mirrors()
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
            self._run(["swapoff", "-a"], check=False)
            self._run(["umount", "-R", str(self.mountpoint)], check=False)
            self.finished = True

    def _validate(self) -> None:
        self.set_status("A validar ambiente liveboot...", 5)
        # Validar ligacao a internet para prevenir falhas fatais no pacstrap e perda de dados do utilizador
        if subprocess.run(["ping", "-c", "1", "archlinux.org"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
            raise ArchInstallError("Sem ligacao a Internet. Aborta para nao danificar o sistema atual.")
        geteuid = getattr(os, "geteuid", None)
        if geteuid is None or geteuid() != 0:
            raise ArchInstallError("A instalacao real precisa de correr como root.")
        if not Path("/run/archiso").exists():
            raise ArchInstallError("Instalacao real permitida apenas no liveboot do Arch.")
        if self.config.get("partition_method") != "auto":
            raise ArchInstallError("So o particionamento automatico esta implementado.")
        if not self.config.get("disk"):
            raise ArchInstallError("Nenhum disco foi selecionado.")
        fs = self.config.get("filesystem", "ext4")
        fs_cmd = "mkfs.btrfs" if fs == "btrfs" else "mkfs.ext4"
        for command in ("sgdisk", "wipefs", "mkfs.fat", fs_cmd, "mount", "pacstrap", "arch-chroot"):
            if not self._command_exists(command):
                raise ArchInstallError(f"Comando obrigatorio em falta: {command}")
        if not self._is_disk_device(self.config["disk"]):
            raise ArchInstallError("O disco selecionado nao e valido.")

        if not self._is_uefi() and self.config.get("bootloader") != "grub":
            raise ArchInstallError("Em BIOS legacy apenas o GRUB esta suportado.")

    def _prepare_partition_layout(self) -> None:
        disk = self.config["disk"]
        suffix = "p" if disk[-1].isdigit() else ""
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
        fs = self.config.get("filesystem", "ext4")
        if fs == "btrfs":
            self._run(["mkfs.btrfs", "-f", self.root_partition])
            self.mountpoint.mkdir(parents=True, exist_ok=True)
            self._run(["mount", self.root_partition, str(self.mountpoint)])
            self._run(["btrfs", "subvolume", "create", f"{self.mountpoint}/@"])
            self._run(["btrfs", "subvolume", "create", f"{self.mountpoint}/@home"])
            self._run(["btrfs", "subvolume", "create", f"{self.mountpoint}/@log"])
            self._run(["btrfs", "subvolume", "create", f"{self.mountpoint}/@pkg"])
            self._run(["btrfs", "subvolume", "create", f"{self.mountpoint}/@snapshots"])
            self._run(["btrfs", "subvolume", "create", f"{self.mountpoint}/@swap"])
            self._run(["umount", str(self.mountpoint)])
            
            # Mount subvolumes
            mount_opts = "rw,noatime,compress=zstd:1,space_cache=v2"
            self._run(["mount", "-o", f"{mount_opts},subvol=@", self.root_partition, str(self.mountpoint)])
            (self.mountpoint / "home").mkdir(parents=True, exist_ok=True)
            self._run(["mount", "-o", f"{mount_opts},subvol=@home", self.root_partition, str(self.mountpoint / "home")])
            (self.mountpoint / "var/log").mkdir(parents=True, exist_ok=True)
            self._run(["mount", "-o", f"{mount_opts},subvol=@log", self.root_partition, str(self.mountpoint / "var/log")])
            (self.mountpoint / "var/cache/pacman/pkg").mkdir(parents=True, exist_ok=True)
            self._run(["mount", "-o", f"{mount_opts},subvol=@pkg", self.root_partition, str(self.mountpoint / "var/cache/pacman/pkg")])
            (self.mountpoint / ".snapshots").mkdir(parents=True, exist_ok=True)
            self._run(["mount", "-o", f"{mount_opts},subvol=@snapshots", self.root_partition, str(self.mountpoint / ".snapshots")])
            (self.mountpoint / "swap").mkdir(parents=True, exist_ok=True)
            self._run(["mount", "-o", f"{mount_opts},subvol=@swap", self.root_partition, str(self.mountpoint / "swap")])
        else:
            self._run(["mkfs.ext4", "-F", self.root_partition])
            self.mountpoint.mkdir(parents=True, exist_ok=True)
            self._run(["mount", self.root_partition, str(self.mountpoint)])
        if self._is_uefi():
            self._run(["mkfs.fat", "-F32", self.efi_partition])
            boot_path = self.mountpoint / "boot"
            boot_path.mkdir(parents=True, exist_ok=True)
            self._run(["mount", self.efi_partition, str(boot_path)])

    def _create_swap(self) -> None:
        swap_size = self.config.get("swap_size", "2G")
        if swap_size == "none":
            self.log("Swap desativado pelo utilizador.")
            return
        if swap_size == "zram":
            self.log("ZRAM selecionado. Sera configurado via zram-generator.")
            return
        self.set_status(f"A criar swapfile de {swap_size}...", 35)
        swapfile = self.mountpoint / "swapfile"
        
        fs = self.config.get("filesystem", "ext4")
        if fs == "btrfs":
            swapfile = self.mountpoint / "swap/swapfile"
            # btrfs requer tratamento especial (chattr +C, no COW). O btrfs-progs trata disso.
            self._run(["btrfs", "filesystem", "mkswapfile", "--size", swap_size, str(swapfile)])
        else:
            # Criar ficheiro de swap padrao para ext4
            self._run(["dd", "if=/dev/zero", f"of={swapfile}", "bs=1M",
                       f"count={self._swap_size_mb(swap_size)}", "status=none"])
            self._run(["chmod", "600", str(swapfile)])
            self._run(["mkswap", str(swapfile)])
            
        self._run(["swapon", str(swapfile)])
        self.log(f"Swapfile de {swap_size} criado e ativado.")

    def _swap_size_mb(self, size: str) -> str:
        """Converte '2G' -> '2048', '4G' -> '4096', etc."""
        size = size.upper().strip()
        if size.endswith("G"):
            return str(int(size[:-1]) * 1024)
        if size.endswith("M"):
            return size[:-1]
        return "2048"

    def _optimize_mirrors(self) -> None:
        self.set_status("A otimizar mirrors com reflector...", 40)
        # Instalar reflector se nao estiver disponivel
        if not self._command_exists("reflector"):
            self._run(["pacman", "-Sy", "--noconfirm", "reflector"], check=False)
        if self._command_exists("reflector"):
            self._run([
                "reflector",
                "--latest", "10",
                "--sort", "rate",
                "--protocol", "https",
                "--save", "/etc/pacman.d/mirrorlist",
            ], check=False)
            self.log("Mirrors otimizados por velocidade.")
        else:
            self.log("Reflector nao disponivel, a usar mirrors predefinidos.")

    def _install_base_system(self) -> None:
        self.set_status("A instalar sistema base com pacstrap...", 45)
        packages = []
        if self.config.get("filesystem") == "btrfs":
            packages.append("btrfs-progs")
        if self.config.get("swap_size") == "zram":
            packages.append("zram-generator")
        shell = self.config.get("shell", "bash")
        if shell != "bash":
            packages.append(shell)
            
        packages.extend(self.config.get("packages", []))
        # Extras podem conter múltiplos pacotes numa string (e.g. "pipewire pipewire-pulse")
        for extra in self.config.get("extra_packages", []):
            if not extra.startswith("aur_"):
                packages.extend(extra.split())
                
        desktop = self.config.get("desktop", "cli")
        packages.extend(self.DESKTOP_PACKAGES.get(desktop, []))
        
        # Injetar pacotes de DM se o utilizador escolheu usar DM num Window Manager
        if self.config.get("use_dm", True) and desktop in self.WM_LAUNCH_COMMANDS:
            if desktop == "i3":
                packages.extend(["lightdm", "lightdm-gtk-greeter"])
            else:
                packages.extend(["sddm", "qt5-wayland", "qt6-wayland"])
                
        # Deteção de CPU (via /proc/cpuinfo) e injeção do microcode correto
        try:
            cpuinfo = Path("/proc/cpuinfo").read_text()
            if "AuthenticAMD" in cpuinfo:
                packages.append("amd-ucode")
            elif "GenuineIntel" in cpuinfo:
                packages.append("intel-ucode")
        except FileNotFoundError:
            pass

        packages.extend(self.VIDEO_PACKAGES.get(self.config.get("video_driver", "auto"), []))
        packages.extend(self._bootloader_packages())
        packages.extend(["linux-firmware", "networkmanager", "sudo"])
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
        shell = self.config.get("shell", "bash")

        if self.config.get("swap_size") == "zram":
            zram_conf = "[zram0]\nzram-size = ram / 2\ncompression-algorithm = zstd\nswap-priority = 100\n"
            self._write_target_file("/etc/systemd/zram-generator.conf", zram_conf)

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

        # Configurar teclado para X11/Wayland (além da consola)
        xkb_raw = self.config.get("xkb_layout", "us:")
        xkb_parts = xkb_raw.split(":", 1)
        xkb_layout = xkb_parts[0] if xkb_parts[0] else "us"
        xkb_variant = xkb_parts[1] if len(xkb_parts) > 1 and xkb_parts[1] else ""
        xkb_conf = (
            'Section "InputClass"\n'
            '    Identifier "system-keyboard"\n'
            '    MatchIsKeyboard "on"\n'
            f'    Option "XkbLayout" "{xkb_layout}"\n'
        )
        if xkb_variant:
            xkb_conf += f'    Option "XkbVariant" "{xkb_variant}"\n'
        xkb_conf += "EndSection\n"
        self._write_target_file("/etc/X11/xorg.conf.d/00-keyboard.conf", xkb_conf)
        
        # O Wayland (Sway) ignora xorg.conf. Vamos configurar um config system-wide para Sway.
        sway_kb_conf = f'input * {{\n    xkb_layout "{xkb_layout}"\n'
        if xkb_variant:
            sway_kb_conf += f'    xkb_variant "{xkb_variant}"\n'
        sway_kb_conf += '}\n'
        self._write_target_file("/etc/sway/config.d/00-keyboard.conf", sway_kb_conf)
        
        self.log(f"Teclado configurado: {xkb_layout}" + (f" ({xkb_variant})" if xkb_variant else ""))
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

        self._chroot(f"ln -sf /usr/share/zoneinfo/{shlex.quote(self.config.get('timezone', 'UTC'))} /etc/localtime")
        self._chroot("hwclock --systohc")
        self._chroot("locale-gen")
        self._chroot("systemctl enable NetworkManager")
        self.log(f"Timezone: {self.config.get('timezone', 'UTC')}")

        if self.config.get("multilib", True):
            pacman_conf = self._read_target_file("/etc/pacman.conf")
            pacman_conf = pacman_conf.replace(
                "#[multilib]\n#Include = /etc/pacman.d/mirrorlist",
                "[multilib]\nInclude = /etc/pacman.d/mirrorlist",
            )
            self._write_target_file("/etc/pacman.conf", pacman_conf)

        self._chroot(f"useradd -m -G wheel -s /bin/{shell} {shlex.quote(username)}")
        if self.config.get("sudo"):
            sudoers_path = self.mountpoint / "etc/sudoers.d/10-wheel"
            sudoers_path.write_text("%wheel ALL=(ALL:ALL) ALL\n", encoding="utf-8")
            self._chroot("chmod 440 /etc/sudoers.d/10-wheel")
        self._chroot("chpasswd", input_text=f"root:{root_password}\n")
        self._chroot("chpasswd", input_text=f"{username}:{user_password}\n")

        desktop = self.config.get("desktop", "cli")
        display_service = self.DISPLAY_SERVICES.get(desktop)
        
        # Sobrescrever display_service se o user pediu DM num Window Manager
        if self.config.get("use_dm", True) and desktop in self.WM_LAUNCH_COMMANDS:
            display_service = "lightdm" if desktop == "i3" else "sddm"

        if display_service:
            self._chroot(f"systemctl enable {shlex.quote(display_service)}")
        elif desktop in self.WM_LAUNCH_COMMANDS:
            # WMs sem display manager: auto-start via TTY login
            launch_cmd = self.WM_LAUNCH_COMMANDS[desktop]
            username = self.config.get("username", "user")
            
            # Para Bash
            bash_profile = f"/home/{username}/.bash_profile"
            bash_code = f'\n# Auto-start {desktop}\nif [ -z "$DISPLAY" ] && [ "$XDG_VTNR" -eq 1 ]; then\n    {launch_cmd}\nfi\n'
            self._write_target_file(bash_profile, self._read_target_file(bash_profile) + bash_code)
            self._chroot(f"chown {shlex.quote(username)}:{shlex.quote(username)} {bash_profile}")
            
            # Para Zsh
            zsh_profile = f"/home/{username}/.zprofile"
            self._write_target_file(zsh_profile, self._read_target_file(zsh_profile) + bash_code)
            self._chroot(f"chown {shlex.quote(username)}:{shlex.quote(username)} {zsh_profile}")
            
            # Para Fish
            fish_dir = f"/home/{username}/.config/fish"
            fish_conf = f"{fish_dir}/config.fish"
            fish_code = f'\n# Auto-start {desktop}\nif status is-login\n    if test -z "$DISPLAY" -a "$XDG_VTNR" = 1\n        {launch_cmd}\n    end\nend\n'
            self._chroot(f"mkdir -p {fish_dir}", check=False)
            self._write_target_file(fish_conf, self._read_target_file(fish_conf) + fish_code)
            self._chroot(f"chown -R {shlex.quote(username)}:{shlex.quote(username)} /home/{username}/.config", check=False)
            # i3 precisa do xorg-server
            if desktop == "i3":
                self._chroot("pacman -S --noconfirm xorg-server xorg-xinit", check=False)
                xinit_content = "exec i3\n"
                xinitrc_path = f"/home/{username}/.xinitrc"
                self._write_target_file(xinitrc_path, xinit_content)
                self._chroot(f"chown {shlex.quote(username)}:{shlex.quote(username)} {xinitrc_path}")
            self.log(f"{desktop} sera iniciado automaticamente ao fazer login.")

        if self.config.get("video_driver") == "vm":
            self._chroot("systemctl enable vmtoolsd", check=False)

        # Injetar variáveis de ambiente críticas para estabilidade Wayland (VMs, NVIDIA, drivers legacy)
        if desktop in ("sway", "hyprland"):
            env_content = self._read_target_file("/etc/environment")
            if "WLR_NO_HARDWARE_CURSORS" not in env_content:
                env_add = "\n# Wayland / VM Compatibility\nWLR_NO_HARDWARE_CURSORS=1\nWLR_RENDERER_ALLOW_SOFTWARE=1\n"
                self._write_target_file("/etc/environment", env_content + env_add)

        # Install AUR Helper
        aur_helpers = [pkg for pkg in self.config.get("extra_packages", []) if pkg.startswith("aur_")]
        if aur_helpers:
            self.set_status("A compilar AUR Helper (aguarde uns minutos)...", 80)
            self._chroot("pacman -S --noconfirm --needed git base-devel", check=False)
            for aur in aur_helpers:
                if aur == "aur_yay":
                    repo_url = "https://aur.archlinux.org/yay-bin.git"
                    target_dir = "/tmp/yay-bin"
                elif aur == "aur_paru":
                    repo_url = "https://aur.archlinux.org/paru-bin.git"
                    target_dir = "/tmp/paru-bin"
                
                self._chroot(f"git clone {repo_url} {target_dir}", check=False)
                self._chroot(f"chown -R {shlex.quote(username)}:{shlex.quote(username)} {target_dir}", check=False)
                self._chroot(f"sudo -u {shlex.quote(username)} bash -c 'cd {target_dir} && makepkg -si --noconfirm'", check=False)

    def _install_bootloader(self) -> None:
        self.set_status("A instalar bootloader...", 85)
        bootloader = self.config.get("bootloader", "grub")
        disk = self.config["disk"]
        
        # Parâmetros de kernel extras dependentes do hardware
        kernel_opts = ""
        if self.config.get("video_driver") == "nvidia":
            kernel_opts += " nvidia-drm.modeset=1"

        if bootloader == "grub":
            if kernel_opts:
                grub_conf = self._read_target_file("/etc/default/grub")
                # Injetar parametros no grub config padrao
                grub_conf = grub_conf.replace('GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet"', f'GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet{kernel_opts}"')
                self._write_target_file("/etc/default/grub", grub_conf)
                
            if self._is_uefi():
                self._chroot("grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ArchTUI")
            else:
                self._chroot(f"grub-install --target=i386-pc {shlex.quote(disk)}")
            self._chroot("grub-mkconfig -o /boot/grub/grub.cfg")
            return

        if bootloader == "systemd-boot":
            kernel = self.config.get("kernel", "linux")
            root_uuid = self._get_blkid_value(self.root_partition, "UUID")
            self._chroot("bootctl --path=/boot install")
            self._write_target_file(
                "/boot/loader/loader.conf",
                "default arch.conf\ntimeout 3\neditor no\n",
            )
            options = f"root=UUID={root_uuid} rw"
            if kernel_opts:
                options += kernel_opts
            if self.config.get("filesystem") == "btrfs":
                options += " rootflags=subvol=@"
                
            entries = ["title   Arch Linux", f"linux   /vmlinuz-{kernel}"]
            if (self.mountpoint / "boot/amd-ucode.img").exists():
                entries.append("initrd  /amd-ucode.img")
            if (self.mountpoint / "boot/intel-ucode.img").exists():
                entries.append("initrd  /intel-ucode.img")
            entries.append(f"initrd  /initramfs-{kernel}.img")
            entries.append(f"options {options}")
            entries.append("")

            self._write_target_file(
                "/boot/loader/entries/arch.conf",
                "\n".join(entries),
            )
            return

        if bootloader == "refind":
            self._chroot("refind-install")
            return

        raise ArchInstallError("Bootloader selecionado nao suportado.")

    def _finalize(self) -> None:
        self.set_status("A finalizar instalacao...", 95)
        self._run(["sync"])
        # Desmontar partições
        self._run(["umount", "-R", str(self.mountpoint)], check=False)
        self.log("Instalacao concluida com sucesso!")
        self.log("O sistema sera reiniciado automaticamente em 10 segundos...")
        self.log("(ou clica em 'Reiniciar Agora')")

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
            self._run(["arch-chroot", str(self.mountpoint), "/bin/bash", "-lc", command], check=check, input_text=input_text)
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
        try:
            return path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ""

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
