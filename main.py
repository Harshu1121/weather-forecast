import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, selectbox and subheader
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
unit = st.selectbox("Temperature Unit", ("Celsius", "Fahrenheit"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    # Get temperature/sky data
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] / 10 for dict in filtered_data]
            if unit == "Fahrenheit":
                temperatures = [temp * 9/5 + 32 for temp in temperatures]
            dates = [dict["dt_txt"] for dict in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": f"Temperature ({unit})"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png", "Rain": "images/rain.png",
                      "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            dates = [dict["dt_txt"] for dict in filtered_data]
            st.write("Image"+"\t\t"+"Date"+"\t\t\t"+"Time")
            for i in range(len(image_paths)):
                st.write("")
                st.image(image_paths[i], width=50)
                st.write("\t\t"+dates[i].split(" ")[0]+"\t\t\t"+dates[i].split(" ")[1])
    except KeyError:
        st.write("That place does not exists...")
