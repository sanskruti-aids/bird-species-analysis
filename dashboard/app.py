"""
Bird Species Analysis — Interactive Streamlit Dashboard
Run with: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🐦 Bird Species Analysis",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    /* Hide default Streamlit Menu and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Reduce top padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* Style Metric Cards with a glassmorphism/modern look */
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease-in-out;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Make headers pop */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    
    /* Improve Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    import sqlite3
    conn = sqlite3.connect('data/bird_data.db')
    df = pd.read_sql_query("SELECT * FROM bird_observations", conn)
    conn.close()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
    df['Humidity'] = pd.to_numeric(df['Humidity'], errors='coerce')
    return df

df = load_data()

# ─────────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────────
st.sidebar.markdown("## 🎛️ Control Panel")
st.sidebar.caption("Fine-tune the data visualizations below.")
st.sidebar.divider()

st.sidebar.markdown("### 🌍 Location")
habitat_options = ['All'] + sorted(df['Location_Type'].dropna().unique().tolist())
selected_habitat = st.sidebar.selectbox("Habitat Type", habitat_options)

admin_options = ['All'] + sorted(df['Admin_Unit_Code'].dropna().unique().tolist())
selected_admin = st.sidebar.selectbox("Admin Unit", admin_options)

st.sidebar.divider()
st.sidebar.markdown("### 🕒 Timeframe")

year_min, year_max = int(df['Year'].min()), int(df['Year'].max())
if year_min == year_max:
    st.sidebar.markdown(f"**Year:** {year_min}")
    selected_years = (year_min, year_max)
else:
    selected_years = st.sidebar.slider("Year Range", year_min, year_max, (year_min, year_max))

season_options = ['All', 'Spring', 'Summer', 'Fall', 'Winter']
selected_season = st.sidebar.selectbox("Season", season_options)

# Apply filters
filtered = df.copy()
if selected_habitat != 'All':
    filtered = filtered[filtered['Location_Type'] == selected_habitat]
if selected_admin != 'All':
    filtered = filtered[filtered['Admin_Unit_Code'] == selected_admin]
filtered = filtered[filtered['Year'].between(selected_years[0], selected_years[1])]
if selected_season != 'All':
    filtered = filtered[filtered['Season'] == selected_season]

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.image("dashboard/banner.png", use_container_width=True)
st.markdown("<h1 style='text-align: center;'>🐦 Bird Species Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em;'>A comprehensive look into bird biodiversity across <b>Forest</b> and <b>Grassland</b> habitats in US National Parks.</p>", unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────────
# KPI Cards
# ─────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📋 Total Observations", f"{len(filtered):,}")
col2.metric("🦅 Unique Species", f"{filtered['Common_Name'].nunique():,}")
col3.metric("📍 Admin Units", f"{filtered['Admin_Unit_Code'].nunique()}")
col4.metric("⚠️ At-Risk Species", str(filtered[filtered['PIF_Watchlist_Status'] == True]['Common_Name'].nunique()))
col5.metric("🌡️ Avg Temp (°C)", f"{filtered['Temperature'].mean():.1f}" if not filtered['Temperature'].isna().all() else "N/A")

st.divider()

# ─────────────────────────────────────────────
# TAB LAYOUT
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🌿 Species Overview",
    "📅 Temporal Analysis",
    "🌤️ Environmental Factors",
    "📍 Spatial Analysis",
    "⚠️ Conservation",
    "📏 Distance & Behavior",
    "👁️ Observer Trends"
])

# ══════════════════════════
# TAB 1: SPECIES OVERVIEW
# ══════════════════════════
with tab1:
    st.subheader("Species Distribution")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Top 15 Most Observed Species**")
        top15 = filtered['Common_Name'].value_counts().head(15).reset_index()
        top15.columns = ['Species', 'Count']
        fig = px.bar(top15, x='Count', y='Species', orientation='h',
                     color='Count', color_continuous_scale='Blues',
                     title='Top 15 Bird Species by Observations')
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("**Species Diversity by Habitat**")
        div = filtered.groupby('Location_Type')['Common_Name'].nunique().reset_index()
        div.columns = ['Habitat', 'Unique Species']
        fig2 = px.pie(div, values='Unique Species', names='Habitat',
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      title='Species Diversity Share by Habitat')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Identification Method Breakdown**")
    id_method = filtered['ID_Method'].value_counts().reset_index()
    id_method.columns = ['Method', 'Count']
    fig3 = px.bar(id_method, x='Method', y='Count',
                  color='Method', title='Bird ID Methods Used',
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**Sex Distribution by Habitat**")
    sex_data = filtered.groupby(['Location_Type','Sex']).size().reset_index(name='Count')
    fig4 = px.bar(sex_data, x='Location_Type', y='Count', color='Sex',
                  barmode='group', title='Sex Ratio by Habitat',
                  color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════
# TAB 2: TEMPORAL ANALYSIS
# ══════════════════════════
with tab2:
    st.subheader("Temporal Patterns")

    monthly = filtered.groupby(['Month','Location_Type']).size().reset_index(name='Count')
    month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                   7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    monthly['Month_Name'] = monthly['Month'].map(month_names)

    fig5 = px.line(monthly, x='Month', y='Count', color='Location_Type',
                   markers=True, title='Monthly Observations by Habitat',
                   labels={'Month':'Month','Count':'Observations'})
    fig5.update_xaxes(tickvals=list(range(1,13)),
                      ticktext=[month_names[m] for m in range(1,13)])
    st.plotly_chart(fig5, use_container_width=True)

    yearly = filtered.groupby(['Year','Location_Type']).size().reset_index(name='Count')
    yearly = yearly.dropna(subset=['Year'])
    fig6 = px.line(yearly, x='Year', y='Count', color='Location_Type',
                   markers=True, title='Yearly Observation Trend',
                   labels={'Year':'Year','Count':'Observations'})
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("**Seasonal Heatmap (Year × Season)**")
    season_year = filtered.groupby(['Year','Season']).size().reset_index(name='Count')
    season_pivot = season_year.pivot(index='Season', columns='Year', values='Count').fillna(0)
    fig7 = px.imshow(season_pivot, aspect='auto',
                     color_continuous_scale='YlOrRd',
                     title='Heatmap: Observations by Season & Year')
    st.plotly_chart(fig7, use_container_width=True)


# ══════════════════════════════
# TAB 3: ENVIRONMENTAL FACTORS
# ══════════════════════════════
with tab3:
    st.subheader("Weather & Environmental Conditions")

    col_e1, col_e2 = st.columns(2)

    with col_e1:
        temp_bins = filtered.groupby(pd.cut(filtered['Temperature'], bins=10)).size().reset_index(name='Count')
        temp_bins['Temp Range'] = temp_bins['Temperature'].astype(str)
        fig8 = px.bar(temp_bins, x='Temp Range', y='Count',
                      title='Observations by Temperature Range',
                      color='Count', color_continuous_scale='RdYlBu_r')
        fig8.update_xaxes(tickangle=45)
        st.plotly_chart(fig8, use_container_width=True)

    with col_e2:
        hum_bins = filtered.groupby(pd.cut(filtered['Humidity'], bins=10)).size().reset_index(name='Count')
        hum_bins['Humidity Range'] = hum_bins['Humidity'].astype(str)
        fig9 = px.bar(hum_bins, x='Humidity Range', y='Count',
                      title='Observations by Humidity Range',
                      color='Count', color_continuous_scale='Blues')
        fig9.update_xaxes(tickangle=45)
        st.plotly_chart(fig9, use_container_width=True)

    st.markdown("**Sky Conditions Impact**")
    sky = filtered.groupby(['Sky','Location_Type']).size().reset_index(name='Count')
    fig10 = px.bar(sky, x='Sky', y='Count', color='Location_Type',
                   barmode='group', title='Observations by Sky Condition',
                   color_discrete_sequence=px.colors.qualitative.Set2)
    fig10.update_xaxes(tickangle=30)
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown("**Wind Conditions Impact**")
    wind = filtered.groupby('Wind').size().reset_index(name='Count').sort_values('Count', ascending=False)
    fig11 = px.bar(wind, x='Count', y='Wind', orientation='h',
                   title='Observations by Wind Condition',
                   color='Count', color_continuous_scale='Greens')
    st.plotly_chart(fig11, use_container_width=True)

    st.markdown("**Disturbance Effect**")
    dist = filtered.groupby('Disturbance').size().reset_index(name='Count').sort_values('Count', ascending=False)
    fig12 = px.bar(dist, x='Disturbance', y='Count',
                   title='Effect of Disturbance on Bird Observations',
                   color='Count', color_continuous_scale='Oranges')
    fig12.update_xaxes(tickangle=20)
    st.plotly_chart(fig12, use_container_width=True)


# ══════════════════════════
# TAB 4: SPATIAL ANALYSIS
# ══════════════════════════
with tab4:
    st.subheader("Spatial & Administrative Analysis")

    richness = filtered.groupby(['Admin_Unit_Code','Location_Type'])['Common_Name'].nunique().reset_index()
    richness.columns = ['Admin Unit', 'Habitat', 'Unique Species']

    fig13 = px.bar(richness, x='Admin Unit', y='Unique Species', color='Habitat',
                   barmode='group', title='Species Richness by Admin Unit & Habitat',
                   color_discrete_sequence=['#4C72B0','#55A868'])
    st.plotly_chart(fig13, use_container_width=True)

    heat_data = richness.pivot(index='Admin Unit', columns='Habitat', values='Unique Species').fillna(0)
    fig14 = px.imshow(heat_data, text_auto=True, aspect='auto',
                      color_continuous_scale='YlGnBu',
                      title='Heatmap: Species Richness per Admin Unit')
    st.plotly_chart(fig14, use_container_width=True)

    st.markdown("**Top Plots by Observation Count**")
    plot_count = filtered.groupby('Plot_Name').size().reset_index(name='Count').sort_values('Count', ascending=False).head(20)
    fig15 = px.bar(plot_count, x='Plot_Name', y='Count',
                   title='Top 20 Observation Plots',
                   color='Count', color_continuous_scale='Viridis')
    fig15.update_xaxes(tickangle=45)
    st.plotly_chart(fig15, use_container_width=True)


# ══════════════════════════
# TAB 5: CONSERVATION
# ══════════════════════════
with tab5:
    st.subheader("⚠️ Conservation & Watchlist Insights")

    at_risk = filtered[filtered['PIF_Watchlist_Status'] == True]

    col_c1, col_c2 = st.columns(2)
    col_c1.metric("At-Risk Species Count", at_risk['Common_Name'].nunique())
    col_c2.metric("At-Risk Observations", len(at_risk))

    st.markdown("**Top At-Risk Species by Observation Count**")
    top_risk = at_risk['Common_Name'].value_counts().head(15).reset_index()
    top_risk.columns = ['Species', 'Count']
    fig16 = px.bar(top_risk, x='Count', y='Species', orientation='h',
                   title='Most Frequently Observed At-Risk Species',
                   color='Count', color_continuous_scale='Reds')
    fig16.update_layout(yaxis={'categoryorder':'total ascending'}, height=450)
    st.plotly_chart(fig16, use_container_width=True)

    st.markdown("**At-Risk Species by Habitat**")
    risk_hab = at_risk.groupby(['Location_Type'])['Common_Name'].nunique().reset_index()
    risk_hab.columns = ['Habitat', 'At-Risk Species']
    fig17 = px.pie(risk_hab, values='At-Risk Species', names='Habitat',
                   title='At-Risk Species Distribution by Habitat',
                   color_discrete_sequence=['#d9534f','#f0ad4e'])
    st.plotly_chart(fig17, use_container_width=True)

    st.markdown("**Regional Stewardship Priority Species**")
    steward = filtered[filtered['Regional_Stewardship_Status'] == True]
    top_stew = steward['Common_Name'].value_counts().head(15).reset_index()
    top_stew.columns = ['Species', 'Count']
    fig18 = px.bar(top_stew, x='Count', y='Species', orientation='h',
                   title='Top Regionally Priority Species',
                   color='Count', color_continuous_scale='Oranges')
    fig18.update_layout(yaxis={'categoryorder':'total ascending'}, height=450)
    st.plotly_chart(fig18, use_container_width=True)

    st.markdown("**Full At-Risk Species Table**")
    risk_table = at_risk[['Common_Name','Scientific_Name','Location_Type',
                           'Admin_Unit_Code','AOU_Code']].drop_duplicates()
    st.dataframe(risk_table.sort_values('Common_Name'), use_container_width=True)

# ══════════════════════════
# TAB 6: DISTANCE & BEHAVIOR
# ══════════════════════════
with tab6:
    st.subheader("📏 Distance and Behavior Analysis")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        if 'Distance' in filtered.columns:
            st.markdown("**Observation Distance Breakdown**")
            dist_counts = filtered['Distance'].value_counts().reset_index()
            dist_counts.columns = ['Distance', 'Count']
            fig_d1 = px.pie(dist_counts, values='Count', names='Distance',
                            title='Proportion of Observations by Distance',
                            color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_d1, use_container_width=True)
            
    with col_d2:
        if 'Flyover_Observed' in filtered.columns:
            st.markdown("**Flyover Frequency**")
            fly_counts = filtered['Flyover_Observed'].value_counts().reset_index()
            fly_counts.columns = ['Flyover', 'Count']
            fly_counts['Flyover'] = fly_counts['Flyover'].astype(str)
            fig_d2 = px.bar(fly_counts, x='Flyover', y='Count',
                            title='Flyover Observations (True vs False)',
                            color='Count', color_continuous_scale='Blues')
            st.plotly_chart(fig_d2, use_container_width=True)

# ══════════════════════════
# TAB 7: OBSERVER TRENDS
# ══════════════════════════
with tab7:
    st.subheader("👁️ Observer Trends & Insights")
    
    col_o1, col_o2 = st.columns(2)
    
    with col_o1:
        if 'Observer' in filtered.columns:
            st.markdown("**Top Observers by Count**")
            obs_counts = filtered['Observer'].value_counts().head(15).reset_index()
            obs_counts.columns = ['Observer', 'Count']
            fig_o1 = px.bar(obs_counts, x='Count', y='Observer', orientation='h',
                            title='Top 15 Most Active Observers',
                            color='Count', color_continuous_scale='Greens')
            fig_o1.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_o1, use_container_width=True)
            
    with col_o2:
        if 'Visit' in filtered.columns:
            st.markdown("**Observation Counts by Visit Number**")
            visit_counts = filtered['Visit'].value_counts().reset_index()
            visit_counts.columns = ['Visit', 'Count']
            fig_o2 = px.bar(visit_counts, x='Visit', y='Count',
                            title='Observations across Different Visits',
                            color='Count', color_continuous_scale='Purples')
            st.plotly_chart(fig_o2, use_container_width=True)

# Footer
st.markdown("---")
st.caption("🐦 Bird Species Observation Analysis | Data: National Park Service Bird Monitoring")
