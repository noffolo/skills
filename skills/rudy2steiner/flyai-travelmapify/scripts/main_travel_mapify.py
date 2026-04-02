#!/usr/bin/env python3
"""
Main entry point for Travel Mapify skill.
Supports both image input (OCR extraction) and direct text input (comma-separated locations).
"""

import os
import sys
import json
import argparse
import subprocess
from typing import List, Dict

# Script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def parse_text_locations(text_input: str) -> List[Dict]:
    """
    Parse comma-separated location names into POI format
    """
    if not text_input.strip():
        return []
    
    # Split by commas and clean up whitespace
    location_names = [name.strip() for name in text_input.split(',') if name.strip()]
    
    pois = []
    for i, name in enumerate(location_names):
        pois.append({
            'name': name,
            'confidence': 1.0,  # High confidence for direct user input
            'source': 'text_input'
        })
    
    return pois

def process_image_input(image_path: str, output_json: str) -> bool:
    """
    Process image input using existing OCR pipeline
    """
    try:
        # Use existing extract_pois_from_image.py script
        extract_script = os.path.join(SCRIPT_DIR, 'extract_pois_from_image.py')
        
        if not os.path.exists(extract_script):
            print(f"Error: OCR script not found: {extract_script}", file=sys.stderr)
            return False
        
        # Run OCR extraction
        cmd = [sys.executable, extract_script, image_path, '--output', output_json]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"OCR extraction failed: {result.stderr}", file=sys.stderr)
            return False
        
        print("OCR extraction completed successfully")
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        return False

def process_text_input(text_input: str, output_json: str) -> bool:
    """
    Process direct text input of location names
    """
    try:
        pois = parse_text_locations(text_input)
        
        if not pois:
            print("Error: No valid locations found in text input", file=sys.stderr)
            return False
        
        # Save to JSON file
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(pois, f, ensure_ascii=False, indent=2)
        
        print(f"Processed {len(pois)} locations from text input")
        return True
        
    except Exception as e:
        print(f"Error processing text input: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Travel Mapify - Create interactive travel maps')
    parser.add_argument('--image', '-i', help='Input image file path (for OCR extraction)')
    parser.add_argument('--locations', '-l', help='Comma-separated location names (direct text input)')
    parser.add_argument('--output-json', '-j', required=True, help='Output JSON file for extracted/geocoded POIs')
    parser.add_argument('--city', default='上海', help='Default city for geocoding (default: 上海)')
    parser.add_argument('--proxy-url', default='http://localhost:8769/api/search', 
                       help='Amap API proxy URL')
    
    args = parser.parse_args()
    
    # Validate input - exactly one of image or locations must be provided
    if args.image and args.locations:
        print("Error: Please provide either --image OR --locations, not both", file=sys.stderr)
        sys.exit(1)
    elif not args.image and not args.locations:
        print("Error: Please provide either --image or --locations", file=sys.stderr)
        sys.exit(1)
    
    # Process input based on type
    temp_poi_file = args.output_json + '.raw_pois.json'
    
    if args.image:
        print(f"Processing image: {args.image}")
        if not os.path.exists(args.image):
            print(f"Error: Image file not found: {args.image}", file=sys.stderr)
            sys.exit(1)
        success = process_image_input(args.image, temp_poi_file)
    else:
        print(f"Processing text locations: {args.locations}")
        success = process_text_input(args.locations, temp_poi_file)
    
    if not success:
        sys.exit(1)
    
    # Now geocode the extracted POIs
    print("Geocoding POIs...")
    geocode_script = os.path.join(SCRIPT_DIR, 'geocode_locations.py')
    
    if not os.path.exists(geocode_script):
        print(f"Error: Geocoding script not found: {geocode_script}", file=sys.stderr)
        sys.exit(1)
    
    # Run geocoding
    cmd = [
        sys.executable, geocode_script, temp_poi_file,
        '--output', args.output_json,
        '--city', args.city,
        '--proxy-url', args.proxy_url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Geocoding failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print("Geocoding completed successfully")
    
    # Clean up temporary file
    try:
        os.remove(temp_poi_file)
    except:
        pass
    
    print(f"Final geocoded POIs saved to: {args.output_json}")

if __name__ == '__main__':
    main()