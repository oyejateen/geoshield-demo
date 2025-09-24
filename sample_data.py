"""
Generate data files for the GeoShield system
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_orthophoto():
    """Create a sample orthophoto image for demonstration"""
    
    # Create a 800x600 image simulating aerial terrain
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='lightgray')
    draw = ImageDraw.Draw(img)
    
    # Draw terrain-like features
    # Add some terrain contours
    for i in range(0, width, 50):
        for j in range(0, height, 50):
            # Create random terrain colors
            color_val = np.random.randint(80, 160)
            terrain_color = (color_val - 20, color_val, color_val - 40)
            draw.rectangle([i, j, i+50, j+50], fill=terrain_color)
    
    # Add some rock-like features
    for _ in range(15):
        x = np.random.randint(0, width-100)
        y = np.random.randint(0, height-100)
        w = np.random.randint(30, 80)
        h = np.random.randint(30, 80)
        rock_color = (np.random.randint(60, 100), np.random.randint(60, 90), np.random.randint(50, 80))
        draw.ellipse([x, y, x+w, y+h], fill=rock_color)
    
    # Add some vegetation areas
    for _ in range(10):
        x = np.random.randint(0, width-80)
        y = np.random.randint(0, height-80)
        w = np.random.randint(40, 80)
        h = np.random.randint(40, 80)
        veg_color = (np.random.randint(40, 80), np.random.randint(80, 120), np.random.randint(40, 80))
        draw.ellipse([x, y, x+w, y+h], fill=veg_color)
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 10), "Orthophoto - Rockfall Monitoring Area", fill='white', font=font)
    draw.text((10, 40), "Coordinates: 24.1712°N, 82.6589°E", fill='white', font=font)
    
    # Save the image
    img.save('sample_orthophoto.jpg', 'JPEG', quality=85)
    print("✅ Orthophoto created: sample_orthophoto.jpg")

def create_sample_csv():
    """Create sample sensor data CSV"""
    
    # Generate realistic sensor data
    np.random.seed(42)
    n_sensors = 15
    n_days = 30
    
    data = []
    for sensor_id in range(1, n_sensors + 1):
        for day in range(n_days):
            timestamp = datetime.now() - timedelta(days=day, hours=np.random.randint(0, 24))
            
            # Generate realistic sensor data with some correlation
            base_displacement = np.random.normal(5, 2)
            base_rainfall = max(0, np.random.normal(20, 15))
            
            # Create some correlation between displacement and rainfall
            displacement = max(0, base_displacement + base_rainfall * 0.1 + np.random.normal(0, 1))
            
            # Some sensors should have higher risk readings
            if sensor_id in [1, 4, 9]:  # High risk sensors
                displacement += np.random.normal(5, 2)
                base_rainfall += np.random.normal(10, 5)
            
            data.append({
                'sensor_id': f'S{sensor_id:03d}',
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'displacement_mm': round(max(0, displacement), 2),
                'pore_pressure_kpa': round(np.random.normal(150, 30), 2),
                'strain_micro': round(np.random.normal(100, 25), 2),
                'vibration_ms2': round(np.random.exponential(2), 3),
                'rainfall_mm': round(max(0, base_rainfall), 1),
                'latitude': round(24.1711917 + np.random.normal(0, 0.005), 6),
                'longitude': round(82.6588845 + np.random.normal(0, 0.005), 6)
            })
    
    df = pd.DataFrame(data)
    df = df.sort_values(['sensor_id', 'timestamp'])
    
    # Save CSV
    df.to_csv('sample_sensor_data.csv', index=False)
    print("✅ Sample sensor data created: sample_sensor_data.csv")
    print(f"📊 Generated {len(df)} records for {n_sensors} sensors over {n_days} days")
    
    return df

if __name__ == "__main__":
    print("🏔️ Creating sample data for GeoShield demo...")
    
    # Create sample files
    create_sample_orthophoto()
    sample_df = create_sample_csv()
    
    # Show summary
    print("\n📋 Sample Data Summary:")
    print(f"- Sensors: {sample_df['sensor_id'].nunique()}")
    print(f"- Records: {len(sample_df)}")
    print(f"- Date range: {sample_df['timestamp'].min()} to {sample_df['timestamp'].max()}")
    print(f"- High displacement readings (>10mm): {len(sample_df[sample_df['displacement_mm'] > 10])}")
    print(f"- High rainfall readings (>50mm): {len(sample_df[sample_df['rainfall_mm'] > 50])}")
    
    print("\n🚀 Sample data created successfully!")
    print("You can now upload these files in the GeoShield application.")
