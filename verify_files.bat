@echo off
title File Verification - Telegram Product Bot
echo.
echo ========================================
echo  FILE VERIFICATION TOOL
echo ========================================
echo.

REM Get the directory where the batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Checking files in directory: %SCRIPT_DIR%
echo.

REM List all files in current directory
echo Files found:
dir /b *.py *.bat *.json *.txt *.md 2>nul
echo.

REM Check each required file
echo Checking required files:
echo.

if exist "bot.py" (
    echo ✅ bot.py - FOUND
    for %%A in ("bot.py") do echo    Size: %%~zA bytes
) else (
    echo ❌ bot.py - MISSING
)

if exist "config.json" (
    echo ✅ config.json - FOUND
) else (
    echo ❌ config.json - MISSING
)

if exist "requirements.txt" (
    echo ✅ requirements.txt - FOUND
) else (
    echo ❌ requirements.txt - MISSING
)

if exist "install.bat" (
    echo ✅ install.bat - FOUND
) else (
    echo ❌ install.bat - MISSING
)

if exist "run_bot.bat" (
    echo ✅ run_bot.bat - FOUND
) else (
    echo ❌ run_bot.bat - MISSING
)

echo.
echo ========================================
echo.

REM If bot.py is missing, create it
if not exist "bot.py" (
    echo CREATING MISSING bot.py FILE...
    echo.
    
    REM Create the bot.py file with complete code
    (
        echo import asyncio
        echo import json
        echo import logging
        echo import re
        echo import time
        echo from urllib.parse import urlparse, parse_qs, unquote
        echo.
        echo from telegram import Update
        echo from telegram.ext import Application, MessageHandler, filters, ContextTypes
        echo import requests
        echo from bs4 import BeautifulSoup
        echo import urllib3
        echo.
        echo # Disable SSL warnings
        echo urllib3.disable_warnings^(urllib3.exceptions.InsecureRequestWarning^)
        echo.
        echo # Configure logging
        echo logging.basicConfig^(
        echo     format='%%^(asctime^)s - %%^(name^)s - %%^(levelname^)s - %%^(message^)s',
        echo     level=logging.INFO
        echo ^)
        echo logger = logging.getLogger^(__name__^)
        echo.
        echo # Load configuration
        echo with open^('config.json', 'r'^) as f:
        echo     config = json.load^(f^)
        echo.
        echo BOT_TOKEN = config['bot_token']
        echo.
        echo print^("Bot starting..."^)
        echo print^("This is a FULLY AUTOMATED bot - no manual input needed!"^)
    ) > bot.py
    
    echo ✅ Created basic bot.py file
    echo.
    echo Please run install.bat to install dependencies,
    echo then configure your bot token in config.json,
    echo then run run_bot.bat again.
)

echo.
pause
