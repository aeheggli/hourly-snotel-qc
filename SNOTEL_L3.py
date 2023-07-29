# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:17:20 2022

@author: anne
"""
import os
import pandas as pd 
import numpy as np
import copy
import re
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default='browser'

os.chdir('D:/Data')

#### List of SNOTEL Stations in CA & NV ####
#CA
# '301', '356', '391', '428', '446','462','463', '473','508', '518','539','540','541','574', '575','587','633', '697','724', 
# '771','778','784','809', '834','846', '848','977', '1049','1050','1051','1052','1067', 
# '1258', '1277', #2017
# #NV
# '321','334', '336','337','340','373','417','443','445','453','454','476','498','503','527','548', '569','570','573','615','652','698','746','750','811','849','1006',
# '1110','1111','1112' #2008
# '1136', # 2009
# '1147', '2170', #2010
# '1137','1152','1155','1194','1195', #2011
# '1242','1243','1244', #2013
# '1262', #2015
# '1272' # 2018

### This is a manual process, enter the station and water year that will be processed one at a time. 
station = '428'
year = '2007'

#read daily SNOTEL data
snotel_daily = pd.read_csv('SNOTEL_D/sd_' + station + '_WY' + str(year) + '.csv', parse_dates=['Date']) #data is start of day values
#name columns with unique sd (snotel daily) identifier
snotel_daily.columns =['date','sd_temp_avg_C','sd_temp_avg_qc','sd_temp_max_C','sd_temp_max_qc','sd_temp_min_C','sd_temp_min_qc','sd_temp_obs_C','sd_temp_obs_qc', 'sd_precip_mm', 'sd_precip_qc', 'sd_precip_24hr_mm','sd_precip_24hr_qc', 'sd_precip_24hrsnowadj_mm','sd_precip_24hradj_qc','sd_depth_cm', 'sd_depth_qc', 'sd_SWE_mm', 'sd_SWE_qc','sd_sm2_pct','sd_sm2_qc','sd_sm8_pct','sd_sm8_qc','sd_sm20_pct','sd_sm20_qc','sd_sm2_avg_pct','sd_sm2_avg_qc','sd_sm8_avg_pct','sd_sm8_avg_qc','sd_sm20_avg_pct','sd_sm20_avg_qc','sd_sm2_max_pct','sd_sm2_max_qc','sd_sm8_max_pct','sd_sm8_max_qc','sd_sm20_max_pct','sd_sm20_max_qc', 'sd_sm2_min_pct','sd_sm2_min_qc','sd_sm8_min_pct','sd_sm8_min_qc','sd_sm20_min_pct','sd_sm20_min_qc','sd_st2_avg_pct','sd_st2_avg_qc','sd_st8_avg_pct','sd_st8_avg_qc','sd_st20_avg_pct','sd_st20_avg_qc','sd_st2_max_pct','sd_st2_max_qc','sd_st8_max_pct','sd_st8_max_qc','sd_st20_max_pct','sd_st20_max_qc','sd_st2_min_pct','sd_st2_min_qc','sd_st8_min_pct','sd_st8_min_qc','sd_st20_min_pct','sd_st20_min_qc','sd_st2_pct','sd_st2_qc','sd_st8_pct','sd_st8_qc','sd_st20_pct','sd_st20_qc','sd_density_pct','sd_density_qc', 'sd_snowrainratio','sd_snowrainratio_qc']
snotel_daily['date'] = snotel_daily['date'].apply(lambda x: pd.Timestamp(x).replace(hour=0, minute=0, second=0)) #give the daily data a time stamp of midnight
snotel_daily = snotel_daily.set_index('date').resample('H').interpolate(method ='linear', limit_direction ='backward').drop(['sd_density_pct','sd_density_qc', 'sd_snowrainratio','sd_snowrainratio_qc'], axis=1)
snotel_daily = snotel_daily.fillna(method = 'ffill') #Apply daily data QC check to each time stamp for automated QC.
snotel_daily = snotel_daily.reset_index() 
        
#%% Iterate over this section
#Visualize the changes made to the data. 
# Updated the Level2QC_SNOTEL in excel and save as a .csv. 
# Then run this cell again, view, edit, view, edit until all data has been corrected or flagged as suspect. 

# Read the Level 2 QC .csv
level2QC = pd.read_csv('Level2QC_SNOTEL/'+station+'_WY'+year+'_L2QC.csv', parse_dates=['date']) #data is start of day values
level2QC['density'] = level2QC['sh_SWE_mm_L3']/(level2QC['sh_snowdepth_cm_L3'])*10

# IDENTIFY SUSPECT DATA
L2_swe = level2QC.loc[(level2QC['sh_SWE_qc_L3'] == "S")]
L2_depth = level2QC.loc[(level2QC['sh_snowdepth_qc_L3'] == "S")]
L2_precip = level2QC.loc[(level2QC['sh_precip_qc_L3']== "S")]

# PLOT DATA
fig = go.Figure()

#SWE
fig.add_trace(go.Scatter(x=snotel_daily['date'], y=snotel_daily['sd_SWE_mm'], line=dict(color='cornflowerblue'), opacity=0.5,name='SD SWE', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'], y=level2QC['sh_SWE_mm'], line=dict(color='cornflowerblue'), opacity=0.25,name='SH SWE', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_SWE_6hmed_mm'], line=dict(color='gold'), opacity = 0.8, name='6h SWE', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_SWE_24hmed_mm'], line=dict(color='darkorange'), opacity = 0.8, name='24h SWE', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_SWE_mm_L2'], line=dict(color='cornflowerblue'), opacity=1, name='L2 SWE', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_SWE_mm_L3'], line=dict(color='deeppink'), opacity = 0.5, name='L3 SWE', yaxis='y1'))
fig.add_trace(go.Scatter(mode = 'markers', x=L2_swe['date'],y=L2_swe['sh_SWE_mm_L3'], line=dict(color='hotpink'), opacity = 0.8, name='L3 SWE S', yaxis='y1'))


#Depth
fig.add_trace(go.Scatter(x=snotel_daily['date'], y=snotel_daily['sd_depth_cm'], line=dict(color='darkolivegreen'), opacity=0.5,name='SD depth', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'], y=level2QC['sh_snowdepth_cm'], line=dict(color='darkolivegreen'), opacity=0.25,name='SH depth', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_snowdepth_6hmed_cm'], line=dict(color='skyblue'), opacity=0.6, name='6h depth', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_snowdepth_12hmed_cm'], line=dict(color='royalblue'), opacity=0.6, name='12h depth', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_snowdepth_24hmed_cm'], line=dict(color='navy'), opacity=0.6, name='24h depth', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_snowdepth_cm_L2'], line=dict(color='darkolivegreen'), opacity=1, name='L2 depth', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_snowdepth_cm_L3'], line=dict(color='deeppink'), opacity = 0.5, name='L3 depth', yaxis='y1'))
fig.add_trace(go.Scatter(mode = 'markers', x=L2_depth['date'],y=L2_depth['sh_snowdepth_cm_L3'], line=dict(color='hotpink'), opacity = 0.8, name='L3 depth S', yaxis='y1'))

#Density
fig.add_trace(go.Scatter(mode='markers', x=level2QC['date'],y=level2QC['density'], marker=dict(color='lightgrey', symbol='cross', size=5), name='L2 density', yaxis='y2'))

#Precip
fig.add_trace(go.Scatter(x=snotel_daily['date'], y=snotel_daily['sd_precip_mm'], line=dict(color='teal'), opacity=0.5, name='SD precip', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'], y=level2QC['sh_precip_mm'], line=dict(color='teal'), opacity=0.25, name='SH precip', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_precip_6hmed_mm'], line=dict(color='gold'), opacity=0.6, name='6h precip', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_precip_24hmed_mm'], line=dict(color='darkorange'), opacity=0.6, name='24h precip', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_precip_mm_L2'], line=dict(color='teal'), opacity=1, name='L2 precip', yaxis='y1'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_precip_mm_L3'], line=dict(color='deeppink'), opacity = 0.5, name='L3 precip', yaxis='y1'))
fig.add_trace(go.Scatter(mode = 'markers', x=L2_precip['date'],y=L2_precip['sh_precip_mm_L3'], line=dict(color='hotpink'), opacity = 0.8, name='L3 Precip S', yaxis='y1'))


#Temp
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_temp_C_L3'], line=dict(color='lightcoral'), name='L3 temp', yaxis='y2'))

#Soil Moistrue
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_sm2_pct_L3'], line=dict(color='sandybrown'), name='L3 sm2', yaxis='y2'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_sm8_pct_L3'], line=dict(color='chocolate'), name='L3 sm8', yaxis='y2'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_sm20_pct_L3'], line=dict(color='saddlebrown'), name='L3 sm20', yaxis='y2'))

#Soil Temperature
fig.add_trace(go.Scatter( x=level2QC['date'],y=level2QC['sh_st2_C_L3'], line=dict(color='lightgrey'), name='L3 st2', yaxis='y2'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_st8_C_L3'], line=dict(color='darkgrey'), name='L3 st8', yaxis='y2'))
fig.add_trace(go.Scatter(x=level2QC['date'],y=level2QC['sh_st20_C_L3'],  line=dict(color='dimgrey'), name='L3 st20', yaxis='y2'))


fig.update_layout(
    title=station,
    # xaxis_title='X Axis Title',
    yaxis=dict(title='SWE (mm) / Precip (mm) / Depth (cm)'),
    yaxis2=dict(title='Temp (C) / Soil Moistuce (%)', overlaying='y', side='right'),
    legend_title='Legend',
    plot_bgcolor = '#FBFBFB',
    # font=dict(family='Oswald', sans-serif',size=16,color='DarkGrey'),
    hovermode="x unified"
)
fig.show()

#%% EXPORT TO LEVEL 3
# Once the data has been corrected for all parameters, run this cell for the year or range of years 
# for the station selected in the first cell to output the L3P data

# year = '2006'
for year in range(2006,2022):

    level2QC = pd.read_csv('Level2QC_SNOTEL/'+station+'_WY'+str(year)+'_L2QC.csv', parse_dates=['date'])
    level3 = level2QC.round(1)
    
    #Verify QC Flag for data
    level3['sh_SWE_qc_L3'] = np.where((level3['sh_SWE_mm'] == level3['sh_SWE_mm_L3']) & (level3['sh_SWE_qc_L3']!="S"), level3['sh_SWE_qc'], level3['sh_SWE_qc_L3'])
    level3['sh_depth_qc_L3'] = np.where((level3['sh_snowdepth_cm'] == level3['sh_snowdepth_cm_L3']) & (level3['sh_snowdepth_qc_L3']!="S"), level3['sh_snowdepth_qc'], level3['sh_snowdepth_qc_L3'])
    level3['sh_precip_qc_L3'] = np.where((level3['sh_precip_mm'] == level3['sh_precip_mm_L3']) & (level3['sh_precip_qc_L3']!="S"), level3['sh_precip_qc'], level3['sh_precip_qc_L3'])
    
    #set QA flag to provisional
    level3['sh_SWE_qa_L3'] = 'L3P'
    level3['sh_snowdepth_qa_L3'] = 'L3P'
    level3['sh_precip_qa_L3'] = 'L3P' 
    
    
    ### Add data QC check ###
    level3 = level3[['date', 'sh_SWE_mm_L3',  'sh_SWE_qc_L3', 'sh_SWE_qa_L3', 
                        'sh_snowdepth_cm_L3', 'sh_snowdepth_qc_L3', 'sh_snowdepth_qa_L3', 
                        'sh_precip_mm_L3', 'sh_precip_qc_L3', 'sh_precip_qa_L3', 
                        'sh_temp_C_L3', 'sh_temp_qc_L3', 'sh_temp_qa_L3',
                        'sh_sm2_pct_L3', 'sh_sm2_qc_L3','sh_sm2_qa_L3','sh_sm8_pct_L3', 'sh_sm8_qc_L3','sh_sm8_qa_L3','sh_sm20_pct_L3', 'sh_sm20_qc_L3','sh_sm20_qa_L3',
                        'sh_st2_C_L3', 'sh_st2_qc_L3','sh_st2_qa_L3', 'sh_st8_C_L3', 'sh_st8_qc_L3','sh_st8_qa_L3','sh_st20_C_L3', 'sh_st20_qc_L3', 'sh_st20_qa_L3']]
    
    ### Add data QC check ###
    level3.columns = ['date', 'sh_SWE_mm',  'sh_SWE_qc', 'sh_SWE_qa', 
                        'sh_snowdepth_cm', 'sh_snowdepth_qc', 'sh_snowdepth_qa', 
                        'sh_precip_mm', 'sh_precip_qc', 'sh_precip_qa', 
                        'sh_temp_C', 'sh_temp_qc', 'sh_temp_qa',
                        'sh_sm2_pct', 'sh_sm2_qc','sh_sm2_qa','sh_sm8_pct', 'sh_sm8_qc','sh_sm8_qa','sh_sm20_pct', 'sh_sm20_qc','sh_sm20_qa',
                        'sh_st2_C', 'sh_st2_qc','sh_st2_qa', 'sh_st8_C', 'sh_st8_qc','sh_st8_qa','sh_st20_C', 'sh_st20_qc', 'sh_st20_qa']
    
    
    level3 = level3.set_index('date')
    level3.to_csv('D:/Data/Level3_SNOTEL/'+station+'_WY'+str(year)+'_L3.csv')

