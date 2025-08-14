import asyncio
import re
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from bs4 import BeautifulSoup
import json
from typing import Optional, Dict, List, Tuple
import time
import io
from PIL import Image
import pytesseract
import base64

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Configuration
BOT_TOKEN = "8414049375:AAFMPUvB2u5KffNPsaAi3xu_DOiy-7dhHIg"
BOT_USERNAME = "@Final_output_formatbot"

class ProductBot:
    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        self.platforms = {
            'amazon': ['amazon.in', 'amazon.com', 'amzn.to', 'amzn-to.co', 'a.co'],
            'flipkart': ['flipkart.com', 'fkrt.cc', 'dl.flipkart.com'],
            'meesho': ['meesho.com', 'meesho.app'],
            'myntra': ['myntra.com', 'myntra.app'],
            'ajio': ['ajio.com', 'ajio.app'],
            'snapdeal': ['snapdeal.com', 'snapdeal.app'],
            'wishlink': ['wishlink.com', 'wishlink.app']
        }
        
        self.shorteners = [
            'cutt.ly', 'fkrt.cc', 'amzn-to.co', 'bitli.in', 'a.co',
            'spoo.me', 'wishlink.com', 'da.gd', 'bit.ly', 'tinyurl.com', 
            'short.link', 'goo.gl', 't.co', 'ow.ly', 'is.gd', 'buff.ly'
        ]
        
        self.processed_messages = set()

    def detect_platform(self, url: str) -> Optional[str]:
        """Detect which e-commerce platform the URL belongs to"""
        domain = urlparse(url).netloc.lower()
        for platform, domains in self.platforms.items():
            if any(d in domain for d in domains):
                return platform
        return None

    def is_shortened_url(self, url: str) -> bool:
        """Check if URL is from a shortener service"""
        domain = urlparse(url).netloc.lower()
        return any(shortener in domain for shortener in self.shorteners)

    def unshorten_url(self, url: str) -> str:
        """Unshorten URL and follow redirects"""
        try:
            response = self.session.head(url, allow_redirects=True, timeout=10)
            return response.url
        except:
            try:
                response = self.session.get(url, allow_redirects=True, timeout=10)
                return response.url
            except:
                return url

    def remove_affiliate_tags(self, url: str) -> str:
        """Remove affiliate parameters from URL"""
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        affiliate_params = [
            'tag', 'ref', 'refRID', 'pf_rd_r', 'pf_rd_p', 'pf_rd_m',
            'pf_rd_s', 'pf_rd_t', 'pf_rd_i', 'linkCode', 'camp',
            'creative', 'creativeASIN', 'ascsubtag', 'asc_campaign',
            'asc_refurl', 'asc_source', 'utm_source', 'utm_medium',
            'utm_campaign', 'utm_term', 'utm_content', 'affid',
            'subid', 'clickid', 'pid', 'sid', 'cid', 'aid', 'tracking',
            'fbclid', 'gclid', 'mc_cid', 'mc_eid', '_branch_match_id'
        ]
        
        clean_params = {k: v for k, v in query_params.items() 
                       if k not in affiliate_params}
        
        clean_query = urlencode(clean_params, doseq=True)
        clean_url = urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, clean_query, parsed.fragment
        ))
        
        return clean_url

    async def extract_text_from_image(self, photo_file) -> str:
        """Extract text from image using OCR"""
        try:
            image_bytes = await photo_file.download_as_bytearray()
            image = Image.open(io.BytesIO(image_bytes))
            
            # Use OCR to extract text
            extracted_text = pytesseract.image_to_string(image)
            return extracted_text.strip()
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""

    def extract_product_info(self, url: str, platform: str, message_text: str = "") -> Dict:
        """Extract product information from URL with enhanced accuracy"""
        try:
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            
            for user_agent in user_agents:
                try:
                    headers = {
                        'User-Agent': user_agent,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none'
                    }
                    
                    response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                    response.raise_for_status()
                    
                    if any(keyword in response.text.lower() for keyword in ['blocked', 'captcha', 'access denied', 'error 403', 'error 404']):
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    break
                    
                except Exception as e:
                    logger.warning(f"Failed with user agent {user_agent}: {e}")
                    continue
            else:
                logger.error("All user agents failed")
                return None
            
            info = {
                'title': '',
                'price': '',
                'sizes': [],
                'pin_code': '110001',
                'gender': '',
                'quantity': '',
                'brand': '',
                'image_url': ''
            }
            
            title = self.extract_title(soup, platform)
            if title:
                parsed_info = self.parse_title(title, platform)
                info.update(parsed_info)
            
            price = self.extract_price(soup, platform)
            if price:
                info['price'] = price
            
            image_url = self.extract_image_url(soup, platform)
            if image_url:
                info['image_url'] = image_url
            
            # Extract sizes (Meesho only)
            if platform == 'meesho':
                info['sizes'] = self.extract_sizes(soup)
                info['pin_code'] = self.extract_pin_code(message_text)
            
            return info
            
        except Exception as e:
            logger.error(f"Error extracting product info: {e}")
            return None

    def extract_image_url(self, soup: BeautifulSoup, platform: str) -> str:
        """Extract product image URL"""
        image_selectors = {
            'amazon': [
                '#landingImage',
                '.a-dynamic-image',
                '#imgBlkFront',
                '.a-button-thumbnail img'
            ],
            'flipkart': [
                '._396cs4._2amPTt._3qGmMb img',
                '._1AtVbE img',
                '.CXW8mj img',
                '._2r_T1I img'
            ],
            'meesho': [
                '[data-testid="product-image"]',
                '.ProductImageCarousel__ImageContainer img',
                '.sc-bcXHqe img'
            ],
            'myntra': [
                '.image-grid-image',
                '.pdp-img img',
                '.image-grid-imageContainer img'
            ],
            'ajio': [
                '.prod-image img',
                '.rilrtl-lazy-img',
                '.product-image img'
            ],
            'snapdeal': [
                '#bx-pager img',
                '.product-image img',
                '.cloudzoom img'
            ]
        }
        
        # Try platform-specific selectors
        if platform in image_selectors:
            for selector in image_selectors[platform]:
                element = soup.select_one(selector)
                if element:
                    img_url = element.get('src') or element.get('data-src') or element.get('data-original')
                    if img_url and img_url.startswith(('http', '//')):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        return img_url
        
        # Try Open Graph image
        og_image = soup.find('meta', property='og:image')
        if og_image:
            img_url = og_image.get('content')
            if img_url and img_url.startswith(('http', '//')):
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                return img_url
        
        return ""

    def extract_title(self, soup: BeautifulSoup, platform: str) -> str:
        """Extract product title from page with enhanced accuracy"""
        selectors = {
            'amazon': [
                '#productTitle',
                'span#productTitle',
                'h1.a-size-large.a-spacing-none.a-color-base',
                '.product-title',
                'h1 span'
            ],
            'flipkart': [
                '.B_NuCI',
                '.yhB1nd', 
                'h1._35KyD6',
                'span.B_NuCI',
                '._35KyD6.col-xs-11.col-sm-11.col-md-11',
                'h1 span'
            ],
            'meesho': [
                '[data-testid="product-title"]',
                'h1[data-testid="product-title"]',
                '.sc-bcXHqe.kZLqhX',
                'h1.sc-bcXHqe',
                '.ProductTitle__Container-sc-1jvw5kh-0 h1',
                'h1'
            ],
            'myntra': [
                '.pdp-name',
                'h1.pdp-name',
                '.pdp-product-name',
                '.pdp-name h1'
            ],
            'ajio': [
                '.prod-name',
                'h1.prod-name',
                '.product-title',
                '.fnl-plp-title'
            ],
            'snapdeal': [
                '#productOverview h1',
                '.pdp-product-name',
                '.product-title',
                'h1.notranslate'
            ],
            'wishlink': [
                '.product-title',
                'h1',
                '.title'
            ]
        }
        
        # Try platform-specific selectors first
        if platform in selectors:
            for selector in selectors[platform]:
                element = soup.select_one(selector)
                if element:
                    title = element.get_text(strip=True)
                    if title and len(title) > 5:
                        return title
        
        json_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    title = data.get('name') or data.get('title')
                    if title and len(title) > 5:
                        return title
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            title = item.get('name') or item.get('title')
                            if title and len(title) > 5:
                                return title
            except:
                continue
        
        # Try meta tags
        meta_selectors = [
            'meta[property="og:title"]',
            'meta[name="title"]',
            'meta[property="twitter:title"]'
        ]
        
        for selector in meta_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get('content', '').strip()
                if title and len(title) > 5:
                    return title
        
        # Try page title as last resort
        title_element = soup.find('title')
        if title_element:
            title = title_element.get_text(strip=True)
            # Clean up title tag content
            title = re.sub(r'\s*[-|:]\s*(Buy|Shop|Amazon|Flipkart|Meesho|Myntra|Ajio|Snapdeal).*$', '', title, flags=re.IGNORECASE)
            if title and len(title) > 5:
                return title
        
        return ""

    def extract_price(self, soup: BeautifulSoup, platform: str) -> str:
        """Extract price from page with enhanced accuracy"""
        price_selectors = {
            'amazon': [
                '.a-price-whole',
                '.a-offscreen',
                '#priceblock_dealprice',
                '#priceblock_ourprice',
                '.a-price-range .a-offscreen',
                'span.a-price-symbol + span.a-price-whole',
                '.a-price .a-offscreen'
            ],
            'flipkart': [
                '._30jeq3._16Jk6d',
                '._1_WHN1',
                '.CEmiEU ._1_WHN1',
                '._30jeq3',
                '._25b18c .notranslate',
                '.CEmiEU .srp-x9Jm',
                '._16Jk6d'
            ],
            'meesho': [
                '[data-testid="product-price"]',
                '.ProductPrice__Container-sc-1jvw5kh-0',
                '.sc-bcXHqe.ProductPrice__PriceText',
                '.ProductPrice__PriceText-sc-1jvw5kh-1',
                'span[data-testid="product-price"]'
            ],
            'myntra': [
                '.pdp-price strong',
                '.pdp-price .pdp-price-info',
                '.product-discountedPrice',
                '.pdp-price span'
            ],
            'ajio': [
                '.prod-sp',
                '.price-current',
                '.current-price',
                '.prod-price .price'
            ],
            'snapdeal': [
                '.payBlkBig',
                '.product-price',
                '.lfloat.product-price',
                '#buyPriceDisplayTotal'
            ],
            'wishlink': [
                '.price',
                '.product-price',
                '.current-price'
            ]
        }
        
        # Try platform-specific selectors
        if platform in price_selectors:
            for selector in price_selectors[platform]:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    price = self.parse_price(text)
                    if price:
                        return price
        
        json_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    offers = data.get('offers', {})
                    if isinstance(offers, dict):
                        price = offers.get('price')
                        if price:
                            return str(int(float(price)))
                    elif isinstance(offers, list) and offers:
                        price = offers[0].get('price')
                        if price:
                            return str(int(float(price)))
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            offers = item.get('offers', {})
                            if isinstance(offers, dict):
                                price = offers.get('price')
                                if price:
                                    return str(int(float(price)))
            except:
                continue
        
        price_patterns = [
            r'₹\s*([0-9,]+(?:\.[0-9]{1,2})?)',
            r'Rs\.?\s*([0-9,]+(?:\.[0-9]{1,2})?)',
            r'INR\s*([0-9,]+(?:\.[0-9]{1,2})?)',
            r'Price[:\s]*₹\s*([0-9,]+(?:\.[0-9]{1,2})?)',
            r'MRP[:\s]*₹\s*([0-9,]+(?:\.[0-9]{1,2})?)',
            r'\b([0-9,]+)\s*rupees?\b'
        ]
        
        page_text = soup.get_text()
        all_prices = []
        
        for pattern in price_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            for match in matches:
                try:
                    price_num = float(match.replace(',', ''))
                    if 10 <= price_num <= 500000:  # Reasonable price range
                        all_prices.append(int(price_num))
                except ValueError:
                    continue
        
        if all_prices:
            from collections import Counter
            price_counts = Counter(all_prices)
            most_common = price_counts.most_common(3)
            
            # Return the most reasonable price (not too high, not too low)
            for price, count in most_common:
                if 50 <= price <= 100000:  # More reasonable range
                    return str(price)
            
            # Fallback to most common price
            return str(most_common[0][0])
        
        return ""

    def parse_price(self, text: str) -> str:
        """Parse price from text with enhanced validation"""
        if not text:
            return ""
        
        clean_text = re.sub(r'[₹$Rs\.INR]', '', text)
        numbers = re.findall(r'[0-9,]+(?:\.[0-9]{1,2})?', clean_text)
        
        valid_prices = []
        for num_str in numbers:
            try:
                price = float(num_str.replace(',', ''))
                if 10 <= price <= 500000:  # Reasonable price range
                    valid_prices.append(int(price))
            except ValueError:
                continue
        
        if valid_prices:
            # Return most reasonable price
            reasonable_prices = [p for p in valid_prices if 50 <= p <= 100000]
            if reasonable_prices:
                return str(min(reasonable_prices))
            return str(min(valid_prices))
        
        return ""

    def extract_sizes(self, soup: BeautifulSoup) -> List[str]:
        """Extract available sizes (Meesho only)"""
        sizes = []
        
        size_selectors = [
            '[data-testid="size-option"]',
            '.size-option',
            '.variant-option',
            '.size-variant',
            '.ProductVariants__Container button',
            '.sc-bcXHqe.ProductVariants__VariantButton',
            '.size-selector button',
            '.variant-selector .option'
        ]
        
        for selector in size_selectors:
            elements = soup.select(selector)
            for element in elements:
                size_text = element.get_text(strip=True)
                if size_text and size_text not in sizes and len(size_text) <= 10:
                    sizes.append(size_text)
        
        # If no sizes found, try regex patterns
        if not sizes:
            page_text = soup.get_text()
            size_patterns = [
                r'\b(XS|S|M|L|XL|XXL|XXXL|Free Size|\d{2,3})\b',
                r'Size[:\s]+((?:XS|S|M|L|XL|XXL|XXXL|Free Size|\d{2,3})(?:\s*,\s*(?:XS|S|M|L|XL|XXL|XXXL|Free Size|\d{2,3}))*)'
            ]
            
            for pattern in size_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match else ""
                    if ',' in match:
                        sizes.extend([s.strip() for s in match.split(',')])
                    else:
                        sizes.append(match)
        
        # Clean and deduplicate sizes
        clean_sizes = []
        for size in sizes:
            size = size.strip().upper()
            if size and size not in clean_sizes and len(size) <= 10:
                clean_sizes.append(size)
        
        return clean_sizes[:10]  # Limit to 10 sizes

    def extract_pin_code(self, message_text: str) -> str:
        """Extract pin code from message text"""
        pin_patterns = [
            r'\bpin[:\s]*(\d{6})\b',
            r'\bpincode[:\s]*(\d{6})\b',
            r'\b(\d{6})\b'
        ]
        
        for pattern in pin_patterns:
            match = re.search(pattern, message_text, re.IGNORECASE)
            if match:
                pin = match.group(1)
                # Basic validation - Indian pin codes start with 1-8
                if pin[0] in '12345678':
                    return pin
        
        return "110001"  # Default Delhi pin code

    def format_output(self, info: Dict, url: str, platform: str) -> str:
        """Format the output message according to platform rules"""
        if not info or not info.get('title'):
            return "❌ Unable to extract product info."
        
        if platform == 'meesho':
            # Meesho format: [Gender] [Quantity] [Clean Title] @[price] rs
            parts = []
            if info.get('gender'):
                parts.append(info['gender'])
            if info.get('quantity'):
                parts.append(info['quantity'])
            parts.append(info['title'])
            
            title_line = ' '.join(filter(None, parts))
            price_text = f"@{info['price']} rs" if info['price'] else ""
            
            message = f"{title_line} {price_text}\n{url}\n"
            
            # Add sizes if available
            if info.get('sizes'):
                if len(info['sizes']) >= 5:
                    message += "\nSize - All"
                else:
                    message += f"\nSize - {', '.join(info['sizes'])}"
            
            message += f"\nPin - {info['pin_code']}\n"
            message += "\n@reviewcheckk"
            
        else:
            # Other platforms format
            if self.is_clothing_item(info['title']):
                # Clothing: [Gender] [Quantity] [Clean Title] @[price] rs
                parts = []
                if info.get('gender'):
                    parts.append(info['gender'])
                if info.get('quantity'):
                    parts.append(info['quantity'])
                parts.append(info['title'])
                title_line = ' '.join(filter(None, parts))
                price_text = f"@{info['price']} rs" if info['price'] else ""
            else:
                # Non-clothing: [Brand] [Clean Title] from @[price] rs
                parts = []
                if info.get('brand'):
                    parts.append(info['brand'])
                parts.append(info['title'])
                title_line = ' '.join(filter(None, parts))
                price_text = f"from @{info['price']} rs" if info['price'] else ""
            
            message = f"{title_line} {price_text}\n{url}\n\n@reviewcheckk"
        
        return message

    def is_clothing_item(self, title: str) -> bool:
        """Check if the item is clothing"""
        clothing_keywords = [
            'shirt', 'tshirt', 't-shirt', 'top', 'dress', 'jeans', 'trouser',
            'pant', 'short', 'skirt', 'blouse', 'kurta', 'saree', 'lehenga',
            'jacket', 'coat', 'sweater', 'hoodie', 'sweatshirt', 'blazer',
            'suit', 'ethnic', 'western', 'casual', 'formal', 'party wear',
            'kurti', 'palazzo', 'dupatta', 'salwar', 'kameez', 'churidar',
            'nightwear', 'innerwear', 'bra', 'panty', 'brief', 'boxer',
            'sock', 'stocking', 'legging', 'jegging', 'capri', 'bermuda'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in clothing_keywords)

    def extract_urls_from_text(self, text: str) -> List[str]:
        """Extract URLs from text with enhanced detection"""
        url_patterns = [
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*$$$$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            r'(?:www\.)?(?:amazon\.in|flipkart\.com|meesho\.com|myntra\.com|ajio\.com|snapdeal\.com|wishlink\.com)(?:/[^\s]*)?',
            r'(?:amzn\.to|fkrt\.cc|cutt\.ly|bitli\.in|spoo\.me|da\.gd)/[^\s]*'
        ]
        
        urls = []
        for pattern in url_patterns:
            found_urls = re.findall(pattern, text, re.IGNORECASE)
            for url in found_urls:
                # Add https if missing
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                # Validate URL
                try:
                    parsed = urlparse(url)
                    if parsed.netloc and parsed.scheme:
                        urls.append(url)
                except:
                    continue
        
        return list(set(urls))  # Remove duplicates

    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process incoming messages automatically"""
        try:
            message = update.message
            if not message:
                return
            
            # Create unique message ID to prevent duplicate processing
            message_id = f"{message.chat_id}_{message.message_id}"
            if message_id in self.processed_messages:
                return
            
            # Skip bot messages
            if message.from_user and message.from_user.is_bot:
                return
            
            # Get text from message or caption
            text = message.text or message.caption or ""
            
            # If message has photo but no text, try OCR
            if message.photo and not text:
                try:
                    photo_file = await message.photo[-1].get_file()
                    extracted_text = await self.extract_text_from_image(photo_file)
                    if extracted_text:
                        text = extracted_text
                        logger.info(f"Extracted text from image: {text[:100]}...")
                except Exception as e:
                    logger.error(f"Failed to process image: {e}")
            
            # Extract URLs from text
            urls = self.extract_urls_from_text(text)
            
            if not urls:
                return
            
            # Mark message as processed
            self.processed_messages.add(message_id)
            
            # Clean up processed messages set if it gets too large
            if len(self.processed_messages) > 1000:
                self.processed_messages.clear()
            
            # Process URLs with time limit
            start_time = time.time()
            processed_count = 0
            
            for url in urls[:3]:  # Limit to 3 URLs per message
                try:
                    original_url = url
                    
                    # Unshorten URL if needed
                    if self.is_shortened_url(url):
                        logger.info(f"Unshortening URL: {url}")
                        url = self.unshorten_url(url)
                    
                    # Clean affiliate tags
                    clean_url = self.remove_affiliate_tags(url)
                    platform = self.detect_platform(clean_url)
                    
                    if not platform:
                        continue
                    
                    logger.info(f"Processing {platform} product: {clean_url}")
                    
                    # Extract product information
                    product_info = self.extract_product_info(clean_url, platform, text)
                    
                    if not product_info:
                        await message.reply_text("❌ Unable to extract product info.")
                        continue
                    
                    # Format output message
                    formatted_message = self.format_output(product_info, clean_url, platform)
                    
                    if platform == 'meesho' and message.photo:
                        await message.reply_photo(
                            photo=message.photo[-1].file_id,
                            caption=formatted_message
                        )
                    else:
                        await message.reply_text(formatted_message, disable_web_page_preview=True)
                    
                    processed_count += 1
                    logger.info(f"Successfully processed {platform} product")
                    
                    # Check time limit (3 seconds max)
                    elapsed = time.time() - start_time
                    if elapsed > 2.5:  # Leave some buffer
                        break
                    
                    # Small delay between processing
                    await asyncio.sleep(0.3)
                    
                except Exception as e:
                    logger.error(f"Error processing URL {url}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error in process_message: {e}")

    def parse_title(self, title: str, platform: str) -> Dict:
        """Parse title to extract gender, quantity, brand, and clean title"""
        info = {
            'title': title,
            'gender': '',
            'quantity': '',
            'brand': ''
        }
        
        if not title:
            return info
        
        marketing_words = [
            'best seller', 'trending', 'new arrival', 'hot deal', 'limited time',
            'exclusive', 'premium', 'luxury', 'branded', 'original', 'authentic',
            'cash on delivery', 'cod available', 'free shipping', 'fast delivery',
            'buy now', 'shop now', 'offer', 'sale', 'discount', 'off', 'deal',
            'combo', 'pack of', 'set of', 'latest', 'stylish', 'trendy',
            'fashionable', 'designer', 'collection', 'special', 'limited edition'
        ]
        
        clean_title = title
        for word in marketing_words:
            clean_title = re.sub(rf'\b{re.escape(word)}\b', '', clean_title, flags=re.IGNORECASE)
        
        # Remove extra spaces and clean up
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        clean_title = re.sub(r'[()[\]{}]', '', clean_title)
        
        gender_patterns = [
            r'\b(men\'?s?|male|boy\'?s?|man)\b',
            r'\b(women\'?s?|female|girl\'?s?|woman|ladies)\b',
            r'\b(unisex|kids?|children)\b'
        ]
        
        for pattern in gender_patterns:
            match = re.search(pattern, clean_title, re.IGNORECASE)
            if match:
                gender_word = match.group(1).lower()
                if gender_word in ['men', 'mens', 'male', 'boy', 'boys', 'man']:
                    info['gender'] = 'Men'
                elif gender_word in ['women', 'womens', 'female', 'girl', 'girls', 'woman', 'ladies']:
                    info['gender'] = 'Women'
                elif gender_word in ['unisex', 'kids', 'kid', 'children']:
                    info['gender'] = 'Unisex'
                break
        
        if self.is_clothing_item(clean_title):
            quantity_patterns = [
                r'\b(\d+)\s*(?:piece|pc|pcs|pack|set)\b',
                r'\b(?:pack\s*of\s*|set\s*of\s*)(\d+)\b'
            ]
            
            for pattern in quantity_patterns:
                match = re.search(pattern, clean_title, re.IGNORECASE)
                if match:
                    qty = int(match.group(1))
                    if 1 <= qty <= 20:
                        info['quantity'] = f"{qty} Piece"
                    break
        
        words = clean_title.split()
        for word in words[:3]:  # Check first 3 words
            if len(word) > 2 and word.isalpha() and word[0].isupper():
                info['brand'] = word
                break
        
        # Clean the final title
        info['title'] = clean_title[:100]  # Limit length
        
        return info

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: config.json not found!")
        print("Please copy config.example.json to config.json and add your bot token")
        input("Press Enter to exit...")
        exit(1)
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON in config.json")
        input("Press Enter to exit...")
        exit(1)

def main():
    """Main function to run the bot"""
    config = load_config()
    TOKEN = config['bot_info']['token']
    
    if TOKEN == "8414049375:AAFMPUvB2u5KffNPsaAi3xu_DOiy-7dhHIg":
        print("ERROR: Please add your actual bot token to config.json")
        print("Get your token from @BotFather on Telegram")
        print("Edit config.json and replace 'YOUR_BOT_TOKEN_HERE' with your token")
        input("Press Enter to exit...")
        return
    
    bot = ProductBot(TOKEN)
    application = Application.builder().token(TOKEN).build()
    
    # Add message handler for all message types
    application.add_handler(MessageHandler(
        filters.TEXT | filters.CAPTION | filters.PHOTO | filters.Document.ALL | filters.FORWARDED, 
        bot.process_message
    ))
    
    logger.info("🤖 Enhanced Product Bot is starting...")
    logger.info("🔍 Features: Auto URL detection, OCR, Image forwarding, 3s response")
    logger.info("📱 Platforms: Amazon, Flipkart, Meesho, Myntra, Ajio, Snapdeal, Wishlink")
    logger.info("🚀 Fully automated - no commands needed!")
    
    # Start the bot
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
