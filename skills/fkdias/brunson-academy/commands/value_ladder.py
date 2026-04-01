#!/usr/bin/env python3
"""
Value Ladder command for Brunson Academy
Based on DotCom Secrets framework
"""
import json
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def load_frameworks():
    """Load processed frameworks from knowledge base"""
    kb_path = Path(__file__).parent.parent / "knowledge_base" / "frameworks.json"
    with open(kb_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_value_ladder(product_name, target_audience=None, price_range=None):
    """
    Build a Value Ladder based on Brunson's framework
    
    Args:
        product_name: Name of the core product
        target_audience: Optional target audience description
        price_range: Optional price range (low, medium, high)
    
    Returns:
        dict: Complete Value Ladder structure
    """
    frameworks = load_frameworks()
    
    # Get Value Ladder concepts from knowledge base
    vl_concepts = frameworks["frameworks_by_type"]["value_ladder"]
    
    # Default structure based on Brunson's framework
    value_ladder = {
        "product": product_name,
        "target_audience": target_audience or "High-value investors",
        "framework": "Russell Brunson Value Ladder (DotCom Secrets)",
        "rungs": []
    }
    
    # Define rungs based on Brunson's framework
    rungs = [
        {
            "name": "Tripwire",
            "description": "Low-cost, low-risk entry point to build trust",
            "price_strategy": "Inexpensive (R$ 0 - R$ 97)",
            "purpose": "Acquire customer, demonstrate value, start relationship",
            "examples": ["Free webinar", "E-book", "Mini-course", "Consultation call"],
            "brunson_reference": "Secret #2: The Value Ladder - Front End"
        },
        {
            "name": "Core Offer",
            "description": "Main product that delivers core transformation",
            "price_strategy": "Mid-range (R$ 997 - R$ 15,000)",
            "purpose": "Deliver primary value, achieve customer goals",
            "examples": ["Masterclass", "Group coaching", "Software license", "Certification"],
            "brunson_reference": "Secret #2: The Value Ladder - Core Offer"
        },
        {
            "name": "Profit Maximizer",
            "description": "High-ticket offer for maximum results",
            "price_strategy": "High-end (R$ 15,000 - R$ 50,000+)",
            "purpose": "Deep transformation, personalized attention, premium results",
            "examples": ["1:1 Mentorship", "VIP Day", "Annual mastermind", "Executive coaching"],
            "brunson_reference": "Secret #2: The Value Ladder - Profit Maximizer"
        },
        {
            "name": "Back-End / Continuity",
            "description": "Ongoing value and community",
            "price_strategy": "Recurring (R$ 997 - R$ 5,000/month)",
            "purpose": "Long-term relationship, ongoing support, community access",
            "examples": ["Membership community", "Monthly mastermind", "Software updates", "Coaching continuity"],
            "brunson_reference": "Secret #2: The Value Ladder - Back End"
        }
    ]
    
    # Customize based on product type
    if "invest" in product_name.lower() or "master" in product_name.lower():
        # Investment/financial product customization
        rungs[0]["examples"] = ["Free investment analysis", "5 Dimensões e-book", "Market webinar"]
        rungs[1]["examples"] = [f"{product_name} program", "Investment framework course"]
        rungs[2]["examples"] = ["1:1 Portfolio review", "VIP investment strategy session"]
        rungs[3]["examples"] = ["Investor community", "Monthly market updates", "Deal flow access"]
    
    elif "course" in product_name.lower() or "training" in product_name.lower():
        # Educational product customization
        rungs[0]["examples"] = ["Free introductory module", "Sample lesson", "Strategy session"]
        rungs[1]["examples"] = [f"Complete {product_name}", "Certification program"]
        rungs[2]["examples"] = ["Personalized coaching add-on", "Implementation support"]
        rungs[3]["examples"] = ["Alumni community", "Advanced modules", "Mastermind group"]
    
    # Adjust pricing based on range
    if price_range == "low":
        rungs[1]["price_strategy"] = "Mid-range (R$ 497 - R$ 2,997)"
        rungs[2]["price_strategy"] = "High-end (R$ 5,000 - R$ 15,000)"
    elif price_range == "high":
        rungs[1]["price_strategy"] = "Mid-range (R$ 5,000 - R$ 25,000)"
        rungs[2]["price_strategy"] = "High-end (R$ 25,000 - R$ 100,000+)"
    
    value_ladder["rungs"] = rungs
    
    # Add implementation tips from knowledge base
    implementation_tips = []
    for concept in vl_concepts[:5]:  # Get first 5 relevant concepts
        if "tripwire" in concept["concept"].lower() or "value" in concept["concept"].lower():
            tip = {
                "tip": concept["concept"],
                "context": concept["context"][:150] + "..." if len(concept["context"]) > 150 else concept["context"],
                "source": concept["book"]
            }
            implementation_tips.append(tip)
    
    value_ladder["implementation_tips"] = implementation_tips
    
    return value_ladder

def format_value_ladder_output(value_ladder, format_type="markdown"):
    """Format Value Ladder for output"""
    if format_type == "markdown":
        return format_markdown(value_ladder)
    elif format_type == "json":
        return json.dumps(value_ladder, indent=2, ensure_ascii=False)
    else:
        return str(value_ladder)

def format_markdown(value_ladder):
    """Format as Markdown for Telegram/readability"""
    output = []
    
    output.append(f"# 🎯 VALUE LADDER: {value_ladder['product']}")
    output.append("")
    output.append(f"**Framework:** {value_ladder['framework']}")
    output.append(f"**Target Audience:** {value_ladder['target_audience']}")
    output.append("")
    output.append("---")
    output.append("")
    
    for i, rung in enumerate(value_ladder["rungs"], 1):
        output.append(f"## {i}. {rung['name'].upper()}")
        output.append("")
        output.append(f"**Descrição:** {rung['description']}")
        output.append(f"**Estratégia de Preço:** {rung['price_strategy']}")
        output.append(f"**Propósito:** {rung['purpose']}")
        output.append("")
        output.append("**Exemplos concretos:**")
        for example in rung["examples"]:
            output.append(f"- {example}")
        output.append("")
        output.append(f"*Referência Brunson:* {rung['brunson_reference']}")
        output.append("")
    
    if value_ladder.get("implementation_tips"):
        output.append("## 💡 DICAS DE IMPLEMENTAÇÃO (Do Brunson)")
        output.append("")
        for tip in value_ladder["implementation_tips"][:3]:  # Limit to 3 tips
            output.append(f"**{tip['tip']}**")
            output.append(f"> {tip['context']}")
            output.append(f"*Fonte: {tip['source']}*")
            output.append("")
    
    output.append("## 🚀 PRÓXIMOS PASSOS")
    output.append("")
    output.append("1. **Definir Tripwire específico** - Criar oferta de entrada")
    output.append("2. **Estruturar Core Offer** - Desenvolver produto principal")
    output.append("3. **Design Profit Maximizer** - Planejar oferta premium")
    output.append("4. **Criar Back-End** - Estabelecer continuidade")
    output.append("5. **Implementar funil** - Conectar os degraus")
    output.append("")
    output.append("---")
    output.append("*Gerado por Brunson Academy • Baseado em DotCom Secrets*")
    
    return "\n".join(output)

def main():
    """Test function"""
    # Example: Master Business Value Ladder
    product = "Master Business"
    audience = "Investidores com 500k+ para aplicar"
    
    print("Building Value Ladder for:", product)
    print("Target:", audience)
    print("-" * 50)
    
    ladder = build_value_ladder(product, audience, price_range="high")
    output = format_value_ladder_output(ladder, "markdown")
    
    # Save to file for testing
    test_path = Path(__file__).parent.parent / "test_value_ladder.md"
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print("Output saved to:", test_path)
    
    # Print preview
    lines = output.split('\n')[:30]
    print("\n".join(lines))
    print("\n... [truncated] ...")
    
    return ladder

if __name__ == "__main__":
    main()