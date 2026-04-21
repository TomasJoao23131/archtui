# ArchTUI

Instalador do Arch Linux com interface TUI interativa em português.

## Funcionalidades

- Interface TUI moderna usando Textual
- Navegação por teclado e rato
- Guia passo a passo com explicações
- 9 passos de instalação: Idioma, Teclado, Partições, Sistema Base, Bootloader, Utilizador, Desktop, Resumo, Instalação
- Sidebar com progresso visual
- Deteção de discos com `lsblk`
- Instalação real em modo automático com `sgdisk`, `pacstrap`, `genfstab` e `arch-chroot`

## Instalação

No live environment do Arch Linux:

```bash
curl -sL https://raw.githubusercontent.com/SEU_USUARIO/archtui/main/install.sh | bash
```

Se quiser usar `curl | bash`, troque `SEU_USUARIO/archtui` pelo URL real do seu repositório ou defina `ARCHTUI_REPO_URL`.

Ou manualmente:

```bash
git clone https://github.com/SEU_USUARIO/archtui.git
cd archtui
./install.sh
```

## Estrutura

```
archtui/
├── install.sh              # Script de instalação
├── installer/
│   ├── main.py             # Aplicação principal
│   ├── core/
│   │   ├── config.py       # Configuração do instalador
│   │   └── state.py        # Estado da instalação
│   └── ui/
│       ├── sidebar.py      # Componente sidebar
│       └── screens/
│           ├── welcome.py   # Ecrã de boas-vindas
│           ├── language.py # Seleção de idioma
│           ├── keyboard.py # Layout de teclado
│           ├── partition.py # Particionamento
│           ├── base.py     # Sistema base
│           ├── bootloader.py # Bootloader
│           ├── user.py     # Utilizador
│           ├── desktop.py  # Ambiente de trabalho
│           ├── summary.py  # Resumo
│           └── installation.py # Instalação
└── README.md
```

## Requisitos

- Arch Linux (live environment)
- Python 3.7+
- biblioteca Textual

## Uso

1. Inicie o live environment do Arch Linux
2. Conecte-se à internet
3. Clone o repositório ou execute o `install.sh`
4. Arranque a TUI com `./install.sh`
5. Escolha `Particionamento Automatico`
6. Selecione o disco alvo correto
7. Escreva `APAGAR` para confirmar a destruição do disco
8. Reveja o resumo e arranque a instalação

## Suportado Agora

- Instalação real apenas no liveboot oficial do Arch
- Apenas modo automático com apagamento total do disco
- GPT automático
- UEFI com partição EFI e raiz
- BIOS legacy com partição BIOS boot e raiz
- GRUB em BIOS ou UEFI
- `systemd-boot` e `rEFInd` apenas em UEFI
- Criação de utilizador, password root, hostname, locale, keymap e ativação do `NetworkManager`
- Ambientes: GNOME, KDE Plasma, XFCE, MATE, Cinnamon e CLI

## Limitações

- O modo manual ainda não está implementado
- Não cria swap automaticamente
- O timezone é configurado para `UTC`
- O URL do repositório em `install.sh` continua a precisar de ser ajustado para o teu repositório real

## Estado Atual

- A interface e a navegação estão funcionais
- As escolhas do utilizador são guardadas no resumo final
- O passo "Instalação" executa comandos reais do Arch em modo automático
- O instalador recusa correr fora do liveboot do Arch

## Controles

- **Enter**: Confirmar seleção
- **Tab**: Navegar entre elementos
- **q**: Sair
- **Rato**: Clicar em botões e selecionar opções
