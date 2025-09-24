# 🏔️ GeoShield - Rockfall Prediction System Demo

A comprehensive demonstration of an advanced geotechnical monitoring and risk assessment platform for rockfall prediction. This demo showcases the core functionality including map visualization, sensor data analysis, risk assessment, and reporting capabilities.

## 🚀 Features

- **📁 Data Upload**: Upload orthophoto images and CSV sensor data
- **🗺️ Interactive Maps**: Visualize risk zones with MapLibre/Folium integration
- **📊 Real-time Analytics**: Charts and visualizations using Plotly
- **📋 Risk Reports**: Generate comprehensive HTML reports
- **📁 GIS Export**: Download shapefiles for QGIS analysis
- **🤖 AI Assistant**: Interactive chat for system guidance
- **⚡ Production-Ready UI**: Clean, professional interface with pagination

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd geoshield-demo
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # Option 1: Clean launch (no warnings)
   python run_clean.py
   
   # Option 2: Standard launch
   streamlit run app.py
   
   # Option 3: Use setup scripts
   ./setup.ps1  # Windows PowerShell
   setup.bat    # Windows Command Prompt
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8501`

## 📊 Demo Data

The system includes sample data generation for demonstration purposes. You can:
- Download sample CSV sensor data
- Upload your own orthophoto images
- View hardcoded risk analysis results

### Sample Data Format

The CSV file should include the following columns:
- `sensor_id`: Unique sensor identifier
- `timestamp`: Date and time of measurement
- `displacement_mm`: Ground displacement in millimeters
- `pore_pressure_kpa`: Pore pressure in kilopascals
- `strain_micro`: Strain measurement in microstrain
- `vibration_ms2`: Vibration in m/s²
- `rainfall_mm`: Rainfall in millimeters
- `latitude`: GPS latitude coordinate
- `longitude`: GPS longitude coordinate

## 🎯 Risk Analysis Logic

The demo uses hardcoded rules for risk assessment:

- **High Risk**: Displacement > 10mm AND Rainfall > 50mm
- **Medium Risk**: Displacement > 7mm OR Rainfall > 30mm
- **Low Risk**: All other conditions

## 📱 Application Structure

### Navigation Pages

1. **📊 Dashboard**: Overview metrics and system status
2. **📁 Data Upload**: File upload and processing interface
3. **🗺️ Map Analysis**: Interactive risk zone visualization
4. **📈 Analytics**: Detailed charts and statistical analysis
5. **📋 Risk Report**: Comprehensive report generation
6. **🤖 AI Assistant**: Interactive help and guidance

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Mapping**: Folium
- **Charts**: Plotly
- **Data Processing**: Pandas, NumPy
- **GIS**: GeoPandas, Shapely
- **UI Components**: Streamlit-option-menu

## 📁 File Structure

```
geoshield-demo/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎨 Customization

The application is designed to be easily customizable:
- Modify risk analysis rules in the `perform_risk_analysis()` function
- Update styling in the CSS section
- Add new chart types in the analytics section
- Extend the AI assistant responses

## 🔍 Usage Instructions

1. **Start with Dashboard**: View system overview and metrics
2. **Upload Data**: Navigate to Data Upload and either:
   - Download and upload the sample CSV
   - Upload your own sensor data
3. **View Analysis**: Check the Map Analysis for risk visualization
4. **Generate Reports**: Create comprehensive reports in the Risk Report section
5. **Ask Questions**: Use the AI Assistant for guidance

## 🚀 Production Deployment

For production deployment:
1. Set up a proper database for sensor data storage
2. Implement real-time data ingestion
3. Add user authentication and authorization
4. Configure proper logging and monitoring
5. Set up automated backup systems

## 📞 Support

This is a demonstration system. For technical questions or customization requests, please refer to the AI Assistant within the application.

## 📄 License

This demo application is provided for demonstration purposes.
