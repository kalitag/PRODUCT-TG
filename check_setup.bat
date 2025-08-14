@echo off
title File Setup Checker - Telegram Product Bot
echo.
echo ========================================
echo  TELEGRAM PRODUCT BOT - SETUP CHECKER
echo ========================================
echo.

REM Get the directory where the batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Checking required files in: %SCRIPT_DIR%
echo.

REM Check for bot.py
if exist "%SCRIPT_DIR%bot.py" (
    echo ✅ bot.py - Found
) else (
    echo ❌ bot.py - MISSING
    echo    This is the main bot file - it should be in the same folder
)

REM Check for config.json
if exist "%SCRIPT_DIR%config.json" (
    echo ✅ config.json - Found
    
    REM Check if token is configured
    findstr "YOUR_BOT_TOKEN_HERE" "%SCRIPT_DIR%config.json" >nul
    if not errorlevel 1 (
        echo    ⚠️  WARNING: Bot token not configured yet
        echo    Please edit config.json and add your bot token from @BotFather
    ) else (
        echo    ✅ Bot token appears to be configured
    )
) else (
    echo ❌ config.json - MISSING
    echo    This file contains bot configuration
)

REM Check for requirements.txt
if exist "%SCRIPT_DIR%requirements.txt" (
    echo ✅ requirements.txt - Found
) else (
    echo ❌ requirements.txt - MISSING
    echo    This file lists required Python packages
)

REM Check for install.bat
if exist "%SCRIPT_DIR%install.bat" (
    echo ✅ install.bat - Found
) else (
    echo ❌ install.bat - MISSING
    echo    This file installs required dependencies
)

REM Check for run_bot.bat
if exist "%SCRIPT_DIR%run_bot.bat" (
    echo ✅ run_bot.bat - Found
) else (
    echo ❌ run_bot.bat - MISSING
    echo    This file starts the bot
)

echo.
echo ========================================
echo  PYTHON ENVIRONMENT CHECK
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python - NOT INSTALLED or not in PATH
    echo    Please install Python 3.8+ from python.org
) else (
    echo ✅ Python - Installed
    python --version
)

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip - NOT AVAILABLE
    echo    pip should come with Python installation
) else (
    echo ✅ pip - Available
)

echo.
echo ========================================
echo  SETUP INSTRUCTIONS
echo ========================================
echo.

if not exist "%SCRIPT_DIR%bot.py" (
    echo 1. MISSING FILES: Some required files are missing
    echo    Please make sure you have downloaded all files correctly
    echo.
)

if exist "%SCRIPT_DIR%config.json" (
    findstr "YOUR_BOT_TOKEN_HERE" "%SCRIPT_DIR%config.json" >nul
    if not errorlevel 1 (
        echo 2. BOT TOKEN: Configure your bot token
        echo    - Open Telegram and search for @BotFather
        echo    - Send /newbot and follow instructions
        echo    - Copy the token and paste it in config.json
        echo.
    )
)

if exist "%SCRIPT_DIR%install.bat" (
    echo 3. INSTALL DEPENDENCIES: Run install.bat
    echo    This will install all required Python packages
    echo.
)

echo 4. START BOT: Run run_bot.bat
echo    The bot will start automatically monitoring messages
echo.

echo ========================================
echo  TROUBLESHOOTING
echo ========================================
echo.
echo If bot.py is missing:
echo - Make sure you downloaded all files from the project
echo - Check that bot.py is in the same folder as this batch file
echo.
echo If Python errors occur:
echo - Make sure Python 3.8+ is installed
echo - Run install.bat to install required packages
echo.
echo If bot doesn't respond:
echo - Check that bot token is correctly configured in config.json
echo - Make sure the bot is added to your group/channel
echo - Check internet connection
echo.

pause
