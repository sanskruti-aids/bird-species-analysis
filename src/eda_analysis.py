"""
Bird Species Analysis — Exploratory Data Analysis (EDA)
Run AFTER data_cleaning.py
Saves all charts to outputs/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('outputs', exist_ok=True)
sns.set_theme(style='whitegrid', palette='muted')

# ─────────────────────────────────────────────
# Load cleaned data
# ─────────────────────────────────────────────
df = pd.read_csv('data/bird_data_clean.csv', low_memory=False)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
print(f"Loaded {len(df):,} rows for EDA\n")


# ══════════════════════════════════════════════
# 1. SPECIES DIVERSITY BY HABITAT
# ══════════════════════════════════════════════
print("📊 1. Species Diversity by Habitat")
diversity = df.groupby('Location_Type')['Common_Name'].nunique().reset_index()
diversity.columns = ['Habitat', 'Unique_Species']

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(diversity['Habitat'], diversity['Unique_Species'],
              color=['#4C72B0','#55A868'], edgecolor='white', linewidth=1.2)
ax.bar_label(bars, padding=3, fontsize=12, fontweight='bold')
ax.set_title('Unique Bird Species by Habitat', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Unique Species')
ax.set_xlabel('Habitat Type')
plt.tight_layout()
plt.savefig('outputs/1_species_diversity_by_habitat.png', dpi=150)
plt.close()
print("   Saved → outputs/1_species_diversity_by_habitat.png")


# ══════════════════════════════════════════════
# 2. TOP 15 MOST OBSERVED SPECIES
# ══════════════════════════════════════════════
print("📊 2. Top 15 Most Observed Species")
top15 = df['Common_Name'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top15.values, y=top15.index, palette='Blues_r', ax=ax)
ax.set_title('Top 15 Most Observed Bird Species', fontsize=14, fontweight='bold')
ax.set_xlabel('Observation Count')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig('outputs/2_top15_species.png', dpi=150)
plt.close()
print("   Saved → outputs/2_top15_species.png")


# ══════════════════════════════════════════════
# 3. MONTHLY OBSERVATION TREND
# ══════════════════════════════════════════════
print("📊 3. Monthly Observation Trends")
df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
monthly = df.groupby(['Month', 'Location_Type']).size().reset_index(name='Count')
month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
               7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
monthly['Month_Name'] = monthly['Month'].map(month_names)

fig, ax = plt.subplots(figsize=(11, 5))
for habitat, grp in monthly.groupby('Location_Type'):
    ax.plot(grp['Month'], grp['Count'], marker='o', linewidth=2, label=habitat)
ax.set_xticks(range(1,13))
ax.set_xticklabels([month_names[m] for m in range(1,13)])
ax.set_title('Monthly Bird Observations by Habitat', fontsize=14, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Observation Count')
ax.legend(title='Habitat')
plt.tight_layout()
plt.savefig('outputs/3_monthly_trend.png', dpi=150)
plt.close()
print("   Saved → outputs/3_monthly_trend.png")


# ══════════════════════════════════════════════
# 4. YEARLY TREND
# ══════════════════════════════════════════════
print("📊 4. Yearly Observation Trend")
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
yearly = df.groupby(['Year','Location_Type']).size().reset_index(name='Count')
yearly = yearly.dropna(subset=['Year'])

fig, ax = plt.subplots(figsize=(11, 5))
for habitat, grp in yearly.groupby('Location_Type'):
    ax.plot(grp['Year'], grp['Count'], marker='s', linewidth=2, label=habitat)
ax.set_title('Yearly Bird Observations by Habitat', fontsize=14, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Observation Count')
ax.legend(title='Habitat')
plt.tight_layout()
plt.savefig('outputs/4_yearly_trend.png', dpi=150)
plt.close()
print("   Saved → outputs/4_yearly_trend.png")


# ══════════════════════════════════════════════
# 5. IDENTIFICATION METHOD DISTRIBUTION
# ══════════════════════════════════════════════
print("📊 5. ID Method Distribution")
id_method = df['ID_Method'].value_counts().head(8)

fig, ax = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax.pie(
    id_method.values, labels=id_method.index,
    autopct='%1.1f%%', startangle=140,
    colors=sns.color_palette('Set2', len(id_method))
)
ax.set_title('Bird Identification Methods', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/5_id_method_pie.png', dpi=150)
plt.close()
print("   Saved → outputs/5_id_method_pie.png")


# ══════════════════════════════════════════════
# 6. SEX RATIO BY HABITAT
# ══════════════════════════════════════════════
print("📊 6. Sex Ratio by Habitat")
sex_data = df.groupby(['Location_Type','Sex']).size().reset_index(name='Count')
sex_pivot = sex_data.pivot(index='Location_Type', columns='Sex', values='Count').fillna(0)

sex_pivot.plot(kind='bar', figsize=(8, 5), edgecolor='white', linewidth=0.8)
plt.title('Sex Distribution by Habitat', fontsize=14, fontweight='bold')
plt.xlabel('Habitat Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.legend(title='Sex', bbox_to_anchor=(1.01, 1))
plt.tight_layout()
plt.savefig('outputs/6_sex_ratio_by_habitat.png', dpi=150)
plt.close()
print("   Saved → outputs/6_sex_ratio_by_habitat.png")


# ══════════════════════════════════════════════
# 7. TEMPERATURE vs OBSERVATION COUNT
# ══════════════════════════════════════════════
print("📊 7. Temperature vs Observation Count")
temp_data = df.groupby(df['Temperature'].round(0)).size().reset_index(name='Count')
temp_data.columns = ['Temperature', 'Count']
temp_data = temp_data.dropna()

fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(temp_data['Temperature'], temp_data['Count'], alpha=0.6, color='tomato', edgecolors='white')
z = np.polyfit(temp_data['Temperature'].dropna(), temp_data['Count'], 1)
p = np.poly1d(z)
ax.plot(sorted(temp_data['Temperature']), p(sorted(temp_data['Temperature'])),
        '--', color='darkred', linewidth=1.5, label='Trend')
ax.set_title('Temperature vs Observation Count', fontsize=14, fontweight='bold')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Observation Count')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/7_temperature_vs_observations.png', dpi=150)
plt.close()
print("   Saved → outputs/7_temperature_vs_observations.png")


# ══════════════════════════════════════════════
# 8. ADMIN UNIT HEATMAP (species richness)
# ══════════════════════════════════════════════
print("📊 8. Admin Unit Species Heatmap")
heat = df.groupby(['Admin_Unit_Code','Location_Type'])['Common_Name'].nunique().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(heat, annot=True, fmt='d', cmap='YlGnBu', linewidths=0.5, ax=ax)
ax.set_title('Species Richness per Admin Unit & Habitat', fontsize=14, fontweight='bold')
ax.set_xlabel('Habitat Type')
ax.set_ylabel('Admin Unit Code')
plt.tight_layout()
plt.savefig('outputs/8_species_richness_heatmap.png', dpi=150)
plt.close()
print("   Saved → outputs/8_species_richness_heatmap.png")


# ══════════════════════════════════════════════
# 9. WATCHLIST STATUS ANALYSIS
# ══════════════════════════════════════════════
print("📊 9. Watchlist Status")
watch = df.groupby(['Location_Type','PIF_Watchlist_Status']).size().reset_index(name='Count')
watch['Status'] = watch['PIF_Watchlist_Status'].map({True:'At-Risk', False:'Not At-Risk', np.nan:'Unknown'})

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for i, (habitat, grp) in enumerate(watch.groupby('Location_Type')):
    grp_clean = grp.dropna(subset=['PIF_Watchlist_Status'])
    axes[i].pie(grp_clean['Count'], labels=grp_clean['Status'],
                autopct='%1.1f%%', startangle=90,
                colors=['#d9534f','#5cb85c','#f0ad4e'])
    axes[i].set_title(f'{habitat} — Watchlist Status', fontweight='bold')
plt.suptitle('PIF Watchlist Status by Habitat', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/9_watchlist_status.png', dpi=150)
plt.close()
print("   Saved → outputs/9_watchlist_status.png")


# ══════════════════════════════════════════════
# 10. DISTURBANCE EFFECT ON COUNT
# ══════════════════════════════════════════════
print("📊 10. Disturbance Effect")
dist = df.groupby('Disturbance').size().reset_index(name='Count').sort_values('Count', ascending=False)

fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=dist, x='Count', y='Disturbance', palette='coolwarm', ax=ax)
ax.set_title('Observations by Disturbance Type', fontsize=14, fontweight='bold')
ax.set_xlabel('Observation Count')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig('outputs/10_disturbance_effect.png', dpi=150)
plt.close()
print("   Saved → outputs/10_disturbance_effect.png")


print("\n✅ EDA complete! All 10 charts saved in outputs/")
