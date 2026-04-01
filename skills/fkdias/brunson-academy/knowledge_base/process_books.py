#!/usr/bin/env python3
"""
Process Brunson book texts for knowledge base
"""
import os
import json
from pathlib import Path
import re

def extract_frameworks(text, book_name):
    """Extract key frameworks from book text"""
    frameworks = {
        "value_ladder": [],
        "epiphany_bridge": [],
        "dream_100": [],
        "webinar": [],
        "scripts": [],
        "concepts": []
    }
    
    # Expert Secrets patterns
    if "Expert Secrets" in book_name or "EXPERT SECRETS" in text[:1000]:
        # Epiphany Bridge structure
        epiphany_patterns = [
            r"Epiphany Bridge",
            r"Secret #6.*Epiphany Bridge",
            r"create.*epiphany",
            r"belief.*pattern",
            r"false belief"
        ]
        
        for pattern in epiphany_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context around match
                start = max(0, match.start() - 200)
                end = min(len(text), match.end() + 300)
                context = text[start:end].strip()
                frameworks["epiphany_bridge"].append({
                    "concept": match.group(),
                    "context": context,
                    "book": book_name,
                    "position": match.start()
                })
    
    # DotCom Secrets patterns
    if "DotCom Secrets" in book_name or "DOTCOM SECRETS" in text[:1000]:
        # Value Ladder patterns
        value_patterns = [
            r"Value Ladder",
            r"Secret #2.*Value Ladder",
            r"tripwire",
            r"core offer",
            r"profit maximizer",
            r"backend offer"
        ]
        
        for pattern in value_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 200)
                end = min(len(text), match.end() + 300)
                context = text[start:end].strip()
                frameworks["value_ladder"].append({
                    "concept": match.group(),
                    "context": context,
                    "book": book_name,
                    "position": match.start()
                })
    
    # Traffic Secrets patterns
    if "Traffic Secrets" in book_name or "TRAFFIC SECRETS" in text[:1000]:
        # Dream 100 patterns
        traffic_patterns = [
            r"Dream 100",
            r"traffic.*secret",
            r"audience",
            r"outreach",
            r"partnership"
        ]
        
        for pattern in traffic_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 200)
                end = min(len(text), match.end() + 300)
                context = text[start:end].strip()
                frameworks["dream_100"].append({
                    "concept": match.group(),
                    "context": context,
                    "book": book_name,
                    "position": match.start()
                })
    
    # General webinar patterns (all books)
    webinar_patterns = [
        r"Perfect Webinar",
        r"webinar.*model",
        r"webinar.*script",
        r"Secret #12.*Perfect Webinar",
        r"Secret #17.*Perfect Webinar"
    ]
    
    for pattern in webinar_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 200)
            end = min(len(text), match.end() + 300)
            context = text[start:end].strip()
            frameworks["webinar"].append({
                "concept": match.group(),
                "context": context,
                "book": book_name,
                "position": match.start()
            })
    
    return frameworks

def process_all_books():
    """Process all extracted book texts"""
    # Paths to extracted texts
    workspace = Path(r"C:\Users\fkdia\.openclaw\workspace")
    books_dir = workspace / "brunson_books"
    
    books = [
        ("Expert_Secrets.txt", "Expert Secrets"),
        ("DotCom_Secrets.txt", "DotCom Secrets"),
        ("Traffic_Secrets.txt", "Traffic Secrets")
    ]
    
    all_frameworks = {
        "books": {},
        "frameworks_by_type": {
            "value_ladder": [],
            "epiphany_bridge": [],
            "dream_100": [],
            "webinar": [],
            "scripts": [],
            "concepts": []
        },
        "stats": {
            "total_books": 0,
            "total_words": 0,
            "total_concepts": 0
        }
    }
    
    for filename, book_name in books:
        filepath = books_dir / filename
        if not filepath.exists():
            print(f"❌ File not found: {filepath}")
            continue
        
        print(f"Processing: {book_name}")
        
        # Read text
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Basic stats
        word_count = len(text.split())
        char_count = len(text)
        
        # Extract frameworks
        frameworks = extract_frameworks(text, book_name)
        
        # Store book data
        all_frameworks["books"][book_name] = {
            "filename": filename,
            "word_count": word_count,
            "char_count": char_count,
            "frameworks_count": sum(len(v) for v in frameworks.values()),
            "frameworks": frameworks
        }
        
        # Aggregate by framework type
        for fw_type, items in frameworks.items():
            all_frameworks["frameworks_by_type"][fw_type].extend(items)
        
        # Update stats
        all_frameworks["stats"]["total_books"] += 1
        all_frameworks["stats"]["total_words"] += word_count
        all_frameworks["stats"]["total_concepts"] += sum(len(v) for v in frameworks.values())
        
        print(f"  Words: {word_count:,}, Concepts: {sum(len(v) for v in frameworks.values())}")
    
    # Save processed data
    output_dir = Path(__file__).parent
    frameworks_path = output_dir / "frameworks.json"
    summary_path = output_dir / "summary.md"
    
    # Save JSON
    with open(frameworks_path, 'w', encoding='utf-8') as f:
        json.dump(all_frameworks, f, indent=2, ensure_ascii=False)
    
    # Create summary
    create_summary(all_frameworks, summary_path)
    
    print(f"\nProcessed {all_frameworks['stats']['total_books']} books")
    print(f"Total words: {all_frameworks['stats']['total_words']:,}")
    print(f"Total concepts: {all_frameworks['stats']['total_concepts']}")
    print(f"Saved to: {frameworks_path}")
    
    return all_frameworks

def create_summary(frameworks, output_path):
    """Create readable summary of frameworks"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 📚 Brunson Books Knowledge Base Summary\n\n")
        
        f.write("## 📊 Statistics\n")
        f.write(f"- **Total Books:** {frameworks['stats']['total_books']}\n")
        f.write(f"- **Total Words:** {frameworks['stats']['total_words']:,}\n")
        f.write(f"- **Total Concepts:** {frameworks['stats']['total_concepts']}\n\n")
        
        f.write("## 📖 Books Processed\n")
        for book_name, data in frameworks["books"].items():
            f.write(f"### {book_name}\n")
            f.write(f"- **Words:** {data['word_count']:,}\n")
            f.write(f"- **Concepts Found:** {data['frameworks_count']}\n")
            
            # List framework types found
            fw_types = [k for k, v in data['frameworks'].items() if v]
            if fw_types:
                f.write(f"- **Framework Types:** {', '.join(fw_types)}\n")
            f.write("\n")
        
        f.write("## 🎯 Frameworks by Type\n")
        for fw_type, items in frameworks["frameworks_by_type"].items():
            if items:
                f.write(f"### {fw_type.replace('_', ' ').title()}\n")
                f.write(f"- **Count:** {len(items)}\n")
                
                # Group by book
                by_book = {}
                for item in items:
                    book = item['book']
                    if book not in by_book:
                        by_book[book] = []
                    by_book[book].append(item['concept'])
                
                for book, concepts in by_book.items():
                    f.write(f"- **{book}:** {len(concepts)} concepts\n")
                    # Show unique concepts
                    unique_concepts = list(set(concepts))[:5]  # Limit to 5
                    for concept in unique_concepts:
                        f.write(f"  - {concept}\n")
                f.write("\n")
        
        f.write("## 🔧 Usage Examples\n")
        f.write("```python\n")
        f.write("# Load frameworks\n")
        f.write("import json\n")
        f.write("with open('frameworks.json', 'r') as f:\n")
        f.write("    data = json.load(f)\n")
        f.write("\n")
        f.write("# Get all Value Ladder concepts\n")
        f.write("value_ladders = data['frameworks_by_type']['value_ladder']\n")
        f.write("print(f\"Found {len(value_ladders)} Value Ladder concepts\")\n")
        f.write("```\n")

if __name__ == "__main__":
    process_all_books()