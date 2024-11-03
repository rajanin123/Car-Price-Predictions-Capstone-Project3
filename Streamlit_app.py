# STREAMLIT APP DEPLOYMENT
# Import Libraries
import streamlit as st
import numpy as np
import pickle
import joblib
from PIL import Image

# Load and resize the car image
car_image = Image.open("C:/Users/Rajan/Desktop/New folder/car_image1.jpg")  # Update path of image
car_image = car_image.resize((500, 350))  # Resize the image

# Load the trained model
model = joblib.load('random_forest_model.pkl')  # Ensure this file path is correct

# SIde bar layout configuration with color

st.markdown(
    """
    <style>
    /* Change sidebar background color to orange */
    [data-testid="stSidebar"] > div:first-child {
        background-color: #FFA500;  /* Orange color */
    }

    /* Reduce image size and center it */
    .car-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;  /* Adjust the width of the image */
    }

    /* Align buttons and text bold */
    button {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Car Price Prediction")

# Display the resized car image
st.image(car_image, use_column_width=False)

# Sidebar for user inputs 
st.sidebar.title("Select Car Features")

# Get user inputs for car features
fuel_type = st.sidebar.selectbox("**Fuel Type**", options=["Petrol", "Diesel", "CNG", "Electric", "LPG"])
km_driven = st.sidebar.number_input("**Km Driven**", min_value=5000, max_value=200000, value=12000, step=1000)
transmission = st.sidebar.selectbox("**Transmission**", options=["Manual", "Automatic"])
model_year = st.sidebar.selectbox("**Model Year**", options=list(range(2000, 2025)))
mileage_kmpl = st.sidebar.number_input("**Mileage (kmpl)**", min_value=0.0, max_value=50.0, step=1.0, value=15.0)
engine_cc = st.sidebar.number_input("**Engine CC**", min_value=500, max_value=5000, step=1, value=1500)
max_power_bhp = st.sidebar.number_input("**Max Power (bhp)**", min_value=50, max_value=500, step=1, value=100)
city = st.sidebar.selectbox("**City**", options=["Chennai", "Jaipur", "Delhi", "Hyderabad", "Kolkata", "Bangalore"])

# Map categorical features to numeric values
fuel_mapping = {"Petrol": 0, "Diesel": 1, "CNG": 2, "Electric": 3, 'LPG': 4}
transmission_mapping = {"Manual": 0, "Automatic": 1}
city_mapping = {"Chennai": 0, "Jaipur": 1, "Delhi": 2, "Hyderabad": 3, "Kolkata": 4, 'Bangalore': 5}
fuel_type_encoded = fuel_mapping[fuel_type]
transmission_encoded = transmission_mapping[transmission]
city_encoded = city_mapping[city]

# Normalize the numeric inputs 
km_driven_norm = (km_driven - 50000) / 150000
mileage_kmpl_norm = (mileage_kmpl - 15.0) / 15.0
engine_cc_norm = (engine_cc - 1500) / 3500
max_power_bhp_norm = (max_power_bhp - 100) / 300

# Create an array for prediction
input_features = np.array([[fuel_type_encoded, km_driven_norm, transmission_encoded, model_year, mileage_kmpl_norm, engine_cc_norm, max_power_bhp_norm, city_encoded]])


# Make predictions button
if st.button('**Predict Car Price**'):
    predicted_price = model.predict(input_features)
    st.markdown(f"### *The estimated car price is: ₹ {predicted_price[0]:,.2f}*")