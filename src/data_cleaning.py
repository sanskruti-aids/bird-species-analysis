"""
Bird Species Analysis - Data Cleaning & Preprocessing
Run this FIRST before any other script.
"""

import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────────
# CONFIG — update paths to your Excel files
# ─────────────────────────────────────────────
FOREST_FILE    = "data/Bird_Monitoring_Data_FOREST.XLSX"
GRASSLAND_FILE = "data/Bird_Monitoring_Data_GRASSLAND.XLSX"
OUTPUT_FILE    = "data/bird_data_clean.csv"

FOREST_SHEETS    = ['ANTI','CATO','CHOH','GWMP','HAFE','MANA','MONO','NACE','PRWI','ROCR','WOTR']
GRASSLAND_SHEETS = ['ANTI','CATO','CHOH','GWMP','HAFE','MANA','MONO','NACE','PRWI','ROCR','WOTR']

# ─────────────────────────────────────────────
# STEP 1 — Load all sheets from both files
# ─────────────────────────────────────────────
def load_all_sheets(filepath, sheets):
    frames = []
    for sheet in sheets:
        try:
            df = pd.read_excel(filepath, sheet_name=sheet, engine='openpyxl')
            df['Source_Sheet'] = sheet
            frames.append(df)
        except Exception as e:
            print(f"  ⚠ Skipped sheet {sheet}: {e}")
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

print("📂 Loading Forest data...")
forest_df = load_all_sheets(FOREST_FILE, FOREST_SHEETS)
print(f"   Loaded {len(forest_df):,} rows from Forest")

print("📂 Loading Grassland data...")
grass_df = load_all_sheets(GRASSLAND_FILE, GRASSLAND_SHEETS)
print(f"   Loaded {len(grass_df):,} rows from Grassland")

# ─────────────────────────────────────────────
# STEP 2 — Align columns (Grassland has
#           'TaxonCode' instead of 'NPSTaxonCode',
#           and no 'Site_Name')
# ─────────────────────────────────────────────
if 'TaxonCode' in grass_df.columns and 'NPSTaxonCode' not in grass_df.columns:
    grass_df.rename(columns={'TaxonCode': 'NPSTaxonCode'}, inplace=True)

if 'Site_Name' not in grass_df.columns:
    grass_df['Site_Name'] = np.nan

if 'Previously_Obs' not in forest_df.columns:
    forest_df['Previously_Obs'] = np.nan

# ─────────────────────────────────────────────
# STEP 3 — Combine into one DataFrame
# ─────────────────────────────────────────────
df = pd.concat([forest_df, grass_df], ignore_index=True)
print(f"\n✅ Combined dataset: {len(df):,} rows, {df.shape[1]} columns")

# ─────────────────────────────────────────────
# STEP 4 — Clean column by column
# ─────────────────────────────────────────────

# 4a. Date → datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')
df['Year'] = df['Year'].fillna(df['Date'].dt.year)
df['Year'] = df['Year'].astype('Int64')

# 4b. Season derived from month
def get_season(m):
    if pd.isna(m): return 'Unknown'
    if m in [3,4,5]:  return 'Spring'
    if m in [6,7,8]:  return 'Summer'
    if m in [9,10,11]: return 'Fall'
    return 'Winter'

df['Season'] = df['Month'].apply(get_season)

# 4c. Sex — standardise free-text
sex_map = {
    'male':'Male', 'm':'Male', 'Male':'Male',
    'female':'Female', 'f':'Female', 'Female':'Female',
    'undetermined':'Undetermined', 'unknown':'Undetermined',
}
df['Sex'] = df['Sex'].str.strip().map(lambda x: sex_map.get(str(x).lower(), 'Undetermined') if pd.notna(x) else 'Undetermined')

# 4d. Boolean columns
for col in ['Flyover_Observed', 'PIF_Watchlist_Status', 'Regional_Stewardship_Status',
            'Initial_Three_Min_Cnt', 'Previously_Obs']:
    if col in df.columns:
        df[col] = df[col].map(lambda x: True if str(x).strip().upper() in ['TRUE','1','YES'] else
                                         False if str(x).strip().upper() in ['FALSE','0','NO'] else np.nan)

# 4e. Numeric — Temperature & Humidity
df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
df['Humidity']    = pd.to_numeric(df['Humidity'],    errors='coerce')

# Fill temperature/humidity with median per Location_Type
for col in ['Temperature', 'Humidity']:
    df[col] = df.groupby('Location_Type')[col].transform(lambda x: x.fillna(x.median()))

# 4f. Drop rows with no species info at all
df.dropna(subset=['Common_Name', 'Scientific_Name'], how='all', inplace=True)

# 4g. Strip whitespace from string columns
str_cols = df.select_dtypes(include=['object', 'string']).columns
for col in str_cols:
    df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)

# 4h. Remove complete duplicates
before = len(df)
df.drop_duplicates(inplace=True)
print(f"   Removed {before - len(df)} duplicate rows")

# ─────────────────────────────────────────────
# STEP 5 — Save cleaned data
# ─────────────────────────────────────────────
os.makedirs('data', exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n💾 Saved cleaned data → {OUTPUT_FILE}")

# Save to SQLite database as required
import sqlite3
db_path = 'data/bird_data.db'
conn = sqlite3.connect(db_path)
df.to_sql('bird_observations', conn, if_exists='replace', index=False)
conn.close()
print(f"💾 Saved data to SQL Database → {db_path}")

# ─────────────────────────────────────────────
# STEP 6 — Quick summary report
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("  CLEANING SUMMARY")
print("="*50)
print(f"  Total records     : {len(df):,}")
print(f"  Unique species    : {df['Common_Name'].nunique()}")
print(f"  Location types    : {df['Location_Type'].value_counts().to_dict()}")
print(f"  Year range        : {df['Year'].min()} – {df['Year'].max()}")
print(f"  Admin units       : {sorted(df['Admin_Unit_Code'].dropna().unique())}")
print(f"  Missing Temp      : {df['Temperature'].isna().sum()}")
print(f"  Missing Humidity  : {df['Humidity'].isna().sum()}")
print("="*50)
