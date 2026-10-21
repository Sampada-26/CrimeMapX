import folium
import pandas as pd

def generate_interactive_map(input_path='data/processed/crime_data_processed.csv'):
    df = pd.read_csv(input_path)
    
    city_summary = df.groupby('City').agg({
        'Report Number': 'count', 
        'Crime Domain': lambda x: x.mode()[0] if not x.empty else 'Unknown'
    }).reset_index()
    city_summary.rename(columns={'Report Number': 'Crime Count'}, inplace=True)
    
    # Base map centered roughly around India (based on your dataset name)
    crime_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    
    # Placeholder city coordinates mapping (Update with your actual city coordinates if available)
    city_coords = {
        'Mumbai': [19.0760, 72.8777],
        'Delhi': [28.6139, 77.2090],
        'Bangalore': [12.9716, 77.5946]
        # Add more cities from your dataset here
    }
    
    for _, row in city_summary.iterrows():
        city = row['City']
        if city in city_coords:
            lat, lon = city_coords[city]
            folium.CircleMarker(
                location=[lat, lon],
                radius=max(5, row['Crime Count'] / 50),
                popup=f"<b>City:</b> {city}<br><b>Crimes:</b> {row['Crime Count']}<br><b>Top Domain:</b> {row['Crime Domain']}",
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(crime_map)
            
    crime_map.save('outputs/maps/interactive_crime_map.html')
    print("Interactive map saved to outputs/maps/interactive_crime_map.html")

if __name__ == "__main__":
    generate_interactive_map()