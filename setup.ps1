Write-Host "🏔️ GeoShield Demo Setup" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "📊 Generating sample data..." -ForegroundColor Yellow
python sample_data.py

Write-Host ""
Write-Host "🚀 Starting GeoShield application (warnings suppressed)..." -ForegroundColor Green
Write-Host "Open your browser to: http://localhost:8501" -ForegroundColor Magenta
Write-Host ""

python run_clean.py
