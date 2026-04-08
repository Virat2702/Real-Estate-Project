# app.py
import streamlit as st

st.set_page_config(
    page_title="Gurgaon Real Estate",
    page_icon="🏢",
    layout="wide"
)

st.title("Gurgaon Real Estate Analytics Portal 🏢")
st.write("Welcome to our Analytics Webpage! Use the sidebar on the left to navigate through our 4 modules.")

st.markdown("""
### Modules:
1. **🔮 Prediction:** Get an AI-driven price estimate for any property in Gurgaon using our model.
2. **📊 Analysis:** Explore market trends, sector comparisons, and property distributions.
3. **🏘️ Recommendation:** Find similar properties based on your specific taste.
""")