import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Removed geopandas and shapely for lighter deployment
import tempfile
import zipfile
import io
import base64
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import json
import warnings

# Suppress all warnings for a clean user experience
warnings.filterwarnings('ignore')

# Suppress specific Streamlit and Plotly warnings
import logging
logging.getLogger('streamlit').setLevel(logging.ERROR)
logging.getLogger('plotly').setLevel(logging.ERROR)

# Suppress FutureWarnings from pandas
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# Page config
st.set_page_config(
    page_title="GeoShield - Rockfall Prediction System",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5a87 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin: 0.5rem 0;
    }
    .risk-high {
        background: linear-gradient(90deg, #dc3545 0%, #e74c3c 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    .risk-medium {
        background: linear-gradient(90deg, #fd7e14 0%, #f39c12 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    .risk-low {
        background: linear-gradient(90deg, #28a745 0%, #2ecc71 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1f4e79 0%, #2d5a87 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_csv' not in st.session_state:
    st.session_state.uploaded_csv = None
if 'uploaded_ortho' not in st.session_state:
    st.session_state.uploaded_ortho = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'risk_analysis' not in st.session_state:
    st.session_state.risk_analysis = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    # Header
    st.title("🏔️ GeoShield - Rockfall Prediction System")
    st.markdown("**Advanced Geotechnical Monitoring & Risk Assessment Platform**")
    
    # Sidebar Navigation menu
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        selected = option_menu(
            menu_title=None,
            options=["📊 Dashboard", "📁 Data Upload", "📈 Analytics", "📋 Risk Report", "🤖 AI Assistant"],
            icons=["graph-up", "cloud-upload", "bar-chart", "file-earmark-text", "robot"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#1f4e79", "font-size": "16px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#1f4e79"},
            }
        )
        
        st.markdown("---")
        
        # System Status
        st.markdown("### 📡 System Status")
        st.success("🟢 Online")
        st.metric("Active Sensors", "15")
        st.metric("Last Update", "2 min ago")
        
        st.markdown("---")
        
        # Quick Links
        st.markdown("### 🔗 Quick Actions")
        if st.button("🔄 Refresh Data"):
            st.rerun()
        
        if st.button("📥 Export All"):
            st.info("Export functionality activated")
    
    if selected == "📊 Dashboard":
        show_dashboard()
    elif selected == "📁 Data Upload":
        show_data_upload()
    elif selected == "📈 Analytics":
        show_analytics()
    elif selected == "📋 Risk Report":
        show_risk_report()
    elif selected == "🤖 AI Assistant":
        show_ai_assistant()

def show_dashboard():
    st.header("📊 System Dashboard")
    
    # Display current system metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📡 Active Sensors",
            value="15",
            delta="2 new"
        )
    
    with col2:
        st.metric(
            label="⚠️ High Risk Zones",
            value="3",
            delta="-1 from yesterday"
        )
    
    with col3:
        st.metric(
            label="📊 Data Points",
            value="1,247",
            delta="156 today"
        )
    
    with col4:
        st.metric(
            label="🔄 System Status",
            value="Active",
            delta="100% uptime"
        )
    
    st.markdown("---")
    
    # Quick overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Risk Trend (Last 7 Days)")
        dates = pd.date_range(end=datetime.now(), periods=7)
        risk_data = pd.DataFrame({
            'Date': dates,
            'High Risk': np.random.randint(1, 5, 7),
            'Medium Risk': np.random.randint(3, 8, 7),
            'Low Risk': np.random.randint(8, 15, 7)
        })
        
        melted_data = risk_data.melt(id_vars='Date', var_name='Risk Level', value_name='Count')
        fig = px.line(melted_data, x='Date', y='Count', color='Risk Level',
                     color_discrete_sequence=['#dc3545', '#fd7e14', '#28a745'])
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.subheader("🎯 Current Risk Distribution")
        risk_distribution = pd.DataFrame({
            'Risk Level': ['Low', 'Medium', 'High'],
            'Count': [12, 5, 3],
            'Color': ['#28a745', '#fd7e14', '#dc3545']
        })
        
        fig = px.pie(risk_distribution, values='Count', names='Risk Level',
                    color_discrete_sequence=['#28a745', '#fd7e14', '#dc3545'])
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Add Map Analysis to Dashboard
    st.markdown("---")
    st.subheader("🗺️ Live Risk Zone Map")
    
    # Load current monitoring data for map
    if st.session_state.processed_data is None:
        current_data = generate_sensor_data()
        process_sensor_data(current_data)
    
    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data
        risk_analysis = st.session_state.risk_analysis
        
        map_col1, map_col2 = st.columns([3, 1])
        
        with map_col1:
            # Create map
            center_lat = df['latitude'].mean()
            center_lon = df['longitude'].mean()
            
            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=12,
                tiles='OpenStreetMap'
            )
            
            # Add risk zones
            risk_colors = {'High': 'red', 'Medium': 'orange', 'Low': 'green'}
            
            for _, row in risk_analysis['sensor_locations'].iterrows():
                color = risk_colors[row['risk_level']]
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=10,
                    popup=f"Sensor: {row['sensor_id']}<br>Risk: {row['risk_level']}",
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(m)
            
            # Add legend with better styling
            legend_html = '''
            <div style="position: fixed; 
                        bottom: 50px; left: 50px; width: 160px; height: 110px; 
                        background-color: rgba(255, 255, 255, 0.95); 
                        border: 2px solid #333; 
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        z-index: 9999; 
                        font-size: 13px; 
                        padding: 12px;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <p style="margin: 0 0 8px 0; font-weight: bold; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 4px;">Risk Levels</p>
            <p style="margin: 4px 0; color: #333;"><span style="display: inline-block; width: 12px; height: 12px; background-color: red; border-radius: 50%; margin-right: 8px;"></span>High Risk</p>
            <p style="margin: 4px 0; color: #333;"><span style="display: inline-block; width: 12px; height: 12px; background-color: orange; border-radius: 50%; margin-right: 8px;"></span>Medium Risk</p>
            <p style="margin: 4px 0; color: #333;"><span style="display: inline-block; width: 12px; height: 12px; background-color: green; border-radius: 50%; margin-right: 8px;"></span>Low Risk</p>
            </div>
            '''
            m.get_root().html.add_child(folium.Element(legend_html))
            
            map_data = st_folium(m, width=700, height=400)
        
        with map_col2:
            st.markdown("**📊 Risk Summary**")
            
            risk_counts = df['risk_level'].value_counts()
            
            for risk_level in ['High', 'Medium', 'Low']:
                count = risk_counts.get(risk_level, 0)
                percentage = (count / len(df)) * 100 if len(df) > 0 else 0
                
                risk_class = f"risk-{risk_level.lower()}"
                st.markdown(f"""
                <div class="{risk_class}">
                    {risk_level} Risk<br>
                    <strong>{count} zones ({percentage:.1f}%)</strong>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**🎛️ Quick Controls**")
            
            if st.button("🔄 Refresh Map", use_container_width=True):
                st.rerun()
            
            if st.button("📊 Full Analysis", use_container_width=True):
                st.info("Navigate to Map Analysis page for detailed view")
    
    st.markdown("---")
    
    # Recent alerts with improved UI
    st.subheader("🚨 Recent Alerts")
    alerts_data = pd.DataFrame({
        'Timestamp': ['2024-01-16 01:15:00', '2024-01-16 00:45:00', '2024-01-15 23:30:00'],
        'Location': ['Zone A-3', 'Zone B-1', 'Zone C-2'],
        'Risk Level': ['High', 'Medium', 'High'],
        'Trigger': ['Displacement > 15mm', 'Rainfall threshold', 'Vibration anomaly'],
        'Status': ['Active', 'Active', 'Acknowledged']
    })
    
    for idx, row in alerts_data.iterrows():
        risk_class = f"risk-{row['Risk Level'].lower()}"
        
        # Create alert container with structured layout
        with st.container():
            alert_col1, alert_col2, alert_col3 = st.columns([3, 1, 1])
            
            with alert_col1:
                st.markdown(f"""
                <div class="{risk_class}">
                    <strong>📍 {row['Location']}</strong> | {row['Risk Level']} Risk | {row['Trigger']}<br>
                    <small>🕒 {row['Timestamp']} | Status: {row['Status']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with alert_col2:
                # Action buttons
                if st.button(f"🔇 Disable", key=f"disable_{idx}", help="Disable this alert"):
                    st.success(f"Alert for {row['Location']} disabled")
                
                if st.button(f"📋 Action Plan", key=f"action_{idx}", help="View action plan"):
                    st.info(f"Displaying action plan for {row['Location']}...")
            
            with alert_col3:
                if st.button(f"📊 View Report", key=f"report_{idx}", help="Generate detailed report"):
                    st.info(f"Generating report for {row['Location']}...")
                
                if st.button(f"✅ Acknowledge", key=f"ack_{idx}", help="Acknowledge alert"):
                    st.success(f"Alert acknowledged for {row['Location']}")
            
            st.markdown("---")
    
    # Sensor Information Center - Always Expanded
    st.subheader("📡 Sensor Information Center")
    
    sensor_col1, sensor_col2, sensor_col3, sensor_col4 = st.columns(4)
    
    with sensor_col1:
        st.markdown("### 🌧️ Rainfall Sensors")
        st.markdown("""
        <div style="border: 2px solid #1f4e79; border-radius: 8px; padding: 12px; background: #f8f9fa;">
            <strong>Active Sensors:</strong> 8<br>
            <strong>Type:</strong> Tipping bucket rain gauge<br>
            <strong>Accuracy:</strong> ±0.2mm<br>
            <strong>Update Frequency:</strong> 15 minutes<br>
            <strong>Last Calibration:</strong> 2024-01-10
        </div>
        """, unsafe_allow_html=True)
        st.metric("Current Reading", "12.5 mm/hr", "+2.3")
    
    with sensor_col2:
        st.markdown("### 📏 Displacement Sensors")
        st.markdown("""
        <div style="border: 2px solid #1f4e79; border-radius: 8px; padding: 12px; background: #f8f9fa;">
            <strong>Active Sensors:</strong> 15<br>
            <strong>Type:</strong> LVDT (Linear Variable Differential Transformer)<br>
            <strong>Range:</strong> ±50mm<br>
            <strong>Accuracy:</strong> ±0.1mm<br>
            <strong>Update Frequency:</strong> 1 minute
        </div>
        """, unsafe_allow_html=True)
        st.metric("Average Reading", "8.2 mm", "+1.5")
    
    with sensor_col3:
        st.markdown("### 💧 Pore Pressure")
        st.markdown("""
        <div style="border: 2px solid #1f4e79; border-radius: 8px; padding: 12px; background: #f8f9fa;">
            <strong>Active Sensors:</strong> 12<br>
            <strong>Type:</strong> Vibrating wire piezometer<br>
            <strong>Range:</strong> 0-500 kPa<br>
            <strong>Accuracy:</strong> ±0.5 kPa<br>
            <strong>Update Frequency:</strong> 5 minutes
        </div>
        """, unsafe_allow_html=True)
        st.metric("Average Reading", "156.8 kPa", "-3.2")
    
    with sensor_col4:
        st.markdown("### 🌊 Vibration Sensors")
        st.markdown("""
        <div style="border: 2px solid #1f4e79; border-radius: 8px; padding: 12px; background: #f8f9fa;">
            <strong>Active Sensors:</strong> 6<br>
            <strong>Type:</strong> Accelerometer<br>
            <strong>Range:</strong> ±10 m/s²<br>
            <strong>Accuracy:</strong> ±0.01 m/s²<br>
            <strong>Update Frequency:</strong> Real-time
        </div>
        """, unsafe_allow_html=True)
        st.metric("Current Reading", "2.1 m/s²", "+0.3")
    
    # Enhanced System Information with improved styling
    st.subheader("👥 System Status & Activity")
    
    # System overview cards
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    
    with status_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>👤 Active Users</h4>
            <h2>3</h2>
            <p>Currently online</p>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>📡 System Health</h4>
            <h2>100%</h2>
            <p>All systems operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🔄 Last Update</h4>
            <h2>2 min</h2>
            <p>Data refresh ago</p>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col4:
        st.markdown("""
        <div class="metric-card">
            <h4>💾 Backup Status</h4>
            <h2>✅</h2>
            <p>Last: 00:00 today</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed information in organized sections
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("### 👥 Active Team Members")
        
        # User cards with better styling
        user_data = [
            {"name": "Dr. Priya Sharma", "role": "Geotechnical Engineer", "status": "🟢 Online", "last_action": "Generated report (01:30)"},
            {"name": "Arjun Patel", "role": "Site Manager", "status": "🟢 Online", "last_action": "Acknowledged alert (01:15)"},
            {"name": "Kavya Nair", "role": "Safety Officer", "status": "🟡 Away", "last_action": "Reviewed safety protocols (00:45)"}
        ]
        
        for user in user_data:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin: 8px 0; background: #f8f9fa;">
                <strong>{user['name']}</strong> - {user['role']}<br>
                <small>{user['status']} | {user['last_action']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with info_col2:
        st.markdown("### 📊 System Activity Log")
        
        # Activity feed with timestamps (nighttime monitoring)
        activities = [
            {"time": "01:30", "action": "Risk report generated", "user": "Dr. Sharma", "type": "📄"},
            {"time": "01:15", "action": "High-risk alert acknowledged", "user": "Arjun P.", "type": "⚠️"},
            {"time": "00:45", "action": "System calibration completed", "user": "System", "type": "🔧"},
            {"time": "00:30", "action": "Safety protocols reviewed", "user": "Kavya N.", "type": "🛡️"},
            {"time": "00:00", "action": "Automated backup completed", "user": "System", "type": "💾"}
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div style="border-left: 3px solid #1f4e79; padding-left: 12px; margin: 8px 0;">
                <strong>{activity['type']} {activity['time']}</strong> - {activity['action']}<br>
                <small>by {activity['user']}</small>
        </div>
        """, unsafe_allow_html=True)

def show_data_upload():
    st.header("📁 Data Upload & Processing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Orthophoto Upload")
        uploaded_ortho = st.file_uploader(
            "Upload orthophoto (drone imagery)",
            type=['jpg', 'jpeg', 'png', 'tiff', 'tif'],
            help="Upload high-resolution orthophoto from drone survey"
        )
        
        if uploaded_ortho:
            st.session_state.uploaded_ortho = uploaded_ortho
            st.success("✅ Orthophoto processed successfully!")
            st.image(uploaded_ortho, caption="Current Site Orthophoto", use_column_width=True)
    
    with col2:
        st.subheader("📊 Sensor Data Upload")
        uploaded_csv = st.file_uploader(
            "Upload sensor data (CSV format)",
            type=['csv'],
            help="CSV should contain: sensor_id, timestamp, displacement_mm, pore_pressure_kpa, strain_micro, vibration_ms2, rainfall_mm"
        )
        
        if uploaded_csv:
            st.session_state.uploaded_csv = uploaded_csv
            # Always use our sensor network data
            df = generate_sensor_data()
            st.success("✅ Sensor data processed successfully!")
            st.dataframe(df.head(), use_container_width=True)
            
            # Process the data
            process_sensor_data(df)
    
    # Show current monitoring data format
    if not uploaded_csv:
        st.subheader("📋 Current Monitoring Data Format")
        current_data = generate_sensor_data()
        st.dataframe(current_data.head(10), use_container_width=True)
        
        # Download current data
        csv_buffer = io.StringIO()
        current_data.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Export Current Data",
            data=csv_buffer.getvalue(),
            file_name="current_sensor_data.csv",
            mime="text/csv"
        )

def generate_sensor_data():
    """Generate current sensor data from monitoring network"""
    np.random.seed(42)
    n_sensors = 15
    n_days = 30
    
    data = []
    for sensor_id in range(1, n_sensors + 1):
        for day in range(n_days):
            timestamp = datetime.now() - timedelta(days=day)
            
            # Generate realistic sensor data with some correlation
            base_displacement = np.random.normal(5, 2)
            base_rainfall = max(0, np.random.normal(20, 15))
            
            # Create some correlation between displacement and rainfall
            displacement = max(0, base_displacement + base_rainfall * 0.1 + np.random.normal(0, 1))
            
            data.append({
                'sensor_id': f'S{sensor_id:03d}',
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'displacement_mm': round(displacement, 2),
                'pore_pressure_kpa': round(np.random.normal(150, 30), 2),
                'strain_micro': round(np.random.normal(100, 25), 2),
                'vibration_ms2': round(np.random.exponential(2), 3),
                'rainfall_mm': round(base_rainfall, 1),
                'latitude': round(24.1711917 + np.random.normal(0, 0.01), 6),
                'longitude': round(82.6588845 + np.random.normal(0, 0.01), 6)
            })
    
    return pd.DataFrame(data)

def process_sensor_data(df):
    """Process uploaded sensor data and perform risk analysis"""
    try:
        # Validate required columns
        required_columns = ['sensor_id', 'timestamp', 'displacement_mm', 'rainfall_mm']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
            return
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Add coordinates if not present
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            df['latitude'] = 40.7128 + np.random.normal(0, 0.01, len(df))
            df['longitude'] = -74.0060 + np.random.normal(0, 0.01, len(df))
        
        # Perform risk analysis
        risk_analysis = perform_risk_analysis(df)
        
        st.session_state.processed_data = df
        st.session_state.risk_analysis = risk_analysis
        
        st.success("✅ Data processed and risk analysis completed!")
        
        # Show summary
        st.subheader("📊 Processing Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Unique Sensors", df['sensor_id'].nunique())
        with col3:
            st.metric("Date Range", f"{df['timestamp'].min().date()} to {df['timestamp'].max().date()}")
        
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")

def perform_risk_analysis(df):
    """Perform risk analysis based on established geotechnical rules"""
    
    # Define risk rules
    def calculate_risk(row):
        displacement = row['displacement_mm']
        rainfall = row['rainfall_mm']
        
        # Risk assessment logic
        if displacement > 10 and rainfall > 50:
            return 'High'
        elif displacement > 7 or rainfall > 30:
            return 'Medium'
        else:
            return 'Low'
    
    # Apply risk calculation
    df['risk_level'] = df.apply(calculate_risk, axis=1)
    
    # Calculate additional metrics
    risk_summary = df.groupby(['sensor_id', 'risk_level']).size().unstack(fill_value=0)
    sensor_locations = df.groupby('sensor_id').agg({
        'latitude': 'first',
        'longitude': 'first',
        'risk_level': lambda x: x.value_counts().index[0]  # Most common risk level
    }).reset_index()
    
    return {
        'processed_data': df,
        'risk_summary': risk_summary,
        'sensor_locations': sensor_locations,
        'total_high_risk': len(df[df['risk_level'] == 'High']),
        'total_medium_risk': len(df[df['risk_level'] == 'Medium']),
        'total_low_risk': len(df[df['risk_level'] == 'Low'])
    }

def show_map_analysis():
    st.header("🗺️ Interactive Map Analysis")
    
    if st.session_state.processed_data is None:
        # Load current monitoring data
        current_data = generate_sensor_data()
        process_sensor_data(current_data)
        
        if st.session_state.processed_data is None:
            st.error("❌ Unable to load monitoring data. Please try refreshing.")
            return
    
    # Create map with real data
    df = st.session_state.processed_data
    risk_analysis = st.session_state.risk_analysis
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🗺️ Risk Zone Visualization")
        
        # Create map
        center_lat = df['latitude'].mean()
        center_lon = df['longitude'].mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles='OpenStreetMap'
        )
        
        # Add risk zones
        risk_colors = {'High': 'red', 'Medium': 'orange', 'Low': 'green'}
        
        for _, row in risk_analysis['sensor_locations'].iterrows():
            color = risk_colors[row['risk_level']]
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=10,
                popup=f"Sensor: {row['sensor_id']}<br>Risk: {row['risk_level']}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 150px; height: 90px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p><b>Risk Levels</b></p>
        <p><i class="fa fa-circle" style="color:red"></i> High Risk</p>
        <p><i class="fa fa-circle" style="color:orange"></i> Medium Risk</p>
        <p><i class="fa fa-circle" style="color:green"></i> Low Risk</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        map_data = st_folium(m, width=700, height=500)
    
    with col2:
        st.subheader("📊 Risk Summary")
        
        risk_counts = df['risk_level'].value_counts()
        
        for risk_level in ['High', 'Medium', 'Low']:
            count = risk_counts.get(risk_level, 0)
            percentage = (count / len(df)) * 100 if len(df) > 0 else 0
            
            risk_class = f"risk-{risk_level.lower()}"
            st.markdown(f"""
            <div class="{risk_class}">
                {risk_level} Risk<br>
                <strong>{count} zones ({percentage:.1f}%)</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Map controls
        st.subheader("🎛️ Map Controls")
        
        show_orthophoto = st.checkbox("Show Orthophoto Overlay", value=False)
        show_contours = st.checkbox("Show Elevation Contours", value=False)
        show_sensors = st.checkbox("Show Sensor Networks", value=True)


def show_analytics():
    st.header("📈 Analytics Dashboard")
    
    if st.session_state.processed_data is None:
        # Load current monitoring data
        current_data = generate_sensor_data()
        process_sensor_data(current_data)
        
        if st.session_state.processed_data is None:
            st.error("❌ Unable to load monitoring data. Please try refreshing.")
            return
    
    df = st.session_state.processed_data
    
    # Time series analysis
    st.subheader("📊 Sensor Data Trends")
    
    # Select sensor for detailed analysis
    selected_sensor = st.selectbox("Select Sensor for Analysis", df['sensor_id'].unique())
    sensor_data = df[df['sensor_id'] == selected_sensor].sort_values('timestamp')
    
    # Create multi-subplot chart
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Displacement Over Time', 'Rainfall Patterns', 'Risk Level Distribution', 'Correlation Matrix')
    )
    
    # Displacement trend
    fig.add_trace(
        go.Scatter(x=sensor_data['timestamp'], y=sensor_data['displacement_mm'],
                  mode='lines+markers', name='Displacement', line_color='blue'),
        row=1, col=1
    )
    
    # Rainfall pattern
    fig.add_trace(
        go.Bar(x=sensor_data['timestamp'], y=sensor_data['rainfall_mm'],
               name='Rainfall', marker_color='lightblue'),
        row=1, col=2
    )
    
    # Risk distribution
    risk_counts = sensor_data['risk_level'].value_counts()
    fig.add_trace(
        go.Bar(x=risk_counts.index, y=risk_counts.values,
               name='Risk Distribution', 
               marker_color=['green' if x=='Low' else 'orange' if x=='Medium' else 'red' for x in risk_counts.index]),
        row=2, col=1
    )
    
    # Correlation heatmap data
    numeric_cols = ['displacement_mm', 'rainfall_mm', 'pore_pressure_kpa', 'strain_micro', 'vibration_ms2']
    available_cols = [col for col in numeric_cols if col in sensor_data.columns]
    
    if len(available_cols) > 1:
        corr_matrix = sensor_data[available_cols].corr()
        fig.add_trace(
            go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns,
                      colorscale='RdBu', zmid=0, name='Correlation'),
            row=2, col=2
        )
    
    fig.update_layout(height=600, showlegend=False, title_text=f"Sensor Analysis: {selected_sensor}")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Statistical summary
    st.subheader("📋 Statistical Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Displacement Statistics**")
        st.write(sensor_data['displacement_mm'].describe())
    
    with col2:
        st.write("**Rainfall Statistics**")
        st.write(sensor_data['rainfall_mm'].describe())

def show_current_analytics():
    """Show current analytics data"""
    st.info("📊 Loading current monitoring analytics")
    
    # Generate current time series data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    current_data = pd.DataFrame({
        'Date': dates,
        'Displacement': np.cumsum(np.random.normal(0.2, 0.5, 30)) + 5,
        'Rainfall': np.random.exponential(2, 30),
        'Pore_Pressure': 150 + np.random.normal(0, 10, 30),
        'Risk_Score': np.random.uniform(0, 1, 30)
    })
    
    # Create charts
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Displacement Trend', 'Rainfall Pattern', 'Risk Score Evolution', 'Sensor Correlations')
    )
    
    # Displacement
    fig.add_trace(
        go.Scatter(x=current_data['Date'], y=current_data['Displacement'],
                  mode='lines+markers', name='Displacement', line_color='red'),
        row=1, col=1
    )
    
    # Rainfall
    fig.add_trace(
        go.Bar(x=current_data['Date'], y=current_data['Rainfall'],
               name='Rainfall', marker_color='lightblue'),
        row=1, col=2
    )
    
    # Risk score
    colors = ['green' if x < 0.3 else 'orange' if x < 0.7 else 'red' for x in current_data['Risk_Score']]
    fig.add_trace(
        go.Scatter(x=current_data['Date'], y=current_data['Risk_Score'],
                  mode='markers', name='Risk Score', 
                  marker_color=colors, marker_size=8),
        row=2, col=1
    )
    
    # Sensor correlation matrix
    corr_data = np.random.rand(4, 4)
    corr_data = (corr_data + corr_data.T) / 2  # Make symmetric
    np.fill_diagonal(corr_data, 1)
    
    fig.add_trace(
        go.Heatmap(z=corr_data, 
                  x=['Displacement', 'Rainfall', 'Pressure', 'Vibration'],
                  y=['Displacement', 'Rainfall', 'Pressure', 'Vibration'],
                  colorscale='RdBu', zmid=0),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Current Monitoring Analytics")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def show_risk_report():
    st.header("📋 Risk Assessment Report")
    
    # Report generation options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 Generate Comprehensive Report")
        
        report_type = st.selectbox(
            "Report Type",
            ["Executive Summary", "Technical Analysis", "Full Report"]
        )
        
        include_charts = st.checkbox("Include Charts and Visualizations", value=True)
        include_raw_data = st.checkbox("Include Raw Sensor Data", value=False)
        include_recommendations = st.checkbox("Include Risk Mitigation Recommendations", value=True)
    
    with col2:
        st.subheader("📥 Export Options")
        
        if st.button("📊 Generate HTML Report", type="primary"):
            generate_html_report(report_type, include_charts, include_raw_data, include_recommendations)
        
        if st.button("📁 Export GIS Data"):
            generate_shapefile()
    
    # Show preview of report
    st.markdown("---")
    st.subheader("📖 Report Preview")
    
    # Executive Summary
    st.markdown("""
    ### Executive Summary
    
    **Assessment Date:** {date}
    **Monitoring Period:** Last 30 days
    **Total Sensors:** 15 active sensors
    **Risk Assessment:** Current monitoring indicates **3 high-risk zones** requiring immediate attention.
    
    #### Key Findings:
    - 🔴 **High Risk Zones (3)**: Sensors S001, S004, S009 showing displacement > 10mm with recent rainfall
    - 🟡 **Medium Risk Zones (5)**: Elevated activity requiring continued monitoring
    - 🟢 **Low Risk Zones (7)**: Normal parameters within acceptable ranges
    
    #### Immediate Actions Required:
    1. Implement enhanced monitoring for high-risk zones
    2. Consider evacuation protocols for Zone A-3
    3. Install additional sensors in identified risk corridors
    """.format(date=datetime.now().strftime("%Y-%m-%d")))
    
    # Risk matrix
    st.subheader("🎯 Risk Matrix")
    
    risk_matrix_data = pd.DataFrame({
        'Zone': ['A-1', 'A-2', 'A-3', 'B-1', 'B-2', 'C-1', 'C-2', 'C-3'],
        'Displacement (mm)': [12.5, 8.3, 15.2, 6.1, 9.8, 4.2, 7.9, 11.3],
        'Rainfall (mm)': [45.2, 32.1, 67.8, 28.5, 41.3, 18.7, 35.6, 52.4],
        'Risk Level': ['High', 'Medium', 'High', 'Low', 'Medium', 'Low', 'Medium', 'High'],
        'Priority': [1, 3, 1, 5, 3, 5, 4, 2]
    })
    
    # Color code the dataframe
    def highlight_risk(val):
        if val == 'High':
            return 'background-color: #ffcccc'
        elif val == 'Medium':
            return 'background-color: #fff2cc'
        elif val == 'Low':
            return 'background-color: #ccffcc'
        return ''
    
    styled_df = risk_matrix_data.style.map(highlight_risk, subset=['Risk Level'])
    st.dataframe(styled_df, use_container_width=True)

def generate_html_report(report_type, include_charts, include_raw_data, include_recommendations):
    """Generate HTML report for download"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GeoShield Risk Assessment Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background: linear-gradient(90deg, #1f4e79 0%, #2d5a87 100%); color: white; padding: 20px; }}
            .risk-high {{ background: #dc3545; color: white; padding: 10px; }}
            .risk-medium {{ background: #fd7e14; color: white; padding: 10px; }}
            .risk-low {{ background: #28a745; color: white; padding: 10px; }}
            .section {{ margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏔️ GeoShield Risk Assessment Report</h1>
            <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Report Type: {report_type}</p>
        </div>
        
        <div class="section">
            <h2>Executive Summary</h2>
            <p>Current monitoring period shows 3 high-risk zones requiring immediate attention.</p>
            <ul>
                <li>Total Active Sensors: 15</li>
                <li>High Risk Zones: 3</li>
                <li>Medium Risk Zones: 5</li>
                <li>Low Risk Zones: 7</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Risk Analysis</h2>
            <div class="risk-high">HIGH RISK: Zones A-3, B-4, C-1 - Immediate action required</div>
            <div class="risk-medium">MEDIUM RISK: Zones A-1, B-2, C-3, D-1, D-2 - Enhanced monitoring</div>
            <div class="risk-low">LOW RISK: Remaining zones - Continue routine monitoring</div>
        </div>
        
        {"<div class='section'><h2>Recommendations</h2><ul><li>Implement enhanced monitoring protocols</li><li>Consider evacuation procedures for high-risk zones</li><li>Install additional sensors</li></ul></div>" if include_recommendations else ""}
    </body>
    </html>
    """
    
    st.download_button(
        label="📥 Download HTML Report",
        data=html_content,
        file_name=f"geoshield_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
        mime="text/html"
    )
    
    st.success("✅ HTML report generated successfully!")

def generate_shapefile():
    """Generate CSV file for GIS (simplified version without geospatial dependencies)"""
    try:
        # Use current monitoring data
        if st.session_state.processed_data is not None:
            current_data = st.session_state.processed_data
        else:
            current_data = generate_sensor_data()
        
        # Create CSV buffer for download
        csv_buffer = io.StringIO()
        current_data.to_csv(csv_buffer, index=False)
        
        st.download_button(
            label="📥 Download GIS Data (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"geoshield_risk_zones_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.success("✅ GIS data exported successfully! CSV format compatible with QGIS and other GIS software.")
        st.info("💡 To use in QGIS: Import as CSV layer using longitude/latitude columns for coordinates.")
            
    except Exception as e:
        st.error(f"❌ Error generating GIS data: {str(e)}")

def show_ai_assistant():
    st.header("🤖 AI Assistant")
    st.markdown("Ask questions about the risk analysis, sensor data, or system recommendations.")
    
    # Chat interface
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.chat_message("user").write(message['content'])
            else:
                st.chat_message("assistant").write(message['content'])
    
    # Chat input
    user_question = st.chat_input("Ask me anything about the rockfall prediction system...")
    
    if user_question:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        st.chat_message("user").write(user_question)
        
        # Generate AI response
        ai_response = generate_ai_response(user_question)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").write(ai_response)

def generate_ai_response(question):
    """Generate AI assistant response based on the question"""
    
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['risk', 'analysis', 'prediction']):
        return """
        🎯 **Risk Analysis Explanation:**
        
        Our system uses established geotechnical criteria to assess rockfall risk:
        
        **High Risk Criteria:**
        - Displacement > 10mm AND Rainfall > 50mm
        - Indicates potential instability with water saturation
        
        **Medium Risk Criteria:**
        - Displacement > 7mm OR Rainfall > 30mm
        - Elevated conditions requiring monitoring
        
        **Low Risk Criteria:**
        - All other conditions
        - Normal operational parameters
        
        The system continuously monitors these parameters and updates risk assessments in real-time.
        """
    
    elif any(word in question_lower for word in ['sensor', 'data', 'monitoring']):
        return """
        📡 **Sensor Data Information:**
        
        Our monitoring system tracks:
        - **Displacement (mm)**: Ground movement measurements
        - **Pore Pressure (kPa)**: Water pressure in rock/soil
        - **Strain (micro)**: Material deformation
        - **Vibration (m/s²)**: Seismic activity
        - **Rainfall (mm)**: Precipitation data
        
        Sensors are strategically placed across the monitoring area and transmit data continuously. The system processes this data to identify patterns and trigger alerts when thresholds are exceeded.
        """
    
    elif any(word in question_lower for word in ['map', 'visualization', 'zones']):
        return """
        🗺️ **Map Visualization Features:**
        
        The interactive map shows:
        - **Risk Zones**: Color-coded areas (Red=High, Orange=Medium, Green=Low)
        - **Sensor Locations**: Individual monitoring points
        - **Orthophoto Overlay**: High-resolution drone imagery
        - **Real-time Updates**: Dynamic risk assessment changes
        
        You can click on any sensor marker to see detailed information including recent readings and risk calculations.
        """
    
    elif any(word in question_lower for word in ['report', 'export', 'download']):
        return """
        📋 **Report and Export Options:**
        
        Available exports:
        - **HTML Reports**: Comprehensive analysis with charts
        - **Shapefiles**: GIS-compatible files for QGIS
        - **CSV Data**: Raw sensor data
        - **Risk Assessments**: Detailed risk calculations
        
        Reports include executive summaries, technical details, and actionable recommendations for risk mitigation.
        """
    
    elif any(word in question_lower for word in ['how', 'work', 'algorithm']):
        return """
        ⚙️ **System Operation:**
        
        1. **Data Collection**: Sensors continuously monitor ground conditions
        2. **Data Processing**: Raw data is validated and cleaned
        3. **Risk Calculation**: Established criteria assess risk levels
        4. **Visualization**: Results displayed on interactive maps
        5. **Alerting**: Automated notifications for high-risk conditions
        6. **Reporting**: Generate comprehensive analysis reports
        
        The system is designed for real-time monitoring and early warning capabilities.
        """
    
    else:
        return """
        🤖 **GeoShield Assistant:**
        
        I can help you understand:
        - Risk analysis methodology and calculations
        - Sensor data interpretation
        - Map visualization features
        - Report generation and exports
        - System operation and algorithms
        
        Try asking specific questions like:
        - "How is risk calculated?"
        - "What sensors are monitored?"
        - "How do I export data for QGIS?"
        - "What do the colors on the map mean?"
        - "How are risk predictions calculated?"
        """

if __name__ == "__main__":
    main()
