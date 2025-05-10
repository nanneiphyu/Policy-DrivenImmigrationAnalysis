#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 20:55:07 2025

@author: nanneiphyu
"""

import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import matplotlib.dates as mdates 
import matplotlib.ticker as ticker

# Regional analysis for each four-years term 
# Part 1 - creating time series and calculating average for every four years 
# by region

lpr = pd.read_csv('combined_immsuptable2d.csv', index_col=0)
lpr['Total'] = lpr['Total'].astype(str).str.replace(',', '')
lpr['Total'] = pd.to_numeric(lpr['Total'], errors='coerce')
lpr.index = pd.to_datetime(lpr.index.astype(str), format='%Y')
##fornt selection
plt.rcParams['font.family'] = 'Toppan Bunkyu Gothic'
plt.rcParams['font.style']  = 'normal'


## Assign values for each four years term and exclude 2021
def term_label(year):
    if 2009 <= year <= 2012:
        return '2009–2012'
    elif 2013 <= year <= 2016:
        return '2013–2016'
    elif 2017 <= year <= 2020:
        return '2017–2020'
    else:
        return None
lpr['Term'] = lpr.index.year.map(term_label)

# Calculate the terms 
term_means = lpr.dropna(subset=['Term']).groupby('Term')['Total'].mean()
print(term_means.to_string())

# Setp up blok terms - four years presidential term 
rep_years = [2012, 2016, 2020]
rep_dates  = pd.to_datetime([str(y) for y in rep_years], format='%Y')

## Set up the figure and plot
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(lpr.index, lpr['Total'], marker='D', linestyle='-', label='Annual Total LPRs',linewidth=2, markersize=8)
ax.plot(rep_dates, term_means.values, marker='D', linestyle='-', label='Average for Each 4-Year Term',linewidth=2, markersize=8)
ax.legend()

# Annotating 
for x,y in zip (rep_dates, term_means.values):
    ax.text( x,y * 1.02, 
            f'{int(y):,}',
            ha='center', va='bottom',
            fontsize=9, color='C1')


## Label each average points
for date, mean in zip(rep_dates, term_means): 
    if date not in rep_dates:
        ax.annotate(
            f'{mean:,.0f}',
            xy=(date, mean),
            xytext = (0,20), 
            textcoords='offset points',
            ha='center', 
            va='bottom',
            fontsize='9',
            color='C1')


# Making the years to be appeard as years only and 
# making the numbers appear as non scientific numbers or actual numbers 
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

## Adding grid lines for xy axis both major and minor 
ax.minorticks_on()
ax.grid(which='major', linestyle='--',
        linewidth=0.5,
        alpha=0.8)
ax.grid(which='minor', linestyle=':', 
       linewidth=0.3, 
       alpha=0.4)
##
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.set_xlim([pd.to_datetime('2009'), pd.to_datetime('2023')]) 
## setting xlim Just to have more space to the right 
print(lpr.index.min(), lpr.index.max())

plt.setp(ax.get_xticklabels(), rotation=35, ha='right')
ax.set_title("Annual Total LPRs by Years (2009 - 2021)", fontsize=15) 
ax.set_xlabel("Years", fontsize=14)
ax.set_ylabel("Number of LPRs", fontsize=14)
fig.tight_layout()
fig.savefig('lpr_annual_region.png', dpi=300)
## Saved the time series by Region 




#%%
# Regional Analysis using QGIS for each four years-term 
# Read files (2009-2012)
files = [
    'lpr_2009_region.csv',
    'lpr_2010_region.csv',
    'lpr_2011_region.csv',
    'lpr_2012_region.csv']
# 
regions = []
for filename in files: 
    region = pd.read_csv(filename,
                         usecols=['Region', 'Total'],
                         thousands=',')
    regions.append(region)

## Concating 
first_term = pd.concat(regions).reset_index(drop=True)
## Group by region and summ across the four years 
all_total_1 = first_term.groupby('Region')['Total'].sum().reset_index()
all_total_1.to_csv('first_term_region_for QGIS.csv')


###
# Load another four years term (2013-2016)
files_2 = [
    'lpr_2013_region.csv',
    'lpr_2014_region.csv',
    'lpr_2015_region.csv',
    'lpr_2016_region.csv']

regions_2 = []
for filename in files: 
    region = pd.read_csv(filename,
                         usecols=['Region', 'Total'],
                         thousands=',')
    regions_2.append(region)

## Concating 
second_term = pd.concat(regions_2).reset_index(drop=True)
## Group by region and summ across the four years 
all_total_2 = second_term.groupby('Region')['Total'].sum().reset_index()
all_total_2.to_csv('second_term_region_for QGIS.csv')

# Load another four years term (2017-2020)
files_3 = [
    'lpr_2017_region.csv',
    'lpr_2018_region.csv',
    'lpr_2019_region.csv',
    'lpr_2020_region.csv']

regions_3 = []
for filename in files: 
    region = pd.read_csv(filename,
                         usecols=['Region', 'Total'],
                         thousands=',')
    regions_3.append(region)

## Concating 
third_term = pd.concat(regions_3).reset_index(drop=True)
## Group by region and summ across the four years 
all_total_3 = third_term.groupby('Region')['Total'].sum().reset_index()
all_total_3.to_csv('thrid_term_region_for QGIS.csv')
print(all_total_3)


## Comaprison maps using QGIS 
## Saved the GQIS project maps as png 
## QGIS maps will be uploaded 



#%%
# Looking at the flow of LPRs based on the CBSA areas - every four years
# Use Heatmap 
# Compare them to see if it has changed over time 

y_2009 = pd.read_csv('merged_join_key_2009_for_QGIS.csv')
cbsa_2009 = y_2009[['NAME', 'CBSAFP', 'Total']]
y_2010 = pd.read_csv('merged_join_key_2010_for_QGIS.csv')
cbsa_2010_to_rename = y_2010[['NAME10', 'CBSAFP10', 'Total']]
cbsa_2010 = cbsa_2010_to_rename.rename(columns={'NAME10': 'NAME', 'CBSAFP10': 'CBSAFP'})

y_2011 = pd.read_csv('merged_join_key_2011_for_QGIS.csv')
cbsa_2011 = y_2011[['NAME', 'CBSAFP', 'Total']]
y_2012 = pd.read_csv('merged_join_key_2012_for_QGIS.csv')
cbsa_2012 = y_2012[['NAME', 'CBSAFP', 'Total']]
## Group the coulmns 
columns = [cbsa_2009, cbsa_2010, cbsa_2011, cbsa_2012]
years = [2009, 2010, 2011, 2012]

## Read csv files 
cbsa_1 = []
for name, year in zip (columns, years): 
    cbsa= name.copy()
    cbsa['Year'] =year
    cbsa_1.append(cbsa)

## Concating 
term_one = pd.concat(cbsa_1, ignore_index=True)
term_one = term_one.infer_objects(copy=False)
pd.set_option('future.no_silent_downcasting', True)

#

# Pivot into a matrix 

heat_map1 = term_one.pivot_table(
    index='CBSAFP',
    columns='Year',
    values='Total',
    aggfunc='sum',
    fill_value=0).reset_index()
print(heat_map1)
## Sorting values based on years 

## pick one name per CBSAFP 
name_map =(
    term_one
    .dropna(subset=['NAME'])
    .groupby('CBSAFP', sort=False)['NAME']
    .first())
heat_map1['NAME'] = heat_map1['CBSAFP'].map(name_map)

## Font 
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.style']  = 'normal'
plt.rcParams['font.size']   = 12


## To make the fig nice and clean, sort the values 
heat_map1["Total_Sum"] = heat_map1[years].sum(axis=1)

# Sort values based on total sum across all four years 
sorted_map = heat_map1.sort_values("Total_Sum", ascending=False)
figure_sorted = sorted_map[years].copy()
# 
yticks = sorted_map['NAME'] # Chose the column for tick
print(sorted_map[['NAME','Total_Sum']].head(10))
# Checking

## Set the hight of the fig cells
cell_height = 0.3 
fig_height = max(5, len(figure_sorted) * cell_height)
fig_width = 12 
fig, ax = plt.subplots (figsize= (fig_width,fig_height), dpi=300)
# Heatmap
sns.heatmap(figure_sorted, cmap='PuRd', 
            annot=True, fmt='.0f', linewidths=0.5, 
            linecolor='gray', 
            xticklabels=years,
            yticklabels=yticks,
            cbar = False, #_kws={'label': 'LPR Total'}, 
            ax=ax)

# Setting cbar title at the top so that it is visible 
cbar= fig.colorbar(
    ax.collections[0],
    orientation='vertical')
cbar.ax.set_title('LPR Total', fontsize=12)

## Set tick labels 
ax.set_xticks([idx + 0.5 for idx  in range(len(years))])
ax.set_xticklabels(years, ha='center', fontsize=12)
# Tiltles, lables and saving file 
plt.title("Annual LPRs Flow into CBSA Areas (2009-2012)", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("CBSA (Metro Area)", fontsize=14)
plt.tight_layout()
plt.savefig('CBSA_lpr_2009-2012.png', dpi=300, bbox_inches='tight')
plt.show()




#%%

## Second Term 
## Read files and select columns to keep 
y_2013 = pd.read_csv('merged_join_key_2013_for_QGIS.csv', thousands=',')
cbsa_2013 = y_2013[['NAME', 'CBSAFP', 'Total']]
y_2014 = pd.read_csv('merged_join_key_2014_for_QGIS.csv')
cbsa_2014 = y_2014[['NAME', 'CBSAFP', 'Total']]
y_2015 = pd.read_csv('merged_join_key_2015_for_QGIS.csv')
cbsa_2015 = y_2015[['NAME', 'CBSAFP', 'Total']]
y_2016 = pd.read_csv('merged_join_key_2016_for_QGIS.csv')
cbsa_2016 = y_2016[['NAME', 'CBSAFP', 'Total']]

## Group the coulmns 
columns_2 = [cbsa_2013, cbsa_2014, cbsa_2015, cbsa_2016]
years_2 = [2013, 2014, 2015, 2016]


## Read csv files and loop
cbsa_2 = []
for name, year in zip (columns_2, years_2): 
    cbsa= name.copy()
    cbsa['Year'] =year
    cbsa_2.append(cbsa)

## Concating data
term_two = pd.concat(cbsa_2, ignore_index=True)
term_two = term_two.infer_objects(copy=False)
pd.set_option('future.no_silent_downcasting', True)


# Pivot into a matrix 
heat_map2 = term_two.pivot_table(
        index='CBSAFP',
        columns='Year',
        values='Total',
        aggfunc='sum',
        fill_value=0).reset_index()
print(heat_map2)
print(heat_map2.columns)

## Pick one name for each CBSAFP
name_map_2 = (
    term_two
    .dropna(subset=['NAME'])
    .groupby('CBSAFP', sort=False)['NAME']
    .first())

heat_map2['NAME'] = heat_map2['CBSAFP'].map(name_map_2)


## Selecting font style and family 

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.style']  = 'normal'
plt.rcParams['font.size']   = 12


#sum the toal across the years 
heat_map2["Total_Sum"] = heat_map2[years_2].sum(axis=1)

# Sort values based on years total sum across years 
sorted_map_2 = heat_map2.sort_values("Total_Sum", ascending=False)
figure_sorted_2 = sorted_map_2[years_2].copy()
yticks = sorted_map_2['NAME']

## Set the hight of the fig cells
cell_height = 0.3 
fig_height = max(5, len(figure_sorted_2) * cell_height)
fig_width = 12 
fig, ax = plt.subplots (figsize= (fig_width,fig_height), dpi=300)
# Heatmap
sns.heatmap(figure_sorted_2, cmap='YlOrRd', 
            annot=True, fmt='.0f', linewidths=0.5, 
            linecolor='white', 
            xticklabels=years_2,
            yticklabels=yticks,
            cbar = False,  
            ax=ax)

# Setting cbar title at the top so that it is visible 
cbar= fig.colorbar(
    ax.collections[0],
    orientation='vertical')
cbar.ax.set_title('LPR Total', fontsize=12)

# Set tick labels 
ax.set_xticks([idx + 0.5 for idx  in range(len(years_2))])
ax.set_xticklabels(years_2, ha='center', fontsize=12)
# Tiltles and labels 
plt.title("Annual LPRs Flow into CBSA Areas (2013-2016)", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("CBSA (Metro Area)", fontsize=14)
plt.tight_layout()
plt.savefig('CBSA_lpr_2013-2016.png', dpi=300, bbox_inches='tight')
plt.show()

#%%
## Third Term 
## Read files and select columns to keep 
y_2017 = pd.read_csv('merged_join_key_2017_for_QGIS.csv')
cbsa_2017 = y_2017[['NAME', 'CBSAFP', 'Total']]
y_2018 = pd.read_csv('merged_join_key_2018_for_QGIS.csv')
cbsa_2018 = y_2018[['NAME', 'CBSAFP', 'Total']]
y_2019 = pd.read_csv('merged_join_key_2019_for_QGIS.csv')
cbsa_2019 = y_2019[['NAME', 'CBSAFP', 'Total']]
y_2020 = pd.read_csv('merged_join_key_2020_for_QGIS.csv')
cbsa_2020 = y_2020[['NAME', 'CBSAFP', 'Total']]

## Group the coulmns 
columns_3 = [cbsa_2017, cbsa_2018, cbsa_2019, cbsa_2020]
years_3 = [2017, 2018, 2019, 2020]


## Read csv files and lopp 
cbsa_3 = []
for name, year in zip (columns_3, years_3): 
    cbsa= name.copy()
    cbsa['Year'] =year
    cbsa_3.append(cbsa)

## Concating data 
term_three = pd.concat(cbsa_3, ignore_index=True)
term_three = term_three.infer_objects(copy=False)
pd.set_option('future.no_silent_downcasting', True)

#

# Pivot into a matrix 
heat_map3 = term_three.pivot_table(
    index='CBSAFP',
    columns='Year',
    values='Total',
    aggfunc='sum',
    fill_value=0).reset_index()
print(heat_map3)
print(heat_map3.columns)

# Set font and style 
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.style']  = 'normal'
plt.rcParams['font.size']   = 12

heat_map3['NAME'] = heat_map1['CBSAFP'].map(name_map)
heat_map3["Total_Sum"] = heat_map3[years_3].sum(axis=1)

# Sort values based on total sum across the years 
sorted_map_3 = heat_map3.sort_values("Total_Sum", ascending=False)
figure_sorted_3 = sorted_map_3[years_3].copy()
yticks = sorted_map_3['NAME']

## Set up and the hight of the fig cells
cell_height = 0.3 
fig_height = max(5, len(figure_sorted_3) * cell_height)
fig_width = 12 
fig, ax = plt.subplots (figsize= (fig_width,fig_height), dpi=300)
## Heatmap 
sns.heatmap(figure_sorted_3, cmap='YlGnBu', 
            annot=True, fmt='.0f', linewidths=0.5, 
            linecolor='gray', 
            xticklabels=years_3,
            yticklabels=yticks,
            cbar = False,  
            ax=ax)

# Setting cbar title at the top so that it is visible 
cbar= fig.colorbar(
    ax.collections[0],
    orientation='vertical')
cbar.ax.set_title('LPR Total', fontsize=12)

## Add tick labels and align 
ax.set_xticks([idx + 0.5 for idx  in range(len(years_3))])
ax.set_xticklabels(years_3, ha='center', fontsize=12)
## Set titles 
plt.title("Annual LPRs Flow into CBSA Areas (2017-2020)", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("CBSA (Metro Area)", fontsize=14)
plt.tight_layout()
plt.savefig('CBSA_lpr_2017-2020.png', dpi=300, bbox_inches='tight')
plt.show()









