# Time's Pixel

Time's Pixel is a data visualization project that blends meteorological data with artistic expression. By using daily sunrise, sunset, and moon time data from Hong Kong, the project transforms temporal patterns into visual art, exploring the rhythm of nature and the passage of time through creative coding.

## 🚀 Latest Updates (2025)

### ✨ Enhanced Menu System with 6 Visualization Options
The project now features a comprehensive pygame-based menu system that provides unified access to both interactive and static visualization modes:

#### 🎮 Interactive Visualizations
1. **Timelapse Animation** - Hong Kong Skyline Journey
2. **3D Time Spiral** - Innovative Temporal Structure  
3. **Interactive Explorer** - Click-to-Discover Interface

#### 🖼️ Static Image Generation
4. **Enhanced Pixel Art** - High-Resolution Static Image
5. **Circular Cosmic Clock** - Radial Time Visualization
6. **Moon Phase Analysis** - Lunar Cycle Visualization

**Menu Features:**
- **Category-based Layout**: Clear visual separation between interactive and static modes
- **Keyboard Shortcuts**: Press 1-6 for quick launch of any visualization
- **Color-coded UI**: Blue theme for interactive, purple theme for static options
- **1400x950 Window**: Optimized for displaying all 6 options comfortably
- **Professional Styling**: Modern card-based interface with hover effects

### 🏗️ Major Project Restructure
The project has been completely reorganized with a professional modular architecture, featuring comprehensive visualization suite and improved user experience.

### 🎨 Three Core Interactive Modes

#### 1. **Timelapse Animation** (`scripts/run_timelapse.py`)
- **16:9 Aspect Ratio**: Optimized for modern displays
- **Adaptive Screen Sizing**: Automatically detects optimal resolution  
- **20% Left Viewport Cropping**: Focus on core visual content
- **Hong Kong Skyline Animation**: Realistic building silhouettes with window lighting
- **Full-Screen Mode**: Press F11 for immersive experience
- **Interactive Controls**: Speed adjustment, time range selection, seasonal presets

#### 2. **3D Time Spiral** (`scripts/run_spiral_3d.py`)
- **Innovative 3D Structure**: 365 days form a beautiful spiral
- **Custom 3D Engine**: Self-built projection and rotation system
- **Astronomical Data Mapping**: Daylight duration controls spiral height
- **Moon Phase Color Coding**: Different lunar phases shown in unique colors
- **Interactive Navigation**: Mouse rotation, wheel zoom, auto-rotation toggle

#### 3. **Interactive Exploration** (`scripts/run_interactive.py`)
- **Click-to-Explore**: Click any pixel for detailed astronomical data
- **Real-time Feedback**: Instant display of sunrise, sunset, moon phase info
- **Multiple Color Palettes**: Switch between naturalistic, vibrant, and monochrome
- **Smooth Scrolling**: Navigate through entire year with wheel or arrow keys

## Project Structure

The project has been reorganized into a clear modular structure:

```
Time-s-Pixel/
├── 📊 data/                           # Astronomical data files
│   ├── hongkong_sunrise_sunset_2024_clean.csv
│   └── moonrise_moonset_2024_clean.csv
├── 📚 docs/                           # Project documentation  
├── 🖼️ output/                         # Generated images and animations
├── 🐍 src/                            # Source code modules
│   ├── core/                          # 🔧 Core functionality
│   │   ├── time_utils.py              # Time processing utilities
│   │   ├── color_palettes.py          # Color scheme definitions
│   │   ├── moon_phases.py             # Moon phase calculations
│   │   ├── twilight_calculator.py     # Advanced sky color calculations
│   │   └── seasonal_markers.py        # Seasonal event markers
│   ├── data_processing/               # 📊 Data handling
│   │   ├── download_data.py           # Download astronomical data
│   │   └── check_data.py              # Clean and validate data
│   └── visualizations/                # 🎨 Visualization modules
│       ├── timelapse_visualization.py    # Hong Kong skyline time-lapse
│       ├── time_spiral_3d.py             # 3D spiral visualization
│       ├── interactive_visualization.py  # Interactive pixel grid
│       ├── enhanced_visualization.py     # Enhanced pixel art
│       ├── circular_visualization.py     # Radial time display
│       └── utils/                        # 🛠️ Visualization utilities
│           ├── generate_circular_image.py
│           └── generate_timelapse_preview.py
├── 🚀 scripts/                        # Launch scripts
│   ├── run_timelapse.py               # Launch timelapse animation
│   ├── run_spiral_3d.py               # Launch 3D spiral visualization  
│   ├── run_interactive.py             # Launch interactive exploration
│   └── examples/                      # 📁 Example scripts
│       ├── sun_moon_365days.py
│       ├── sun_moon_animation.py
│       └── sun_moon_365days_pygame.py
├── 🎮 timelapse_visualization.py      # 🌟 MAIN MENU SYSTEM 🌟
├── 🔄 run_timelapse_direct.py         # Direct timelapse launcher (compatibility)
└── 📋 requirements.txt                # Python dependencies
```

## Quick Start

### 🎯 Main Menu (Recommended - Enhanced!)
```bash
# Launch the comprehensive menu system to explore all 6 visualizations
python timelapse_visualization.py
```

The enhanced main menu provides:
- **🎨 Visual Interface**: Beautiful category-based cards showing each visualization
- **🖱️ Click-to-Launch**: Click "🚀 Launch" for interactive or "🎨 Generate" for static images
- **⌨️ Keyboard Shortcuts**: Press 1-6 for quick launch of any visualization
- **📋 Feature Overview**: See all capabilities with category separation
- **🎮 Interactive Section**: Timelapse, 3D Spiral, and Interactive Explorer
- **🖼️ Static Generation**: Enhanced Pixel Art, Circular Clock, and Moon Analysis

### 🚀 Direct Launch Scripts
```bash
# Interactive Visualizations
python scripts/run_timelapse.py     # 1. Timelapse Animation 
python scripts/run_spiral_3d.py    # 2. 3D Spiral Visualization
python scripts/run_interactive.py  # 3. Interactive Explorer

# Static Image Generation
python src/visualizations/enhanced_visualization.py          # 4. Enhanced Pixel Art
python src/visualizations/utils/generate_circular_image.py  # 5. Circular Cosmic Clock  
python src/visualizations/accurate_moon_visualization.py    # 6. Moon Phase Analysis
```

### 🔄 Backward Compatibility
```bash
# Direct timelapse launcher (maintains old behavior)
python run_timelapse_direct.py
```

### 🛠️ Setup and Installation
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install required packages
pip install -r requirements.txt

# Or install individually:
# pip install pygame pandas numpy pillow imageio
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

## 🎮 Features and Controls

### Timelapse Animation Controls
- **SPACE**: Pause/Resume animation
- **← →**: Change animation speed (0.01x to 5.0x)
- **Q W**: Fine speed control (cycle presets)
- **↑ ↓**: Jump days forward/backward
- **1-9**: Quick time range presets (Dawn, Morning, Sunset, Night, Seasons)
- **T**: Toggle time range loop
- **R**: Reset to day 1
- **F11**: Toggle fullscreen mode
- **ESC**: Exit application

### 3D Spiral Controls
- **Mouse Movement**: Rotate 3D view
- **Mouse Wheel**: Zoom in/out
- **WASD/Arrow Keys**: Fine rotation control
- **SPACE**: Toggle auto-rotation
- **R**: Reset view to default
- **ESC**: Exit application

### Interactive Mode Controls
- **Click**: Select any pixel for detailed info
- **Mouse Wheel**: Scroll through timeline
- **↑ ↓**: Navigate with arrow keys
- **P**: Change color palette
- **T**: Toggle twilight information
- **Home/End**: Jump to beginning/end
- **ESC**: Exit application

## 🎨 Advanced Features

### Enhanced Display Technology
- **Adaptive Resolution**: Automatically detects optimal screen size
- **16:9 Aspect Ratio**: Perfect for modern widescreen displays
- **Viewport Cropping**: 20% left-side cropping for focused viewing
- **Full-Screen Support**: Immersive F11 full-screen experience
- **Performance Optimization**: Pre-computed data for smooth real-time interaction

### Astronomical Accuracy
- **Real Moon Phases**: Accurate lunar cycle calculations
- **Twilight Zones**: Civil, nautical, and astronomical twilight
- **Seasonal Events**: 13 major astronomical events marked
- **Hong Kong Observatory Data**: Official 2024 sunrise/sunset/moonrise/moonset times

### Color Palette System
- **Naturalistic**: Realistic atmospheric colors
- **Vibrant**: Enhanced saturated artistic colors  
- **Monochrome**: Elegant grayscale representations
- **Classic**: Traditional astronomical visualization colors

## Data Processing

### Download and Clean Data
```bash
# Download fresh data from Hong Kong Observatory
python -m src.data_processing.download_data

# Clean and validate the data (preserves NaN for missing astronomical events)
python -m src.data_processing.check_data
```

**Important**: The data cleaning process now correctly preserves NaN values for days when moon doesn't rise or set, ensuring astronomical accuracy.

## 🏗️ Technical Architecture

### Modular Design
- **8 Core Modules**: Separated concerns for maintainability
- **Smart Import System**: Automatic path resolution for different environments
- **Error Handling**: Comprehensive fallback mechanisms
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Performance Optimizations
- **Pre-computed Astronomical Data**: Calculated once, used throughout
- **Batch Rendering**: Optimized drawing for smooth animation
- **Memory Management**: Efficient handling of large datasets
- **Caching System**: Smart caching of expensive calculations

## Recent Enhancements (Legacy Documentation)

The following section preserves information about earlier development phases:

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

### 📁 Development Structure (For Contributors)
```
src/
├── core/                              # Core astronomical calculations
│   ├── time_utils.py                  # Time parsing and data loading
│   ├── color_palettes.py              # Color scheme management
│   ├── moon_phases.py                 # Lunar calculations
│   ├── twilight_calculator.py         # Advanced sky colors
│   └── seasonal_markers.py            # Astronomical events
├── data_processing/                   # Data acquisition and cleaning
│   ├── download_data.py               # Hong Kong Observatory API
│   └── check_data.py                  # Data validation and cleaning
└── visualizations/                    # Visualization implementations
    ├── timelapse_visualization.py     # Main skyline animation
    ├── time_spiral_3d.py              # 3D spiral innovation
    ├── interactive_visualization.py   # Click-to-explore interface
    ├── circular_visualization.py      # Radial time display
    ├── enhanced_visualization.py      # Advanced pixel art
    └── utils/                         # Helper utilities
        ├── generate_circular_image.py
        └── generate_timelapse_preview.py
```

### 🎯 Output Files
- `enhanced_sun_moon_365days.png` - High-resolution linear timeline
- `circular_time_visualization.png` - Circular cosmic clock
- `sun_moon_365days_animation.gif` - Animated yearly progression
- `sun_moon_animation_2024.gif` - Optimized timelapse animation
- Various specialized astronomical visualizations

## 🤝 Contributing

This project welcomes contributions from artists, coders, and data enthusiasts. The modular architecture makes it easy to:
- Add new visualization modes
- Implement different color palettes
- Integrate additional astronomical data sources
- Create new interactive features

## 📄 License

This project is open source and available for educational and artistic use.
