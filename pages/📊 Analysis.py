import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title='Gurgaon Real Estate Analytics', layout='wide')

# --- 1. DATA LOADING (WITH CACHING) ---
@st.cache_data
def load_data():
    # Update this path to your actual dataset location
    df = pd.read_csv(r'D:\major project\datasets\data_viz1.csv')
    
    # Load feature text for the wordcloud
    with open('feature_text.pkl', 'rb') as f:
        feature_text = pickle.load(f)
        
    # Pre-calculate sector-wise averages for the map
    group_df = df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()
    
    return df, feature_text, group_df

# Load the data once
try:
    new_df, feature_text, group_df = load_data()
except Exception as e:
    st.error(f"Error loading files. Please check your file paths. Error: {e}")
    st.stop()

# --- 2. HEADER & KPI METRICS ---
st.title('Gurgaon Real Estate Analytics Dashboard 📊')
st.markdown("An interactive exploration of price trends, geographic distribution, and property features across Gurgaon.")

# Top-level KPI Cards
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Listings", f"{len(new_df):,}")
m2.metric("Avg. Price", f"₹{new_df['price'].mean():.2f} Cr")
m3.metric("Avg. SqFt Price", f"₹{int(new_df['price_per_sqft'].mean()):,}")
m4.metric("Sectors Analyzed", len(new_df['sector'].unique()))

st.divider()

# --- 3. GEOSPATIAL ANALYSIS ---
st.header('📍 Geographic Price Hotspots')
st.info("The map shows average sector prices. Redder bubbles indicate higher price per sq.ft., while bubble size represents the average built-up area.")

fig_map = px.scatter_mapbox(
    group_df, 
    lat="latitude", 
    lon="longitude", 
    color="price_per_sqft", 
    size='built_up_area',
    color_continuous_scale='RdYlGn_r', # Red to Green
    zoom=10.5, # Zoomed in slightly more for better city view
    mapbox_style="open-street-map", # <--- THE FIX FOR THE WHITE BACKGROUND
    opacity=0.7, # <--- Lets you see the roads underneath the bubbles
    height=600, 
    hover_name=group_df.index,
    labels={'price_per_sqft': 'Price/SqFt'}
)

fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig_map, use_container_width=True)

# --- 4. FEATURE & DISTRIBUTION ANALYSIS ---
st.divider()
col1, col2 = st.columns([1, 1])

with col1:
    st.header('☁️ Most Common Features')
    # Generate WordCloud
    wc = WordCloud(width=800, height=800, 
                   background_color='white', 
                   colormap='magma',
                   stopwords=set(['s']), 
                   min_font_size=10).generate(feature_text)
    
    fig_wc, ax_wc = plt.subplots(figsize=(8, 8))
    ax_wc.imshow(wc, interpolation='bilinear')
    ax_wc.axis("off")
    st.pyplot(fig_wc)

with col2:
    st.header('⚖️ Price Distribution by Type')
    fig_dist, ax_dist = plt.subplots(figsize=(10, 8.2))
    sns.histplot(data=new_df, x='price', hue='property_type', kde=True, element="step", ax=ax_dist)
    ax_dist.set_title("Density of Property Prices (Cr)")
    ax_dist.set_xlabel("Price in Crores")
    st.pyplot(fig_dist)

# --- 5. INTERACTIVE DRILL-DOWN SECTION ---
st.divider()
st.header('🔍 Detailed Drill-Down')

# Using Tabs to organize the deep-dive analysis
tab1, tab2 = st.tabs(["Area vs Price Scatter", "BHK & Sector Analysis"])

with tab1:
    st.subheader("Correlation between Size and Cost")
    selected_type = st.radio("Property Category:", ["flat", "house"], horizontal=True)
    
    fig_scatter = px.scatter(
        new_df[new_df['property_type'] == selected_type], 
        x='built_up_area', 
        y='price', 
        color='bedRoom',
        size='price_per_sqft', # Third dimension
        hover_data=['sector'],
        labels={'built_up_area': 'Built-up Area (Sq.Ft)', 'price': 'Price (Cr)'},
        color_continuous_scale='Viridis',
        template='plotly_white'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("BHK Inventory Mix")
        sector_list = ['overall'] + sorted(new_df['sector'].unique().tolist())
        sel_sector = st.selectbox('Filter by Sector:', sector_list)
        
        # Dynamic filtering for the Pie Chart
        plot_df = new_df if sel_sector == 'overall' else new_df[new_df['sector'] == sel_sector]
        
        fig_pie = px.pie(
            plot_df, 
            names='bedRoom', 
            hole=0.4, # Donut style
            title=f"BHK Distribution in {sel_sector.capitalize()}"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_b:
        st.subheader("Price Variability per BHK")
        # Focusing on common BHK sizes for a cleaner Box Plot
        fig_box = px.box(
            new_df[new_df['bedRoom'] <= 5], 
            x='bedRoom', 
            y='price', 
            color='bedRoom',
            labels={'bedRoom': 'Number of Bedrooms', 'price': 'Price (Cr)'},
            title="Price Outliers and Ranges"
        )
        st.plotly_chart(fig_box, use_container_width=True)

st.divider()