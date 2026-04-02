#!/usr/bin/env python3
"""
Geocode POI locations using Amap Web API through local proxy server.
Resolves location names to precise coordinates (longitude, latitude).
"""

import os
import sys
import json
import argparse
import requests
from typing import List, Dict, Optional

# Default Amap API configuration
DEFAULT_PROXY_URL = "http://localhost:8769/api/search"
DEFAULT_CITY = "重庆"  # Default city for geocoding

class AmapGeocoder:
    def __init__(self, proxy_url: str = DEFAULT_PROXY_URL, city: str = DEFAULT_CITY):
        self.proxy_url = proxy_url
        self.city = city
        
    def geocode_poi(self, poi_name: str) -> Optional[Dict]:
        """
        Geocode a single POI name to get coordinates and additional info
        """
        try:
            params = {
                'q': poi_name,
                'city': self.city
            }
            
            response = requests.get(self.proxy_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('error'):
                print(f"Geocoding error for '{poi_name}': {data['error']}", file=sys.stderr)
                return None
                
            pois = data.get('pois', [])
            if not pois:
                print(f"No results found for '{poi_name}'", file=sys.stderr)
                return None
                
            # Use the first (most relevant) result
            best_match = pois[0]
            
            # Extract coordinates
            location_str = best_match.get('location', '')
            if not location_str or ',' not in location_str:
                print(f"Invalid location format for '{poi_name}': {location_str}", file=sys.stderr)
                return None
                
            lng, lat = location_str.split(',')
            
            return {
                'name': best_match.get('name', poi_name),
                'location': [float(lng), float(lat)],
                'address': best_match.get('address', ''),
                'rating': best_match.get('rating', ''),
                'id': best_match.get('id', ''),
                'confidence': 0.9  # High confidence for API results
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Network error geocoding '{poi_name}': {e}", file=sys.stderr)
            return None
        except (ValueError, KeyError) as e:
            print(f"Data parsing error for '{poi_name}': {e}", file=sys.stderr)
            return None
    
    def geocode_pois(self, pois: List[Dict]) -> List[Dict]:
        """
        Geocode multiple POIs and return enriched results
        """
        geocoded_pois = []
        
        for i, poi in enumerate(pois):
            print(f"Geocoding {i+1}/{len(pois)}: {poi['name']}")
            
            geocoded = self.geocode_poi(poi['name'])
            if geocoded:
                # Preserve original confidence and merge with geocoded data
                geocoded['original_name'] = poi['name']
                geocoded['confidence'] = min(geocoded.get('confidence', 0.9), poi.get('confidence', 1.0))
                geocoded_pois.append(geocoded)
            else:
                # Keep original POI with low confidence if geocoding fails
                fallback_poi = {
                    'name': poi['name'],
                    'location': None,  # Will need manual verification
                    'address': '',
                    'rating': '',
                    'id': f'fallback_{i}',
                    'confidence': 0.2,
                    'original_name': poi['name']
                }
                geocoded_pois.append(fallback_poi)
        
        return geocoded_pois

def main():
    parser = argparse.ArgumentParser(description='Geocode POIs using Amap API')
    parser.add_argument('input_file', help='Input JSON file with POIs to geocode')
    parser.add_argument('--output', '-o', help='Output JSON file path (default: stdout)')
    parser.add_argument('--proxy-url', default=DEFAULT_PROXY_URL, 
                       help=f'Local proxy URL (default: {DEFAULT_PROXY_URL})')
    parser.add_argument('--city', default=DEFAULT_CITY,
                       help=f'City for geocoding (default: {DEFAULT_CITY})')
    parser.add_argument('--min-confidence', type=float, default=0.3,
                       help='Minimum confidence threshold (default: 0.3)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)
    
    # Load input POIs
    with open(args.input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # Extract POIs from input
    if isinstance(input_data, list):
        pois_to_geocode = input_data
    elif 'filtered_pois' in input_data:
        pois_to_geocode = input_data['filtered_pois']
    elif 'pois' in input_data:
        pois_to_geocode = input_data['pois']
    else:
        print("Error: Input file must contain POIs in 'filtered_pois', 'pois', or as root array", file=sys.stderr)
        sys.exit(1)
    
    if not pois_to_geocode:
        print("No POIs to geocode", file=sys.stderr)
        sys.exit(1)
    
    # Initialize geocoder
    geocoder = AmapGeocoder(proxy_url=args.proxy_url, city=args.city)
    
    # Geocode POIs
    geocoded_pois = geocoder.geocode_pois(pois_to_geocode)
    
    # Filter by confidence
    filtered_geocoded = [poi for poi in geocoded_pois if poi['confidence'] >= args.min_confidence]
    
    # Prepare output
    result = {
        'input_file': args.input_file,
        'proxy_url': args.proxy_url,
        'city': args.city,
        'total_input_pois': len(pois_to_geocode),
        'geocoded_pois': geocoded_pois,
        'filtered_geocoded_pois': filtered_geocoded,
        'successful_geocodes': len([p for p in geocoded_pois if p['location'] is not None]),
        'requires_verification': len([p for p in geocoded_pois if p['location'] is None])
    }
    
    # Output result
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()