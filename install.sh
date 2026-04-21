#!/bin/bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
   echo "Este script precisa de ser executado como root (use sudo)."
   exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="${ARCHTUI_REPO_URL:-https://github.com/SEU_USUARIO/archtui.git}"
TARGET_DIR="${ARCHTUI_TARGET_DIR:-/opt/archtui}"

if [[ ! -f "$SCRIPT_DIR/run.py" || ! -f "$SCRIPT_DIR/requirements.txt" ]]; then
    echo "A obter o projecto completo..."

    if ! command -v git >/dev/null 2>&1; then
        pacman -Sy --noconfirm git
    fi

    rm -rf "$TARGET_DIR"
    git clone "$REPO_URL" "$TARGET_DIR"
    SCRIPT_DIR="$TARGET_DIR"
fi

if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
    echo "Python nao encontrado. A instalar..."
    pacman -Sy --noconfirm python python-pip
fi

PYTHON_BIN="$(command -v python3 || command -v python)"

if ! "$PYTHON_BIN" -m pip show textual >/dev/null 2>&1; then
    echo "A instalar dependencias Python..."
    "$PYTHON_BIN" -m pip install -r "$SCRIPT_DIR/requirements.txt"
fi

echo "A iniciar o ArchTUI..."
"$PYTHON_BIN" "$SCRIPT_DIR/run.py"