#!/bin/bash
BASENAME="behandler"
VENV=".env"

execute(){
  virtualenv "$VENV"
  source "$VENV/bin/activate"  
  python3 "$BASENAME.py" "$@"
}

build(){
  local BASENAME="$1"
  local SCRIPT="$BASENAME.py"
  local BIN_NAME="$BASENAME.bin"
  local INSTALL_DIR="$HOME/.config/$BASENAME"
  local SYMLINK="$HOME/bin/$BASENAME"
  

  if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
  fi
  mkdir -p "$INSTALL_DIR"

  virtualenv "$VENV"
  source "$VENV/bin/activate"

  pip install --upgrade pip
  pip install colorama nuitka

  rm -r "$INSTALL_DIR"

  python3 -m nuitka \
    --standalone \
    --no-deployment-flag=self-execution\
    --output-dir="$INSTALL_DIR" \
    --remove-output \
    --follow-imports \
    --lto=yes \
    --clang \
    --jobs=6 \
    --assume-yes-for-downloads \
    "$SCRIPT"

  mkdir -p "$HOME/bin"

  if [ -f "$SYMLINK" ]; then
    rm "$SYMLINK"
  fi

  ln -sf "$INSTALL_DIR/$BASENAME.dist/$BIN_NAME" "$SYMLINK"

  deactivate
}

if [ $# -eq 0 ]; then
  build "$BASENAME"

else
  case "$1" in
    execute)
      shift
      execute "$@"
      ;;
    *)
      echo "Not recognized."
      exit 1
      ;;
  esac
fi