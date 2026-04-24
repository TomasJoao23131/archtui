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
- 🖱️ **Navegação versátil** suportando teclado e rato
- 📚 **Guia passo a passo** com explicações claras em cada ecrã
- 📊 **Barra lateral** com progresso visual (✓ completo, ▸ atual, ○ pendente)
- 💽 **Deteção automática de discos** recorrendo ao `lsblk`
- ⚙️ **Instalação real e automatizada** via `sgdisk`, `pacstrap`, `genfstab` e `arch-chroot`

## 🛤️ Os 9 Passos da Instalação

| Passo | O que configura |
|:-----:|-----------------|
| **1** | 🌍 **Idioma:** Locale do sistema (pt_BR, pt_PT, en_US, es_ES) |
| **2** | ⌨️ **Teclado:** Layout da consola (ABNT2, QWERTY PT, US, ES) |
| **3** | 💽 **Partições:** Disco alvo + particionamento automático GPT |
| **4** | 📦 **Sistema Base:** Hostname + pacotes base + extras opcionais |
| **5** | 🥾 **Bootloader:** GRUB, systemd-boot ou rEFInd |
| **6** | 👤 **Utilizador:** Nome, palavra-passe, sudo, root password |
| **7** | 🖥️ **Ambiente:** Desktop (GNOME, KDE, XFCE, etc.) + driver de vídeo |
| **8** | 📋 **Resumo:** Revisão completa de todas as configurações |
| **9** | 🚀 **Instalação:** Execução real com barra de progresso e logs detalhados |

## 🚀 Instalação e Uso

Inicie o computador com a pen drive do **live environment** oficial do Arch Linux. Assim que o terminal abrir, execute um dos métodos abaixo:

### Método 1: Download Rápido (Recomendado)
Faça o download do script e execute diretamente:
```bash
ARCHTUI_REPO_URL=https://github.com/TomasJoao23131/archtui.git \
  curl -sL https://raw.githubusercontent.com/TomasJoao23131/archtui/main/install.sh | sudo bash
```

### Método 2: Clonar o Repositório Manualmente
Se preferir, pode clonar e inspecionar o código antes de executar:
```bash
git clone https://github.com/TomasJoao23131/archtui.git
cd archtui
sudo ./install.sh
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
| `Enter`     | Confirmar seleção atual |
| `Tab`       | Saltar entre os diferentes campos no ecrã |
| `q`         | Cancelar e sair do instalador |
| `Rato`      | Clicar livremente em botões, abas e listas |

## ✅ O que é suportado

- **Instalação completa** dentro do liveboot oficial do Arch Linux.
- **Particionamento automático** (apaga todo o disco e cria o esquema ideal).
- **GPT Automático** suportado tanto em sistemas UEFI como BIOS/Legacy.
  - *UEFI:* Partição EFI (512 MB) + Raiz.
  - *BIOS:* Partição BIOS boot (1 MB) + Raiz.
- **Bootloaders:** GRUB (ambos UEFI/BIOS), systemd-boot (apenas UEFI), rEFInd (apenas UEFI).
- **Ambientes Desktop:** GNOME, KDE Plasma, XFCE, MATE, Cinnamon, ou Modo CLI (Sem desktop).
- **Drivers de Vídeo:** Auto-deteção, Intel, AMD, NVIDIA, Virtual Machine (VMware/VirtualBox).
- Criação de utilizador, privilégios `sudo`, configuração de senhas, hostname, locale e keymap da consola.
- **Ativação automática** do `NetworkManager` após instalar a interface.

## 🚧 Limitações Atuais

- **Particionamento Manual:** Ainda não implementado (usar auto particionamento).
- **Swap:** Atualmente o script não cria partição `swap` automaticamente.
- **Timezone:** Encontra-se fixo em `UTC` por predefinição.
- **Ligação à Internet:** Obrigatória no live environment (via cabo ou Wi-Fi através de `iwctl`).
