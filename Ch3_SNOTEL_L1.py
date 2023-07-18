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

stationid = ['428','356','778']
# stationid = [
#             # #CA
#             # '301', '356', '391','446','462','463','473','428','508','518','539','540','541','574','575','587','633','697','724', '771','784','778','809','834','846','848','977','1049','1050','1051','1052','1067', 
#             # '1258', '1277', #2017
#             # #NV
#             # '321','334', '336','337','340','373','417','443','445','453','454','476','498','503','527','548', '569','570','573','615','652','698','746','750','811','849','1006',
#             # '1110','1111','1112' #2008
#             # '1136' # 2009
#             # '1147', '2170' #2010
#             # '1137','1152','1155','1194','1195', #2011
#             # '1242','1243','1244', #2013
#             # '1262', #2015
#             # '1258', #2017
#             # '1272' # 2018
#             ]

    
SWE_tolerance = 25.4 #mm 1"
snowdepth_tolerance = 15.24 #cm 6"
precip_tolerance = 25.4 #mm 1"

for station in stationid:  
    #max and min values for station POR
    por_SWE = pd.read_csv('SNOTELmetadata/Snow Water Equivalent Water Year Peak for 2023.csv') # https://www.nrcs.usda.gov/wps/portal/wcc/home/quicklinks/imap#version=167&elements=&networks=SNTL&states=!&counties=!&hucs=&minElevation=&maxElevation=&elementSelectType=all&activeOnly=true&activeForecastPointsOnly=false&hucLabels=false&hucIdLabels=false&hucParameterLabels=false&stationLabels=&overlays=&hucOverlays=&basinOpacity=75&basinNoDataOpacity=25&basemapOpacity=100&maskOpacity=0&mode=data&openSections=dataElement,parameter,date,basin,options,elements,location,networks,labels,stationList&controlsOpen=true&popup=&popupMulti=&popupBasin=&base=esriNgwm&displayType=station&basinType=6&dataElement=WTEQP&depth=-8&parameter=MAX&frequency=DAILY&duration=I&customDuration=&dayPart=B&monthPart=E&forecastPubDay=1&forecastExceedance=50&useMixedPast=true&seqColor=1&divColor=3&scaleType=D&scaleMin=&scaleMax=&referencePeriodType=POR&referenceBegin=1981&referenceEnd=2010&minimumYears=5&hucAssociations=true&relativeDate=0&lat=42.715&lon=-116.862&zoom=6.0
    por_depth = pd.read_csv('SNOTELmetadata/Snow Depth Water Year Peak for 2023.csv') # https://www.nrcs.usda.gov/wps/portal/wcc/home/quicklinks/imap#version=167&elements=&networks=SNTL&states=!&counties=!&hucs=&minElevation=&maxElevation=&elementSelectType=all&activeOnly=true&activeForecastPointsOnly=false&hucLabels=false&hucIdLabels=false&hucParameterLabels=false&stationLabels=&overlays=&hucOverlays=&basinOpacity=75&basinNoDataOpacity=25&basemapOpacity=100&maskOpacity=0&mode=data&openSections=dataElement,parameter,date,basin,options,elements,location,networks,labels,stationList&controlsOpen=true&popup=&popupMulti=&popupBasin=&base=esriNgwm&displayType=station&basinType=6&dataElement=SNWDP&depth=-8&parameter=MAX&frequency=DAILY&duration=I&customDuration=&dayPart=B&monthPart=E&forecastPubDay=1&forecastExceedance=50&useMixedPast=true&seqColor=1&divColor=3&scaleType=D&scaleMin=&scaleMax=&referencePeriodType=POR&referenceBegin=1981&referenceEnd=2010&minimumYears=5&hucAssociations=true&relativeDate=0&lat=42.715&lon=-116.862&zoom=6.0
    por_precip = pd.read_csv('SNOTELmetadata/365 day Precipitation October 1, 2021 through September 30, 2022.csv') # https://www.nrcs.usda.gov/wps/portal/wcc/home/quicklinks/imap#version=167&elements=&networks=SNTL&states=!&counties=!&hucs=&minElevation=&maxElevation=&elementSelectType=all&activeOnly=true&activeForecastPointsOnly=false&hucLabels=false&hucIdLabels=false&hucParameterLabels=false&stationLabels=&overlays=&hucOverlays=&basinOpacity=75&basinNoDataOpacity=25&basemapOpacity=100&maskOpacity=0&mode=data&openSections=dataElement,parameter,date,basin,options,elements,location,networks,labels,stationList&controlsOpen=true&popup=&popupMulti=&popupBasin=&base=esriNgwm&displayType=station&basinType=6&dataElement=PREC&depth=-8&parameter=MAX&frequency=DAILY&duration=custom&customDuration=365&dayPart=B&monthPart=E&forecastPubDay=1&forecastExceedance=50&useMixedPast=true&seqColor=1&divColor=3&scaleType=D&scaleMin=&scaleMax=&referencePeriodType=POR&referenceBegin=1981&referenceEnd=2010&minimumYears=5&hucAssociations=true&relativeDate=-241&lat=51.041&lon=-111.577&zoom=5.0
    por_SWE = por_SWE.loc[por_SWE['ID'] == int(station)]
    por_depth = por_depth.loc[por_depth['ID'] == int(station)]
    por_precip = por_precip.loc[por_precip['ID'] == int(station)]
    
    SWEmax = (int(por_SWE['Maximum_POR_inches'])*25.4) #mm
    SWEmin = 0  #mm 
    SWE1hrmax = 25.4 #mm
    SWE1hrmin = -25.4  #mm
    depthmax = (int(por_depth['Maximum_POR_inches'])*2.54) #cm
    depthmin = 0 #cm
    depth1hrmax = 20 #cm
    depth1hrmin = -20 #cm
    precipseasonmax = int(por_precip['Maximum_POR_inches'])*25.4 #mm
    precipseasonmin = 0 #mm
    precip1hrmax = 25.4 #mm/hr # gets rid of major spikes but keeps some snow plugs
    precip1hrmin = -5 #mm/hr #
    # tempmax = int(por['air_temp_max'])
    # tempmin = int(por['air_temp_min'])

    for year in range(2023, 2024): # this loops i through from WYstart (included) to WYend (not included) in 1 year chunks
        #read L0 data
        snotel_L0 = pd.read_csv('Level0_SNOTEL/'+station+'_WY'+str(year)+'_L0.csv', parse_dates=['date'])
        snotel_L0 = snotel_L0.set_index('date')
        
        #read daily SNOTEL data
        snotel_daily = pd.read_csv('SNOTEL_D/sd_' + station + '_WY' + str(year) + '.csv', parse_dates=['Date']) #data is start of day values
        #name columns with unique sd (snotel daily) identifier
        snotel_daily.columns =['date','sd_temp_avg_C','sd_temp_avg_qc','sd_temp_max_C','sd_temp_max_qc','sd_temp_min_C','sd_temp_min_qc','sd_temp_obs_C','sd_temp_obs_qc', 'sd_precip_mm', 'sd_precip_qc', 'sd_precip_24hr_mm','sd_precip_24hr_qc', 'sd_precip_24hrsnowadj_mm','sd_precip_24hradj_qc','sd_depth_cm', 'sd_depth_qc', 'sd_SWE_mm', 'sd_SWE_qc','sd_sm2_pct','sd_sm2_qc','sd_sm8_pct','sd_sm8_qc','sd_sm20_pct','sd_sm20_qc','sd_sm2_avg_pct','sd_sm2_avg_qc','sd_sm8_avg_pct','sd_sm8_avg_qc','sd_sm20_avg_pct','sd_sm20_avg_qc','sd_sm2_max_pct','sd_sm2_max_qc','sd_sm8_max_pct','sd_sm8_max_qc','sd_sm20_max_pct','sd_sm20_max_qc', 'sd_sm2_min_pct','sd_sm2_min_qc','sd_sm8_min_pct','sd_sm8_min_qc','sd_sm20_min_pct','sd_sm20_min_qc','sd_st2_avg_pct','sd_st2_avg_qc','sd_st8_avg_pct','sd_st8_avg_qc','sd_st20_avg_pct','sd_st20_avg_qc','sd_st2_max_pct','sd_st2_max_qc','sd_st8_max_pct','sd_st8_max_qc','sd_st20_max_pct','sd_st20_max_qc','sd_st2_min_pct','sd_st2_min_qc','sd_st8_min_pct','sd_st8_min_qc','sd_st20_min_pct','sd_st20_min_qc','sd_st2_pct','sd_st2_qc','sd_st8_pct','sd_st8_qc','sd_st20_pct','sd_st20_qc','sd_density_pct','sd_density_qc', 'sd_snowrainratio','sd_snowrainratio_qc']
        snotel_daily['date'] = snotel_daily['date'].apply(lambda x: pd.Timestamp(x).replace(hour=0, minute=0, second=0)) #give the daily data a time stamp of midnight
        snotel_daily = snotel_daily.set_index('date').resample('H').interpolate(method ='linear', limit_direction ='backward').drop(['sd_density_pct','sd_density_qc', 'sd_snowrainratio','sd_snowrainratio_qc'], axis=1)
        snotel_daily = snotel_daily.fillna(method = 'ffill') #Apply daily data QC check to each time stamp for automated QC.
        
        #create QC dataframe and reset all indexes to plot later
        df_qc = pd.concat([snotel_L0, snotel_daily], axis=1)
        df_qc = df_qc.reset_index()
    
        ##### Level 1 #####
        #### SWE ####
            #Range check
        df_qc['sh_SWE_mm_L1'] = np.where((df_qc['sh_SWE_mm'] < SWEmin), 0, df_qc['sh_SWE_mm'])
        df_qc['sh_SWE_mm_L1'] = np.where((df_qc['sh_SWE_mm_L1'] > SWEmax), np.nan, df_qc['sh_SWE_mm_L1'])
            #Rate of change check
        df_qc['sh_SWE_mm_L1'] = np.where((df_qc['sh_SWE_mm_L1'].diff() > SWE1hrmax) , np.nan, df_qc['sh_SWE_mm_L1'])
        df_qc['sh_SWE_mm_L1'] = np.where((df_qc['sh_SWE_mm_L1'].diff() < SWE1hrmin) , np.nan, df_qc['sh_SWE_mm_L1'])
            #Fill missing data up for up to 24 hours. 
        df_qc['sh_SWE_mm_L1'] = df_qc['sh_SWE_mm_L1'].interpolate(method ='linear', limit_direction ='backward', limit = 24)
            #QC Flag
        df_qc['sh_SWE_qc_L1'] = 'E'
        df_qc['sh_SWE_qc_L1'] = np.where((df_qc['sh_SWE_mm_L1'] == np.nan), 'S', df_qc['sh_SWE_qc'])
        df_qc['sh_SWE_qc_L1'] = np.where((df_qc['sd_SWE_mm'] > df_qc['sh_SWE_mm_L1']+SWE_tolerance) | (df_qc['sd_SWE_mm'] < df_qc['sh_SWE_mm_L1']-SWE_tolerance) , 'S', df_qc['sh_SWE_qc_L1'])
            #QA Flags
        df_qc['sh_SWE_qa_L1'] = 'L1'
    
        #### Snow Depth ####
            #Range check
        df_qc['sh_snowdepth_cm_L1'] = np.where((df_qc['sh_snowdepth_cm'] < depthmin) , 0, df_qc['sh_snowdepth_cm'])
        df_qc['sh_snowdepth_cm_L1'] = np.where((df_qc['sh_snowdepth_cm'] > depthmax) , np.nan, df_qc['sh_snowdepth_cm_L1'])
            #Fill missing data up for up to 24 hours. 
        df_qc['sh_snowdepth_cm_L1'] = df_qc['sh_snowdepth_cm_L1'].interpolate(method ='linear', limit_direction ='backward', limit = 24)
            #Rate of change check
        df_qc['sh_snowdepth_cm_L1'] = np.where((df_qc['sh_snowdepth_cm_L1'].diff() > depth1hrmax) , np.nan, df_qc['sh_snowdepth_cm_L1'])
        df_qc['sh_snowdepth_cm_L1'] = np.where((df_qc['sh_snowdepth_cm_L1'].diff() < depth1hrmin) , np.nan, df_qc['sh_snowdepth_cm_L1'])
            # Fill missing data up for up to 24 hours. 
        df_qc['sh_snowdepth_cm_L1'] = df_qc['sh_snowdepth_cm_L1'].interpolate(method ='linear', limit_direction ='backward', limit = 24)
            #QC Flag
        df_qc['sh_snowdepth_qc_L1'] = np.where((df_qc['sh_snowdepth_cm_L1'] == np.nan), 'S', df_qc['sh_snowdepth_qc'])
        df_qc['sh_snowdepth_qc_L1'] = np.where((df_qc['sd_depth_cm'] > df_qc['sh_snowdepth_cm_L1']+snowdepth_tolerance) | (df_qc['sd_depth_cm'] < df_qc['sh_snowdepth_cm_L1']-snowdepth_tolerance), 'S', df_qc['sh_snowdepth_qc_L1'])
            #QA Flags
        df_qc['sh_snowdepth_qa_L1'] = 'L1'
    
        #### Precip - EXPERIMENTAL ####
            #Range check
        df_qc['sh_precip_mm_L1'] = np.where((df_qc['sh_precip_mm'] < precipseasonmin), 0, df_qc['sh_precip_mm'])
        df_qc['sh_precip_mm_L1'] = np.where((df_qc['sh_precip_mm'] > precipseasonmax), np.nan, df_qc['sh_precip_mm_L1'])
            #Fill missing data up for up to 24 hours. 
        df_qc['sh_precip_mm_L1'] = df_qc['sh_precip_mm_L1'].interpolate(method ='linear', limit_direction ='backward', limit = 24)
            #Rate of change check -  no rate of change QC, only flagging because of issues with snow plugs
            #QC Flag
        df_qc['sh_precip_qc_L1'] = np.where((df_qc['sh_precip_mm_L1'] == np.nan), 'S', df_qc['sh_precip_qc'])
        df_qc['sh_precip_qc_L1'] = np.where((df_qc['sh_precip_mm_L1'].diff() > precip1hrmax), 'S', df_qc['sh_precip_qc_L1'])
        df_qc['sh_precip_qc_L1'] = np.where((df_qc['sh_precip_mm_L1'].diff() < precip1hrmin), 'S', df_qc['sh_precip_qc_L1'])
        df_qc['sh_precip_qc_L1'] = np.where((df_qc['sd_precip_mm'] < df_qc['sh_precip_mm_L1']+precip_tolerance) | (df_qc['sd_precip_mm'] > df_qc['sh_precip_mm_L1']-precip_tolerance), 'A', df_qc['sh_precip_qc_L1'])
        df_qc['sh_precip_qc_L1'] = np.where((df_qc['sd_precip_mm'] > df_qc['sh_precip_mm_L1']+precip_tolerance) | (df_qc['sd_precip_mm'] < df_qc['sh_precip_mm_L1']-precip_tolerance), 'S', df_qc['sh_precip_qc_L1'])
          #QA Flags
        df_qc['sh_precip_qa_L1'] = 'L1'
    
        #### Temp ####
            # NOAA9
        df_qc['sh_temp_C_L1'] = 610558.226380138*(((df_qc['sh_temp_C']+65.929))/194.45)**9 - 2056177.65461394*(((df_qc['sh_temp_C']+65.929))/194.45)**8 + 2937046.42906361*(((df_qc['sh_temp_C']+65.929))/194.45)**7 - 2319657.12916417*(((df_qc['sh_temp_C']+65.929))/194.45)**6 + 1111854.33825836*(((df_qc['sh_temp_C']+65.929))/194.45)**5 - 337069.883250001*(((df_qc['sh_temp_C']+65.929))/194.45)**4 + 66105.7015922199*(((df_qc['sh_temp_C']+65.929))/194.45)**3 - 8386.78320604513*(((df_qc['sh_temp_C']+65.929))/194.45)**2 + 824.818021779729*(((df_qc['sh_temp_C']+65.929))/194.45) - 86.7321006757439
        # df_qc['sh_temp_C_L1'] = np.where((df_qc['sh_temp_C_L1'] < tempmin), np.nan, df_qc['sh_temp_C_L1'])
        # df_qc['sh_temp_C_L1'] = np.where((df_qc['sh_temp_C_L1'] > tempmax), np.nan, df_qc['sh_temp_C_L1'])
            #set all values to edited
        df_qc['sh_temp_qc_L1'] = 'E'
            #QC Flag
        # df_qc['sh_temp_qc_L1'] = np.where((df_qc['sh_temp_C_L1'] > tempmax), 'S', df_qc['sh_temp_qc_L1'])
        # df_qc['sh_temp_qc_L1'] = np.where((df_qc['sh_temp_C_L1'] < tempmin), 'S', df_qc['sh_temp_qc_L1'])
        df_qc['sh_temp_qc_L1'] = np.where((df_qc['sh_temp_C_L1'] == np.nan), 'S', df_qc['sh_temp_qc_L1'])
            #QA Flags
        df_qc['sh_temp_qa_L1'] = 'L1'
    
        #### Soil Moisture ####
        df_qc['sh_sm2_pct_L1'] = df_qc['sh_sm2_pct'] #already QCd by NRCS
        df_qc['sh_sm8_pct_L1'] = df_qc['sh_sm8_pct'] #already QC'd by NRCS
        df_qc['sh_sm20_pct_L1'] = df_qc['sh_sm20_pct'] #already QC'd by NRCS
        df_qc['sh_sm2_qc_L1'] = 'V' 
        df_qc['sh_sm8_qc_L1'] = 'V' 
        df_qc['sh_sm20_qc_L1'] = 'V' 
        df_qc['sh_sm2_qa_L1'] = 'L3' 
        df_qc['sh_sm8_qa_L1'] = 'L3' 
        df_qc['sh_sm20_qa_L1'] = 'L3' 
    
        #### Soil Temperature ####
        df_qc['sh_st2_C_L1'] = df_qc['sh_st2_C'] #already QC'd by NRCS
        df_qc['sh_st8_C_L1'] = df_qc['sh_st8_C'] #already QC'd by NRCS
        df_qc['sh_st20_C_L1'] = df_qc['sh_st20_C'] #already QC'd by NRCS
        df_qc['sh_st2_qc_L1'] = 'V' 
        df_qc['sh_st8_qc_L1'] = 'V' 
        df_qc['sh_st20_qc_L1'] = 'V' 
        df_qc['sh_st2_qa_L1'] = 'L3' 
        df_qc['sh_st8_qa_L1'] = 'L3' 
        df_qc['sh_st20_qa_L1'] = 'L3' 
    
        #Verify QC Flag for data
        df_qc['sh_SWE_qc_L1'] = np.where((df_qc['sh_SWE_mm'] == df_qc['sh_SWE_mm_L1']) & (df_qc['sh_SWE_qc_L1']!="S"), df_qc['sh_SWE_qc'], df_qc['sh_SWE_qc_L1'])
        df_qc['sh_snowdepth_qc_L1'] = np.where((df_qc['sh_snowdepth_cm'] == df_qc['sh_snowdepth_cm_L1']) & (df_qc['sh_snowdepth_qc_L1']!="S"), df_qc['sh_snowdepth_qc'], df_qc['sh_snowdepth_qc_L1'])
        df_qc['sh_precip_qc_L1'] = np.where((df_qc['sh_precip_mm'] == df_qc['sh_precip_mm_L1']) & (df_qc['sh_precip_qc_L1']!="S"), df_qc['sh_precip_qc'], df_qc['sh_precip_qc_L1'])
    
        #Create Level 1 Data
        level1 = copy.deepcopy(df_qc)
        level1 = level1.round(1) #round to one decimal
        #select the columns and order of parameters included
        level1 = level1[['date','sh_SWE_mm_L1', 'sh_SWE_qc_L1','sh_SWE_qa_L1',
                         'sh_snowdepth_cm_L1', 'sh_snowdepth_qc_L1', 'sh_snowdepth_qa_L1',
                         'sh_precip_mm_L1', 'sh_precip_qc_L1', 'sh_precip_qa_L1',
                         'sh_temp_C_L1', 'sh_temp_qc_L1', 'sh_temp_qa_L1',
                         'sh_sm2_pct_L1', 'sh_sm2_qc_L1','sh_sm2_qa_L1','sh_sm8_pct_L1', 'sh_sm8_qc_L1','sh_sm8_qa_L1','sh_sm20_pct_L1', 'sh_sm20_qc_L1','sh_sm20_qa_L1',
                         'sh_st2_C_L1', 'sh_st2_qc_L1','sh_st2_qa_L1', 'sh_st8_C_L1', 'sh_st8_qc_L1','sh_st8_qa_L1','sh_st20_C_L1', 'sh_st20_qc_L1', 'sh_st20_qa_L1']]
        #rename the columns so the do not have L1 at the end
        level1.columns=['date','sh_SWE_mm', 'sh_SWE_qc','sh_SWE_qa',
                         'sh_snowdepth_cm', 'sh_snowdepth_qc', 'sh_snowdepth_qa',
                         'sh_precip_mm', 'sh_precip_qc', 'sh_precip_qa',
                         'sh_temp_C', 'sh_temp_qc', 'sh_temp_qa',
                         'sh_sm2_pct', 'sh_sm2_qc','sh_sm2_qa','sh_sm8_pct', 'sh_sm8_qc','sh_sm8_qa','sh_sm20_pct', 'sh_sm20_qc','sh_sm20_qa',
                         'sh_st2_C', 'sh_st2_qc','sh_st2_qa', 'sh_st8_C', 'sh_st8_qc','sh_st8_qa','sh_st20_C', 'sh_st20_qc', 'sh_st20_qa']
        level1 = level1.set_index('date')
        
        
        # Export
        level1.to_csv('Level1_SNOTEL/'+station+'_WY'+str(year)+'_L1.csv')
    
        # PLOT DATA
        df_qc['density'] = df_qc['sh_SWE_mm_L1']/df_qc['sh_snowdepth_cm_L1']*10
    
        # DROP SUSPECT DATA
        level1 = level1.reset_index()
        L1_swe = level1.loc[(level1['sh_SWE_qc']== "S")]
        L1_depth = level1.loc[(level1['sh_snowdepth_qc'] == "S")]
        L1_precip = level1.loc[(level1['sh_precip_qc']== "S")]
    
        fig = go.Figure()
    
        #SWE
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sd_SWE_mm'], line=dict(color='cornflowerblue'), opacity=0.5,name='SD SWE', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sh_SWE_mm'], line=dict(color='cornflowerblue'), opacity=0.25,name='SH SWE', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_SWE_mm_L1'], line=dict(color='cornflowerblue'), opacity = 0.35, name='L1 SWE', yaxis='y1'))
        fig.add_trace(go.Scatter(mode = 'markers', x=L1_swe['date'],y=L1_swe['sh_SWE_mm'], line=dict(color='hotpink'), opacity = 0.8, name='L1 SWE S', yaxis='y1'))
    
        # Depth
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sd_depth_cm'], line=dict(color='darkolivegreen'), opacity=0.5,name='SD depth', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sh_snowdepth_cm'], line=dict(color='darkolivegreen'), opacity=0.25,name='SH depth', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sh_snowdepth_cm_L1'], line=dict(color='darkolivegreen'), opacity=0.35, name='L1 depth', yaxis='y1'))
        fig.add_trace(go.Scatter(mode = 'markers', x=L1_depth['date'],y=L1_depth['sh_snowdepth_cm'], line=dict(color='hotpink'), opacity = 0.8, name='L1 depth S', yaxis='y1'))
    
        #Density
        fig.add_trace(go.Scatter(mode='markers', x=df_qc['date'],y=df_qc['density'], marker=dict(color='lightgrey', symbol='cross', size=5), name='L2 density', yaxis='y2'))
    
        #Precip
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sd_precip_mm'], line=dict(color='teal'), opacity=0.5, name='SD precip', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'], y=df_qc['sh_precip_mm'], line=dict(color='teal'), opacity=0.25, name='SH precip', yaxis='y1'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_precip_mm_L1'], line=dict(color='teal'), opacity=0.35, name='L1 precip', yaxis='y1'))
        fig.add_trace(go.Scatter(mode = 'markers', x=L1_precip['date'],y=L1_precip['sh_precip_mm'], line=dict(color='hotpink'), opacity = 0.8, name='L1 Precip S', yaxis='y1'))
    
        #Temp
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_temp_C_L1'], line=dict(color='lightcoral'), name='L3 temp', yaxis='y2'))
    
        # Soil Moistrue
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_sm2_pct_L1'], line=dict(color='sandybrown'), name='L3 sm2', yaxis='y2'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_sm8_pct_L1'], line=dict(color='chocolate'), name='L3 sm8', yaxis='y2'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_sm20_pct_L1'], line=dict(color='saddlebrown'), name='L3 sm20', yaxis='y2'))
    
        #Soil Temperature
        fig.add_trace(go.Scatter( x=df_qc['date'],y=df_qc['sh_st2_C_L1'], line=dict(color='lightgrey'), name='L3 st2', yaxis='y2'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_st8_C_L1'], line=dict(color='darkgrey'), name='L3 st8', yaxis='y2'))
        fig.add_trace(go.Scatter(x=df_qc['date'],y=df_qc['sh_st20_C_L1'],  line=dict(color='dimgrey'), name='L3 st20', yaxis='y2'))
        
        fig.update_layout(
            title=station,
            # xaxis_title='X Axis Title',
            yaxis=dict(title='SWE (mm) / Precip (mm) / Depth (cm)'),
            yaxis2=dict(title='Temp (C) / Soil Moistuce (%)', overlaying='y', side='right'),
            legend_title='Legend',
            plot_bgcolor = '#FBFBFB',
        )
        fig.show()
        
