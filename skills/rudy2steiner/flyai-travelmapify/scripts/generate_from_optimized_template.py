#!/usr/bin/env python3
"""
Generate travel maps using the optimized Shanghai template as the main template.
This replaces the unified template with the enhanced version that has:
- Real FlyAI hotel search integration
- No alert popups (notification system instead)
- Loading states and timeout handling
- Professional UX improvements
"""

import os
import sys
import json
import argparse
import re

def load_optimized_template():
    """Load the optimized Shanghai template"""
    template_path = '/Users/xuandu/.openclaw/workspace/apps/shanghai-travel/shanghai-final-optimized.html'
    if not os.path.exists(template_path):
        # Fallback to assets template if Shanghai template not found
        template_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'unified-map-template.html')
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_poi_js_array(pois):
    """Generate JavaScript POI array from POI list"""
    js_lines = ['        var markers = [];']
    js_lines.append('        var poiList = [')
    
    for poi in pois:
        name = poi.get('name', 'Unnamed Location')
        address = poi.get('address', '')
        rating = poi.get('rating', '')
        poi_id = poi.get('id', '')
        
        # Handle location coordinates
        if isinstance(poi.get('location'), list) and len(poi['location']) == 2:
            lng, lat = poi['location'][0], poi['location'][1]
        else:
            # Use approximate coordinates if not available (shouldn't happen with proper geocoding)
            lng, lat = 116.4074, 39.9042  # Beijing default
        
        js_lines.append('            {')
        js_lines.append(f'                name: "{name}",')
        js_lines.append(f'                location: [{lng}, {lat}],')
        js_lines.append(f'                address: "{address}",')
        js_lines.append(f'                rating: "{rating}",')
        js_lines.append(f'                id: "{poi_id}"')
        js_lines.append('            },')
    
    # Remove trailing comma from last item if exists
    if len(js_lines) > 2:
        js_lines[-1] = '            }'
    
    js_lines.append('        ];')
    return '\n'.join(js_lines)

def replace_poi_section(template_content, pois):
    """Replace the POI initialization section in the template"""
    poi_js = generate_poi_js_array(pois)
    
    # Find the existing POI section pattern
    pattern = r'var markers = \[\];\s+var poiList = \[[\s\S]*?\];'
    
    if re.search(pattern, template_content):
        # Replace existing POI section
        new_content = re.sub(pattern, poi_js, template_content)
    else:
        # If pattern not found, try alternative pattern
        alt_pattern = r'var poiList = \[[\s\S]*?\];'
        if re.search(alt_pattern, template_content):
            new_content = re.sub(alt_pattern, poi_js, template_content)
        else:
            # If no POI section found, insert after markers declaration
            markers_pattern = r'(var markers = \[\];)'
            if re.search(markers_pattern, template_content):
                new_content = re.sub(markers_pattern, f'\\1\n{poi_js}', template_content)
            else:
                raise ValueError("Could not find POI section in template")
    
    return new_content

def main():
    parser = argparse.ArgumentParser(description='Generate travel map using optimized template')
    parser.add_argument('input_file', help='Input JSON file with geocoded POIs')
    parser.add_argument('output_file', help='Output HTML file path')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)
    
    # Load POIs
    with open(args.input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # Extract POIs
    if isinstance(input_data, list):
        pois = input_data
    elif 'filtered_geocoded_pois' in input_data:
        pois = input_data['filtered_geocoded_pois']
    elif 'geocoded_pois' in input_data:
        pois = input_data['geocoded_pois']
    else:
        print("Error: Input file must contain POIs in 'filtered_geocoded_pois', 'geocoded_pois', or as root array", file=sys.stderr)
        sys.exit(1)
    
    if not pois:
        print("Error: No POIs found in input file", file=sys.stderr)
        sys.exit(1)
    
    # Load template
    try:
        template_content = load_optimized_template()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Replace POI section
    try:
        updated_content = replace_poi_section(template_content, pois)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Travel map generated using optimized template: {args.output_file}")
    print(f"\n💡 IMPORTANT: To view the map properly, start a local HTTP server:")
    print(f"   cd /Users/xuandu/.openclaw/workspace")
    print(f"   python3 -m http.server 9000")
    print(f"   Then open: http://localhost:9000/{os.path.basename(args.output_file)}")

if __name__ == '__main__':
    main()