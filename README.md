# Time's Pixel

Time's Pixel is a data visualization project that blends meteorological data with artistic expression. By using daily sunrise, sunset, and moon time data from Hong Kong, the project transforms temporal patterns into visual art, exploring the rhythm of nature and the passage of time through creative coding.

## Project Vision

This project aims to:
- Visualize the interplay between sunlight and moonlight over the course of a year.
- Express the concept of time as a mosaic or pixelated artwork, where each day is a unique pixel shaped by natural phenomena.
- Encourage viewers to reflect on the cyclical beauty of time and its impact on our environment.

## Data Source

The primary dataset is sourced from the Hong Kong Observatory's open data API:
- [Sunrise, Sunset, and Moon Time Data (2024)](https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=SRS&year=2024&rformat=csv)

This dataset includes:
- Daily sunrise and sunset times
- Duration of daylight
- Moonrise and moonset times

## Workflow

1. **Data Acquisition & Cleaning**: Download and preprocess the CSV data to ensure accuracy and usability.
2. **Feature Extraction**: Parse and structure the data to extract sunrise, sunset, daylight duration, and moon time.
3. **Creative Visualization**: Develop an artistic representation using the processed data, experimenting with pixel art, generative patterns, or other visual metaphors.

## Artistic Approach

The visualization will treat each day as a pixel, colored and shaped by its unique solar and lunar timings. The result will be a tapestry of time, revealing hidden patterns and inviting new interpretations of daily cycles.

## Getting Started

1. Clone the repository.
2. Follow the instructions to download and clean the data.
3. Run the visualization script to generate the artwork.

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
