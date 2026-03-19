import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from pathlib import Path


# ==========================================
# 1. PAGE CONFIGURATION & UI SETUP
# ==========================================
st.set_page_config(
    page_title="AMAC Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)
    


# Custom CSS for SaaS-like minimal styling
#st.markdown("""
 #   <style>
  #  .block-container { padding-top: 2rem; padding-bottom: 2rem; }
   # h1 { color: #1E3A8A; font-weight: 700; }
    #.stMetric { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; }
    #</style>
#""", unsafe_allow_html=True)
# Custom CSS for SaaS-like minimal styling
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* IMPROVEMENT 1: Removed the hardcoded '#1E3A8A' color. 
       Allowing Streamlit to use its native text colors ensures the title is 
       dark blue/black in light mode and white/light-grey in dark mode. */
    h1 { font-weight: 700; }
    
    /* IMPROVEMENT 2: Replaced the hardcoded '#F8FAFC' background with 
       'var(--secondary-background-color)'. This native variable automatically 
       switches between a light grey in Light Mode and a dark grey in Dark Mode. 
       Also changed the border to a semi-transparent grey so it works in both themes. */
    .stMetric { 
        background-color: var(--secondary-background-color); 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid rgba(128, 128, 128, 0.2); 
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LOADING & PREPROCESSING
# ==========================================
  

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "Data" / "cleaned" / "amac_rental_master_v2.csv"
df = pd.read_csv(DATA_PATH)

#file = "../Data/cleaned/amac_rental_master_v2.csv"
#df = pd.read_csv(file)
df = df.dropna(subset=['Bedrooms', 'District', 'Property Category', 'District Tier', 'Price(Float)'])

#df['Bedrooms'] = pd.to_numeric(df['Bedrooms'], errors='coerce')
df = df.dropna(subset=['Bedrooms']) 

# ==========================================
# 3. SIDEBAR: INTERACTIVE FILTERS
# ==========================================
st.sidebar.image("https://img.icons8.com/fluency/96/city-buildings.png", width=60) # Placeholder logo
st.sidebar.title("Filter Options")
st.sidebar.markdown("Refine the market data:")

# Dynamic Filter States
min_price = float(df['Price(Float)'].min())
max_price = float(df['Price(Float)'].max())

price_range = st.sidebar.slider(
    "Rent Price Range (₦)", 
    min_value=min_price, 
    max_value=max_price, 
    value=(min_price, max_price),
    step=500000.0,
    format="₦%d"
)

selected_bedrooms = st.sidebar.multiselect(
    "Bedrooms",
    options=sorted(df['Bedrooms'].unique()),
    default=sorted(df['Bedrooms'].unique())
)

selected_districts = st.sidebar.multiselect(
    "Districts",
    options=sorted(df['District'].unique()),
    default=sorted(df['District'].unique())
)

selected_categories = st.sidebar.multiselect(
    "Property Category",
    options=sorted(df['Property Category'].unique()),
    default=sorted(df['Property Category'].unique())
)

selected_tiers = st.sidebar.multiselect(
    "District Tier",
    options=sorted(df['District Tier'].unique()),
    default=sorted(df['District Tier'].unique())
)

# Apply Filters to Dataframe
filtered_df = df[
    (df['Price(Float)'] >= price_range[0]) &
    (df['Price(Float)'] <= price_range[1]) &
    (df['Bedrooms'].isin(selected_bedrooms)) &
    (df['District'].isin(selected_districts)) &
    (df['Property Category'].isin(selected_categories)) &
    (df['District Tier'].isin(selected_tiers))
]

# ==========================================
# 4. MAIN DASHBOARD AREA
# ==========================================
st.title("AMAC Rental Intelligence Dashboard")
st.markdown("A comprehensive analysis of the Abuja Municipal Area Council rental market.")
st.markdown("---")
st.markdown("Abuja rental prices can be all over the place." 
            "This dashboard pulls real listing data and breaks it down visually"
            "so you can see what different areas actually cost,"
            "compare property types, and know if a price is fair before you commit.")
st.markdown("---")

# Handle empty state if filters are too aggressive
if filtered_df.empty:
    st.warning("No listings found for the selected criteria. Please adjust your filters.")
    st.stop()

# --- KPI METRICS SECTION ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    avg_rent = filtered_df['Price(Float)'].mean()
    st.metric(label="Average Rent", value=f"₦{avg_rent:,.0f}")

with kpi2:
    med_rent = filtered_df['Price(Float)'].median()
    st.metric(label="Median Rent", value=f"₦{med_rent:,.0f}")

with kpi3:
    # Most expensive district based on median price
    top_district = filtered_df.groupby('District')['Price(Float)'].median().idxmax()
    #st.metric(label="Most Expensive District", value=top_district)
    st.metric(
    label="Most Expensive District", 
    value=top_district,
    help="We use the 'Median' (the middle price) instead of the 'Average.' "
         "This is more accurate because it isn't skewed by a few ultra-expensive "
         "mansions in places like Maitama. It represents what a typical renter should expect."
    )

with kpi4:
    st.metric(label="Total Listings Analyzed", value=f"{len(filtered_df):,}")

st.markdown("---")

# --- VISUALIZATION GRID ---

# Row 1: Distribution & Bedrooms
col1, col2 = st.columns(2)

with col1:
    st.subheader("Rental Price Distribution")
    fig_dist = px.histogram(
        filtered_df, x="Price(Float)", nbins=50, 
        marginal="box", color_discrete_sequence=['#3B82F6'],
        labels={"Price(Float)": "Annual Rent (₦)"}
    )
    fig_dist.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_dist, use_container_width=True)

with col2:
    st.subheader("Price Variance by Bedroom Count")
    fig_box = px.box(
        filtered_df, x="Bedrooms", y="Price(Float)", 
        color="Bedrooms",
        labels={"Price(Float)": "Annual Rent (₦)", "Bedrooms": "No. of Bedrooms"}
    )
    fig_box.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_box, use_container_width=True)


# Row 2: District Analysis
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Average Rent per District")
    district_avg = filtered_df.groupby('District')['Price(Float)'].mean().reset_index()
    district_avg = district_avg.sort_values('Price(Float)', ascending=True)
    fig_dist_bar = px.bar(
        district_avg, x="Price(Float)", y="District", orientation='h',
        color="Price(Float)", color_continuous_scale="Blues",
        labels={"Price(Float)": "Average Rent (₦)"}
    )
    fig_dist_bar.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_dist_bar, use_container_width=True)

with col4:
    st.subheader("Market Segmentation by Tier")
    tier_avg = filtered_df.groupby('District Tier')['Price(Float)'].mean().reset_index()
    fig_tier = px.bar(
        tier_avg, x="District Tier", y="Price(Float)",
        color="District Tier", color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={"Price(Float)": "Average Rent (₦)"}
    )
    fig_tier.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_tier, use_container_width=True)


# Row 3: Market Composition
st.markdown("---")
col5, col6 = st.columns(2)

with col5:
    st.subheader("Property Category Market Share")
    cat_counts = filtered_df['Property Category'].value_counts().reset_index()
    cat_counts.columns = ['Property Category', 'Count']
    fig_pie = px.pie(
        cat_counts, names="Property Category", values="Count",
        hole=0.4, color_discrete_sequence=px.colors.sequential.Teal
    )
    fig_pie.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with col6:
    st.subheader("Listings Volume by Source")
    source_counts = filtered_df['Source'].value_counts().reset_index()
    source_counts.columns = ['Source', 'Listings Count']
    fig_source = px.bar(
        source_counts, x="Source", y="Listings Count",
        color="Source", color_discrete_sequence=['#10B981', '#6366F1'],
        text_auto=True
    )
    fig_source.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_source, use_container_width=True)

# Footer
st.markdown("""
    <div style='text-align: center; color: #64748B; padding-top: 2rem;'>
        AMAC Rental Intelligence Dashboard | Designed for Real Estate Market Analysis
    </div>
""", unsafe_allow_html=True)
