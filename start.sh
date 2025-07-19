#!/bin/bash
set -e

if [ ! -d "venv" ]; then
  echo "[+] Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate

echo "[+] Installing dependencies..."
pip install -r requirements.txt

echo "[+] Installing Playwright browser..."
playwright install chromium

echo "[+] Starting script..."
python run.py
