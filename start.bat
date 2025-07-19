@echo off
IF NOT EXIST venv (
    echo [+] Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo [+] Installing dependencies...
pip install -r requirements.txt

echo [+] Installing Playwright browser...
playwright install chromium

echo [+] Running script...
python run.py
