@echo off
title Telegram Product Bot - Easy_uknowbot (FULLY AUTOMATED)
echo.
echo ========================================
echo  FULLY AUTOMATED Telegram Product Bot
echo ========================================
echo.

REM Get the directory where the batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Check if bot.py exists
if not exist "%SCRIPT_DIR%bot.py" (
    echo ERROR: bot.py not found in current directory
    echo Current directory: %SCRIPT_DIR%
    echo Please make sure bot.py is in the same folder as this batch file
    echo.
    echo Files in current directory:
    dir /b *.py 2>nul || echo No Python files found
    echo.
    echo SOLUTION: Run check_setup.bat to verify all files
    pause
    exit /b 1
)

REM Check if config.json exists and has valid token
if not exist "%SCRIPT_DIR%config.json" (
    echo ERROR: config.json not found
    echo Please make sure config.json is in the same folder
    pause
    exit /b 1
)

REM Check if bot token is configured
findstr "YOUR_BOT_TOKEN_HERE" "%SCRIPT_DIR%config.json" >nul
if not errorlevel 1 (
    echo ERROR: Bot token not configured!
    echo.
    echo Please edit config.json and replace "YOUR_BOT_TOKEN_HERE" 
    echo with your actual bot token from @BotFather
    echo.
    echo Steps to get bot token:
    echo 1. Open Telegram and search for @BotFather
    echo 2. Send /newbot command
    echo 3. Follow instructions to create your bot
    echo 4. Copy the token and paste it in config.json
    echo.
    pause
    exit /b 1
)

echo Bot Username: @Easy_uknowbot
echo Mode: FULLY AUTOMATED - No manual input needed!
echo Status: Starting...
echo.
echo Starting AUTOMATED bot...
echo.
echo ✅ Bot will automatically detect ALL product links
echo ✅ No commands or tagging required  
echo ✅ Works in groups, channels, private chats
echo ✅ Processes Amazon, Flipkart, Meesho, Myntra, Ajio, Snapdeal, Wishlink
echo ✅ OCR text extraction from images
echo ✅ Image forwarding for Meesho products
echo ✅ 3-second response time optimization
echo.
echo Press Ctrl+C to stop the bot
echo.

REM Run the bot with error handling and auto-restart
:start
python "%SCRIPT_DIR%bot.py"
set EXIT_CODE=%ERRORLEVEL%

if %EXIT_CODE% neq 0 (
    echo.
    echo Bot stopped with error code: %EXIT_CODE%
    echo Auto-restarting in 5 seconds...
    echo Press Ctrl+C to cancel restart
    timeout /t 5 /nobreak >nul
    if not errorlevel 1 goto start
)

echo.
echo Bot stopped normally.
pause
