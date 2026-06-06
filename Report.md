# Bird Species Observation Analysis - Project Report

## 1. Project Overview
This project aims to analyze the distribution and diversity of bird species in two distinct ecosystems: forests and grasslands across various US National Parks (Admin Units). By examining bird observation data, the project uncovers patterns of habitat preference, the influence of environmental conditions, and highlights conservation priorities.

## 2. Approach & Methodology
The project followed a structured, data-driven approach:
- **Data Cleaning and Preprocessing:** Handled missing data, converted dates to proper formats, derived seasons, consolidated 11 forest and 11 grassland Excel sheets, unified mismatched columns, and stored the final dataset into an SQLite Database (`bird_data.db`) for efficient querying.
- **Exploratory Data Analysis (EDA):** Performed extensive analysis focusing on spatial distribution, temporal activity, species richness, and the effect of environmental factors.
- **Data Visualization:** Built an interactive dashboard using **Streamlit** and **Plotly** to visualize the findings dynamically.

## 3. Key Findings & Analyses Performed

### A. Species & Spatial Analysis
- **Finding:** Forest habitats exhibit distinct species dominance compared to grasslands. High observation counts often correlate with specific administrative units (e.g., CHOH, ROCR) which serve as biodiversity hotspots.
- **Visualization:** Bar charts and pie charts illustrate species distribution across habitats, while heatmaps indicate biodiversity hotspots per Admin Unit.

### B. Temporal Trends
- **Finding:** Bird observation frequency fluctuates heavily based on the season and month, with Spring and early Summer showing peak observation activity.
- **Visualization:** Monthly and yearly line charts, alongside seasonal heatmaps, clearly track activity peaks and migratory patterns.

### C. Environmental Impact
- **Finding:** The majority of observations occur within specific optimal temperature and humidity ranges. Extreme weather conditions drastically reduce the number of sightings.
- **Visualization:** Histograms and bar charts display the correlation between weather parameters (Temperature, Humidity, Wind, Sky) and observation volume.

### D. Distance and Behavior
- **Finding:** A significant portion of birds is identified via vocalizations rather than pure visual identification. Distances vary heavily by species and habitat density, and flyovers represent a notable portion of sightings.
- **Visualization:** Distance breakdown pie charts and flyover bar charts illustrate behavioral patterns during sightings in the dashboard.

### E. Observer Trends
- **Finding:** A handful of dedicated observers contribute to a large portion of the dataset. Repeated visits to the same plot help build a more complete picture of local species richness.
- **Visualization:** Horizontal bar charts show observer contribution, while visit charts track repeated observation counts.

### F. Conservation Insights
- **Finding:** Several species flagged on the PIF Watchlist and Regional Stewardship lists were identified. Protecting these specific forest and grassland zones is critical for these at-risk species.
- **Visualization:** Dedicated metrics and bar charts pinpoint at-risk species, aiding direct conservation targeting.

## 4. Actionable Business & Ecological Insights
1. **Targeted Conservation:** Focus habitat restoration and protection efforts in specific Admin Units that showed the highest concentration of PIF Watchlist species.
2. **Optimized Resource Allocation:** Schedule eco-tourism events and primary monitoring campaigns during identified peak seasons and optimal weather conditions to maximize success rates.
3. **Observer Training:** Utilize the ID method data to train future observers. Since many birds are identified by sound, prioritizing auditory birding skills will significantly improve data collection efficiency in dense habitats.
