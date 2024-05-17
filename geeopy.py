import os
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

# Function to get the location using Nominatim geolocator with retries
def get_location(lat, lon, retries=3, delay=2):
    geolocator = Nominatim(user_agent="geo_locator", timeout=10)
    for attempt in range(retries):
        try:
            location = geolocator.reverse((lat, lon), language='en')
            return location.address if location else "Location not found"
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                return "Geocoding service unavailable"

def main():
    st.title("Location Finder")

    # Option to upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Check if latitude and longitude columns exist
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            st.success("Latitude and Longitude columns found.")

            # Initialize a list to store location names
            location_names = []

            # Iterate over rows and fetch location names
            for index, row in df.iterrows():
                lat = row['Latitude']
                lon = row['Longitude']
                location_name = get_location(lat, lon)
                location_names.append(location_name)

            # Add location names as a new column in the DataFrame
            df['Location Name'] = location_names

            # Create a map centered at the first location
            map_center = [df['Latitude'][0], df['Longitude'][0]]
            my_map = folium.Map(location=map_center, zoom_start=12)

            # Add markers for each location
            for index, row in df.iterrows():
                lat = row['Latitude']
                lon = row['Longitude']
                location_name = row['Location Name']
                folium.Marker([lat, lon], popup=location_name).add_to(my_map)

            # Display the map using folium_static
            folium_static(my_map)

            # Save the DataFrame with location names to the specified directory
            output_directory = os.path.expanduser("~/Desktop")
            txt_filename = os.path.join(output_directory, "location_names.txt")
            with open(txt_filename, 'w', encoding='utf-8') as txt_file:
                for location_name in location_names:
                    txt_file.write(location_name + '\n')
            st.success(f"Location names saved to {txt_filename}")

        else:
            st.error("Latitude and/or Longitude columns not found in the uploaded CSV file.")
    else:
        st.info("Please upload a CSV file.")

if __name__ == "__main__":
    main()
