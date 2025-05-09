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






#%%
# Looking at the flow of LPRs based on the CBSA areas every four years
# Use Heatmap 
# Compare them to see if it has changed over time 


files = [
    'merged_join_key_2009_for_QGIS.csv',
    'merged_join_key_2010_for_QGIS copy.csv',
    'merged_join_key_2011_for_QGIS.csv',
    'merged_join_key_2012_for_QGIS.csv']

## Read the files 
cbsa_1 = []
for filename in files: 
    cbsa= pd.read_csv(filename,
                         usecols=['NAME', 'Total', 'CBSAFP'])
    cbsa_1.append(cbsa)

## Concating 
term_one = pd.concat(cbsa_1).reset_index(drop=True)
## Group by region and summ across the four years 
all_cbsa_1 = term_one.groupby('NAME')['Total'].sum().reset_index()
print(all_cbsa_1)
all_cbsa_1.to_csv('cbsa_term_one_for_join.csv')




terms = {
    '2009–2012': [2009, 2010, 2011, 2012],
    '2013–2016': [2013, 2014, 2015, 2016],
    '2017–2020': [2017, 2018, 2019, 2020],

## Second Term 
files = [
    'merged_join_key_2013_for_QGIS.csv',
    'merged_join_key_2014_for_QGIS.csv',
    'merged_join_key_2015_for_QGIS.csv',
    'merged_join_key_2016_for_QGIS.csv']



## Read the files 
cbsa_2 = []
for filename in files: 
    cbsa= pd.read_csv(filename,
                         usecols=['NAME', 'Total'])
    cbsa_2.append(cbsa)

## Concating 
term_two = pd.concat(cbsa_2).reset_index(drop=True)
## Group by region and summ across the four years 
all_cbsa_2 = term_two.groupby('NAME')['Total'].sum().reset_index()
print(all_cbsa_2)
all_cbsa_2.to_csv('cbsa_term_two_for_join.csv')
## 
## Third Term 
files = [
    'cbsa_2017_for_join.csv',
    'cbsa_2018_for_join.csv',
    'cbsa_2019_for_join.csv',
    'merged_join_key_2020_for_QGIS.csv']

## Read the files 
cbsa_3 = []
for filename in files: 
    cbsa= pd.read_csv(filename,
                         usecols=['NAME', 'Total'])
    cbsa_3.append(cbsa)

## Concating 
term_three = pd.concat(cbsa_3).reset_index(drop=True)
## Group by region and summ across the four years 
all_cbsa_3 = term_three.groupby('NAME')['Total'].sum().reset_index()
print(all_cbsa_3)
all_cbsa_3.to_csv('cbsa_term_three_for_join.csv')



















# Percentage calcualtions of non-cbsa, others and unknown  
# show the world map 
# show the toal of cbsa in the map for all years
# show in the world map of the total or comapre the GIS map
# for each presidential term and a glimpse of 2021














