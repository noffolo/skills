# 📚 Brunson Books Knowledge Base Summary

## 📊 Statistics
- **Total Books:** 3
- **Total Words:** 218,545
- **Total Concepts:** 540

## 📖 Books Processed
### Expert Secrets
- **Words:** 62,027
- **Concepts Found:** 160
- **Framework Types:** epiphany_bridge, webinar

### DotCom Secrets
- **Words:** 59,584
- **Concepts Found:** 70
- **Framework Types:** value_ladder, webinar

### Traffic Secrets
- **Words:** 96,934
- **Concepts Found:** 310
- **Framework Types:** dream_100, webinar

## 🎯 Frameworks by Type
### Value Ladder
- **Count:** 57
- **DotCom Secrets:** 57 concepts
  - VALUE LADDER
  - core offer
  - tripwire
  - backend offer
  - Tripwire

### Epiphany Bridge
- **Count:** 120
- **Expert Secrets:** 120 concepts
  - Epiphany Bridge
  - create a new future. That is the goal of a good Epiphany
  - Belief Pattern
  - belief pattern
  - belief  pattern

### Dream 100
- **Count:** 299
- **Traffic Secrets:** 299 concepts
  - DREAM 100
  - Audience
  - TRAFFIC SECRET
  - Traffic  Secret
  - Dream 100

### Webinar
- **Count:** 64
- **Expert Secrets:** 40 concepts
  - Webinar  presentation  script
  - webinars  using  my  weekly  webinar  model
  - Webinar Model
  - Perfect Webinar
  - Webinar  script
- **DotCom Secrets:** 13 concepts
  - WEBINAR REGISTRATION SCRIPT
  - Perfect Webinar
  - WEBINAR SCRIPT
  - Webinar script
  - PERFECT WEBINAR
- **Traffic Secrets:** 11 concepts
  - Perfect Webinar
  - webinar  script
  - webinar, you can still follow the five-step script
  - webinar script
  - Webinar script

## 🔧 Usage Examples
```python
# Load frameworks
import json
with open('frameworks.json', 'r') as f:
    data = json.load(f)

# Get all Value Ladder concepts
value_ladders = data['frameworks_by_type']['value_ladder']
print(f"Found {len(value_ladders)} Value Ladder concepts")
```
