# Telegram Product Bot Setup Guide

## 🚀 Quick Setup

### 1. Get Bot Token
1. Message @BotFather on Telegram
2. Create new bot with `/newbot`
3. Copy the bot token

### 2. Configure Bot
1. Copy `config.example.json` to `config.json`
2. Replace `YOUR_BOT_TOKEN_HERE` with your actual token
3. Customize bot name and username if needed

### 3. Install & Run
\`\`\`bash
# Install dependencies
install.bat

# Start the bot
run_bot.bat
\`\`\`

## 🔧 Configuration

Edit `config.json`:
- `token`: Your bot token from @BotFather
- `name`: Your bot's display name
- `username`: Your bot's username (with @)

## 🛡️ Security Notes

- **NEVER** commit `config.json` to GitHub
- Keep your bot token private
- The `.gitignore` file protects sensitive data

## 📱 Usage

The bot works automatically:
- Add to groups/channels or use privately
- Automatically detects product links
- Extracts and formats product information
- No commands needed - fully automated!

## 🐛 Troubleshooting

**"No module named 'telegram'"**
- Run `install.bat` to install dependencies

**"Invalid token"**
- Check your bot token in `config.json`
- Get new token from @BotFather if needed

**Bot not responding**
- Ensure bot is added to group/channel
- Check bot has message permissions
