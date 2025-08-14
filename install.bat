@echo off
echo Installing Enhanced Telegram Product Bot Dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing required packages...
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install all packages from requirements.txt with force reinstall
echo Installing all required packages...
python -m pip install --force-reinstall -r requirements.txt

REM Install additional packages that might be missing
echo Installing additional dependencies...
python -m pip install --upgrade python-telegram-bot==20.7
python -m pip install --upgrade requests beautifulsoup4 pillow pytesseract lxml html5lib

REM Verify installation
echo.
echo Verifying installation...
python -c "import telegram; print('✓ python-telegram-bot installed successfully')" 2>nul || echo "✗ python-telegram-bot installation failed"
python -c "import requests; print('✓ requests installed successfully')" 2>nul || echo "✗ requests installation failed"
python -c "import bs4; print('✓ beautifulsoup4 installed successfully')" 2>nul || echo "✗ beautifulsoup4 installation failed"
python -c "import PIL; print('✓ Pillow installed successfully')" 2>nul || echo "✗ Pillow installation failed"
python -c "import pytesseract; print('✓ pytesseract installed successfully')" 2>nul || echo "✗ pytesseract installation failed"

echo.
echo ================================
echo Installing Tesseract OCR Engine...
echo ================================
echo.

REM Check if Tesseract is already installed
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo Tesseract OCR not found in PATH
    echo.
    echo IMPORTANT: For OCR functionality, please:
    echo 1. Download Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki
    echo 2. Install it to: C:\Program Files\Tesseract-OCR\
    echo 3. Add it to your system PATH
    echo.
    echo The bot will work without OCR, but won't extract text from images
) else (
    echo ✓ Tesseract OCR is already installed and working
)

echo.
echo ================================
echo Installation completed!
echo ================================
echo.
echo Next steps:
echo 1. Get your bot token from @BotFather on Telegram
echo 2. Edit config.json and replace "8414049375:AAFMPUvB2u5KffNPsaAi3xu_DOiy-7dhHIg" with your token
echo 3. Run the bot using: run_bot.bat
echo.
echo The bot will automatically process ALL product links without any commands!
echo.
pause
