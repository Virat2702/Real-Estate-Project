import streamlit as st
import pickle
import numpy as np
import pandas as pd

# 1. Page Config
st.set_page_config(page_title='Price Prediction', page_icon='🔮', layout='wide')

# 2. CACHING (The secret to speed!)
@st.cache_data
def load_dataframe():
    with open('df.pkl', 'rb') as file:
        return pickle.load(file)

@st.cache_resource
def load_pipeline():
    with open('pipeline.pkl', 'rb') as file:
        return pickle.load(file)

try:
    df = load_dataframe()
    pipeline = load_pipeline()
except FileNotFoundError:
    st.error("Error: Could not find df.pkl or pipeline.pkl. Please ensure they are in the same folder.")
    st.stop()

# --- MAIN UI ---
st.title('🔮 Predict Property Price in Gurgaon')
st.markdown("Enter the property details below to get an estimated market value.")
st.write("---")

# 3. LAYOUT (Using Columns for a clean Dashboard look)
st.subheader("1. Core Property Details")
col1, col2, col3 = st.columns(3)

with col1:
    property_type = st.selectbox('Property Type', ['flat', 'house'])
    sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

with col2:
    # Added min, max, and a default value for area
    built_up_area = st.number_input('Built Up Area (Sq.Ft)', min_value=100.0, max_value=20000.0, value=1500.0, step=50.0)
    property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

with col3:
    floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

st.write("---")

st.subheader("2. Room Configuration")
col4, col5, col6 = st.columns(3)

with col4:
    bedrooms = st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist()))
with col5:
    bathroom = st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist()))
with col6:
    balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))

st.write("---")

st.subheader("3. Additional Amenities")
col7, col8, col9, col10 = st.columns(4)

with col7:
    furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
with col8:
    luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
with col9:
    servant_room = st.selectbox('Servant Room', [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
with col10:
    store_room = st.selectbox('Store Room', [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

st.write("---")

# 4. PREDICTION BUTTON & OUTPUT
if st.button('Predict Price', type='primary', use_container_width=True):
    with st.spinner('Calculating market value...'):
        
        # Form a dataframe exactly matching the training data columns
        data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 'built_up_area', 'servant room', 'store room', 'furnishing_type', 'luxury_category', 'floor_category']
        
        one_df = pd.DataFrame(data, columns=columns)
        
        # Predict and inverse log transform
        base_price = np.expm1(pipeline.predict(one_df))[0]
        
        # Calculate range and prevent negative lower bounds
        low = max(0.01, base_price - 0.24) 
        high = base_price + 0.24
        
        # Display the result beautifully
        st.success("Analysis Complete!")
        st.metric(label="Estimated Price Range", value=f"₹ {round(low, 2)} Cr  —  ₹ {round(high, 2)} Cr")
        st.caption("Note: This estimate is based on the current market model with a standard error margin of ± 24 Lakhs.")