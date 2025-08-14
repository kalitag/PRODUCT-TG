# Telegram Product Bot - Easy_uknowbot (FULLY AUTOMATED)

A **fully automated** Telegram bot that monitors ALL messages and automatically detects e-commerce product links, extracts product information, and formats them into clean deal posts **without any manual input required**.

## 🤖 FULL AUTOMATION FEATURES

- **🔄 Zero Manual Input**: Bot automatically monitors ALL messages in groups, channels, and private chats
- **🔍 Auto Link Detection**: Finds product links in any message without being tagged or commanded
- **⚡ Instant Processing**: Extracts and formats product info automatically within seconds
- **🎯 Smart Filtering**: Only processes supported e-commerce platforms
- **🚀 24/7 Operation**: Runs continuously without human intervention

## 🛍️ Supported Platforms

- **Amazon** (amazon.in, amazon.com, amzn.to, amzn-to.co, a.co)
- **Flipkart** (flipkart.com, fkrt.cc, dl.flipkart.com)
- **Meesho** (meesho.com, meesho.app)
- **Myntra** (myntra.com, myntra.app)
- **Ajio** (ajio.com, ajio.app)
- **Snapdeal** (snapdeal.com, snapdeal.app)
- **Wishlink** (wishlink.com, wishlink.app)
- **Nykaa** (nykaa.com, nykaa.app)
- **TataCliq** (tatacliq.com, tatacliq.app)

## 🔗 Supported URL Shorteners

Automatically unshortens and processes:
- cutt.ly, fkrt.cc, amzn-to.co, bitli.in, a.co
- spoo.me, wishlink.com, da.gd, bit.ly, tinyurl.com
- short.link, goo.gl, t.co, ow.ly, is.gd, buff.ly

## 🚀 Quick Start

### 1. Install Dependencies
\`\`\`bash
Double-click install.bat
\`\`\`
This automatically installs all required Python packages.

### 2. Run the Bot
\`\`\`bash
Double-click run_bot.bat
\`\`\`
The bot starts and runs **fully automated** - no further input needed!

## 🔄 How It Works (AUTOMATED)

1. **Someone posts ANY message** with a product link in any chat
2. **Bot automatically detects** the link (no commands/tags needed)
3. **Extracts product information** instantly
4. **Posts formatted deal** as a reply
5. **Continues monitoring** for more links automatically

**No tagging required! No commands needed! Completely hands-off operation!**

## 📝 Output Formats

### Meesho Format
\`\`\`
[Gender] [Quantity] [Clean Title] @[price] rs
[Full Non-Affiliate Link]

Size - [Available Sizes]
Pin - [Pin Code]

@reviewcheckk
\`\`\`

### Other Platforms Format
\`\`\`
[Brand] [Clean Title] from @[price] rs
[Full Non-Affiliate Link]

@reviewcheckk
\`\`\`

## ⚙️ Bot Configuration

- **Bot Username**: @Easy_uknowbot
- **Mode**: FULLY AUTOMATED
- **Runtime**: 24/7 continuous operation
- **Response Time**: < 3 seconds per message
- **Max URLs per message**: 3 (to prevent spam)

## 🎯 Usage

1. **Add bot to your group/channel** or message it directly
2. **That's it!** The bot will automatically:
   - Monitor all messages
   - Detect product links
   - Extract product info
   - Post formatted deals

**No commands, no tagging, no manual work required!**

## 🛡️ Smart Features

- **Duplicate Prevention**: Won't process the same message twice
- **Bot Message Filtering**: Ignores messages from other bots
- **Rate Limiting**: Built-in delays to prevent spam
- **Error Recovery**: Auto-restarts on errors
- **Enhanced URL Detection**: Finds links even without http://

## 📁 Files Structure

- `bot.py` - Main automated bot code
- `install.bat` - One-click dependency installer
- `run_bot.bat` - Bot runner with auto-restart
- `requirements.txt` - Python dependencies
- `config.json` - Bot configuration
- `README.md` - This documentation

## 🔧 Troubleshooting

1. **Python not found**: Install Python 3.8+ from python.org
2. **Dependencies missing**: Run `install.bat` again
3. **Bot not responding**: Check internet connection and restart
4. **Permission errors**: Run as administrator

## 📊 Technical Details

- **Framework**: python-telegram-bot v20+
- **Web Scraping**: requests + BeautifulSoup4
- **URL Processing**: Advanced regex with multiple patterns
- **Platform Detection**: Domain-based identification
- **Price Extraction**: Multi-pattern price detection
- **Title Cleaning**: Removes affiliate tags and marketing fluff
- **Memory Management**: Automatic cleanup of processed messages

## 🎉 Ready to Use!

Your bot is now **100% automated**! Just run it and it will handle everything automatically. Perfect for deal channels, shopping groups, or personal use!
