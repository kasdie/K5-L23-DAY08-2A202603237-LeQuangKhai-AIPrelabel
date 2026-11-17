#!/bin/zsh
cd "$(dirname "$0")" || exit 1
.venv/bin/python scripts/gold_session.py timer
read "?Nhấn Enter để đóng cửa sổ. "
