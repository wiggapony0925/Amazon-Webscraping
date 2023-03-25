import requests
from bs4 import BeautifulSoup
import streamlit as st
import folium
import time

# Function to get the current temperature data
def get_temp_data():
    
    url = "https://weather.com/weather/today/l/New+York+NY+USNY0996:1:US"
    
    # Send a request to the website and get the HTML response
    page = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # temperature data
    temp_elem = soup.find('span', {'class': 'CurrentConditions--tempValue--MHmYY'})
   
    # Check if the temperature data was found
    if temp_elem is not None:
        temp = temp_elem.text.replace('°', '')
        return int(temp)
   
    else:
        return None

def precip_data():
    url = "https://weather.com/weather/today/l/New+York+NY+USNY0996:1:US"
    
     # Send a request to the website and get the HTML response
    page = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')
    precip_elem = soup.find('div', {'class': 'CurrentConditions--precipValue--RBVJT'})
    if precip_elem is not None:
        precip = precip_elem.text.replace('%', '')
        return int(precip)
    else:
        return None
    

global precip
# Set the app header and page layout
st.set_page_config(page_title='NYC Temperature', page_icon=':sunny:')
st.title('NYC Temperature')
st.write('This app shows the current temperature in New York City.')
st.markdown("---")


# Define a function to update the temperature data and map
def update_map():
    # Get the current temperature data
    temp = get_temp_data()
    precip = precip_data()
    # Check if the temperature data was found
    if temp is not None:
        # Display the current temperature
        st.subheader(f"Current Temperature: {temp}°F")
        st.subheader(f"Current Precipitation: {precip}°F")
        st.write("")
        if temp > 55:
            st.write("perfect day to go play sport and go out")
        else:
            st.write("stay home lol")
       
    
        # Show the temperature data on a map
        nyc_coords = (40.7128, -74.0060)
        map = folium.Map(location=nyc_coords, zoom_start=10)
        folium.Marker(location=nyc_coords, popup=f"Temperature: {temp}°F").add_to(map)
        map.add_child(folium.LatLngPopup())
        map.add_child(folium.ClickForMarker(popup='Waypoint'))
        folium.TileLayer('openstreetmap').add_to(map)
        folium.TileLayer('Stamen Terrain').add_to(map)
        folium.TileLayer('Stamen Toner').add_to(map)
        folium.TileLayer('stamenterrain').add_to(map)
        folium.TileLayer('cartodbpositron').add_to(map)
        folium.LayerControl().add_to(map)
        map_html = f'<div style="width: 1200px;height: 500px;display: block;margin-left: auto;margin-right: auto;">{map._repr_html_()}</div>'
        st.components.v1.html(map_html)

        time.sleep(60)  # wait for 60 seconds before updating the temperature data
    else:
        # Display an error message if the temperature data was not found
        st.write("Error: Could not retrieve temperature data.")
        return


# Call the update_map function to display the initial temperature data and map
   
update_map()

# Add a refresh button to allow the user to manually update the temperature data and map
if st.button("Refresh"):
    update_map()

