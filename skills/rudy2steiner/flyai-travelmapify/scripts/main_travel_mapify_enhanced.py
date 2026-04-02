#!/usr/bin/env python3
"""
Enhanced main entry point for Travel Mapify skill.
Supports both image input (OCR extraction) and direct text input (comma-separated locations).
Automatically starts HTTP server and hotel search server when generating maps.
"""

import os
import sys
import json
import argparse
import subprocess
import socket
import time
from typing import List, Dict

# Script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = "/Users/xuandu/.openclaw/workspace"

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_http_server(port=9000):
    """Start HTTP server in background if not already running"""
    if is_port_in_use(port):
        print(f"HTTP server already running on port {port}")
        return True
    
    try:
        # Start HTTP server in background
        cmd = [sys.executable, "-m", "http.server", str(port)]
        http_process = subprocess.Popen(
            cmd,
            cwd=WORKSPACE_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp  # Create new process group
        )
        
        # Wait a moment for server to start
        time.sleep(1)
        
        if http_process.poll() is None:
            print(f"HTTP server started on http://localhost:{port}")
            return True
        else:
            print(f"Failed to start HTTP server on port {port}")
            return False
            
    except Exception as e:
        print(f"Error starting HTTP server: {e}", file=sys.stderr)
        return False

def start_hotel_search_server(port=8770):
    """Start hotel search server in background if not already running"""
    if is_port_in_use(port):
        print(f"Hotel search server already running on port {port}")
        return True
    
    try:
        hotel_server_script = os.path.join(WORKSPACE_DIR, "apps", "shanghai-travel", "hotel-search-server-real.py")
        if not os.path.exists(hotel_server_script):
            # Try alternative location
            hotel_server_script = os.path.join(WORKSPACE_DIR, "hotel-search-server-real.py")
            if not os.path.exists(hotel_server_script):
                print("Error: Hotel search server script not found", file=sys.stderr)
                return False
        
        # Start hotel search server in background
        cmd = [sys.executable, hotel_server_script, str(port)]
        hotel_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp  # Create new process group
        )
        
        # Wait a moment for server to start
        time.sleep(1)
        
        if hotel_process.poll() is None:
            print(f"Hotel search server started on http://localhost:{port}")
            return True
        else:
            print(f"Failed to start hotel search server on port {port}")
            return False
            
    except Exception as e:
        print(f"Error starting hotel search server: {e}", file=sys.stderr)
        return False

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

def generate_map_with_optimized_template(input_json, output_html):
    """Generate map using Beijing template with user input POIs"""
    try:
        # Use Beijing template generator (primary)
        generate_script = os.path.join(SCRIPT_DIR, 'generate_from_beijing_template.py')
        if not os.path.exists(generate_script):
            # Fallback to unique ID generator
            generate_script = os.path.join(SCRIPT_DIR, 'generate_with_unique_id.py')
            if not os.path.exists(generate_script):
                # Fallback to clean template
                generate_script = os.path.join(SCRIPT_DIR, 'generate_from_clean_template.py')
                if not os.path.exists(generate_script):
                    print(f"Error: No template generators found", file=sys.stderr)
                    return False
        
        cmd = [sys.executable, generate_script, input_json, output_html]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Map generation failed: {result.stderr}", file=sys.stderr)
            return False
        
        print(f"Map generated successfully: {output_html}")
        return True
        
    except Exception as e:
        print(f"Error generating map: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Travel Mapify - Create interactive travel maps')
    parser.add_argument('--image', '-i', help='Input image file path (for OCR extraction)')
    parser.add_argument('--locations', '-l', help='Comma-separated location names (direct text input)')
    parser.add_argument('--output-html', '-o', required=True, help='Output HTML file for the travel map')
    parser.add_argument('--city', default='上海', help='Default city for geocoding (default: 上海)')
    parser.add_argument('--proxy-url', default='http://localhost:8769/api/search', 
                       help='Amap API proxy URL')
    parser.add_argument('--http-port', type=int, default=9000, help='HTTP server port (default: 9000)')
    parser.add_argument('--hotel-port', type=int, default=8770, help='Hotel search server port (default: 8770)')
    
    args = parser.parse_args()
    
    # Validate input - exactly one of image or locations must be provided
    if args.image and args.locations:
        print("Error: Please provide either --image OR --locations, not both", file=sys.stderr)
        sys.exit(1)
    elif not args.image and not args.locations:
        print("Error: Please provide either --image or --locations", file=sys.stderr)
        sys.exit(1)
    
    # Create temporary JSON file for POIs
    temp_json = args.output_html.replace('.html', '_pois.json')
    
    # Process input based on type
    temp_poi_file = temp_json + '.raw_pois.json'
    
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
        '--output', temp_json,
        '--city', args.city,
        '--proxy-url', args.proxy_url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Geocoding failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print("Geocoding completed successfully")
    
    # Clean up temporary raw POI file
    try:
        os.remove(temp_poi_file)
    except:
        pass
    
    # Generate map using optimized template
    print("Generating travel map with optimized template...")
    if not generate_map_with_optimized_template(temp_json, args.output_html):
        sys.exit(1)
    
    # Clean up temporary JSON file
    try:
        os.remove(temp_json)
    except:
        pass
    
    # Start required servers
    print("\nStarting required servers...")
    http_success = start_http_server(args.http_port)
    hotel_success = start_hotel_search_server(args.hotel_port)
    
    if http_success and hotel_success:
        print(f"\n✅ Travel map ready!")
        print(f"🔗 Access your map at: http://localhost:{args.http_port}/{os.path.basename(args.output_html)}")
        print(f"🏨 Hotel search functionality: ACTIVE")
        print(f"🚀 All servers running successfully!")
    else:
        print(f"\n⚠️  Travel map generated but some servers may not be running")
        print(f"🔗 Manual access: http://localhost:{args.http_port}/{os.path.basename(args.output_html)}")
        if not http_success:
            print(f"❌ HTTP server failed to start - please start manually")
        if not hotel_success:
            print(f"❌ Hotel search server failed to start - hotel search may not work")

if __name__ == '__main__':
    main()