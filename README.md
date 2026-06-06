# 🐦 Bird Species Observation Analysis

Analysis of bird species across Forest and Grassland habitats in US National Parks.

## Project Structure
```
bird-species-analysis/
├── data/                        ← Place your Excel files here
│   ├── Bird_Monitoring_Data_FOREST.XLSX
│   └── Bird_Monitoring_Data_GRASSLAND.XLSX
├── src/
│   ├── data_cleaning.py         ← Step 1: Clean & merge data
│   └── eda_analysis.py          ← Step 2: Generate EDA charts
├── dashboard/
│   └── app.py                   ← Step 3: Streamlit dashboard
├── outputs/                     ← Auto-generated charts saved here
├── requirements.txt
└── README.md
```

## Setup & Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run data cleaning first
python src/data_cleaning.py

# 4. Run EDA (saves charts to outputs/)
python src/eda_analysis.py

# 5. Launch interactive dashboard
streamlit run dashboard/app.py
```

## Key Features
- **10 EDA charts** saved automatically to `outputs/`
- **Interactive Streamlit dashboard** with sidebar filters
- Covers: Species diversity, temporal trends, environmental correlations, conservation insights
