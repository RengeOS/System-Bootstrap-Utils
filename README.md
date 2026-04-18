# Notes:

## Init venv
python3 -m venv .venv

## Source venv
source .venv/bin/activate.fish

## Install all libs
pip install -r requirements.txt

## Build it in one binary
pyinstaller --onefile main.py --collect-all namelib1 namelib2
