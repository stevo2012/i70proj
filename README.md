# I-70 Eisenhower Tunnel Traffic Predictor

An advanced machine learning web application that predicts I-70 traffic conditions at Eisenhower Tunnel based on weather data and ski traffic patterns.

## Features

- **Advanced ML Model**: Random Forest trained on 20+ years of hourly traffic and weather data
- **Domain Expertise**: Time-decay weather features that model real road conditions
- **Real-time Predictions**: Interactive web interface for instant traffic predictions
- **Ski-Specific**: Accounts for Colorado ski traffic patterns and seasonal variations

## Technology Stack

- **Backend**: Python Flask API
- **Machine Learning**: scikit-learn Random Forest with custom feature engineering
- **Frontend**: HTML/CSS/JavaScript with responsive design
- **Data**: 344K+ hourly records spanning 2004-2024

## Quick Start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Ensure model files are present:
   - `i70_advanced_model.pkl`
   - `i70_advanced_features.pkl`

3. Run the application:
   ```
   python app.py
   ```

4. Open http://localhost:5000 in your browser

## Model Performance

- **Mean Absolute Error**: ~X vehicles/hour on test data
- **R² Score**: ~0.X (explains X% of traffic variance)
- **Advanced Features**: Temperature-dependent precipitation impact, time-decay effects

## Key Features Engineered

- `Road_Severity_Index`: Physics-based road condition assessment
- `Road_Ice_Risk_6h`: Recent precipitation weighted by freezing conditions
- `Ski_Departure_Weather`: Friday evening ski traffic with bad weather
- `Current_Snow_Impact`: Active snowfall impact on traffic flow

## Data Sources

- **Traffic**: I-70 Eisenhower Tunnel hourly vehicle counts
- **Weather**: Loveland Ski Area meteorological observations
- **Time Period**: January 2004 - November 2024

## Author

Built as a portfolio project demonstrating end-to-end data science skills from raw data collection through production deployment.