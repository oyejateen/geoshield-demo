@echo off
echo 🏔️ GeoShield Demo Setup
echo ==================

echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo 📊 Generating sample data...
python sample_data.py

echo.
echo 🚀 Starting GeoShield application (warnings suppressed)...
echo Open your browser to: http://localhost:8501
echo.
python run_clean.py
