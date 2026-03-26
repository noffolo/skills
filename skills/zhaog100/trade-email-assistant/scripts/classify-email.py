#!/usr/bin/env python3
# Copyright (c) 2026 思捷娅科技 (SJYKJ)
# License: MIT
"""关键词分类引擎 - stdin JSON → stdout JSON"""

import json
import sys
import os
import logging
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "email-classify.log"),
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("classify-email")

RULES = {
    "inquiry": {
        "priority": 0,
        "keywords": [
            "inquiry", "quote", "price", "MOQ", "sample request",
            "interested in", "could you send", "product catalog",
            "询价", "报价", "样品", "采购", "wholesale",
            "looking for", "need price", "how much", "unit price",
            "can you provide", "please send me"
        ]
    },
    "order": {
        "priority": 1,
        "keywords": [
            "order", "payment", "invoice", "PO ", "confirmation",
            "订单", "付款", "发票", "TT ", "L/C",
            "place order", "purchase order", "bank transfer",
            "western union", "pay pal"
        ]
    },
    "logistics": {
        "priority": 2,
        "keywords": [
            "shipping", "tracking", "customs", "clearance", "ETA",
            "BL ", "物流", "海关", "清关", "运单", "Bill of Lading",
            "shipment", "delivery", "freight", "container",
            "DHL", "FedEx", "UPS", "TNT", "EMS"
        ]
    },
    "platform": {
        "priority": 3,
        "keywords": [
            "Amazon", "Alibaba", "AliExpress", "eBay", "Shopify",
            "account", "listing", "review", "FBA",
            "store", "product listing", "product page"
        ]
    }
}

def classify_email(email_data):
    text = f"{email_data.get('subject', '')} {email_data.get('body_text', '')} {email_data.get('body_preview', '')}".lower()
    
    best_match = None
    best_count = 0
    matched_keywords = []
    
    for category, rule in RULES.items():
        found = []
        for kw in rule["keywords"]:
            if kw.lower() in text:
                found.append(kw)
        if len(found) > best_count:
            best_count = len(found)
            best_match = category
            matched_keywords = found
    
    if best_match:
        return {
            "message_id": email_data["message_id"],
            "uid": email_data["uid"],
            "from": email_data.get("from", ""),
            "subject": email_data.get("subject", ""),
            "category": best_match,
            "priority": RULES[best_match]["priority"],
            "confidence": min(best_count / 3.0, 1.0),
            "method": "keyword",
            "matched_keywords": matched_keywords
        }
    else:
        return None

def main():
    try:
        stdin_data = sys.stdin.read()
        if not stdin_data.strip():
            print(json.dumps({"error": "No input data", "results": [], "unclassified": []}))
            sys.exit(1)
        
        data = json.loads(stdin_data)
        emails = data.get("emails", [])
        if not emails:
            print(json.dumps({"results": [], "unclassified": [], "total_input": 0}))
            return
        
        results = []
        unclassified = []
        
        for em in emails:
            classified = classify_email(em)
            if classified:
                results.append(classified)
            else:
                unclassified.append({
                    "message_id": em["message_id"],
                    "uid": em["uid"],
                    "from": em.get("from", ""),
                    "subject": em.get("subject", ""),
                    "reason": "未匹配任何关键词规则"
                })
        
        # Sort results by priority
        results.sort(key=lambda x: x["priority"])
        
        output = {
            "total_input": len(emails),
            "total_classified": len(results),
            "total_unclassified": len(unclassified),
            "results": results,
            "unclassified": unclassified
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        log.info("Classified %d/%d emails, %d unclassified", len(results), len(emails), len(unclassified))
        
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)
    except Exception as e:
        log.error("Classify error: %s", e)
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
