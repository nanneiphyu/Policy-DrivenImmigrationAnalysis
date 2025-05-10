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

# Part 1 - - data filtering and barplot
# Filtering and Compiling data for 2009
# Lawful Permanent Residents 


lpr_2009 = pd.read_csv('2009_ImmSupTable2D.csv', skiprows=3, header=1)
## Replacing missing values with NaN
pd.set_option('future.no_silent_downcasting', True)
lpr_2009 = lpr_2009.replace(['D', '-'], np.nan)
lpr_2009_filtered = lpr_2009.dropna(axis=1, how='all')
print(lpr_2009_filtered)
##
#lpr_2009_filtered.to_csv('lpr_2009_filtered.csv', index=False)
# Saved the file just incase to use it in another part 

## Selecting Specific rows for the dataframe 
lpr_2009_filtered = lpr_2009_filtered.iloc[2:9]
## Checking the result 
print(lpr_2009_filtered.columns)
## Prepare for the barchart 

lpr_2009_filtered= lpr_2009_filtered.reset_index(drop=True)
lpr_2009_filtered = lpr_2009_filtered.set_index("Region and country of birth")
lpr_2009_filtered = lpr_2009_filtered.rename_axis('Region')

print(lpr_2009_filtered)
##
lpr_2009_filtered.to_csv('lpr_2009_region.csv')



## Just with two columns 
lpr_2009_region = pd.read_csv('lpr_2009_region.csv', thousands=',')

## Sorting values 
lpr_2009_region = lpr_2009_region.sort_values('Total', ascending=True).reset_index(drop=True)
##

#Select rows to keep 
lpr_2009_region = lpr_2009_region [['Region', 'Total']]
# Check the result again 
print(lpr_2009_region)

def shortened_number(num):
    if num>=1_000_000:
        return f'{num/1_000_000:.1f}M'
    elif num >=1_000:
        return f'{num/1_000:.1f}K'
    else:
        return str(num)
# Creating a barchart for region only - first 
plt.rcParams['font.family'] = 'Toppan Bunkyu Gothic'
plt.rcParams['font.style']  = 'normal'
plt.rcParams['font.size']   = 12
fig, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.barh(lpr_2009_region['Region'], 
                lpr_2009_region['Total'], 
                color='blue')
max_value = lpr_2009_region ['Total'].max()
#min_value = 1000
ax1.set_xlim(0, max_value * 1.10)

for index, value in enumerate(lpr_2009_region['Total']):
    if value >= 1000:  
        ax1.text(value, index, shortened_number(value), va='center', ha='left', fontsize=11, rotation=360) 
    
ax1.set_title('Total Number of Lawful Permanent Residents by Region (2009)')
ax1.set_xlabel('Numbers of LPRs')
ax1.set_ylabel('Region')

fig.tight_layout()
fig.savefig('lpr_2009_region.png', dpi=300)
# Saved the figure for region only

#%%
# Part 2 
# Extracting data and Creating csv files based on country of origin and settlement destinations 

lpr_2009 = pd.read_csv('2009_ImmSupTable2D.csv', skiprows=3, header=1)
pd.set_option('future.no_silent_downcasting', True)
## Replacing missing values with NaN
lpr_2009_country = lpr_2009.replace(['D', '-'], np.nan)
lpr_2009_country = lpr_2009_country.dropna(axis=1, how='all')
print(lpr_2009_country)
print(lpr_2009_country.columns.tolist())
print(lpr_2009_country.head())


## Selecting Specific rows for the dataframe 
lpr_2009_country = lpr_2009_country.iloc[11:-13]
print(lpr_2009_country)

lpr_2009_filtered = lpr_2009_country.reset_index(drop=True)
lpr_2009_filtered = lpr_2009_filtered.rename(columns={"Region and country of birth": "Country"})
## Remove rows that are not necessary 
lpr_2009_filtered = lpr_2009_filtered.drop(columns=['Non-CBSA', 'Other & Unknown'])
##
lpr_cols = lpr_2009_filtered.columns.drop('Country')
lpr_2009_final = lpr_2009_filtered.dropna(subset=lpr_cols, how='all').reset_index(drop=True)
##lpr_2012_final = lpr_filtered_by_country[lpr_filtered_by_country['Country'].str.strip() != 'Unknown']
print(lpr_2009_final)
## Saving files for the map - that will be need later
lpr_2009_final.to_csv('lpr_2009_by_country.csv', index=False)

#%%


## Part-3

## Filter out the Country and Total columns only 
lpr_2009_country_total = pd.read_csv('lpr_2009_by_country.csv')

## Read Iso file to comapre the countries 
iso_data = pd.read_csv('ISO.csv', encoding='latin1')
## Filter out mismatches 
iso_countries = set(iso_data['NAME_LONG'].str.strip())
lpr_countries = set(lpr_2009_country_total['Country'].str.strip())
##
matched_countries  = sorted(lpr_countries  & iso_countries)
mismatched_countries = sorted(lpr_countries - iso_countries)
print(f'Macthed ({len(matched_countries)}):\n', matched_countries)
print(f'Mismatched ({len(mismatched_countries)}):\n', mismatched_countries)

## Renaming all the names to make it consistent with other original data files
## Only because they use country names each year that not always consistent
to_rename_csv = {
    'Antigua-Barbuda': 'Antigua and Barbuda', 
    'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
    'Czech Republic': 'Czechia', 
    'Saint Kitts-Nevis': 'Saint Kitts and Nevis', 
    'Cape Verde': 'Cabo Verde', 
    'Macedonia': 'North Macedonia', 
    'British Virgin Islands': 'Virgin Islands, British', 
    'U.S. Virgin Islands': 'United States Virgin Islands'
    }
lpr_2009_country_total['Country'] = lpr_2009_country_total['Country'].replace(to_rename_csv)
#

to_drop_csv = [
    'Soviet Union, former',
    'Serbia and Montenegro1',
    'France', 
    'Kosovo',
    'Norway',
    'Czechoslovakia, former',
    "Cote d'Ivoire",   
    'Netherlands Antilles', 
    'Guadeloupe', 
    'French Guiana', 
    'Gibraltar', 
    'Martinique', 
    'Reunion'
]

countries_dropped = lpr_2009_country_total[~lpr_2009_country_total['Country'].isin(to_drop_csv)].reset_index(drop=True)
print(countries_dropped)

merged_iso_csv = pd.merge(countries_dropped,iso_data[['NAME_LONG', 'ISO_A3']], left_on='Country', right_on='NAME_LONG', how='left', indicator=True)
print(merged_iso_csv['_merge'].value_counts())
merged_iso_csv = merged_iso_csv.drop(columns=['_merge'])
# merged_iso_csv = merged_iso_csv.rename(columns={'NAME_LONG': "NAME"})
## Saving this for later use 
merged_iso_csv.to_csv('lpr_added_iso_cbsa_2009.csv', index=False)


## Selecting two columns only and saving the file 
merged_iso_csv_final= merged_iso_csv [['Country', 'Total', 'NAME_LONG', 'ISO_A3']]
print(merged_iso_csv_final) 
merged_iso_csv_final.to_csv('lpr_2009_country_total_only.csv', index=False)
## Saved this for country specific maps 

#%%
## Top 20 countries with high lpr flow in 2021 

# Reading file
merged_lpr = pd.read_csv('lpr_2009_country_total_only.csv', thousands=',')

# Sorting by Total and select top 20
top20_lpr = merged_lpr.sort_values('Total', ascending=False).head(20)
print(top20_lpr)
# Creating horizontal bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top20_lpr['Country'][::-1], top20_lpr['Total'][::-1])
# 4. Labels and title
ax.set_xlabel('Total LPRs')
ax.set_title('Top 20 Countries by Total LPRs (2009)')
max_value = top20_lpr['Total'].max()

ax.set_xlim(0, max_value * 1.1) 
# Annotating bars with values
for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width):,}', 
            va='center', fontsize=10)

fig.tight_layout()
fig.savefig('top_20_lpr_2009.png', dpi=300)
# Saved the figure for top lpr by country of birth 
#%%
# Let's focus on the data with csba areas
cbsa_2009 = pd.read_csv('lpr_added_iso_cbsa_2009.csv', thousands=',')
cbsa_2009 = cbsa_2009.drop(columns=['Total', 'NAME_LONG', 'ISO_A3'])
cbsa_transposed = cbsa_2009.set_index('Country').T
print(cbsa_transposed)
#
cbsa_transposed.index.name = 'NAME'
cbsa_transposed['Total'] = cbsa_transposed.sum(axis=1)

## Check rows with all missing values and drop them all 
null_counts = cbsa_transposed.isna().sum()
total_rows = len(cbsa_transposed)
all_null_cols = null_counts[null_counts == total_rows].index.tolist()
cbsa_transposed_clean = cbsa_transposed.dropna(axis=1, how='all')
print(cbsa_transposed_clean)
print(len(cbsa_transposed_clean))
cbsa_transposed_clean.to_csv('cbsa_2009_for_join.csv')
# Saved the file 


# trim the data just for QGIS 
join = pd.read_csv('cbsa_2009_for_join.csv')
join_key = join[['NAME', 'Total']]
join_key = join_key.copy()
join_key ['NAME'] = join_key ['NAME'].str.strip()

# Read the CBSA shapefile
gdf = gpd.read_file('tl_2009_us_cbsa.zip')
gdf = gdf.copy()
gdf['NAME'] = gdf['NAME'].str.strip()
# Merging based on names of CBSA
merged_join_key = gdf.merge(join_key,on='NAME', how='inner') 

# keep only those that match
print(f"CSV rows:      {len(join_key)}")
print(f"Merged shapes: {len(merged_join_key)}")


csv_names = set(merged_join_key['NAME'])
shp_names = set(gdf['NAME'])

missing_in_shp = sorted(csv_names - shp_names)
missing_in_csv = sorted(shp_names - csv_names)

print({len(missing_in_shp)})
print({len(missing_in_csv)})

## Find the names that didn't match
mismatched = join_key[~join_key['NAME'].isin(merged_join_key['NAME'])]
mismatched_names = mismatched['NAME'].tolist()
print(mismatched_names)
## Find the closest names in shp 
from difflib import get_close_matches

for name in mismatched_names: 
    print(f"\n{name} ->",
          get_close_matches(name, list(shp_names), n=5, cutoff=0.5))
## Got the names that are closley related

## Rename all the mistached that didn't join 
## only becasue there is inconsistency to join with the map 
to_rename_cbsa = {
    'Sacramento--Arden-Arcade-Roseville, CA': 'Sacramento--Arden-Arcade--Roseville, CA',
    'Nashville-Davidson-Murfreesboro-Franklin, TN': 'Nashville-Davidson--Murfreesboro--Franklin, TN',
    'Saint Louis, MO-IL': 'St. Louis, MO-IL'
    }
join_key['NAME'] = join_key['NAME'].replace(to_rename_cbsa)
join_key_final = join_key
merged_fater_rename = gdf.merge(join_key, on='NAME', how='inner')
## Check if they matched 
print(len(join_key_final))
print('\nAfter renaming:', len(merged_fater_rename))
# merged_fater_rename = merged_fater_rename[['NAME', 'Total']]

## 
merged_fater_rename.to_csv('merged_join_key_2009_for_QGIS.csv', index=False)

# Saved the file 
## Join in QGIS to show it on the map and 2011 analysis complete
###### COMPLETE for 2011 






















#