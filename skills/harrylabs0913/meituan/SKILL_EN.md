---
name: meituan-ec
description: "CLI tool for Meituan food delivery and local services - search restaurants, find coupons, and track red packets"
---

# Meituan Skill

A command-line interface for Meituan (美团), China's leading platform for food delivery and local services. This skill provides restaurant search, coupon discovery, and red packet tracking capabilities.

## Description

Meituan is a comprehensive CLI tool for one of China's largest local services platforms. Originally a group-buying platform, Meituan has evolved into a dominant player in food delivery, hotel booking, entertainment, and other local services. The platform connects millions of consumers with restaurants, delivery services, and local businesses.

### Use Cases

- **Food Delivery**: Find restaurants and compare delivery options
- **Deal Discovery**: Discover coupons and promotional red packets
- **Restaurant Research**: Compare ratings, prices, and reviews
- **Local Services**: Find beauty salons, gyms, and other local businesses
- **Price Comparison**: Compare deals across different restaurants

## Installation

```bash
# Install the ecommerce-core dependency first
pip install -r ../ecommerce-core/requirements.txt

# Install the Meituan skill
pip install -e .
```

## Usage

### Commands

#### Search Food/Restaurants
```bash
meituan food "火锅"
meituan food "烧烤" --location beijing --limit 20
```

Search for restaurants and food options by keyword.

- **Arguments:**
  - `query` - Search keyword (e.g., cuisine type, dish name)
  - `--location` - Location filter (city name, default: auto-detect)
  - `--limit` - Number of results (default: 20)

**Example:**
```bash
# Search for hot pot
meituan food "hot pot"

# Search in specific city
meituan food "sushi" --location shanghai --limit 30

# Find BBQ places
meituan food "barbecue" --location beijing
```

#### Login
```bash
meituan login
```

Authenticate with Meituan using QR code. Opens a browser window with a QR code that can be scanned with the Meituan mobile app. Session tokens are securely stored.

#### Red Packet Info
```bash
meituan redpacket
```

Show available red packets (digital coupons/vouchers) and promotional deals. Displays discount amounts, minimum order requirements, and expiration dates.

**Example:**
```bash
# List all available red packets
meituan redpacket

# Find food delivery coupons
meituan redpacket | grep -i "food"
```

## Features

- **Restaurant Search with Caching**: Fast and efficient restaurant discovery with intelligent caching
- **QR Code Login**: Secure authentication via Meituan mobile app
- **Red Packet/Coupon Tracking**: Comprehensive tracking of available discounts and promotions
- **Rating & Price Information**: Display restaurant ratings, price ranges, and delivery fees
- **Anti-Detection Browser Automation**: Stealth automation for reliable data extraction

## Examples

### Finding Food
```bash
# Search for specific cuisine
meituan food "pizza"

# Find restaurants with delivery
meituan food "noodles" --location beijing --limit 20

# Search for cheap eats
meituan food "fast food" --limit 50
```

### Finding Deals
```bash
# Check available coupons
meituan redpacket

# Find discounts above 20 yuan
meituan redpacket | grep -E "[2-9][0-9]+"
```

### Location-Based Search
```bash
# Search in different cities
meituan food "sichuan cuisine" --location chengdu
meituan food "japanese" --location hangzhou
```

## Technical Details

### Data Storage

| Data Type | Location |
|-----------|----------|
| Session Tokens | `~/.openclaw/data/ecommerce/auth.db` |
| Search Cache | `~/.openclaw/data/ecommerce/ecommerce.db` |

### Dependencies

- `ecommerce-core` framework (required)
- Browser automation with anti-detection capabilities
- SQLite for data persistence

### Platform Coverage

Meituan provides access to:

- **Food Delivery**: Real-time ordering from thousands of restaurants
- **Restaurant Booking**: Table reservations for dine-in
- **Hotel Booking**: Accommodation reservations
- **Entertainment**: Movie tickets, event bookings
- **Local Services**: Beauty, fitness, cleaning, and more

### Anti-Detection Implementation

- Randomized action timing
- Human-like browsing patterns
- Session management
- Request throttling