# Fitness Tracker 🏃‍♂️

A comprehensive fitness tracking application built with Streamlit that analyzes sensor data from mobile devices to track activities, calculate metrics, and provide health insights.

## Features

- 📊 **Activity Detection**: Automatically classifies activities as walking, running, stairs, or sitting based on GPS and elevation data
- 📍 **GPS Tracking**: Visualizes your route on an interactive map with speed and elevation profiles
- 🏔️ **Elevation Analysis**: Tracks elevation gain, floors climbed, and provides elevation charts
- 🔢 **Comprehensive Metrics**: 
  - Distance traveled (km)
  - Average speed
  - Duration
  - Estimated steps
  - Calories burned (based on MET values)
  - Life expectancy impact estimates
- 📈 **Visual Analytics**: 
  - Interactive maps showing GPS tracks
  - Speed vs. time charts
  - Elevation profiles
  - Activity distribution pie charts
- 🎯 **Activity Comparison**: Compare performance across different activity types
- 💾 **Data Import**: Supports loading sensor data from multiple folders and automatically extracts ZIP files

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd hackathon_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Prepare your data**: Place your sensor data CSV files in folders. The app looks for files matching the pattern `sensorlog_*.csv` or any CSV file containing GPS columns (latitude, longitude, timestamp).

2. **Run the application**:
```bash
# From the parent directory (one level above hackathon_app)
streamlit run hackathon_app/app.py
```

3. **Configure and analyze**:
   - Enter the folder path(s) containing your sensor data (one per line)
   - Enter your weight in kg
   - Click "Analyze"

4. **View results**:
   - **Overview Tab**: See session summaries with all metrics
   - **Activities Tab**: Compare aggregated data by activity type
   - **Sessions Tab**: View detailed visualizations for each session

## Data Format

The app expects CSV files with the following columns:

### Required for GPS tracking:
- `timestamp` - Unix timestamp in milliseconds or datetime string
- `latitude` - GPS latitude coordinate
- `longitude` - GPS longitude coordinate

### Optional:
- `altitude` - Elevation in meters (for elevation gain calculations)

### Supported file naming patterns:
- `sensorlog_pos_*.csv` - Position/GPS data
- `sensorlog_accel_*.csv` - Accelerometer data
- `sensorlog_orient_*.csv` - Orientation data
- `sensorlog_angvel_*.csv` - Angular velocity data
- `sensorlog_magfield_*.csv` - Magnetic field data

The app will also accept any CSV file that contains GPS columns (latitude, longitude, timestamp) regardless of filename.

## Project Structure

```
hackathon_app/
├── app.py              # Main Streamlit application
├── loader.py           # Data loading and session management
├── metrics.py          # Fitness metrics calculations
├── activity.py         # Activity classification and prediction
├── plots.py            # Visualization functions
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## How It Works

### Activity Classification

Activities are classified based on:
- **Walking**: Average speed 1.5-6.0 km/h
- **Running**: Average speed 6.0-12.0 km/h  
- **Stairs**: Floors per minute ≥ 1.0 and speed < 6.0 km/h
- **Sitting/Idle**: Speed < 1.5 km/h
- **Cycling**: Speed ≥ 12.0 km/h (mapped to walking for consistency)

### Metrics Calculation

- **Distance**: Calculated using the Haversine formula for GPS coordinates
- **Speed**: Derived from distance and time intervals
- **Elevation Gain**: Sum of positive altitude changes
- **Floors**: Elevation gain divided by 3 meters per floor
- **Steps**: Estimated based on activity type:
  - Walking: ~1,300 steps/km
  - Running: ~1,000 steps/km
  - Stairs: ~16 steps/floor
- **Calories**: Calculated using MET (Metabolic Equivalent of Task) values
- **Life Expectancy**: Estimated impact based on weekly MET-minutes

### Speed Prediction

The app includes a predictive model that forecasts speed for the next 30 seconds using:
- Exponential Moving Average (EMA) smoothing
- Autoregressive (AR) modeling
- Mean reversion to recent activity levels

## Features in Detail

### KPI Dashboard
- Total minutes of activity
- Total distance (km)
- Elevation gain (meters)
- Floors climbed
- Calories burned
- Projected life expectancy impact

### Health Insights
- Weekly MET-minutes if activity is repeated daily
- Life expectancy impact estimates
- Activity recommendations

### Visualizations
- **Map View**: Interactive GPS track visualization
- **Speed Chart**: Speed over time for each session
- **Elevation Profile**: Elevation changes during activity
- **Activity Distribution**: Pie chart showing time spent in each activity type

## Requirements

See `requirements.txt` for the complete list. Main dependencies:
- streamlit >= 1.31
- pandas >= 2.0
- numpy >= 1.23
- plotly >= 5.18

## Troubleshooting

### No sessions found
- Verify your folder paths are correct
- Ensure CSV files exist in the folders
- Check that CSV files contain GPS columns (latitude, longitude, timestamp)
- The app will show debug information about what files were found

### Map not displaying
- Requires internet connection for map tiles
- Ensure GPS data (latitude/longitude) is present in your CSV files

### No elevation data
- Elevation calculations require an `altitude` column in your CSV files
- The app will still work without elevation data, but elevation metrics will be zero

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Acknowledgments

Built for the MATLAB Mobile Fitness Tracker Hackathon. Inspired by the [MathWorks MATLAB Mobile Fitness Tracker](https://github.com/mathworks/matlab-mobile-fitness-tracker) challenge.

---

**Note**: Life expectancy estimates are illustrative and not medical advice. Always consult healthcare professionals for health-related decisions.

