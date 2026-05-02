<div align="center">
  <h1>🚀 ArchTUI</h1>
  <p><b>Instalador do Arch Linux com interface TUI interativa em português.</b></p>
</div>

---

## 📖 O que é?

O **ArchTUI** é um instalador guiado do Arch Linux que corre diretamente no terminal.
Em **9 passos simples**, ele configura e instala o Arch Linux no seu computador, de forma visual, amigável e sem a necessidade de memorizar dezenas de comandos complexos.

## ✨ Funcionalidades

- 🎨 **Interface TUI moderna** utilizando a excelente biblioteca [Textual](https://textual.textualize.io/)
- ⌨️ **Navegação 100% via teclado** optimizada para o TTY
- 📚 **Guia passo a passo** com explicações claras em cada ecrã
- 📊 **Barra lateral** com progresso visual (✓ completo, ▸ atual, ○ pendente)
- 💽 **Deteção automática de discos** recorrendo ao `lsblk`
- ⚙️ **Instalação real e automatizada** via `sgdisk`, `pacstrap`, `genfstab` e `arch-chroot`

## 🛤️ Os 9 Passos da Instalação

| Passo | O que configura |
|:-----:|-----------------|
| **1** | 🌍 **Idioma:** Locale do sistema (35+ idiomas suportados) |
| **2** | ⌨️ **Teclado:** Layout por país + variantes (no dead keys, Dvorak, etc.) |
| **3** | 💽 **Partições:** Disco alvo + particionamento automático GPT |
| **4** | 📦 **Sistema Base:** Hostname + pacotes base + extras opcionais |
| **5** | 🥾 **Bootloader:** GRUB, systemd-boot ou rEFInd |
| **6** | 👤 **Utilizador:** Nome, palavra-passe, sudo, root password |
| **7** | 🖥️ **Ambiente:** Desktop/WM (12 opções) + driver de vídeo |
| **8** | 📋 **Confirmar:** Revisão completa de todas as configurações |
| **9** | 🚀 **Instalação:** Execução real com barra de progresso + reboot automático |

## 🚀 Instalação e Uso

Inicie o computador com a pen drive do **live environment** oficial do Arch Linux. 

⚠️ **Atenção:** É necessária uma ligação à Internet ativa para descarregar o instalador. 
Se estiver a usar Wi-Fi, conecte-se primeiro executando o utilitário `iwctl`:
1. `iwctl` (para entrar na ferramenta)
2. `station wlan0 scan` (procurar redes)
3. `station wlan0 get-networks` (listar redes)
4. `station wlan0 connect NOME_DA_REDE` (ligar à rede)
5. `exit` (para sair)

Assim que o terminal abrir e estiver ligado à Internet, execute os seguintes comandos:

```bash
pacman -Sy --noconfirm git
git clone https://github.com/TomasJoao23131/archtui.git
cd archtui
bash install.sh
```

## 📂 Estrutura do Projeto

```text
archtui/
├── run.py                      # Ponto de entrada rápido
├── install.sh                  # Script de instalação e arranque (Bootstrapper)
├── requirements.txt            # Dependências Python (textual>=0.50.0)
└── installer/
    ├── main.py                 # App principal (Classe ArchTUI)
    ├── core/
    │   └── arch_installer.py   # Motor e comandos de instalação reais
    └── ui/
        ├── styles.tcss         # Estilos visuais e temas (CSS-like)
        ├── sidebar.py          # Sidebar reativa + Lógica de InstallerScreen
        └── screens/            # Diferentes ecrãs da aplicação
            ├── welcome.py      # Ecrã Inicial
            ├── language.py     # Passo 1
            ├── keyboard.py     # Passo 2
            ├── partition.py    # Passo 3
            ├── base.py         # Passo 4
            ├── bootloader.py   # Passo 5
            ├── user.py         # Passo 6
            ├── desktop.py      # Passo 7
            ├── summary.py      # Passo 8
            └── installation.py # Passo 9
```

## 📋 Requisitos para uso standalone

Caso queira testar a interface num sistema já instalado (modo simulação/teste UI):
- Python 3.10 ou superior
- Biblioteca Textual: `pip install textual`
*(O `install.sh` instala tudo automaticamente no live environment).*

## 🎮 Controlos da Interface

| Tecla / Ação | Função |
|-------------|--------|
| `↑` / `↓`   | Navegar entre opções numa lista |
| `Espaço`    | Marcar/desmarcar opções (ex: Checkboxes) |
| `Tab`       | Saltar para o campo seguinte no ecrã |
| `Shift+Tab` | Voltar ao campo anterior no ecrã |
| `Enter`     | Confirmar seleção atual |
| `q`         | Cancelar e sair do instalador |


## ✅ O que é suportado

- **Instalação completa** dentro do liveboot oficial do Arch Linux.
- **Particionamento automático** (apaga todo o disco e cria o esquema ideal).
  - **Sistemas de Ficheiros:** `ext4` (padrão) ou `BTRFS` (com criação automática de subvolumes `@`, `@home`, `@log`, `@pkg`, `@snapshots` para fácil integração com o Timeshift).
- **GPT Automático** suportado tanto em sistemas UEFI como BIOS/Legacy.
  - *UEFI:* Partição EFI (512 MB) + Raiz.
  - *BIOS:* Partição BIOS boot (1 MB) + Raiz.
- **Bootloaders:** GRUB (ambos UEFI/BIOS), systemd-boot (apenas UEFI), rEFInd (apenas UEFI).
- **Ambientes Desktop:** GNOME, KDE Plasma, XFCE, MATE, Cinnamon, Budgie, LXQt, Deepin, ou Modo CLI.
- **Window Managers:** i3, Sway, Hyprland — com auto-start configurado automaticamente.
- **Drivers de Vídeo:** Auto-deteção, Intel, AMD, NVIDIA (proprietário), Nouveau (NVIDIA open-source), VM (VMware/VirtualBox).
- **35+ idiomas** e **48+ layouts de teclado** com variantes (no dead keys, internacional, etc.).
- **Configuração de teclado** tanto para consola (vconsole) como para ambiente gráfico (X11/Wayland).
- **Criação de utilizador**, privilégios `sudo`, passwords, hostname, locale, keymap e seleção de **Shell** (`Bash`, `Zsh`, ou `Fish`).
- **Reboot automático** com countdown de 10 segundos após conclusão da instalação.
- **Otimização de mirrors** via `reflector` antes do `pacstrap` para downloads mais rápidos.
- **Gestão de Swap:** Escolha entre **ZRAM** (compactação rápida em RAM, recomendado), Swapfile (2GB, 4GB, 8GB) ou desativado.
- **50+ fusos horários** organizados por região.
- **Seleção de Kernel:** `linux` (padrão), `linux-lts` (estabilidade) ou `linux-zen` (gaming/desktop).
- **Instruções WiFi** integradas no ecrã inicial para ligação via `iwctl`.
- **16+ pacotes extras** opcionais, incluindo instalação nativa de **AUR Helpers** (`yay-bin`, `paru-bin`), Firefox, Git, PipeWire, Bluetooth, Flatpak, etc.
- **Ativação automática** do `NetworkManager` após instalar a interface.
- **Repositório Multilib** (`[multilib]`) configurável no ecrã inicial para suporte a aplicações de 32-bits (ex: Steam, Wine).

## 🚧 Limitações Atuais

- **Particionamento Manual:** Ainda não implementado (usar auto particionamento).
- **Disco Encryption (LUKS):** Ainda não suportado.
- **Ligação à Internet:** Obrigatória no live environment (via cabo ou Wi-Fi através de `iwctl`).
