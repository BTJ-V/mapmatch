import folium
from folium import plugins

# Create a folium map centered at Kukatpally
m = folium.Map(location=[17.498126, 78.390369], zoom_start=15)

# Add drawing tools
plugins.Draw(
    export=True,  # Enable the export button
    filename='data.geojson'  # Specify the filename for the GeoJSON
).add_to(m)

# Save the interactive map
m.save("interactive_map.html")
print("Interactive map created as 'interactive_map.html'. Open it in a web browser to draw and save your route.")
