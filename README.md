# Instascrape

Simple cross-platform Instagram scraper 

## 🚀 Usage

### 🔧 Requirements

- Python 3.8+
- Git (to clone repo)

---

### 🖥 Run it (Linux/macOS)

```bash
chmod +x start.sh
./start.sh
````

### 🪟 Run it (Windows)

Double-click `start.bat`
*or*
Run in terminal:

```bat
start.bat
```

---

## 🛠 What it does

1. Creates a virtual environment (`venv/`)
2. Installs dependencies from `requirements.txt`
3. Installs the required Playwright browser (Chromium)
4. Runs the scraper via `run.py`

---

## 🧼 To reset

If stuff breaks or you want a clean install:

```bash
rm -rf venv
./start.sh
```

---

## 📝 Notes

* First run might take a bit — Chromium download is \~100MB.
* Script assumes you're online.
* No bundling, packaging, or PyInstaller needed. Just run it.

---

## 📂 Structure

```
Instascrape/
├── main.py              # Some goofy ahh modules
├── run.py               # Main entry point
├── requirements.txt     # Dependencies
├── start.sh             # Linux/macOS launcher
├── start.bat            # Windows launcher
└── README.md            # You're here
```
