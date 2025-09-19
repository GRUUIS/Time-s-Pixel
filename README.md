# Time's Pixel

Time's Pixel is a data visualization project that blends meteorological data with artistic expression. By using daily sunrise, sunset, and moon time data from Hong Kong, the project transforms temporal patterns into visual art, exploring the rhythm of nature and the passage of time through creative coding.

## Project Structure

The project has been reorganized into a clear modular structure:

```
Time-s-Pixel/
├── README.md                          # Project documentation
├── data/                              # Raw and processed CSV data
├── docs/                              # Additional documentation
├── output/                            # Generated images and animations
├── src/                               # Source code modules
│   ├── core/                          # Core astronomical calculations
│   │   ├── time_utils.py              # Time parsing and data loading
│   │   ├── color_palettes.py          # Color scheme definitions
│   │   ├── moon_phases.py             # Moon phase calculations
│   │   ├── twilight_calculator.py     # Advanced sky color calculations
│   │   └── seasonal_markers.py        # Seasonal event markers
│   ├── data_processing/               # Data cleaning and processing
│   │   ├── download_data.py           # Download astronomical data
│   │   └── check_data.py              # Clean and validate data
│   └── visualizations/                # Visualization implementations
│       ├── timelapse_visualization.py # Hong Kong skyline time-lapse
│       ├── interactive_visualization.py # Interactive pixel grid
│       ├── circular_visualization.py  # Radial time display
│       ├── enhanced_visualization.py  # Enhanced pixel art
│       └── other visualization files...
├── interactive_visualization.py       # Quick launcher for interactive mode
├── timelapse_visualization.py         # Quick launcher for timelapse mode
└── Legacy compatibility files...
```

## Quick Start

### Method 1: Using Launcher Scripts (Recommended)
```bash
# Interactive pixel grid visualization
python interactive_visualization.py

# Hong Kong skyline time-lapse
python timelapse_visualization.py
```

### Method 2: Direct Module Access
```bash
# Run specific visualizations
python -m src.visualizations.circular_visualization
python -m src.visualizations.enhanced_visualization
```

## Data Processing

### Download and Clean Data
```bash
# Download fresh data from Hong Kong Observatory
python -m src.data_processing.download_data

# Clean and validate the data (preserves NaN for missing astronomical events)
python -m src.data_processing.check_data
```

**Important**: The data cleaning process now correctly preserves NaN values for days when moon doesn't rise or set, ensuring astronomical accuracy.

## Recent Enhancements (Updates)

The project has been significantly enhanced with advanced astronomical calculations, interactive visualizations, and multiple viewing modes:

### New Visualization Modes

#### Interactive Circular Visualization
- **File**: `circular_visualization.py`
- **Features**: Radial layout with days arranged in a circle, hours radiating from center
- **Controls**: 
  - Click any point to select day/hour
  - S - Toggle seasonal markers
  - R - Rotate 30 degrees
  - ← → - Fine rotation
  - ESC - Exit

#### Interactive Linear Timeline
- **File**: `interactive_visualization.py` 
- **Features**: Scrollable timeline with optimized screen sizing and real-time data panel
- **Controls**: Click to select, scroll to navigate, hover for previews

#### Static High-Resolution Generator
- **File**: `generate_circular_image.py`
- **Output**: Professional 1200x1200 PNG circular visualization

### Advanced Astronomical Features

#### Enhanced Color Palettes (`color_palettes.py`)
- **Naturalistic**: Realistic atmospheric colors
- **Vibrant**: Enhanced saturated artistic colors
- **Monochrome**: Elegant grayscale representations
- **Classic**: Traditional astronomical visualization colors

#### Accurate Moon Phase System (`moon_phases.py`)
- Real lunar cycle calculations using astronomical algorithms
- Visual phase representations with color-coded illumination
- Precise moon visibility and illumination percentages

#### Advanced Twilight Calculations (`twilight_calculator.py`)
- **Civil Twilight**: Sun 6° below horizon
- **Nautical Twilight**: Sun 12° below horizon
- **Astronomical Twilight**: Sun 18° below horizon
- **Blue Hour**: Optimal photography lighting conditions
- **Golden Hour**: Warm sunset/sunrise atmospheric colors

#### Comprehensive Seasonal Markers (`seasonal_markers.py`)
- **13 Major Astronomical Events** including:
  - Solstices and Equinoxes (4 events)
  - Meteor shower peaks: Quadrantids, Lyrids, Perseids, Geminids
  - Lunar events: Supermoons and partial lunar eclipse
  - Planetary oppositions: Mars and Jupiter
- **Interactive Features**: Animated breathing effects, proximity-based labeling, toggle controls
- **Educational Content**: Detailed descriptions and astronomical significance

### Technical Improvements

#### Modular Architecture
- **8 Specialized Modules**: Separated concerns for better maintainability
- **Enhanced Data Processing**: Automated download and validation systems
- **Performance Optimization**: Pre-calculated pixel colors for smooth interaction

#### Interactive Controls
- **Real-time Data Display**: Click any day/hour for detailed astronomical information
- **Smooth Navigation**: Optimized scrolling and rotation with fine controls
- **Toggle Systems**: Show/hide seasonal markers and other visual elements

### Installation and Usage

#### Prerequisites
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install required packages
pip install pygame pandas numpy pillow imageio
```

#### Running the Visualizations
```bash
# Interactive circular cosmic clock
python circular_visualization.py

# Scrollable linear timeline
python interactive_visualization.py

# Generate static high-resolution image
python generate_circular_image.py

# Download and process data
python download_data.py
```

### Output Files
- `circular_time_visualization.png` - High-resolution circular cosmic clock
- `enhanced_sun_moon_365days.png` - Advanced linear visualization
- `sun_moon_365days_animation.gif` - Animated yearly progression
- Various other specialized visualizations

### Project Structure
```
├── circular_visualization.py      # Interactive circular layout
├── interactive_visualization.py   # Scrollable timeline
├── generate_circular_image.py     # Static image generator
├── seasonal_markers.py           # Astronomical events system
├── moon_phases.py                # Lunar calculations
├── twilight_calculator.py        # Sky color calculations
├── color_palettes.py             # Color management system
├── time_utils.py                 # Time processing utilities
└── download_data.py              # Automated data acquisition
```

## License

This project is open source and welcomes contributions from artists, coders, and data enthusiasts.
