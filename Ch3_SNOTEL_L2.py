# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 19:05:26 2022

@author: anne
"""
import os
import pandas as pd 
import numpy as np
import copy
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default='browser'

# os.chdir('/Users/anne/OneDrive/Data')
os.chdir('D:/Data')

# DONE through WY2022: '356','428','778',
            # #CA
            # '301', '391', '446','462','463', '473','508', '518','539','540','541','574', '575','587','633', '697','724', 
            # '771','784', '809', '834','846', '848','977', '1049','1050','1051','1052','1067', 
            # '1258', '1277', #2017
            # #NV
            # '321','334', '336','337','340','373','417','443','445','453','454','476','498','503','527','548', '569','570','573','615',
            # '652','698','746','750','811','849','1006',
            # '1110','1111','1112' #2008
            # '1136', # 2009
            # '1147', '2170', #2010
            # '1137','1152','1155','1194','1195', #2011
            # '1242','1243','1244', #2013
            # '1262', #2015
            # '1272' # 2018

stationid = ['778']

SWE1hrmax = 24.5 #mm
SWE1hrmin = -10  #mm
depth1hrmax = 10 #cm
depth1hrmin = -10 #cm
precip1hrmax = 25.4 #mm/hr 
precip1hrmin = -0 #mm/hr #

SWE_tolerance = 25.4 #mm 1"
snowdepth_tolerance = 15.24 #cm 6"
precip_tolerance = 25.4 #mm 2"

for station in stationid: 
    for year in range(2023, 2024): # this loops i through from WYstart (included) to WYend (not included) in 1 year chunks
        #read L0 data
        snotel_L0 = pd.read_csv('Level0_SNOTEL/'+station+'_WY'+str(year)+'_L0.csv', parse_dates=['date'])
        snotel_L0 = snotel_L0.set_index('date')
        snotel_L0 = snotel_L0.add_suffix('_L0')
        
        #read L0 data
        snotel_L1 = pd.read_csv('Level1_SNOTEL/'+station+'_WY'+str(year)+'_L1.csv', parse_dates=['date'])
        snotel_L1 = snotel_L1.set_index('date')
        snotel_L1 = snotel_L1.add_suffix('_L1')
    
        #read daily SNOTEL data
        snotel_daily = pd.read_csv('SNOTEL_D/sd_' + station + '_WY' + str(year) + '.csv', parse_dates=['Date']) #data is start of day values
        #name columns with unique sd (snotel daily) identifier
        snotel_daily.columns =['date','sd_temp_avg_C','sd_temp_avg_qc','sd_temp_max_C','sd_temp_max_qc','sd_temp_min_C','sd_temp_min_qc','sd_temp_obs_C','sd_temp_obs_qc', 'sd_precip_mm', 'sd_precip_qc', 'sd_precip_24hr_mm','sd_precip_24hr_qc', 'sd_precip_24hrsnowadj_mm','sd_precip_24hradj_qc','sd_depth_cm', 'sd_depth_qc', 'sd_SWE_mm', 'sd_SWE_qc','sd_sm2_pct','sd_sm2_qc','sd_sm8_pct','sd_sm8_qc','sd_sm20_pct','sd_sm20_qc','sd_sm2_avg_pct','sd_sm2_avg_qc','sd_sm8_avg_pct','sd_sm8_avg_qc','sd_sm20_avg_pct','sd_sm20_avg_qc','sd_sm2_max_pct','sd_sm2_max_qc','sd_sm8_max_pct','sd_sm8_max_qc','sd_sm20_max_pct','sd_sm20_max_qc', 'sd_sm2_min_pct','sd_sm2_min_qc','sd_sm8_min_pct','sd_sm8_min_qc','sd_sm20_min_pct','sd_sm20_min_qc','sd_st2_avg_pct','sd_st2_avg_qc','sd_st8_avg_pct','sd_st8_avg_qc','sd_st20_avg_pct','sd_st20_avg_qc','sd_st2_max_pct','sd_st2_max_qc','sd_st8_max_pct','sd_st8_max_qc','sd_st20_max_pct','sd_st20_max_qc','sd_st2_min_pct','sd_st2_min_qc','sd_st8_min_pct','sd_st8_min_qc','sd_st20_min_pct','sd_st20_min_qc','sd_st2_pct','sd_st2_qc','sd_st8_pct','sd_st8_qc','sd_st20_pct','sd_st20_qc','sd_density_pct','sd_density_qc', 'sd_snowrainratio','sd_snowrainratio_qc']
        snotel_daily['date'] = snotel_daily['date'].apply(lambda x: pd.Timestamp(x).replace(hour=0, minute=0, second=0)) #give the daily data a time stamp of midnight
        snotel_daily = snotel_daily.set_index('date').resample('H').interpolate(method ='linear', limit_direction ='backward').drop(['sd_density_pct','sd_density_qc', 'sd_snowrainratio','sd_snowrainratio_qc'], axis=1)
        snotel_daily = snotel_daily.fillna(method = 'ffill') #Apply daily data QC check to each time stamp for automated QC.
        
        #create QC dataframe and reset all indexes to plot later
        df_qc = pd.concat([snotel_L0, snotel_L1, snotel_daily], axis=1)
        df_qc = df_qc.reset_index() 
    
        ##### Level 2 #####
        #### SWE ####
        df_qc['sh_SWE_mm_L2'] = df_qc['sh_SWE_mm_L1']
            # Calculate guides values for dynamic smoothing and manual QC process
        df_qc['sh_SWE_6hmed_mm'] = df_qc['sh_SWE_mm_L2'].rolling(6, center=True, closed='right').median() 
        df_qc['sh_SWE_6hdiff'] = df_qc['sh_SWE_6hmed_mm'].diff() #to fill in manual difference in excell once SWE is verified
        df_qc['sh_SWE_24hmed_mm'] = df_qc.sh_SWE_mm_L2.rolling(24, center=True, closed='right').median() 
        df_qc['sh_SWE_24hdiff'] = df_qc['sh_SWE_24hmed_mm'].diff()
            #Dynamic smoothing and daily data check
        df_qc['sh_SWE_mm_L2'] = df_qc['sh_SWE_6hmed_mm']
        df_qc['sh_SWE_mm_L2'] = np.where((df_qc['sh_SWE_24hdiff'] <= 0) & (df_qc['sd_temp_max_C'] > 7), df_qc['sh_SWE_24hmed_mm'], df_qc['sh_SWE_mm_L2']) #if hourly SWE has no change or is decreasing over 24 hours, apply 24 hr rolling median to smooth diurnal flutter
        df_qc['sh_SWE_mm_L2'] = np.where((df_qc['sd_SWE_mm'].diff() <= 0) & (df_qc['sd_temp_max_C'] > 7) , df_qc['sh_SWE_24hmed_mm'], df_qc['sh_SWE_mm_L2']) #if daily SWE has no change or is decreasing, then apply 24 hr rolling median to smooth diurnal flutter - yes, you need both versions!
        df_qc['sh_SWE_mm_L2'] = np.where((df_qc['sd_temp_max_C'] > 7), df_qc['sh_SWE_24hmed_mm'], df_qc['sh_SWE_mm_L2']) #Smooth diurnal flutter for any day with maximum air temp over 7 °C
        df_qc['sh_SWE_mm_L2'] = np.where((df_qc['sd_SWE_mm'] == 0), 0, df_qc['sh_SWE_mm_L2']) #if daily QC product is 0 then set all hourly data to 0
          #QA/QC Flag
        df_qc['sh_SWE_qc_L2'] = 'E'
        df_qc['sh_SWE_qc_L2'] = np.where((df_qc['sh_SWE_mm_L2'] == np.nan), 'S', df_qc['sh_SWE_qc_L2'])
        df_qc['sh_SWE_qc_L2'] = np.where((df_qc['sh_SWE_mm_L2'].diff() > SWE1hrmax) , 'S', df_qc['sh_SWE_qc_L2'])
        df_qc['sh_SWE_qc_L2'] = np.where((df_qc['sh_SWE_mm_L2'].diff() < SWE1hrmin) , 'S', df_qc['sh_SWE_qc_L2'])
        df_qc['sh_SWE_qc_L2'] = np.where((df_qc['sd_SWE_mm'] > df_qc['sh_SWE_mm_L2']+SWE_tolerance) | (df_qc['sd_SWE_mm'] < df_qc['sh_SWE_mm_L2']-SWE_tolerance) , 'S', df_qc['sh_SWE_qc_L2'])
        df_qc['sh_SWE_qa_L2'] = 'L2' #Flag data QA as passing automated QC
    
        #### Snow Depth ####
        df_qc['sh_snowdepth_cm_L2'] = df_qc['sh_snowdepth_cm_L1']
            #Calculate median values for manual QC
        df_qc['sh_snowdepth_6hmed_cm'] = df_qc.sh_snowdepth_cm_L2.rolling(6, center=True, closed='right').median()
        df_qc['sh_snowdepth_6hdiff'] = df_qc['sh_snowdepth_6hmed_cm'].diff()
        df_qc['sh_snowdepth_12hmed_cm'] = df_qc.sh_snowdepth_cm_L2.rolling(12, center=True, closed='right').median()
        df_qc['sh_snowdepth_12hdiff'] = df_qc['sh_snowdepth_12hmed_cm'].diff()
        df_qc['sh_snowdepth_24hmed_cm'] = df_qc.sh_snowdepth_cm_L2.rolling(24, center=True, closed='right').median()
        df_qc['sh_snowdepth_24hdiff'] = df_qc['sh_snowdepth_24hmed_cm'].diff()
            #Dynamic smoothing
        df_qc['sh_snowdepth_cm_L2'] = df_qc['sh_snowdepth_cm_L1']
        df_qc['sh_snowdepth_cm_L2'] = np.where((df_qc['sh_snowdepth_24hdiff'] <= 0), df_qc['sh_snowdepth_24hmed_cm'], df_qc['sh_snowdepth_cm_L2']) #no change in depth or compaction/melting then apply 24 hr rolling median to smooth diurnal flutter
        df_qc['sh_snowdepth_cm_L2'] = np.where((df_qc['sd_temp_max_C'] > 7), df_qc['sh_snowdepth_24hmed_cm'], df_qc['sh_snowdepth_cm_L2']) #days with max temp above 7C has no precip according to CSSL findings so smooth diurnal flutter
        df_qc['sh_snowdepth_cm_L2'] = np.where((df_qc['sd_depth_cm'] == 0), 0, df_qc['sh_snowdepth_cm_L2']) #if daily QC product has 0 then set all hourly data to 0
            #QA/QC Flag
        df_qc['sh_snowdepth_qc_L2'] = np.where((df_qc['sh_snowdepth_cm_L2'] == np.nan), 'S', df_qc['sh_snowdepth_qc_L1'])
        df_qc['sh_snowdepth_qc_L2'] = np.where((df_qc['sd_depth_cm'] > df_qc['sh_snowdepth_cm_L2']+snowdepth_tolerance) | (df_qc['sd_depth_cm'] < df_qc['sh_snowdepth_cm_L2']-snowdepth_tolerance), 'S', df_qc['sh_snowdepth_qc_L2'])
        df_qc['sh_snowdepth_qa_L2'] = 'L2' #Flag data QA as passing automated QC
    
        #### Precip - EXPERIMENTAL ####
        df_qc['sh_precip_mm_L2'] = df_qc['sh_precip_mm_L1']
          #Calculate median values for manual QC
        df_qc['sh_precip_6hmed_mm'] = df_qc.sh_precip_mm_L2.rolling(6, center=True, closed='right').median()
        df_qc['sh_precip_6hrdiff'] = df_qc['sh_precip_6hmed_mm'].diff() 
        df_qc['sh_precip_12hmed_mm'] = df_qc.sh_precip_mm_L2.rolling(12, center=True, closed='right').median()
        df_qc['sh_precip_12hrdiff'] = df_qc['sh_precip_12hmed_mm'].diff() 
        df_qc['sh_precip_24hmed_mm'] = df_qc.sh_precip_mm_L2.rolling(24, center=True, closed='right').median()
        df_qc['sh_precip_24hrdiff'] = df_qc['sh_precip_24hmed_mm'].diff() 
            #Dynamic smoothing
        df_qc['sh_precip_mm_L2'] = df_qc['sh_precip_12hmed_mm'] 
        df_qc['sh_precip_mm_L2'] = np.where((df_qc['sh_precip_24hrdiff'] <= 0), df_qc['sh_precip_24hmed_mm'], df_qc['sh_precip_mm_L2']) #no change in precip or sligth decrease from temp swing then apply 24 hr rolling median to smooth diurnal flutter
        df_qc['sh_precip_mm_L2'] = np.where((df_qc['sd_temp_max_C'] > 7), df_qc['sh_precip_24hmed_mm'], df_qc['sh_precip_mm_L2']) #days with max temp above 7C has no precip according to CSSL findings so smooth diurnal flutter
        df_qc['sh_precip_mm_L2'] = np.where((df_qc['sd_precip_mm'] == 0), 0, df_qc['sh_precip_mm_L2']) #if daily QC product has 0 then set all hourly data to 0
        df_qc['sh_precip_mm_L2'] = df_qc['sh_precip_mm_L2'].diff() #treat data as 1 hour incremental data to select when to use precip data or use SWE data
        df_qc['sh_precip_mm_L2'] = np.where((df_qc['sd_precip_mm'].diff(72) == 0), 0, df_qc['sh_precip_mm_L2'])
        df_qc['sh_precip_mm_L2'] = np.where((df_qc['sh_precip_mm_L2'] < -5), 0, df_qc['sh_precip_mm_L2'])
        df_qc['sh_precip_mm_L2'] = np.where((df_qc['sh_precip_mm_L2'] > 150), 0, df_qc['sh_precip_mm_L2'])
        df_qc['sh_precip_mm_L2'] = df_qc['sh_precip_mm_L2'].cumsum() #add it all up
        df_qc['sh_precip_mm_L2'] = np.where((df_qc['sh_precip_mm_L2'] < 0), 0, df_qc['sh_precip_mm_L2'])
            #QA/QC Flag
        df_qc['sh_precip_qc_L2'] = 'E'
        df_qc['sh_precip_qc_L2'] = np.where((df_qc['sh_precip_mm_L2'] == np.nan), 'S', df_qc['sh_precip_qc_L2'])
        df_qc['sh_precip_qc_L2'] = np.where((df_qc['sd_precip_mm'] < df_qc['sh_precip_mm_L2']+precip_tolerance) | (df_qc['sd_precip_mm'] > df_qc['sh_precip_mm_L2']-precip_tolerance), 'A', df_qc['sh_precip_qc_L2'])
        df_qc['sh_precip_qc_L2'] = np.where((df_qc['sd_precip_mm'] > df_qc['sh_precip_mm_L2']+precip_tolerance) | (df_qc['sd_precip_mm'] < df_qc['sh_precip_mm_L2']-precip_tolerance), 'S', df_qc['sh_precip_qc_L2'])
        df_qc['sh_precip_qc_L2'] = np.where((df_qc['sh_precip_mm_L2'].diff() < precip1hrmin), 'S', df_qc['sh_precip_qc_L2'])
        df_qc['sh_precip_qc_L2'] = np.where((df_qc['sh_precip_mm_L2'].diff() > precip1hrmax), 'S', df_qc['sh_precip_qc_L2'])
        df_qc['sh_precip_qa_L2'] = 'L2' #Flag data QA as passing automated QC
    
        #### Temperature ####
        df_qc['sh_temp_C_L2'] = df_qc['sh_temp_C_L1']
            #QA/QC Flag
        df_qc['sh_temp_qc_L2'] = df_qc['sh_temp_qc_L1']
        df_qc['sh_temp_qa_L2'] = 'L2'
    
        #### Soil Moisture ####
        df_qc['sh_sm2_pct_L2'] = df_qc['sh_sm2_pct_L1'] #already QC'd by NRCS
        df_qc['sh_sm8_pct_L2'] = df_qc['sh_sm8_pct_L1'] #already QC'd by NRCS
        df_qc['sh_sm20_pct_L2'] = df_qc['sh_sm20_pct_L1'] #already QC'd by NRCS
        df_qc['sh_sm2_qc_L2'] = 'V' 
        df_qc['sh_sm8_qc_L2'] = 'V' 
        df_qc['sh_sm20_qc_L2'] = 'V' 
        df_qc['sh_sm2_qa_L2'] = 'L3' 
        df_qc['sh_sm8_qa_L2'] = 'L3' 
        df_qc['sh_sm20_qa_L2'] = 'L3' 
    
        #### Soil Temperature ####
        df_qc['sh_st2_C_L2'] = df_qc['sh_st2_C_L1'] #already QC'd by NRCS
        df_qc['sh_st8_C_L2'] = df_qc['sh_st8_C_L1'] #already QC'd by NRCS
        df_qc['sh_st20_C_L2'] = df_qc['sh_st20_C_L1'] #already QC'd by NRCS
        df_qc['sh_st2_qc_L2'] = 'V' 
        df_qc['sh_st8_qc_L2'] = 'V' 
        df_qc['sh_st20_qc_L2'] = 'V' 
        df_qc['sh_st2_qa_L2'] = 'L3' 
        df_qc['sh_st8_qa_L2'] = 'L3' 
        df_qc['sh_st20_qa_L2'] = 'L3' 
        
        # Verify QC Flag for data
        df_qc['sh_SWE_qc_L2'] = np.where((df_qc['sh_SWE_mm_L0'] == df_qc['sh_SWE_mm_L2']) & (df_qc['sh_SWE_qc_L2']!="S"), df_qc['sh_SWE_qc_L0'], df_qc['sh_SWE_qc_L2'])
        df_qc['sh_snowdepth_qc_L2'] = np.where((df_qc['sh_snowdepth_cm_L0'] == df_qc['sh_snowdepth_cm_L2']) & (df_qc['sh_snowdepth_qc_L2']!="S"), df_qc['sh_snowdepth_qc_L0'], df_qc['sh_snowdepth_qc_L2'])
        df_qc['sh_precip_qc_L2'] = np.where((df_qc['sh_precip_mm_L0'] == df_qc['sh_precip_mm_L2']) & (df_qc['sh_precip_qc_L2']!="S"), df_qc['sh_precip_qc_L0'], df_qc['sh_precip_qc_L2'])

    
        #Create Level 2 Data
        level2 = copy.deepcopy(df_qc)
        level2 = level2.round(1) #round to one decimal
        level2 =level2[['date','sh_SWE_mm_L2', 'sh_SWE_qc_L2','sh_SWE_qa_L2','sh_snowdepth_cm_L2', 'sh_snowdepth_qc_L2', 'sh_snowdepth_qa_L2','sh_precip_mm_L2', 'sh_precip_qc_L2', 'sh_precip_qa_L2',
                        'sh_temp_C_L2', 'sh_temp_qc_L2', 'sh_temp_qa_L2','sh_sm2_pct_L2', 'sh_sm2_qc_L2','sh_sm2_qa_L2','sh_sm8_pct_L2', 'sh_sm8_qc_L2','sh_sm8_qa_L2','sh_sm20_pct_L2', 'sh_sm20_qc_L2','sh_sm20_qa_L2',
                        'sh_st2_C_L2', 'sh_st2_qc_L2','sh_st2_qa_L2', 'sh_st8_C_L2', 'sh_st8_qc_L2','sh_st8_qa_L2','sh_st20_C_L2', 'sh_st20_qc_L2', 'sh_st20_qa_L2']]
        level2.columns = ['date','sh_SWE_mm', 'sh_SWE_qc','sh_SWE_qa','sh_snowdepth_cm', 'sh_snowdepth_qc', 'sh_snowdepth_qa','sh_precip_mm', 'sh_precip_qc', 'sh_precip_qa',
                        'sh_temp_C', 'sh_temp_qc', 'sh_temp_qa','sh_sm2_pct', 'sh_sm2_qc','sh_sm2_qa','sh_sm8_pct', 'sh_sm8_qc','sh_sm8_qa','sh_sm20_pct', 'sh_sm20_qc','sh_sm20_qa',
                        'sh_st2_C', 'sh_st2_qc','sh_st2_qa', 'sh_st8_C', 'sh_st8_qc','sh_st8_qa','sh_st20_C', 'sh_st20_qc', 'sh_st20_qa']
        level2 = level2.set_index('date')
    
        # Export
        level2.to_csv('Level2_SNOTEL/'+station+'_WY'+str(year)+'_L2.csv')
    
        # PLOT DATA
        df_qc['density'] = df_qc['sh_SWE_mm_L2']/df_qc['sh_snowdepth_cm_L2']*10
    
        # IDENTIFY SUSPECT DATA
        level2 = level2.reset_index()
        L2_swe = level2.loc[(level2['sh_SWE_qc']== "S")]
        L2_depth = level2.loc[(level2['sh_snowdepth_qc'] == "S")]
        L2_precip = level2.loc[(level2['sh_precip_qc']== "S")]
    
        fig = go.Figure()
    
        #SWE
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sd_SWE_mm'], line=dict(color='cornflowerblue'), opacity=0.5,name='SD SWE', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sh_SWE_mm_L0'], line=dict(color='cornflowerblue'), opacity=0.25,name='L0 SWE', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_SWE_mm_L1'], line=dict(color='cornflowerblue'), opacity = 0.35, name='L1 SWE', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_SWE_mm_L2'], line=dict(color='hotpink'), opacity = 0.35, name='L2 SWE', yaxis='y1'))
        fig.add_trace(go.Scatter(mode = 'markers', x=L2_swe['date'],y=L2_swe['sh_SWE_mm'], line=dict(color='hotpink'), opacity = 0.8, name='L2 SWE S', yaxis='y1'))
    
        # Depth
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sd_depth_cm'], line=dict(color='darkolivegreen'), opacity=0.5,name='SD depth', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sh_snowdepth_cm_L0'], line=dict(color='darkolivegreen'), opacity=0.25,name='L0 depth', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sh_snowdepth_cm_L1'], line=dict(color='darkolivegreen'), opacity=0.35, name='L1 depth', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_snowdepth_cm_L2'], line=dict(color='hotpink'), opacity = 0.35, name='L2 depth', yaxis='y1'))
        fig.add_trace(go.Scatter(mode = 'markers', x=L2_depth['date'],y=L2_depth['sh_snowdepth_cm'], line=dict(color='hotpink'), opacity = 0.8, name='L2 depth S', yaxis='y1'))
    
        #Density
        fig.add_trace(go.Scatter(mode='markers', x=df_qc['date'],y=df_qc['density'], marker=dict(color='lightgrey', symbol='cross', size=5), name='L2 density', yaxis='y2'))
    
        #Precip
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sd_precip_mm'], line=dict(color='teal'), opacity=0.5, name='SD precip', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sh_precip_mm_L0'], line=dict(color='teal'), opacity=0.25, name='L0 precip', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_precip_mm_L1'], line=dict(color='teal'), opacity=0.35, name='L1 precip', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_precip_mm_L2'], line=dict(color='hotpink'), opacity = 0.35, name='L2 precip', yaxis='y1'))
        fig.add_trace(go.Scatter(mode = 'markers', x=L2_precip['date'],y=L2_precip['sh_precip_mm'], line=dict(color='hotpink'), opacity = 0.8, name='L2 Precip S', yaxis='y1'))
    
        #Temp
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_temp_C_L2'], line=dict(color='lightcoral'), name='L3 temp', yaxis='y2'))
    
        # Soil Moistrue
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_sm2_pct_L2'], line=dict(color='sandybrown'), name='L3 sm2', yaxis='y2'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_sm8_pct_L2'], line=dict(color='chocolate'), name='L3 sm8', yaxis='y2'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_sm20_pct_L2'], line=dict(color='saddlebrown'), name='L3 sm20', yaxis='y2'))
    
        #Soil Temperature
        fig.add_trace(go.Scatter( x=df_qc['date'],y=df_qc['sh_st2_C_L2'], line=dict(color='lightgrey'), name='L3 st2', yaxis='y2'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_st8_C_L2'], line=dict(color='darkgrey'), name='L3 st8', yaxis='y2'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_st20_C_L2'],  line=dict(color='dimgrey'), name='L3 st20', yaxis='y2'))
        
        fig.update_layout(
            title=station,
            # xaxis_title='X Axis Title',
            yaxis=dict(title='SWE (mm) / Precip (mm) / Depth (cm)'),
            yaxis2=dict(title='Temp (C) / Soil Moistuce (%)', overlaying='y', side='right'),
            legend_title='Legend',
            plot_bgcolor = '#FBFBFB',
        )
        fig.show()

#%%
        ##### LEVEL 2 for manual QC process #####
        #### ONLY RUN ONCE! ###
        #comment out and run if you want to create a file for manual QC    
        level2QC = copy.deepcopy(df_qc)
        level2QC = level2QC.round(1) #round to one decimal
        level2QC['sh_SWE_L2diff'] = level2QC['sh_SWE_mm_L2'].diff()
        level2QC['sh_snowdepth_L2diff'] = level2QC['sh_snowdepth_cm_L2'].diff()
        level2QC['sh_precip_diff'] = level2QC['sh_precip_mm_L0'].diff()
        level2QC['sh_precip_L2diff'] = level2QC['sh_precip_mm_L2'].diff()
        # add level 3 data to manually edit in excel 
        level2QC['sh_SWE_mm_L3'] = level2QC['sh_SWE_mm_L2']
        level2QC['sh_precip_mm_L3'] = level2QC['sh_precip_mm_L2']
        level2QC['sh_snowdepth_cm_L3'] = level2QC['sh_snowdepth_cm_L2']
        
        level2QC = level2QC[['date', 'sh_SWE_mm_L0', 'sh_SWE_qc_L0', 'sh_SWE_6hmed_mm', 'sh_SWE_6hdiff', 'sh_SWE_24hmed_mm', 'sh_SWE_24hdiff', 'sh_SWE_mm_L2','sh_SWE_L2diff', 'sh_SWE_mm_L2',  'sh_SWE_qc_L2', 'sh_SWE_qa_L2', 
                            'sh_snowdepth_cm_L0', 'sh_snowdepth_qc_L0', 'sh_snowdepth_6hmed_cm', 'sh_snowdepth_12hmed_cm', 'sh_snowdepth_24hmed_cm', 'sh_snowdepth_cm_L2', 'sh_snowdepth_cm_L3', 'sh_snowdepth_qc_L2', 'sh_snowdepth_qa_L2', 
                            'sh_precip_mm_L0', 'sh_precip_diff','sh_precip_qc_L0', 'sh_precip_6hmed_mm', 'sh_precip_6hrdiff','sh_precip_24hmed_mm', 'sh_precip_24hrdiff', 'sh_precip_mm_L2', 'sh_precip_L2diff', 'sh_precip_mm_L3', 'sh_precip_qc_L2', 'sh_precip_qa_L2', 
                            'sh_temp_C_L2', 'sh_temp_qc_L2', 'sh_temp_qa_L2',
                            'sh_sm2_pct_L2', 'sh_sm2_qc_L2','sh_sm2_qa_L2','sh_sm8_pct_L2', 'sh_sm8_qc_L2','sh_sm8_qa_L2','sh_sm20_pct_L2', 'sh_sm20_qc_L2','sh_sm20_qa_L2',
                            'sh_st2_C_L2', 'sh_st2_qc_L2','sh_st2_qa_L2', 'sh_st8_C_L2', 'sh_st8_qc_L2','sh_st8_qa_L2','sh_st20_C_L2', 'sh_st20_qc_L2', 'sh_st20_qa_L2']]
       
        level2QC.columns = ['date', 'sh_SWE_mm', 'sh_SWE_qc','sh_SWE_6hmed_mm', 'sh_SWE_6hdiff', 'sh_SWE_24hmed_mm', 'sh_SWE_24hdiff', 'sh_SWE_mm_L2','sh_SWE_L2diff', 'sh_SWE_mm_L3',  'sh_SWE_qc_L3', 'sh_SWE_qa_L3', 
                            'sh_snowdepth_cm', 'sh_snowdepth_qc', 'sh_snowdepth_6hmed_cm', 'sh_snowdepth_12hmed_cm', 'sh_snowdepth_24hmed_cm', 'sh_snowdepth_cm_L2', 'sh_snowdepth_cm_L3', 'sh_snowdepth_qc_L3', 'sh_snowdepth_qa_L3', 
                            'sh_precip_mm', 'sh_precip_diff', 'sh_precip_qc', 'sh_precip_6hmed_mm', 'sh_precip_6hrdiff', 'sh_precip_24hmed_mm', 'sh_precip_24hrdiff', 'sh_precip_mm_L2', 'sh_precip_L2diff', 'sh_precip_mm_L3', 'sh_precip_qc_L3', 'sh_precip_qa_L3', 
                            'sh_temp_C_L3', 'sh_temp_qc_L3', 'sh_temp_qa_L3',
                            'sh_sm2_pct_L3', 'sh_sm2_qc_L3','sh_sm2_qa_L3','sh_sm8_pct_L3', 'sh_sm8_qc_L3','sh_sm8_qa_L3','sh_sm20_pct_L3', 'sh_sm20_qc_L3','sh_sm20_qa_L3',
                            'sh_st2_C_L3', 'sh_st2_qc_L3','sh_st2_qa_L3', 'sh_st8_C_L3', 'sh_st8_qc_L3','sh_st8_qa_L3','sh_st20_C_L3', 'sh_st20_qc_L3', 'sh_st20_qa_L3']
    
        level2QC = level2QC.set_index('date')
        # export
        level2QC.to_csv('/Users/anne/OneDrive/Data/Level2QC_SNOTEL/'+station+'_WY'+str(year)+'_L2QC.csv')
