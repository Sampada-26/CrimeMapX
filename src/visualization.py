import folium
import pandas as pd
from pathlib import Path

def generate_crime_map(file_path='data/processed/crime_data_processed.csv', output_path='outputs/maps/crime_map.html'):
    print("Generating city-level crime summary map...")
    project_root = Path(__file__).resolve().parent.parent
    file_path = Path(file_path)
    output_path = Path(output_path)
    if not file_path.is_absolute():
        file_path = project_root / file_path
    if not output_path.is_absolute():
        output_path = project_root / output_path
    df = pd.read_csv(file_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if 'city' not in df.columns:
        print("Error: 'city' column not found in dataset.")
        return

    # Aggregate crime counts by city
    city_counts = df['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'crime_count']
    
    # Approximate coordinates for major cities (You can adjust or map these based on your specific dataset locations)
    # Adding a fallback dictionary for standard coordinates
    city_coords = {
        'Mumbai': [19.0760, 72.8777],
        'Delhi': [28.7041, 77.1025],
        'Bangalore': [12.9716, 77.5946],
        'Hyderabad': [17.3850, 78.4867],
        'Chennai': [13.0827, 80.2707],
        'Kolkata': [22.5726, 88.3639],
        'Pune': [18.5204, 73.8567],
        'Ahmedabad': [23.0225, 72.5714]
    }
    
    # Initialize map centered around a default location (e.g., India center)
    crime_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="OpenStreetMap")
    
    for _, row in city_counts.iterrows():
        city_name = row['city']
        count = row['crime_count']
        
        # Get coordinates if available, otherwise skip or use a default offset
        coords = city_coords.get(city_name, [20.0, 78.0]) # fallback
        
        # Add a circle marker sized by crime frequency
        folium.CircleMarker(
            location=coords,
            radius=min(max(count / 50, 5), 25), # Scale radius based on frequency
            popup=f"<b>City:</b> {city_name}<br><b>Total Crimes:</b> {count}",
            color='crimson',
            fill=True,
            fill_color='red',
            fill_opacity=0.6
        ).add_to(crime_map)
        
    crime_map.save(str(output_path))
    print(f"City-level map saved successfully to {output_path}!")

if __name__ == "__main__":
    generate_crime_map()