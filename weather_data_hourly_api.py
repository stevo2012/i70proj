# Download 20 Years of Hourly Weather Data for Loveland Ski Area
import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta

print("=== DOWNLOADING 20 YEARS OF LOVELAND WEATHER DATA ===")

# Loveland Ski Area coordinates  
latitude = 39.6806
longitude = -105.8989

# Match your traffic data date range
start_date = "2004-01-01"
end_date = "2024-11-30"   # Your traffic data goes to Nov 2024

print(f"📍 Location: Loveland Ski Area ({latitude}, {longitude})")
print(f"📅 Date range: {start_date} to {end_date}")
print(f"⏱️ This is ~20 years of hourly data - may take a few minutes...\n")

# API configuration
url = "https://archive-api.open-meteo.com/v1/archive"

# WARNING: 20 years of hourly data is ~175,000 records!
# Some APIs have limits, so let's download in yearly chunks to be safe
def download_weather_by_year(year):
    """Download one year of weather data"""
    year_start = f"{year}-01-01"
    year_end = f"{year}-12-31"
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': year_start,
        'end_date': year_end,
        'hourly': [
            'temperature_2m',       # Hourly temperature
            'precipitation',        # Hourly precipitation  
            'snow_depth',          # Snow depth on ground
            'weather_code',        # Weather condition code
            'relative_humidity_2m', # Humidity (bonus feature!)
            'wind_speed_10m'       # Wind speed (bonus feature!)
        ],
        'temperature_unit': 'fahrenheit',
        'precipitation_unit': 'inch', 
        'wind_speed_unit': 'mph',
        'timezone': 'America/Denver'
    }
    
    print(f"📡 Downloading {year}...", end=" ")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Convert to DataFrame
            hourly_data = data['hourly']
            df = pd.DataFrame({
                'datetime': pd.to_datetime(hourly_data['time']),
                'temperature_2m': hourly_data['temperature_2m'],
                'precipitation': hourly_data['precipitation'], 
                'snow_depth': hourly_data['snow_depth'],
                'weather_code': hourly_data['weather_code'],
                'humidity': hourly_data['relative_humidity_2m'],
                'wind_speed': hourly_data['wind_speed_10m']
            })
            
            print(f"✅ Got {len(df):,} records")
            return df
            
        else:
            print(f"❌ Failed (Status: {response.status_code})")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Download data year by year
all_data = []
years = range(2004, 2025)  # 2004 through 2024

print("🚀 Starting download...\n")
start_time = time.time()

for year in years:
    year_data = download_weather_by_year(year)
    
    if year_data is not None:
        all_data.append(year_data)
        
        # Be nice to their servers - small delay between requests
        time.sleep(0.5)
    else:
        print(f"⚠️  Failed to download {year} - continuing with others...")

# Combine all years
if all_data:
    print(f"\n🔗 Combining {len(all_data)} years of data...")
    weather_df = pd.concat(all_data, ignore_index=True)
    
    # Filter to exact date range (in case 2024 has extra months)
    weather_df = weather_df[
        (weather_df['datetime'] >= start_date) & 
        (weather_df['datetime'] <= end_date)
    ]
    
    print(f"✅ Final dataset: {len(weather_df):,} hourly records")
    
    # Data quality summary
    print(f"\n📊 DATA QUALITY SUMMARY:")
    print(f"• Date range: {weather_df['datetime'].min()} to {weather_df['datetime'].max()}")
    print(f"• Temperature range: {weather_df['temperature_2m'].min():.1f}°F to {weather_df['temperature_2m'].max():.1f}°F")
    print(f"• Max precipitation: {weather_df['precipitation'].max():.2f} inches/hour")
    print(f"• Max snow depth: {weather_df['snow_depth'].max():.1f} inches") 
    print(f"• Max wind speed: {weather_df['wind_speed'].max():.1f} mph")
    
    # Missing data check
    print(f"\n🔍 MISSING DATA CHECK:")
    for col in weather_df.columns:
        if col != 'datetime':
            missing = weather_df[col].isnull().sum()
            missing_pct = missing / len(weather_df) * 100
            print(f"• {col}: {missing:,} missing ({missing_pct:.2f}%)")
    
    # Hours with snow
    snow_hours = (weather_df['snow_depth'] > 0).sum()
    print(f"\n❄️ Hours with snow on ground: {snow_hours:,} ({snow_hours/len(weather_df)*100:.1f}%)")
    
    # Save the data
    filename = 'loveland_hourly_weather_2004_2024.csv'
    weather_df.to_csv(filename, index=False)
    
    elapsed_time = time.time() - start_time
    print(f"\n💾 Saved as '{filename}'")
    print(f"⏱️  Download completed in {elapsed_time:.1f} seconds")
    
    # Show sample data
    print(f"\n📋 SAMPLE DATA (first 10 rows):")
    print(weather_df.head(10))
    
    print(f"\n🎯 SUCCESS! You now have:")
    print(f"✅ 20 years of hourly weather data")
    print(f"✅ Same location as your traffic data") 
    print(f"✅ Variables that match your model needs")
    print(f"✅ Bonus features (humidity, wind) for model improvement")
    print(f"✅ Ready to merge with your traffic data!")
    
else:
    print("❌ Failed to download any weather data. Check your internet connection.")

print(f"\n📚 WHAT I LEARNED FROM THE DOCS:")
print(f"• API endpoint structure from their documentation")
print(f"• Parameter names by reading their variable list") 
print(f"• Unit options from their configuration docs")
print(f"• Rate limits and best practices from their usage guide")
print(f"\n💡 Always read the documentation - don't guess!")