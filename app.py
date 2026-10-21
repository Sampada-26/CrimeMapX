import streamlit as st
import pandas as pd
from pathlib import Path

# --- PAGE CONFIGURATION ---
PROJECT_ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="CrimeMapX Dashboard",
    page_icon="🚨",
    layout="wide"
)

# --- LOAD DATA & FILES ---
@st.cache_data
def load_data():
    df = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "crime_data_processed.csv")
    return df

@st.cache_data
def load_rules():
    rules_path = PROJECT_ROOT / "outputs" / "results" / "association_rules.csv"
    if rules_path.is_file():
        return pd.read_csv(rules_path)
    return pd.DataFrame()

df = load_data()
rules_df = load_rules()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🚨 CrimeMapX Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio("Select View", ["Overview & Metrics", "Association Rule Mining", "Geospatial City Map"])

# --- PAGE 1: OVERVIEW & METRICS ---
if page == "Overview & Metrics":
    st.title("🛡️ CrimeMapX: Crime Intelligence & Pattern Analysis Dashboard")
    st.markdown("Welcome to the executive dashboard for exploring processed crime data, behavioral rules, and regional distributions.")
    
    # Key Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", len(df))
    col2.metric("Unique Cities", df['city'].nunique() if 'city' in df.columns else 0)
    col3.metric("Crime Domains", df['crime_domain'].nunique() if 'crime_domain' in df.columns else 0)
    col4.metric("Discovered Rules", len(rules_df))
    
    st.markdown("---")
    
    # Quick Data Preview
    st.subheader("📋 Processed Dataset Sample")
    st.dataframe(df.head(10), width='stretch')

# --- PAGE 2: ASSOCIATION RULE MINING ---
elif page == "Association Rule Mining":
    st.title("🔗 Association Rule Mining (Apriori)")
    st.markdown("Explore hidden behavioral patterns, co-occurrences, and correlations across crime attributes.")
    
    if rules_df.empty:
        st.warning("No association rules found. Please run `python main.py` first to generate the rules CSV.")
    else:
        # Filtering controls
        st.sidebar.markdown("### Filter Rules")
        min_lift = st.sidebar.slider("Minimum Lift", float(rules_df['lift'].min()), float(rules_df['lift'].max()), 1.0)
        min_conf = st.sidebar.slider("Minimum Confidence", float(rules_df['confidence'].min()), float(rules_df['confidence'].max()), 0.5)
        
        filtered_rules = rules_df[(rules_df['lift'] >= min_lift) & (rules_df['confidence'] >= min_conf)]
        
        st.info(f"Showing {len(filtered_rules)} rules matching your filter criteria.")
        
        # Display rules table
        st.dataframe(
            filtered_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']],
            width='stretch'
        )

# --- PAGE 3: GEOSPATIAL CITY MAP ---
elif page == "Geospatial City Map":
    st.title("🗺️ Regional Crime Summary Map")
    st.markdown("Visualizing aggregated crime volume distribution across cities.")
    
    map_path = PROJECT_ROOT / "outputs" / "maps" / "crime_map.html"
    if map_path.is_file():
        with open(map_path, 'r', encoding='utf-8') as f:
            map_html = f.read()
        
        # Render the HTML map inside Streamlit
        st.components.v1.html(map_html, height=600, scrolling=True)
    else:
        st.warning("Interactive map not found. Please run `python main.py` to generate the map file.") 