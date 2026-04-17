# 🏙️ PropIntel: AI-Based Real Estate Multi-Service Hub (Gurgaon)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-orange)
![Streamlit](https://img.shields.io/badge/Deployment-Streamlit-red)
![AWS](https://img.shields.io/badge/Cloud-AWS%20EC2-yellow)

##  Overview
The **Real Estate Multi-Service Hub** is an end-to-end Machine Learning platform designed to bring transparency and data-driven intelligence to the highly volatile Gurgaon real estate market. 

This project encompasses the entire ML lifecycle: from scraping and deep-cleaning unstructured property listings, to engineering specialized features (like a custom *Luxury Score*), to training an optimized **Random Forest Regressor**, and finally deploying a 3-module interactive web application.

##  Key Features
The platform is divided into three core user-facing modules:
1. ** Price Predictor:** Enter property details (Sector, BHK, Area, Luxury Tier) to get an instant, AI-driven price estimate with ~90% accuracy.
2. ** Market Analysis:** Interactive dashboards featuring price-area scatter plots, sector-wise heatmaps, and property distribution charts.
3. ** Recommendation Engine:** A content-based filtering system using Cosine Similarity to suggest the top 5 most similar properties based on user taste and lifestyle requirements.

##  Tech Stack
* **Language:** Python
* **Data Processing & EDA:** Pandas, NumPy, YData Profiling
* **Machine Learning:** Scikit-Learn (Random Forest, Extra Trees, ColumnTransformer, RandomizedSearchCV)
* **Visualizations:** Plotly, Seaborn, Matplotlib, WordCloud
* **Web Deployment:** Streamlit
* **Cloud & DevOps:** AWS EC2, Docker

##  System Architecture & Pipeline
1. **Data Preprocessing:** Merged raw flats and houses data, standardized units (Lacs to Crores), handled missing values, and mapped 50+ messy neighborhood strings to official Sectors.
2. **Feature Engineering:** Extracted precise area metrics (Super Built-up vs. Carpet), clustered furnishing levels using K-Means, and calculated a weighted `luxury_score` based on property amenities.
3. **Outlier Treatment:** Removed anomalies using IQR and domain-specific logic (e.g., Area-to-Room ratios).
4. **Model Selection:** Benchmarked 11 algorithms (including XGBoost, LASSO, and SVR). Ensemble methods outperformed linear models due to the non-linear nature of real estate pricing.
5. **Hyperparameter Tuning:** Optimized the **Random Forest Regressor** using `RandomizedSearchCV` (n_estimators=300, max_depth=20).
6. **Deployment:** Exported the entire preprocessing and modeling pipeline as a `.pkl` file and integrated it into a Streamlit Multi-Page application deployed on AWS.

##  Model Performance
* **Algorithm:** Random Forest Regressor
* **R-Squared ($R^2$):** `0.9005` (Explains 90% of the price variance in the market)
* **Mean Absolute Error (MAE):** `0.45` Crores (Highly accurate given the market range of ₹50 Lacs to ₹30+ Crores)

##  How to Run Locally

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/propintel-gurgaon.git](https://github.com/your-username/propintel-gurgaon.git)
cd propintel-gurgaon
