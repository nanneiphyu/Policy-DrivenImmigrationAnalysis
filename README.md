## Data-Driven Immigration Analysis
 Lawful permanent residents (LPRs), also known as “green card” holders, are aliens who are lawfully authorized to live permanently within the United States. This is a comprehensive analysis of the flow of Lawful Permanent Residents into the United States annually and how their settlement patterns have changed over the years into the Core Based Statistical Areas. 
 
 ## Objective 
 The purpose of this is to identify the numbers of population who have received Lawful Permanent Residents each four-years (representing Presidential terms) and the region they come from in comparison; to identify the top 20 countries where the number of Lawful Permanent Residents come from; and to analyze their settlement patterns particularly in Core Based Statistical Areas (Metro Areas) and examine if they have changed during each Presidential Period (from 2009 through 2020 - approximately three presidential terms). 
 #
 ## Sources
 #### This project utilizes information from sources where many sorts of immmigration data are available.
 ##### 1. Department of Homeland Security (https://www.dhs.gov). 
 ##### 2. Natural Earth (https://www.naturalearthdata.com/downloads/). 
 ##### 3. Census Bureau (https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html).
 ## Comparisons of Total Lawful Permanent Residents (LPRs)
 # Scripts ['clean_combined.py']
 ## Overall Numbers of LPRs Aanlysis (Three Presidential Terms - Approximate)
<p align="center">
  <img src="lpr_2009_region.png" width="200" alt="2009">
  <img src="lpr_2010_region.png" width="200" alt="2010">
  <img src="lpr_2011_region.png" width="200" alt="2011">
  <img src="lpr_2012_region.png" width="200" alt="2012">
</p>

#
<p align="center">
  <img src="lpr_2013_region.png" width="200" alt="2009">
  <img src="lpr_2014_region.png" width="200" alt="2010">
  <img src="lpr_2015_region.png" width="200" alt="2011">
  <img src="lpr_2016_region.png" width="200" alt="2012">
</p>

#
<p align="center">
  <img src="lpr_2017_region.png" width="200" alt="2009">
  <img src="lpr_2018_region.png" width="200" alt="2010">
  <img src="lpr_2019_region.png" width="200" alt="2011">
  <img src="lpr_2020_region.png" width="200" alt="2012">
</p>

##### Findings: Over 1 million individuals have obtained LPR status each year since 2009. The number of total LPRs peaked in 2016, almost 1.2 million. It was lowest in 2020 due to closures of USCIS offices during the COVID pandemic which impacted LPR admissions. There was a steady, rapid decline in the total LPR number during 2016-2020 which indicates the impact of policy changes during the Trump administration.

#
## Time Series Analysis By Each Approximate Presidential Term
<p align="center">
  <img src="lpr_annual_region.png" width="600" alt="Time Series">
</p>

##### This time series represents the total numbers of people who have obtained LPRs each year from 2009 to 2020. In 2009, it starts off with over 1,100,000 numbers of LPRs, however, then fluctuates over the years. However, there is a significant rise of LPRs in 2016 during President Obama's second term. In 2020, there is a remarkable drop down to approximately 720,000 in the numbers of LPRs before the end of President's Trump's administration compared to three presidential terms. The average numbers of LPRs for each four-year terms is represented by  - 1,066,778 (2009-2012), 1,060,401 (2013-2016), 990,703 (2017-2020) each respectively.  

#
## Regional Analysis of LPRs By Each Approximate Presidential Term
<p align="center">
    <img src="lpr_region_1st_term.png" width="200">
    <img src="second_term_lpr_by_region.png" width="200">
    <img src="third_term_lpr_by_region.png" width="200">
</p>
#
##### The maps additionally represents the numbers of LPRs coming six regions (Africa, Asia, Europe, North America, South America) around the world including regions of the world that are not explicitly identified. 

## Top 20 Countries LPRs By Each Approximate Presidential Term
<p align="center">
  <img src="top_20_lpr_2009.png" width="200">
  <img src="top_20_lpr_2010.png" width="200">
  <img src="top_20_lpr_2011.png" width="200">
  <img src="top_20_lpr_2012.png" width="200">
</p>


#
<p align="center">
  <img src="top_20_lpr_2013.png" width="200">
  <img src="top_20_lpr_2014.png" width="200">
  <img src="top_20_lpr_2015.png" width="200">
  <img src="top_20_lpr_2016.png" width="200">
</p>

#
<p align="center">
  <img src="top_20_lpr_2017.png" width="200">
  <img src="top_20_lpr_2018.png" width="200">
  <img src="top_20_lpr_2019.png" width="200">
  <img src="top_20_lpr_2020.png" width="200">
</p>

# 
##### Mexico was the single largest country of origin for LPRs in the U.S throughout the 2009-2020 period. The most notable trend within this period was the significant increase in LPRs from Asian countries, particularly China and India which ranked second and third, rivaling and sometimes exceeding numbers from Mexico in combined numbers. Mexico, the Dominican Republic, Cuba, and several Central American countries continually remained major sources, reflecting long-standing migration patterns and their family ties. Increase in LPRs from Cuba was significant in 2018 which ranked second in total LPRs potentially attributed by the surge in Cuban arrivals in 2015 and 2016 driven by fears of policy changes affected by normalization of U.S.-Cuba relations. Therefore, in 2018, Cuban nationals who had already arrived in the US waiting for the processing became adjusted from a previous status to LPR.

#


## CBSA Analysis By Each Approximate Presidential Term
<p align="center">
  <img src="CBSA_lpr_2009-2012.png" width="200">
  <img src="CBSA_lpr_2013-2016.png" width="200">
  <img src="CBSA_lpr_2017-2020.png" width="200">
</p>

#
##### Looking at all three heatmaps together, there’s a clear shift in migration patterns over time. Between 2009 and 2012, LPR inflows were heavily concentrated in major metro areas like New York, Los Angeles, and Miami, with New York consistently leading by a huge margin. Other metro areas like Chicago, Houston, and Washington maintained steady numbers of LPRs, but migration was still highly concentrated in the largest cities. Fast forward to 2017-2020, we see a downward trend in overall LPR numbers, especially by 2020. New York, Los Angeles, and Miami still hold top positions, but their inflows dropped significantly—New York’s numbers declined from 172K in 2017 to 98K in 2020. Other metro areas also experienced declines, spreading migration more evenly across regions. By 2021-2024, post-pandemic stagnation began. While some climb up was seen in 2021, totals stayed the same instead of going back up. Migration still remained spread out across regions other than concentrations in NYC and LA. This suggests a long-term shift in settlement patterns.
#
##### Finally, this suggests: 
##### 1.	A steady decline in LPR inflows overall, especially in major hubs.
##### 2.	A redistribution of migration, with smaller metro areas absorbing more inflows.
##### 3.	Post-2020 stagnation, with LPR numbers stabilizing at lower levels instead of climbing back up.
##### 4.	External influences, including policy changes, economic shifts, and the pandemic, playing a major role in shaping migration flows.
