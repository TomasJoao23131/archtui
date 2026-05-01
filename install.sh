#!/bin/bash
set -euo pipefail

# ============================================================
# ArchTUI — Script de instalação e arranque
# Corre no live environment do Arch Linux como root.
# ============================================================

if [[ $EUID -ne 0 ]]; then
   echo "Erro: Este script precisa de ser executado como root."
   echo "  Exemplo: sudo ./install.sh"
   exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${ARCHTUI_TARGET_DIR:-/opt/archtui}"

# Se não estamos dentro do repositório clonado, obtê-lo
if [[ ! -f "$SCRIPT_DIR/run.py" || ! -f "$SCRIPT_DIR/requirements.txt" ]]; then
    echo "A obter o projeto completo..."

    if [[ -z "${ARCHTUI_REPO_URL:-}" ]]; then
        echo "Erro: Defina ARCHTUI_REPO_URL com o URL do repositório."
        echo "  Exemplo: ARCHTUI_REPO_URL=https://github.com/TomasJoao23131/archtui.git ./install.sh"
        exit 1
    fi

    if ! command -v git >/dev/null 2>&1; then
        echo "A instalar git..."
        pacman -Sy --noconfirm git
    fi

    rm -rf "$TARGET_DIR"
    git clone "$ARCHTUI_REPO_URL" "$TARGET_DIR"
    SCRIPT_DIR="$TARGET_DIR"
fi

# Garantir que Python e Pip estão instalados
if ! command -v python3 >/dev/null 2>&1 || ! python3 -m pip --version >/dev/null 2>&1; then
    echo "A instalar dependências de sistema (Python e Pip)..."
    pacman -Sy --noconfirm python python-pip
fi

PYTHON_BIN="$(command -v python3 || command -v python)"

# Instalar dependências Python se necessário
if ! "$PYTHON_BIN" -m pip show textual >/dev/null 2>&1; then
    echo "A instalar dependências Python..."
    "$PYTHON_BIN" -m pip install --break-system-packages -r "$SCRIPT_DIR/requirements.txt"
fi

# ── Preparar o terminal para Unicode e cores ──
# O tty básico do Arch live não suporta Unicode por defeito.
# Precisamos de uma fonte que tenha os caracteres especiais (bordas, setas, etc.)
if [[ "$(tty)" == /dev/tty* ]]; then
    # Instalar fonte Terminus se não estiver disponível
    if ! pacman -Qi terminus-font >/dev/null 2>&1; then
        echo "A instalar fonte do terminal..."
        pacman -S --noconfirm terminus-font >/dev/null 2>&1
    fi
    # Usar a fonte Terminus grande com suporte a Unicode
    setfont ter-124n 2>/dev/null || setfont ter-120n 2>/dev/null || true
fi

# Garantir locale UTF-8 para caracteres especiais
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
export TERM="${TERM:-linux}"

echo ""
echo "  ArchTUI — Instalador do Arch Linux"
echo "  -----------------------------------"
echo ""
"$PYTHON_BIN" "$SCRIPT_DIR/run.py"