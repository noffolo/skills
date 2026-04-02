#!/usr/bin/env python3
"""
Enhanced route extraction from travel planning images using AI analysis.
Supports both sequential routes (multi-city loops) and multi-day itineraries.
"""

import os
import sys
import json
import argparse
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    """
    Extract text from image using Tesseract OCR with Chinese+English support
    """
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        text = pytesseract.image_to_string(
            img, 
            lang='chi_sim+eng',
            config='--psm 6 --oem 1'
        )
        return text.strip()
    
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}", file=sys.stderr)
        return ""

def analyze_route_structure(text, ai_analysis):
    """
    Analyze route structure based on AI analysis and extracted text.
    Handles three main types:
    1. Sequential multi-city routes (like Hainan circular route)
    2. Multi-day itineraries (like Sanya 2-day plan)
    3. Hub-and-spoke geographic maps (like hand-drawn Sanya map)
    """
    # Check if this is a multi-day itinerary based on AI analysis
    if "Day 1" in ai_analysis or "第1天" in ai_analysis or "两日游" in ai_analysis:
        return parse_multi_day_itinerary(ai_analysis)
    elif "凤凰机场" in ai_analysis or "枢纽" in ai_analysis or "hub" in ai_analysis.lower() or "spoke" in ai_analysis.lower():
        return parse_hub_and_spoke_map(ai_analysis)
    elif "→" in ai_analysis or "环线" in ai_analysis or "环岛" in ai_analysis:
        return parse_sequential_route(ai_analysis)
    else:
        # Fallback to basic POI extraction
        return parse_basic_pois(ai_analysis)

def parse_multi_day_itinerary(ai_analysis):
    """
    Parse multi-day itinerary structure with day-by-day breakdowns
    """
    days = []
    
    # Split by day markers
    day_sections = []
    if "Day 1" in ai_analysis:
        # English format
        sections = ai_analysis.split("Day ")
        for section in sections[1:]:  # Skip first empty part
            if section.strip():
                day_num = section.split(":")[0].split()[0] if ":" in section else section.split()[0]
                day_content = "Day " + section
                day_sections.append((f"Day {day_num}", day_content))
    else:
        # Chinese format
        sections = ai_analysis.split("第")
        for section in sections[1:]:
            if section.strip() and "天" in section:
                day_num = section.split("天")[0]
                day_content = f"第{section}"
                day_sections.append((f"第{day_num}天", day_content))
    
    for day_name, day_content in day_sections:
        # Extract locations in order for this day
        locations = extract_locations_from_day_content(day_content)
        days.append({
            'day': day_name,
            'locations': locations,
            'description': day_content[:200] + "..." if len(day_content) > 200 else day_content
        })
    
    return {
        'route_type': 'multi_day_itinerary',
        'days': days,
        'total_days': len(days)
    }

def extract_locations_from_day_content(day_content):
    """
    Extract ordered locations from day content, preserving sequence
    """
    locations = []
    
    # Look for location patterns with arrows or sequences
    lines = day_content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Look for location names followed by details
        if any(loc_marker in line for loc_marker in ['→', '起点', '终点', '推荐', '亮点']):
            # Extract location name before details
            if '→' in line:
                parts = line.split('→')
                for part in parts:
                    loc = part.strip().split('(')[0].split('（')[0].strip()
                    if loc and len(loc) > 1:
                        locations.append(loc)
            else:
                # Try to extract location from line
                loc = extract_location_from_line(line)
                if loc:
                    locations.append(loc)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_locations = []
    for loc in locations:
        if loc not in seen:
            unique_locations.append(loc)
            seen.add(loc)
    
    return unique_locations

def extract_locations_from_route_line(line):
    """
    Extract locations from a route line that may contain arrows and distances
    """
    locations = []
    
    # Handle arrow-separated locations
    if '→' in line:
        parts = line.split('→')
        for part in parts:
            # Remove distance info and other details
            clean_part = part.split('km')[0].split('(')[0].split('（')[0]
            clean_part = clean_part.replace('约', '').replace('打车', '').replace('骑行', '').replace('步行', '').strip()
            if clean_part and len(clean_part) > 1:
                locations.append(clean_part)
    else:
        # Try to extract individual locations
        loc = extract_location_from_line(line)
        if loc:
            locations.append(loc)
    
    return locations

def extract_location_from_line(line):
    """
    Extract location name from a line of text
    """
    # Remove time/duration info
    line = line.split('分钟')[0].split('小时')[0].split('(')[0].split('（')[0]
    line = line.replace('打车', '').replace('骑行', '').replace('步行', '').replace('乘船', '')
    line = line.strip(' →').strip()
    
    # Keep only reasonable length location names
    if 2 <= len(line) <= 30 and any(c.isalpha() or '\u4e00' <= c <= '\u9fff' for c in line):
        return line
    return None

def parse_sequential_route(ai_analysis):
    """
    Parse sequential route with arrows (→) indicating direction
    """
    # Find the main route sequence
    route_line = ""
    if "→" in ai_analysis:
        lines = ai_analysis.split('\n')
        for line in lines:
            if "→" in line and len(line.split("→")) > 2:
                route_line = line
                break
    
    if not route_line:
        # Fallback: look for any line with multiple locations
        lines = ai_analysis.split('\n')
        for line in lines:
            if any(loc_word in line for loc_word in ['三亚', '海口', '文昌', '琼海', '万宁', '陵水']):
                route_line = line
                break
    
    locations = []
    if route_line:
        # Split by arrow and clean up
        parts = route_line.split('→')
        for part in parts:
            loc = part.strip().split('(')[0].split('（')[0].strip()
            if loc and len(loc) > 1:
                locations.append(loc)
    
    return {
        'route_type': 'sequential_route',
        'locations': locations,
        'is_circular': '环线' in ai_analysis or '环岛' in ai_analysis,
        'description': ai_analysis[:200] + "..." if len(ai_analysis) > 200 else ai_analysis
    }

def parse_hub_and_spoke_map(ai_analysis):
    """
    Parse hub-and-spoke geographic map with central hub and multiple route branches
    """
    routes = []
    
    # Look for route sections in the AI analysis
    lines = ai_analysis.split('\n')
    current_route = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for route headers
        if any(route_marker in line for route_marker in ['北部海岸线', '西部海岛', '市中心经典线', '东部海湾线', '南部公路风景线', 'Northern Coast', 'Western Island', 'Central City', 'Eastern Bay', 'Southern Scenic']):
            if current_route:
                routes.append(current_route)
            current_route = {
                'name': line.strip('【】🔹✅⚠️📍🗺️📌').strip(),
                'locations': [],
                'distances': []
            }
        elif current_route and ('→' in line or 'km' in line):
            # Extract locations and distances from route line
            locations_in_line = extract_locations_from_route_line(line)
            current_route['locations'].extend(locations_in_line)
            
            # Extract distance if present
            if 'km' in line:
                import re
                distance_match = re.search(r'(\d+\.?\d*)\s*km', line)
                if distance_match:
                    current_route['distances'].append(float(distance_match.group(1)))
    
    if current_route:
        routes.append(current_route)
    
    # Remove duplicates while preserving order in each route
    for route in routes:
        seen = set()
        unique_locations = []
        for loc in route['locations']:
            if loc not in seen:
                unique_locations.append(loc)
                seen.add(loc)
        route['locations'] = unique_locations
    
    return {
        'route_type': 'hub_and_spoke_map',
        'hub': '凤凰机场' if '凤凰机场' in ai_analysis else 'Central Hub',
        'routes': routes,
        'total_routes': len(routes),
        'description': ai_analysis[:200] + "..." if len(ai_analysis) > 200 else ai_analysis
    }

def parse_basic_pois(ai_analysis):
    """
    Fallback basic POI extraction when route structure isn't clear
    """
    # Use existing POI extraction logic
    lines = ai_analysis.split('\n')
    pois = []
    
    location_keywords = [
        '街', '路', '广场', '公园', '博物馆', '景区', '大厦', '中心',
        'street', 'road', 'avenue', 'plaza', 'park', 'museum', 'center',
        '机场', '码头', '港口', '车站', 'airport', 'port', 'station'
    ]
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 2:
            continue
            
        if any(skip_word in line.lower() for skip_word in ['phone', 'tel', '电话', '联系方式', 'contact']):
            continue
            
        has_location_keyword = any(keyword in line for keyword in location_keywords)
        has_chinese_chars = any('\u4e00' <= char <= '\u9fff' for char in line)
        has_english_words = any(char.isalpha() for char in line)
        
        if has_chinese_chars or has_location_keyword or (has_english_words and len(line.split()) <= 5):
            poi_name = line.replace('\t', ' ').replace('  ', ' ').strip()
            if poi_name:
                pois.append(poi_name)
    
    return {
        'route_type': 'basic_pois',
        'locations': pois,
        'description': ai_analysis[:200] + "..." if len(ai_analysis) > 200 else ai_analysis
    }

def main():
    parser = argparse.ArgumentParser(description='Extract route structure from travel planning images')
    parser.add_argument('image_path', help='Path to the input image file')
    parser.add_argument('--ai-analysis', required=True, help='AI analysis text of the image content')
    parser.add_argument('--output', '-o', help='Output JSON file path (default: stdout)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image_path):
        print(f"Error: Image file not found: {args.image_path}", file=sys.stderr)
        sys.exit(1)
    
    # Extract raw text (for reference)
    raw_text = extract_text_from_image(args.image_path)
    
    # Analyze route structure using AI analysis
    route_data = analyze_route_structure(raw_text, args.ai_analysis)
    
    # Prepare output
    result = {
        'source_image': args.image_path,
        'extracted_text': raw_text,
        'ai_analysis': args.ai_analysis,
        'route_data': route_data
    }
    
    # Output result
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Route extraction results saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()