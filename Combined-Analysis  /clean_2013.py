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
# Filtering and Compiling data for 2013
# Lawful Permanent Residents 


lpr = pd.read_csv('2013_immsuptable2d.csv', skiprows=2, header=1)
## Replacing missing values with NaN
pd.set_option('future.no_silent_downcasting', True)
lpr_2013 = lpr.replace(['D', '-'], np.nan)
lpr_2013 = lpr_2013.dropna(axis=1, how='all')
print(lpr_2013)


## Selecting Specific rows for the dataframe 
lpr_2013 = lpr_2013.iloc[2:9]
## Checking the result 
print(lpr_2013.columns)
## Prepare for the barchart 

lpr_2013 = lpr_2013.reset_index(drop=True)
lpr_2013 = lpr_2013.set_index("Region and country of birth")
lpr_2013 = lpr_2013.rename_axis('Region')
print(lpr_2013)
##
lpr_2013.to_csv('lpr_2013_region.csv')



## Just with two columns 
lpr_2013_region = pd.read_csv('lpr_2013_region.csv', thousands=',')

## Sorting values 
lpr_2013_region = lpr_2013_region.sort_values('Total', ascending=True).reset_index(drop=True)
print(lpr_2013_region)
##

#Select rows to keep 
lpr_2013_region = lpr_2013_region [['Region', 'Total']]
# Check the result again 
print(lpr_2013_region)

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
bars = ax1.barh(lpr_2013_region['Region'], 
                lpr_2013_region['Total'], 
                color='orange')
max_value = lpr_2013_region ['Total'].max()
# Anotating 
for index, value in enumerate(lpr_2013_region['Total']):
    if value >= 1000:  
        ax1.text(value, index, shortened_number(value), va='center', ha='left', fontsize=11, rotation=360) 
# Titles and labels 
ax1.set_title('Total Number of Lawful Permanent Residents by Region (2013)')
ax1.set_xlabel('Numbers of LPRs')
ax1.set_ylabel('Region')
ax1.set_xlim(0, max_value * 1.10)
fig.tight_layout()
fig.savefig('lpr_2013_region.png', dpi=300)
# Saved the figure for region only

#%%
# Part 2 
# Extracting data and Creating csv files based on country of origin and settlement destinations 
lpr_2013_country = pd.read_csv('2013_immsuptable2d.csv', skiprows=2, header=1)
pd.set_option('future.no_silent_downcasting', True)
## Replacing missing values with NaN
lpr_2013_country = lpr_2013_country.replace(['D', '-'], np.nan)
lpr_2013_country = lpr_2013_country.dropna(axis=1, how='all')
print(lpr_2013_country)
print(lpr_2013_country.columns.tolist())
print(lpr_2013_country.head())


## Selecting Specific rows for the dataframe 
lpr_2013_country = lpr_2013_country.iloc[11:-10]
print(lpr_2013_country)
##
lpr_2013_filtered = lpr_2013_country.rename(columns={"Region and country of birth": "Country"})
## Remove columns that are not necessary 
lpr_2013_filtered = lpr_2013_filtered.drop(columns=['Non-CBSA', 'Other & Unknown'])
##
lpr_cols = lpr_2013_filtered.columns.drop('Country')
lpr_2013_final = lpr_2013_filtered.dropna(subset=lpr_cols, how='all').reset_index(drop=True)
##
print(lpr_2013_final)
## Saving files for the map - that will be need later
lpr_2013_final.to_csv('lpr_2013_by_country.csv', index=False)



## Part-3

## Filter out the Country and Total columns only 
lpr_2013_country_total = pd.read_csv('lpr_2013_by_country.csv')

## Read Iso file to comapre the countries 
iso_data = pd.read_csv('ISO.csv', encoding='latin1')

## Filter out mismatches 
iso_countries = set(iso_data['NAME_LONG'].str.strip())
lpr_countries = set(lpr_2013_country_total['Country'].str.strip())

matched_countries  = sorted(lpr_countries  & iso_countries)
mismatched_countries = sorted(lpr_countries - iso_countries)

print(f'Macthed ({len(matched_countries)}):\n', matched_countries)
print(f'Mismatched ({len(mismatched_countries)}):\n', mismatched_countries)

## Renaming all the names to make it consistent with other original data files
## Only because the country names each year are not always consistent or the same
to_rename_csv = {
    'Antigua-Barbuda': 'Antigua and Barbuda', 
    'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
    'Czech Republic': 'Czechia', 
    'Saint Kitts-Nevis': 'Saint Kitts and Nevis', 
    'Cape Verde': 'Cabo Verde', 
    'Macedonia': 'North Macedonia', 
    'British Virgin Islands': 'Virgin Islands, British',
    }
lpr_2013_country_total['Country'] = lpr_2013_country_total['Country'].replace(to_rename_csv)
#
# Dopping columns 
to_drop_csv = [
    'Soviet Union, former',
    'Serbia and Montenegro1',
    'France', 
    'Kosovo',
    'Norway',
    'Czechoslovakia, former',
    "Cote d'Ivoire",    
    'Netherlands Antilles'
]
# Check after dropping 
countries_dropped = lpr_2013_country_total[~lpr_2013_country_total['Country'].isin(to_drop_csv)].reset_index(drop=True)
print(countries_dropped)
# Merge again 
merged_iso_csv = pd.merge(countries_dropped,iso_data[['NAME_LONG', 'ISO_A3']], left_on='Country', right_on='NAME_LONG', how='left', indicator=True)
print(merged_iso_csv['_merge'].value_counts())
merged_iso_csv = merged_iso_csv.drop(columns=['_merge'])
# 

## Saving this for later use 
merged_iso_csv.to_csv('lpr_added_iso_cbsa_2013.csv', index=False)


## Selecting two columns only and saving the file 
merged_iso_csv_final= merged_iso_csv [['Country', 'Total', 'NAME_LONG', 'ISO_A3']]
print(merged_iso_csv_final) 
merged_iso_csv_final.to_csv('lpr_2013_country_total_only.csv', index=False)
## Saved this for country specific maps 

#%%
## Top 20 countries of lpr flow in 2013

# Reading file
merged_lpr = pd.read_csv('lpr_2013_country_total_only.csv', thousands=',')

# Sorting by Total and select top 20
top20_lpr = merged_lpr.sort_values('Total', ascending=False).head(20)
print(top20_lpr)

# Creating horizontal bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top20_lpr['Country'][::-1], top20_lpr['Total'][::-1])
#
ax.set_xlabel('Total LPRs')
ax.set_title('Top 20 Countries by Total LPRs (2013)')
max_value = top20_lpr['Total'].max()

ax.set_xlim(0, max_value * 1.1) 
# Annotating bars with values
for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width):,}', 
            va='center', fontsize=10)

fig.tight_layout()
fig.savefig('top_20_lpr_2013.png', dpi=300)
# Saved the figure for top lpr by country of birth 

#%%
# Let's focus on the data with csba areas
cbsa_2013 = pd.read_csv('lpr_added_iso_cbsa_2013.csv', thousands=',')
cbsa_2013 = cbsa_2013.drop(columns=['Total', 'NAME_LONG', 'ISO_A3'])
cbsa_transposed = cbsa_2013.set_index('Country').T
print(cbsa_transposed)
#
cbsa_transposed.index.name = 'NAME'
cbsa_transposed['Total'] = cbsa_transposed.sum(axis=1)

## Check rows with all missing values 
null_counts = cbsa_transposed.isna().sum()
total_rows = len(cbsa_transposed)
all_null_cols = null_counts[null_counts == total_rows].index.tolist()
cbsa_transposed_clean = cbsa_transposed.dropna(axis=1, how='all')
#
print(cbsa_transposed_clean)
print(len(cbsa_transposed_clean))

cbsa_transposed_clean.to_csv('cbsa_2013_for_join.csv')
# Saved the file 


# trim the data just for QGIS 
join = pd.read_csv('cbsa_2013_for_join.csv')
join_key = join[['NAME', 'Total']]
join_key = join_key.copy()
join_key ['NAME'] = join_key ['NAME'].str.strip()

# Read the CBSA shapefile and clean up 
gdf = gpd.read_file('tl_2013_us_cbsa.zip')
gdf = gdf.copy()
gdf['NAME'] = gdf['NAME'].str.strip()
# Merging based on names of CBSA
merged_join_key = gdf.merge(join_key,on='NAME', how='inner') 

# keep only those that match and find the missing keys 
print(f"CSV rows:      {len(join_key)}")
print(f"Merged shapes: {len(merged_join_key)}")
#
csv_names = set(merged_join_key['NAME'])
shp_names = set(gdf['NAME'])
#
missing_in_shp = sorted(csv_names - shp_names)
missing_in_csv = sorted(shp_names - csv_names)
print({len(missing_in_shp)})
print({len(missing_in_csv)})
#

## Find the names that didn't match
mismatched = join_key[~join_key['NAME'].isin(merged_join_key['NAME'])]
mismatched_names = mismatched['NAME'].tolist()
print(mismatched_names)
print(len(mismatched_names))
## Find the closest names in shp 
from difflib import get_close_matches

for name in mismatched_names: 
    print(f"\n{name} ->",
          get_close_matches(name, list(shp_names), n=5, cutoff=0.5))
## Got the names that are closley related


## Rename all the mistached that didn't join 
to_rename_cbsa = {
    'New York-Northern New Jersey-Long Island, NY-NJ-PA': 'New York-Newark-Jersey City, NY-NJ-PA',
    'Los Angeles-Long Beach-Santa Ana, CA': 'Los Angeles-Long Beach-Anaheim, CA',
    'Miami-Fort Lauderdale-Pompano Beach, FL':'Miami-Fort Lauderdale-West Palm Beach, FL',
    'Chicago-Joliet-Naperville, IL-IN-WI': 'Chicago-Naperville-Elgin, IL-IN-WI',
    'Houston-Sugar Land-Baytown, TX': 'Houston-The Woodlands-Sugar Land, TX',
    'San Francisco-Oakland-Fremont, CA': 'San Francisco-Oakland-Hayward, CA',
    'Boston-Cambridge-Quincy, MA-NH': 'Boston-Cambridge-Newton, MA-NH',
    'Atlanta-Sandy Springs-Marietta, GA': 'Atlanta-Sandy Springs-Roswell, GA', 
    'San Diego-Carlsbad-San Marcos, CA': 'San Diego-Carlsbad, CA',
    'Detroit-Warren-Livonia, MI': 'Detroit-Warren-Dearborn, MI',
    'Phoenix-Mesa-Glendale, AZ': 'Phoenix-Mesa-Scottsdale, AZ',
    'Baltimore-Towson, MD': 'Baltimore-Columbia-Towson, MD',
    'Las Vegas-Paradise, NV': 'Las Vegas-Henderson-Paradise, NV',
    'Sacramento--Arden-Arcade--Roseville, CA': 'Sacramento--Roseville--Arden-Arcade, CA',
    'Denver-Aurora-Broomfield, CO': 'Denver-Aurora-Lakewood, CO',
    'Austin-Round Rock-San Marcos, TX': 'Austin-Round Rock, TX',
    'Charlotte-Gastonia-Rock Hill, NC-SC': 'Charlotte-Concord-Gastonia, NC-SC',
    'Honolulu, HI': 'Urban Honolulu, HI',
    'Providence-New Bedford-Fall River, RI-MA':'Providence-Warwick, RI-MA',
    'Indianapolis-Carmel, IN': 'Indianapolis-Carmel-Anderson, IN',
    'Raleigh-Cary, NC':'Raleigh, NC',
    'Cleveland-Elyria-Mentor, OH':'Cleveland-Elyria, OH',
    'Worcester, MA': 'Worcester, MA-CT', 
    'Cincinnati-Middletown, OH-KY-IN': 'Cincinnati, OH-KY-IN',
    'San Juan-Caguas-Guaynabo, PR': 'San Juan-Carolina-Caguas, PR',
    }
join_key['NAME'] = join_key['NAME'].replace(to_rename_cbsa)
join_key_final = join_key
#
merged_fater_rename = gdf.merge(join_key, on='NAME', how='left', validate='1:1')
print(len(join_key_final))
print('\nAfter renaming:', len(merged_fater_rename))


merged_join_key.to_csv('merged_join_key_2013_for_QGIS.csv', index=False)

# Saved the file 
## Join in QGIS to show it on the map and 2013 analysis complete
###### COMPLETE for 2013















