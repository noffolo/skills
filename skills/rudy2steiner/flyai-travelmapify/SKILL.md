---
name: flyai-travelmapify
version: 1.0.0
description: Parse travel planning inputs (images OR comma-separated location names) and generate interactive travel route maps with POI management and FlyAI hotel integration. Use when a user provides either a travel planning image (screenshot, photo, or diagram) OR a list of comma-separated location names, and wants to convert it into an interactive web-based travel map with searchable POIs, route optimization, FlyAI hotel search, and professional presentation.
author: xuandu
license: MIT
tags: [travel, maps, routing, ocr, geocoding, flyai, hotels]
---

# Travel Mapify

Transform travel planning images into interactive, professional travel route maps.

## Overview

This skill automatically:
1. **Supports dual input modes**: Process travel planning images (OCR) OR direct comma-separated location names
2. **Extracts POIs** from images using OCR and AI analysis (image mode)
3. **Parses location names** directly from text input (text mode)
4. **Geocodes locations** to get precise coordinates using Amap API
5. **Generates interactive maps** with route optimization and POI management
6. **Integrates real hotel search** using FlyAI for actual hotel recommendations
7. **Creates professional outputs** ready for sharing and presentation

## When to Use

**Image Input Mode:**
- User uploads a travel planning screenshot/image with location names
- User wants to convert a hand-drawn or digital travel itinerary into an interactive map
- User has a photo of a travel plan written on paper or displayed on screen

**Text Input Mode:**
- User provides comma-separated location names directly (e.g., "上海外滩,上海迪士尼乐园,豫园")
- User wants to quickly create a travel map from a simple list of destinations
- User has location names but no visual reference image

**Hotel Integration Mode:**
- User wants real hotel recommendations near their destination
- User needs actual pricing and availability data
- User wants booking links for hotels through FlyAI integration

## Workflow

### Step 1: Input Processing and POI Extraction

**For Image Input:**
- Analyze the uploaded image using OCR to extract text
- Identify location names, addresses, and POI information
- Filter and validate extracted POIs

**For Text Input:**
- Parse comma-separated location names directly
- Create POI entries with high confidence (user-provided)
- No OCR processing required

### Step 2: Geocoding and Coordinate Resolution
- Use Amap geocoding API to resolve location names to precise coordinates
- Handle ambiguous locations with user confirmation
- Validate coordinate accuracy

### Step 3: Enhanced Map Generation
- **Use optimized Shanghai template as main template** with all UX improvements
- Create a single dual-mode interface with toggle between Edit/View modes
- Implement drag-and-drop and arrow button reordering (edit mode only)
- Generate optimized route with directional arrows
- Add "Generate Final" functionality to download clean version
- **Integrate real FlyAI hotel search** with professional loading states
- **Replace alert popups** with notification system

### Step 4: Automatic Server Management
- **Automatically start HTTP server** on port 9000 (or specified port)
- **Automatically start hotel search server** on port 8770 (or specified port)
- **Check if servers are already running** to avoid conflicts
- **Provide direct access URLs** in output
- **Ensure all functionality is ready** when map creation completes

### Step 4: Professional Output Delivery
- Provide unified HTML file that works in both editing and presentation contexts
- Include clear instructions for toggling modes and generating final version
- Ensure mobile-responsive design

## File Structure

```
travel-mapify/
├── SKILL.md
├── scripts/
│   ├── main_travel_mapify_enhanced.py     # **ENHANCED MAIN**: Auto-starts servers + dual input
│   ├── main_travel_mapify.py              # Legacy main entry point (dual input: image/text)
│   ├── extract_pois_from_image.py         # OCR + AI POI extraction
│   ├── geocode_locations.py               # Amap geocoding integration
│   ├── generate_travel_map.py             # Legacy HTML template generation
│   ├── generate_unified_map.py            # Legacy unified dual-mode HTML generation
│   └── generate_from_optimized_template.py # Uses enhanced Shanghai template
├── references/
│   ├── amap_api_guide.md                 # Amap API usage patterns
│   └── poi_validation_rules.md           # POI validation and filtering rules
└── assets/
    ├── templates/
    │   ├── editable-map-template.html      # Left-panel editable template
    │   ├── final-map-template.html         # Final presentation template
    │   └── unified-map-template.html       # Dual-mode template (edit/view)
    └── icons/
        ├── north-indicator.svg
        └── poi-marker.svg
```

**Main Template**: The skill now uses `/Users/xuandu/.openclaw/workspace/apps/shanghai-travel/shanghai-final-optimized.html` as the primary template, which includes:
- Real FlyAI hotel search integration
- Professional notification system (no alert popups)
- Loading states with timeout handling
- Enhanced UX with smart defaults

**Automatic Server Management**: The enhanced main script automatically starts both HTTP server (port 9000) and hotel search server (port 8770) when generating maps, ensuring all functionality is ready immediately.

## Usage Examples

### Image Input - Basic Usage
User: "Here's my travel plan screenshot, can you make it interactive?"
→ Skill extracts POIs via OCR, geocodes them, and generates interactive map

### Image Input - Advanced Usage  
User: "I have a photo of our Beijing itinerary, please create a shareable map"
→ Skill processes image, validates locations, creates optimized route with professional styling

### Text Input - Direct Locations
User: "上海外滩,上海迪士尼乐园,豫园"
→ Skill parses locations directly, geocodes them, and generates interactive map

### Text Input - Simple List
User: "Create a travel map for: Tokyo Tower, Shibuya Crossing, Meiji Shrine"
→ Skill extracts location names, geocodes them, creates optimized route

### Hotel Search Integration
User: Clicks "搜酒店" button in generated map
→ Real FlyAI hotel search returns actual hotel data with prices and booking links
→ No mock data - uses real-time Fliggy MCP integration
→ Professional UX with loading states and notifications (no alert popups)
→ Default dates: today for check-in, tomorrow for check-out (1-night stay)

### Customization Request
User: "Can you adjust the route order and add missing locations?"
→ Skill provides editable interface with search functionality and reordering tools

## Technical Requirements

- **OCR Support**: Chinese and English text extraction from images
- **Amap API Key**: Valid Amap Web API key for geocoding and map tiles
- **Local Proxy**: Running local proxy server for Amap API requests (port 8769)
- **Web Browser**: Modern browser with JavaScript support for interactive features

## Output Files

The skill generates HTML files using the **enhanced Shanghai template** as the main template:

**`[location]-travel-map-optimized.html`** - Dual-mode interface with all professional enhancements:
- **Real FlyAI Hotel Search Integration**:
  - Actual hotel data with prices and booking links
  - Loading states with "搜索中..." button text
  - 5-second timeout with auto-re-enable
  - No mock data - uses real Fliggy MCP integration
- **Professional UX Improvements**:
  - Notification system instead of alert popups
  - Auto-hiding messages after 3 seconds
  - Smart date defaults (today check-in, tomorrow check-out)
- **Edit Mode (📝)**: Full-featured editing interface with:
  - Left-panel POI management
  - Search functionality for adding new locations
  - Drag-and-drop and arrow button reordering
  - Real-time map preview
- **View Mode (👁️)**: Clean presentation version with:
  - Optimized route display
  - Numbered POI markers with directional arrows
  - Professional styling ready for sharing
- **Generate Final**: Download button to create a clean version without edit controls

Files are self-contained and work in any modern web browser when served via HTTP server.

## Error Handling

- **Poor Image Quality**: Request higher quality image or manual POI entry
- **Ambiguous Locations**: Present options for user selection
- **API Rate Limits**: Implement retry logic with exponential backoff
- **Missing Coordinates**: Fall back to approximate coordinates with user verification
- **HTML Display Issues**: Use local HTTP server instead of file:// protocol
- **Map Loading Failures**: Check AMap API key restrictions and network connectivity
- **localStorage Corruption**: Implement fallback data and validation logic

## Enhanced UX Features

**Professional User Interface:**
- **No alert popups**: All messages displayed in non-intrusive notification area
- **Loading states**: Hotel search button shows "搜索中..." during API calls
- **Timeout handling**: 5-second timeout automatically re-enables search button
- **Auto-hiding notifications**: Messages disappear after 3 seconds
- **Visual feedback**: Error messages in red, success messages in green

**Smart Defaults:**
- **Date selection**: Today for check-in, tomorrow for check-out (1-night stay)
- **Hotel sorting**: Results sorted by distance from destination
- **Top results**: Shows top 5 closest hotels for better user experience

## Best Practices

- Always verify extracted POIs with the user before finalizing
- Provide clear instructions for customizing the generated maps
- Optimize for mobile viewing with responsive design
- Include north indicator and scale reference for professional appearance
- **Always test via HTTP server**: Never rely on file:// protocol for web applications
- **Implement robust error handling**: Wrap API calls and provide user feedback
- **Validate all inputs**: Sanitize data before processing
- **Document dependencies**: Clearly specify API keys, network, and browser requirements