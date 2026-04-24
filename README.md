# ArchTUI

Instalador do Arch Linux com interface TUI interativa em português.

## O que é?

O ArchTUI é um instalador guiado do Arch Linux que corre no terminal.
Em 9 passos simples, configura e instala o Arch Linux no seu computador,
sem precisar de memorizar comandos.

## Funcionalidades

- Interface TUI moderna usando [Textual](https://textual.textualize.io/)
- Navegação por teclado e rato
- Guia passo a passo com explicações claras em cada ecrã
- Barra lateral com progresso visual (✓ completo, ▸ atual, ○ pendente)
- Deteção automática de discos com `lsblk`
- Instalação real com `sgdisk`, `pacstrap`, `genfstab` e `arch-chroot`

## Os 9 Passos

| Passo | O que configura |
|-------|-----------------|
| 1. Idioma | Locale do sistema (pt_BR, pt_PT, en_US, es_ES) |
| 2. Teclado | Layout da consola (ABNT2, QWERTY PT, US, ES) |
| 3. Partições | Disco alvo + particionamento automático GPT |
| 4. Sistema Base | Hostname + pacotes base + extras opcionais |
| 5. Bootloader | GRUB, systemd-boot ou rEFInd |
| 6. Utilizador | Nome, palavra-passe, sudo, root password |
| 7. Ambiente | Desktop (GNOME/KDE/XFCE/etc.) + driver de vídeo |
| 8. Resumo | Revisão de tudo antes de instalar |
| 9. Instalação | Execução real com progresso e logs |

## Instalação

No live environment do Arch Linux:

```bash
# Opção 1: Clonar e correr
git clone https://github.com/SEU_USUARIO/archtui.git
cd archtui
sudo ./install.sh

# Opção 2: Usar curl (defina o URL do repositório)
ARCHTUI_REPO_URL=https://github.com/SEU_USUARIO/archtui.git \
  curl -sL https://raw.githubusercontent.com/SEU_USUARIO/archtui/main/install.sh | sudo bash
```

> **Nota:** Substitua `SEU_USUARIO` pelo seu nome de utilizador no GitHub.

## Estrutura

```
archtui/
├── run.py                      # Ponto de entrada
├── install.sh                  # Script de instalação e arranque
├── requirements.txt            # Dependência: textual>=0.50.0
└── installer/
    ├── main.py                 # App principal (ArchTUI)
    ├── core/
    │   └── arch_installer.py   # Motor de instalação real
    └── ui/
        ├── styles.tcss         # Estilos visuais (tema Arch)
        ├── sidebar.py          # Sidebar reativa + InstallerScreen
        └── screens/
            ├── welcome.py      # Boas-vindas
            ├── language.py     # Passo 1 — Idioma
            ├── keyboard.py     # Passo 2 — Teclado
            ├── partition.py    # Passo 3 — Partições
            ├── base.py         # Passo 4 — Sistema Base
            ├── bootloader.py   # Passo 5 — Bootloader
            ├── user.py         # Passo 6 — Utilizador
            ├── desktop.py      # Passo 7 — Ambiente
            ├── summary.py      # Passo 8 — Resumo
            └── installation.py # Passo 9 — Instalação
```

## Requisitos

- Arch Linux (live environment)
- Python 3.10+
- Biblioteca Textual (`pip install textual`)

## Controlos

| Tecla | Ação |
|-------|------|
| ↑ ↓ | Navegar entre opções |
| Enter | Confirmar seleção |
| Tab | Saltar entre campos |
| q | Sair do instalador |
| Rato | Clicar em botões e opções |

## Suportado

- Instalação completa no liveboot oficial do Arch
- Particionamento automático com apagamento total do disco
- GPT automático (UEFI ou BIOS legacy)
- UEFI: partição EFI (512 MB) + raiz
- BIOS: partição BIOS boot (1 MB) + raiz
- Bootloaders: GRUB (UEFI/BIOS), systemd-boot (UEFI), rEFInd (UEFI)
- Ambientes: GNOME, KDE Plasma, XFCE, MATE, Cinnamon, CLI
- Drivers de vídeo: auto, Intel, AMD, NVIDIA, VM
- Criação de utilizador, sudo, passwords, hostname, locale, keymap
- Ativação automática do NetworkManager

## Limitações

- Particionamento manual ainda não implementado
- Não cria partição swap automaticamente
- Timezone fixo em UTC
- Requer ligação à internet no live environment
