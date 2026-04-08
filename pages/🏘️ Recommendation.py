import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page Config
st.set_page_config(page_title='Property Recommender', layout='wide')

# 1. Load Data with Caching
@st.cache_resource
def load_data():
    # Load the distance matrix
    location_df = pickle.load(open('location_distance.pkl', 'rb'))
    # Load the three similarity matrices
    cs1 = pickle.load(open('cosine_sim1.pkl', 'rb')) 
    cs2 = pickle.load(open('cosine_sim2.pkl', 'rb')) 
    cs3 = pickle.load(open('cosine_sim3.pkl', 'rb')) 
    return location_df, cs1, cs2, cs3

location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_data()

# 2. Recommendation Function
def recommend_properties_with_scores(property_name, top_n=5):
    # Hybrid Weights: 50% Amenities, 30% Price/Area, 20% Keywords
    cosine_sim_matrix = (0.5 * cosine_sim1) + (0.3 * cosine_sim2) + (0.2 * cosine_sim3)
    
    try:
        # Get index of the selected property
        idx = location_df.index.get_loc(property_name)
        sim_scores = list(enumerate(cosine_sim_matrix[idx]))
        
        # Sort by similarity score
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Take top_n (excluding itself)
        top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
        top_scores = [round(float(i[1]), 2) for i in sorted_scores[1:top_n+1]]
        
        # Get names
        top_properties = location_df.index[top_indices].tolist()
        
        return pd.DataFrame({
            'Property Name': top_properties,
            'Match Score': top_scores
        })
    except Exception as e:
        st.error(f"Error finding recommendations: {e}")
        return pd.DataFrame()

# --- MAIN UI ---

st.title('Smart Property Recommender 🏡')
st.markdown("Find properties nearby and discover similar options based on your preferences.")

# SECTION 1: SEARCH FILTERS (On Main Page)
st.write("---")
st.subheader('🔍 Step 1: Search by Location & Radius')

col_search1, col_search2 = st.columns(2)

with col_search1:
    selected_location = st.selectbox(
        'Select Center Point (Landmark/Park)', 
        sorted(location_df.columns.to_list())
    )

with col_search2:
    radius = st.number_input(
        'Radius in Kms', 
        min_value=1.0, 
        max_value=100.0, 
        value=5.0,
        step=0.5
    )

# LOGIC: Filter based on Radius
distance_threshold = radius * 1000
result_ser = location_df[location_df[selected_location] < distance_threshold][selected_location].sort_values()
nearby_apartments = result_ser.index.tolist()

# SECTION 2: SELECTION & RECOMMENDATION
st.write("---")
col_select, col_rec = st.columns([1, 2])

with col_select:
    st.subheader("Step 2: Pick a Property")
    
    if not nearby_apartments:
        st.warning("No apartments found in this radius. Showing all instead.")
        nearby_apartments = sorted(location_df.index.to_list())
    
    selected_apartment = st.selectbox(
        'Select a property to see matches', 
        nearby_apartments
    )
    
    # Show distance if it was part of the search
    if selected_apartment in result_ser:
        dist_km = round(result_ser[selected_apartment] / 1000, 2)
        st.info(f"📍 Distance: **{dist_km} km** from {selected_location}")

with col_rec:
    st.subheader("Step 3: Get Recommendations")
    
    if st.button('Find Similar Properties', use_container_width=True):
        with st.spinner('Calculating Similarity Scores...'):
            recommendation_df = recommend_properties_with_scores(selected_apartment)
            
            if not recommendation_df.empty:
                st.write(f"Top 5 matches similar to **{selected_apartment}**:")
                
                # Display Table
                st.dataframe(recommendation_df, use_container_width=True)
                
                # Display Visual Chart
                chart_data = recommendation_df.set_index('Property Name')
                st.bar_chart(chart_data)
            else:
                st.error("Could not find similarities for this property.")

st.write("---")