# Time's Pixel

**Astronomical Data Visualization Suite** - Transform Hong Kong's daily sun and moon cycles into interactive art and animations. Experience time through pixels, spirals, and cosmic patterns.

## 🚀 Quick Start

### Main Menu (Recommended)
```bash
python main_menu.py
```
**Enhanced Menu System** featuring 6 visualization modes with clean, modern interface.

## 🎨 Visualization Modes

### Interactive Visualizations
1. **Timelapse Animation** - Hong Kong skyline with realistic day/night cycles
2. **3D Time Spiral** - Innovative temporal structure with interactive 3D navigation  
3. **Interactive Explorer** - Click any pixel for detailed astronomical data
4. **Dynamic Circular Clock** - Real-time radial time exploration

### Static Image Generation
5. **Circular Cosmic Clock** - High-resolution radial time visualization
6. **Moon Phase Analysis** - Accurate lunar cycle visualization with scientific data

## 🏗️ Project Structure

```
Time-s-Pixel/
├── data/                           # Astronomical datasets
│   ├── hongkong_sunrise_sunset_2024_clean.csv
│   └── moonrise_moonset_2024_clean.csv
├── src/                            # Core source code
│   ├── core/                          # Astronomical calculations
│   │   ├── time_utils.py              # Time processing
│   │   ├── color_palettes.py          # Color schemes  
│   │   ├── moon_phases.py             # Lunar calculations
│   │   ├── twilight_calculator.py     # Sky color algorithms
│   │   └── seasonal_markers.py        # Astronomical events
│   ├── data_processing/               # Data handling
│   │   ├── download_data.py           # HKO API integration
│   │   └── check_data.py              # Data validation
│   └── visualizations/                # Visualization engines
│       ├── timelapse_visualization.py    # Skyline animation
│       ├── time_spiral_3d.py             # 3D spiral
│       ├── interactive_visualization.py  # Interactive grid
│       ├── circular_visualization.py     # Dynamic circular
│       ├── enhanced_visualization.py     # Enhanced pixel art
│       ├── accurate_moon_visualization.py # Moon analysis
│       ├── advanced_twilight_visualization.py # Twilight study
│       ├── visualize_sun_moon.py          # Basic visualization
│       └── utils/                        # Generation utilities
│           ├── generate_circular_image.py
│           └── generate_timelapse_preview.py
├── scripts/                        # Launch scripts
│   ├── run_timelapse.py               # Timelapse launcher
│   ├── run_spiral_3d.py               # 3D spiral launcher
│   ├── run_interactive.py             # Interactive launcher
│   ├── image_viewer.py                # Image display utility
│   ├── examples/                      # Example implementations
│   └── image_generation/              # Static image generators
├── output/                         # Generated content
│   ├── images/                        # Static visualizations
│   └── animations/                    # GIF animations
├── main_menu.py                    # Main menu system
├── timelapse_visualization.py      # Direct timelapse runner
└── requirements.txt                # Dependencies
```

## Installation

```bash
# Clone and setup
git clone <repository-url>
cd Time-s-Pixel

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

**Required packages**: pygame, pandas, numpy, pillow, imageio

## 🎮 Controls

### Timelapse Animation
- **SPACE**: Pause/Resume
- **← →**: Speed control (0.01x to 5.0x)
- **1-9**: Time presets (Dawn, Day, Sunset, Seasons)
- **F11**: Fullscreen mode

### 3D Time Spiral  
- **Mouse**: Rotate view
- **Wheel**: Zoom
- **SPACE**: Auto-rotation toggle
- **R**: Reset view

### Interactive Explorer
- **Click**: Detailed astronomical data
- **Wheel**: Scroll timeline
- **P**: Change color palette
- **T**: Toggle twilight info

### Circular Visualization
- **Click**: Select day/hour
- **R**: Rotate 30°
- **← →**: Fine rotation
- **S**: Toggle seasonal markers

## 🎨 Features

### Astronomical Accuracy
- **Real Data**: Hong Kong Observatory 2024 official data
- **Moon Phases**: Accurate lunar cycle calculations  
- **Twilight Zones**: Civil, nautical, astronomical twilight
- **Seasonal Events**: 13 major astronomical markers

### Visual Excellence
- **Adaptive Display**: Auto-detects optimal resolution
- **Color Palettes**: Naturalistic, vibrant, monochrome, classic
- **Smooth Animation**: 60 FPS with optimized rendering
- **Professional UI**: Modern card-based interface

### Interactive Innovation
- **Real-time Data**: Click any pixel for detailed info
- **3D Navigation**: Custom-built 3D engine
- **Viewport Optimization**: Smart cropping for focused viewing
- **Performance**: Pre-computed data for smooth interaction

## 📊 Data Processing

```bash
# Download fresh data from Hong Kong Observatory
python -m src.data_processing.download_data

# Clean and validate data
python -m src.data_processing.check_data
```

## 🎯 Output Examples

Generated files include:
- `enhanced_sun_moon_365days.png` - High-resolution timeline
- `circular_time_visualization.png` - Cosmic clock (1200×1200)
- `accurate_moon_visualization.png` - Moon phase analysis
- `sun_moon_animation_2024.gif` - Yearly animation
- `hongkong_timelapse_preview.png` - Sample frames

## 🤝 Contributing

Contributions welcome! The modular architecture supports:
- New visualization modes
- Additional color palettes  
- Extended astronomical data
- Enhanced interactive features

## 📄 License

Open source - Available for educational and artistic use.
