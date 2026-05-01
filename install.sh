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

# Fallback para quando o script é corrido via pipe (curl | bash)
SCRIPT_FILE="${BASH_SOURCE[0]:-}"
if [[ -n "$SCRIPT_FILE" ]]; then
    SCRIPT_DIR="$(cd -- "$(dirname -- "$SCRIPT_FILE")" && pwd)"
else
    SCRIPT_DIR="$PWD"
fi
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

# Garantir que Python está instalado
if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
    echo "Python não encontrado. A instalar..."
    pacman -Sy --noconfirm python python-pip
fi

PYTHON_BIN="$(command -v python3 || command -v python)"

# Instalar dependências Python se necessário
if ! "$PYTHON_BIN" -m pip show textual >/dev/null 2>&1; then
    echo "A instalar dependências Python..."
    "$PYTHON_BIN" -m pip install --break-system-packages -r "$SCRIPT_DIR/requirements.txt"
fi

echo ""
echo "  ⬡  ArchTUI — Instalador do Arch Linux"
echo "  ─────────────────────────────────────"
echo ""
"$PYTHON_BIN" "$SCRIPT_DIR/run.py"