#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 20:55:07 2025

@author: nanneiphyu
"""

import pandas as pd 
import os 
import zipfile 
import matplotlib.pyplot as plt 
import seaborn as sns
import geopandas as gpd 
import numpy as np

# Part 1 
# Filtering and Compiling data for 2010
# Lawful Permanent Residents 


lpr_2010 = pd.read_excel('2010_immsuptable2d.xlsx', skiprows=2, header=1)
## Replacing missing values with NaN
lpr_2010 = lpr_2010.replace(['D', '-'], np.nan).infer_objects(copy=False)
## Selecting Specific rows for the dataframe 
lpr_2010 = lpr_2010.iloc[2:9]
## Checking the result 
print(lpr_2010.columns)
lpr_2010 = lpr_2010.reset_index(drop=True)
lpr_2010 = lpr_2010.set_index("Region and country of birth")
lpr_2010 = lpr_2010.rename_axis('Region')
lpr_2010.to_csv('lpr_2010_region.csv')

# Checked again 

lpr_2010_region = pd.read_csv('lpr_2010_region.csv')
print(lpr_2010_region)
lpr_2010_region = lpr_2010_region.sort_values("Total", ascending=True)
print(lpr_2010_region)

# Creating a barchart for region only - first 
plt.rcParams['font.family'] = 'Toppan Bunkyu Gothic'
plt.rcParams['font.style']  = 'normal'
plt.rcParams['font.size']   = 12
fig, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.barh(lpr_2010_region['Region'], lpr_2010_region['Total'], color='royalblue')

def shortened_number(num):
    if num>=1_000_000:
        return f'{num/1_000_000:.1f}M'
    elif num >=1_000:
        return f'{num/1_000:.1f}K'
    else:
        return str(num)

ax1.set_title('Total Number of Lawful Permanent Residents by Region (2010)')
ax1.set_xlabel('Numbers of LPRs')
ax1.set_ylabel('Region')

for index, value in enumerate(lpr_2010_region['Total']):
    if value >= 1000:  
        ax1.text(value, index, shortened_number(value), va='center', fontsize=7.5, rotation=360) 

fig.tight_layout()
fig.savefig('lpr_2010_region.png', dpi=300)
# Saved the figure for region only
#%%
# Part 2 
# Extracting data and Creating a file based on country of origin and settlement destinations 
lpr_2010_by_country = pd.read_excel('2010_immsuptable2d.xlsx', skiprows=2, header=1)
pd.set_option('future.no_silent_downcasting', True)
lpr_2010_by_country = lpr_2010_by_country.astype(object)
pd.set_option('display.max_columns', None)
print(lpr_2010_by_country.columns.tolist())
print(lpr_2010_by_country.head())


## Replacing missing values with NaN
lpr_2010_by_country = lpr_2010_by_country.replace({'D': np.nan, '-': np.nan})

## Selecting Specific rows for the dataframe 
lpr_2010_by_country = lpr_2010_by_country.iloc[11:-8]
print(lpr_2010_by_country)
lpr_2010_filtered_by_country = lpr_2010_by_country.reset_index(drop=True)
lpr_2010_filtered_by_country = lpr_2010_filtered_by_country.rename(columns={"Region and country of birth": "Country"})

## Remove rows that are not necessary 
lpr_2010_filtered_by_country = lpr_2010_filtered_by_country.drop(columns=['Non-CBSA', 'Other & Unknown'])
# 
lpr_cols = lpr_2010_filtered_by_country.columns.drop('Country')
lpr_filtered = lpr_2010_filtered_by_country.dropna(subset=lpr_cols, how='all').reset_index(drop=True)
lpr_2010_filtered_final = lpr_filtered[lpr_filtered['Country'].str.strip() != 'Unknown']
print(lpr_2010_filtered_final)

## Saving files for the map - that will be need later
lpr_2010_filtered_final.to_csv('lpr_2010_by_country.csv', index=False)




## Part-3

## Filter out the country and Total columns only and
lpr_2010_country_total = pd.read_csv('lpr_2010_by_country.csv')

## Read Iso file to comapre the countries 
iso_data = pd.read_csv('ISO.csv', encoding='latin1')

## Filter out mismatches 
iso_countries = set(iso_data['NAME_LONG'].str.strip())
lpr_countries = set(lpr_2010_country_total['Country'].str.strip())
matched_countries  = sorted(lpr_countries  & iso_countries)
mismatched_countries = sorted(lpr_countries - iso_countries)
print(f'Macthed ({len(matched_countries)}):\n', matched_countries)
print(f'Mismatched ({len(mismatched_countries)}):\n', mismatched_countries)

## Renaming all the names to make it consistent with other original data 
to_rename_csv = {
    'Antigua-Barbuda': 'Antigua and Barbuda', 
    'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
    'Czech Republic': 'Czechia', 
    'Saint Kitts-Nevis': 'Saint Kitts and Nevis', 
    'Cape Verde': 'Cabo Verde', 
    'Macedonia': 'North Macedonia', 
    'British Virgin Islands': 'Virgin Islands, British'
    }


lpr_2010_country_total['Country'] = lpr_2010_country_total['Country'].replace(to_rename_csv)

to_drop_csv = [
    'Soviet Union, former',
    'Serbia and Montenegro1',
    'France', 
    'Kosovo',
    'Norway',
    'Czechoslovakia, former',
    "Cote d'Ivoire",  
    'French Guiana', 
    'Gibraltar', 
    'Guadeloupe', 
    'Martinique', 
    'Netherlands Antilles'
]


countries_dropped = lpr_2010_country_total[~lpr_2010_country_total['Country'].isin(to_drop_csv)].reset_index(drop=True)
print(countries_dropped)
merged_iso_csv = pd.merge(countries_dropped,iso_data[['NAME_LONG', 'ISO_A3']], left_on='Country', right_on='NAME_LONG', how='left', indicator=True)
print(merged_iso_csv['_merge'].value_counts())
merged_iso_csv = merged_iso_csv.drop(columns=['_merge'])
merged_iso_csv = merged_iso_csv.rename(columns={'NAME_LONG': "NAME"})
## Saving this for later use 
merged_iso_csv.to_csv('lpr_added_iso_cbsa_2010.csv', index=False)

## Selecting two columns only and saving the file 
merged_iso_csv_final= merged_iso_csv [['Country', 'Total', 'NAME', 'ISO_A3']]
print(merged_iso_csv_final) 
merged_iso_csv_final.to_csv('lpr_2010_country_total_only.csv', index=False)
## Saved this for country specific maps 



#%%
## Top 20 countries with high lpr flow in 2010
# Reading the file 
merged_lpr = pd.read_csv('lpr_added_iso_cbsa_2010.csv')

# Sorting by Total descending and select top 20
top20_lpr = merged_lpr.sort_values('Total', ascending=False).head(20)

# Creating horizontal bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top20_lpr['Country'][::-1], top20_lpr['Total'][::-1])
# 

ax.set_xlabel('Total LPRs')
ax.set_title('Top 20 Countries by Total LPRs (2010)')
max_value = top20_lpr['Total'].max()

ax.set_xlim(0, max_value * 1.1) 
# Annotating bars with values
for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width):,}', 
            va='center', fontsize=10)

# Figure saved
fig.tight_layout()
fig.savefig('top_20_lpr_2010.png', dpi=300)

#%% CBSA
# Let's focus on the data with csba areas
## To join data on QGIS - to look at the flow of LPRs by country first 
cbsa_2010 = pd.read_csv('lpr_added_iso_cbsa_2010.csv')
print(cbsa_2010)
# Dropping columns that are not necessary
cbsa_2010 = cbsa_2010.drop(columns=['Total', 'NAME', 'ISO_A3'])
cbsa_transposed = cbsa_2010.set_index('Country').T
print(cbsa_transposed)
cbsa_transposed.index.name = 'NAME'
cbsa_transposed['Total'] = cbsa_transposed.sum(axis=1)
## Check rows with all missing values 
null_counts = cbsa_transposed.isna().sum()
print(null_counts)
total_rows = len(cbsa_transposed)
all_null_cols = null_counts[null_counts == total_rows].index.tolist()
cbsa_transposed_clean = cbsa_transposed.dropna(axis=1, how='all')
print(cbsa_transposed_clean)
cbsa_transposed_clean.to_csv('cbsa_2010_for_join.csv')
# Saved the file 


# trim the data jsut for QGIS so that I can check if they match or not 
join = pd.read_csv('cbsa_2010_for_join.csv')
join_key = join[['NAME', 'Total']]
join_key = join_key.copy()
join_key ['NAME'] = join_key ['NAME'].str.strip()
join_key = join_key.rename(columns={'NAME': 'NAME10'})
print(join_key)
# Read the CBSA shapefile
gdf = gpd.read_file('tl_2010_us_cbsa10.zip')
gdf = gdf.copy()
gdf['NAME10'] = gdf['NAME10'].str.strip()
# Merging based on names of CBSA
merged_join_key = gdf.merge(join_key,on='NAME10', how='inner') 

# keep only those that match
print(f"CSV rows:      {len(join_key)}")
print(f"Merged shapes: {len(merged_join_key)}")

csv_names = set(merged_join_key['NAME10'])
shp_names = set(gdf['NAME10'])
missing_in_shp = sorted(csv_names - shp_names)
missing_in_csv = sorted(shp_names - csv_names)

print({len(missing_in_shp)})
print({len(missing_in_csv)})

## Find the names that didn't match
mismatched = join_key[~join_key['NAME10'].isin(merged_join_key['NAME10'])]
mismatched_names = mismatched['NAME10'].tolist()
print(mismatched_names)
## Find the closest names in shp 
from difflib import get_close_matches

for name in mismatched_names: 
    print(f"\n{name} ->",
          get_close_matches(name, list(shp_names), n=5, cutoff=0.5))
## Got the names that are closley related


## Rename all the mistached that didn't join 
to_rename_cbsa = {
    'Chicago-Naperville-Joliet, IL-IN-WI': 'Chicago-Joliet-Naperville, IL-IN-WI', 
    'Phoenix-Mesa-Scottsdale, AZ': 'Phoenix-Mesa-Glendale, AZ', 
    'Orlando-Kissimmee, FL': 'Orlando-Kissimmee-Sanford, FL', 
    'Portland-Vancouver-Beaverton, OR-WA': 'Portland-Vancouver-Hillsboro, OR-WA', 
    'Austin-Round Rock, TX': 'Austin-Round Rock-San Marcos, TX', 
    'Charlotte-Gastonia-Concord, NC-SC': 'Charlotte-Gastonia-Rock Hill, NC-SC', 
    'San Antonio, TX':'San Antonio-New Braunfels, TX',
    'Saint Louis, MO-IL': 'St. Louis, MO-IL'
    }
join_key['NAME10'] = join_key['NAME10'].replace(to_rename_cbsa)
join_key_final = join_key
merged_fater_rename = gdf.merge(join_key, on='NAME10', how='inner')
print(len(join_key_final))
print('\nAfter renaming:', len(merged_fater_rename))
merged_fater_rename.to_csv('merged_join_key_2010_for_QGIS.csv', index=False)

# Saved the file 
## Join in QGIS to show it on the map and 2010 analysis complete
###### COMPLETE for 2010





























#