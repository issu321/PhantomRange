@echo off
echo 🔮 PhantomRange Installer
echo =========================

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    exit /b 1
)

if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo 📥 Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist "assets" mkdir assets

echo ✅ Installation complete!
echo 🚀 Launching PhantomRange...
venv\Scripts\python -m streamlit run app.py
