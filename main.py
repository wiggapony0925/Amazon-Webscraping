import requests
from bs4 import BeautifulSoup
import streamlit as st
import matplotlib.pyplot as plt

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

# Set the Streamlit app configuration
st.set_page_config(page_title="NYC Temperature Checker", page_icon=":sunny:")

# Set the app header
st.title("NYC Temperature Checker")

# Get the current temperature data
temp = get_temp_data()

# Check if the temperature data was found
if temp is not None:
    # Display the current temperature
    st.write(f"Current Temperature: {temp}°F")

    # Define the color-coding for the temperature range
    if temp < 32:
        color = 'blue'
    elif temp < 60:
        color = 'green'
    elif temp < 80:
        color = 'orange'
    else:
        color = 'red'

    # Define the x and y data for the graph
    x = ['NYC']
    y = [temp]

    # Plot the graph with color-coding
    fig, ax = plt.subplots()
    ax.bar(x, y, color=color)
    ax.set_ylim(0, 100)
    ax.set_ylabel('Temperature (°F)')
    ax.set_title('Current Temperature in NYC')
    st.pyplot(fig)
else:
    # Display an error message 
    st.write("Error: Temperature data not found")
