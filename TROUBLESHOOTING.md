# Troubleshooting Guide

## Common Issues and Solutions

### 1. "bot.py not found" Error

**Problem:** The batch file can't find bot.py
**Solutions:**
- Make sure all files are in the same folder
- Run the batch file from the correct directory
- Check that bot.py actually exists in the folder

### 2. "No module named 'telegram'" Error

**Problem:** Python packages not installed
**Solutions:**
- Run `install.bat` first before running the bot
- If still failing, manually run: `pip install python-telegram-bot requests beautifulsoup4 pillow pytesseract`

### 3. Bot Token Issues

**Problem:** Bot token not configured or invalid
**Solutions:**
- Copy `config.example.json` to `config.json`
- Get your bot token from @BotFather on Telegram
- Replace "YOUR_BOT_TOKEN_HERE" with your actual token

### 4. OCR Not Working

**Problem:** Tesseract OCR not installed
**Solutions:**
- Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Install it and add to PATH
- Restart command prompt after installation

### 5. Bot Not Responding

**Problem:** Bot doesn't process messages
**Solutions:**
- Check if bot token is valid
- Ensure bot is added to the group/channel
- Check internet connection
- Look at console for error messages

## File Structure
\`\`\`
telegram-product-bot/
├── bot.py                 # Main bot code
├── config.json           # Bot configuration (create from example)
├── config.example.json   # Configuration template
├── requirements.txt      # Python dependencies
├── install.bat          # Dependency installer
├── run_bot.bat          # Bot runner
├── README.md            # Documentation
└── TROUBLESHOOTING.md   # This file
\`\`\`

## Getting Help

If you're still having issues:
1. Check the console output for specific error messages
2. Ensure all files are in the same directory
3. Try running `install.bat` again
4. Make sure your bot token is correct
