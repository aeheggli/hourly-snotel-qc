# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:05:18 2020

@author: Anne Heggli with help from Lauren Bolotin
"""
import csv
import requests
import pandas as pd
import re

station = [
            # '428:CA:SNTL'# ,
            # '356:CA:SNTL' ,'778:CA:SNTL' , #Single station
            '301:CA:SNTL','356:CA:SNTL' , '1051:CA:SNTL','1067:CA:SNTL','391:CA:SNTL','977:CA:SNTL','428:CA:SNTL','446:CA:SNTL','462:CA:SNTL','463:CA:SNTL','473:CA:SNTL','1049:CA:SNTL','1277:CA:SNTL','508:CA:SNTL', '518:CA:SNTL','1050:CA:SNTL','539:CA:SNTL','540:CA:SNTL','541:CA:SNTL','574:CA:SNTL','575:CA:SNTL','587:CA:SNTL','633:CA:SNTL','784:CA:SNTL','697:CA:SNTL','724:CA:SNTL','771:CA:SNTL','778:CA:SNTL', '1258:CA:SNTL','1052:CA:SNTL','809:CA:SNTL','834:CA:SNTL','846:CA:SNTL','848:CA:SNTL',
            '321:NV:SNTL','334:NV:SNTL', '336:NV:SNTL','337:NV:SNTL','340:NV:SNTL','1155:NV:SNTL',
            '1111:NV:SNTL','373:NV:SNTL','1152:NV:SNTL','417:NV:SNTL',
            '443:NV:SNTL','445:NV:SNTL','453:NV:SNTL','454:NV:SNTL','1243:NV:SNTL','476:NV:SNTL','1262:NV:SNTL','1195:NV:SNTL','498:NV:SNTL','503:NV:SNTL','527:NV:SNTL','548:NV:SNTL','549:NV:SNTL','1150:NV:SNTL','569:NV:SNTL','570:NV:SNTL','1310:NV:SNTL','573:NV:SNTL','1112:NV:SNTL','1006:NV:SNTL','1242:NV:SNTL','615:NV:SNTL','1207:NV:SNTL','652:NV:SNTL','1272:NV:SNTL','1244:NV:SNTL','698:NV:SNTL','2170:NV:SNTL','1110:NV:SNTL','746:NV:SNTL','750:NV:SNTL','1194:NV:SNTL','811:NV:SNTL','1136:NV:SNTL','1137:NV:SNTL','849:NV:SNTL','1147:NV:SNTL'
           ]

#California : done through June 5, 2023
# '301:CA:SNTL','356:CA:SNTL' ,'1051:CA:SNTL','1067:CA:SNTL','391:CA:SNTL','977:CA:SNTL','428:CA:SNTL','446:CA:SNTL','462:CA:SNTL','463:CA:SNTL','473:CA:SNTL','1049:CA:SNTL','1277:CA:SNTL','508:CA:SNTL', '518:CA:SNTL','1050:CA:SNTL','539:CA:SNTL','540:CA:SNTL','541:CA:SNTL','574:CA:SNTL','575:CA:SNTL','587:CA:SNTL','633:CA:SNTL','784:CA:SNTL','697:CA:SNTL','724:CA:SNTL','771:CA:SNTL','778:CA:SNTL', '1258:CA:SNTL','1052:CA:SNTL','809:CA:SNTL','834:CA:SNTL','846:CA:SNTL','848:CA:SNTL'

#Nevada : done through June 5, 2023
# '321:NV:SNTL','334:NV:SNTL','336:NV:SNTL','337:NV:SNTL','340:NV:SNTL','1155:NV:SNTL','1111:NV:SNTL','373:NV:SNTL','1152:NV:SNTL','417:NV:SNTL','443:NV:SNTL','445:NV:SNTL','453:NV:SNTL','454:NV:SNTL','1243:NV:SNTL','476:NV:SNTL','1262:NV:SNTL','1195:NV:SNTL','498:NV:SNTL','503:NV:SNTL','527:NV:SNTL','548:NV:SNTL','549:NV:SNTL','1150:NV:SNTL','569:NV:SNTL','570:NV:SNTL','1310:NV:SNTL','573:NV:SNTL','1112:NV:SNTL','1006:NV:SNTL','1242:NV:SNTL','615:NV:SNTL','1207:NV:SNTL','652:NV:SNTL','1272:NV:SNTL','1244:NV:SNTL','698:NV:SNTL','2170:NV:SNTL','1110:NV:SNTL','746:NV:SNTL','750:NV:SNTL','1194:NV:SNTL','811:NV:SNTL','1136:NV:SNTL','1137:NV:SNTL','849:NV:SNTL','1147:NV:SNTL'

#Oregon : 
# '302:OR:SNTL','1000:OR:SNTL','304:OR:SNTL','1166:OR:SNTL','331:OR:SNTL','341:OR:SNTL','343:OR:SNTL','344:OR:SNTL','351:OR:SNTL','357:OR:SNTL','361:OR:SNTL','362:OR:SNTL','388:OR:SNTL','395:OR:SNTL','398:OR:SNTL','401:OR:SNTL','406:OR:SNTL','422:OR:SNTL','1010:OR:SNTL','434:OR:SNTL','440:OR:SNTL','442:OR:SNTL','464:OR:SNTL','470:OR:SNTL','1314:OR:SNTL','477:OR:SNTL','479:OR:SNTL','483:OR:SNTL','945:OR:SNTL','494:OR:SNTL','504:OR:SNTL','523:OR:SNTL','526:OR:SNTL','529:OR:SNTL','1158:OR:SNTL','545:OR:SNTL','552:OR:SNTL','558:OR:SNTL','563:OR:SNTL','584:OR:SNTL','605:OR:SNTL','608:OR:SNTL','614:OR:SNTL','619:OR:SNTL','1079:OR:SNTL','1084:OR:SNTL','647:OR:SNTL','651:OR:SNTL','653:OR:SNTL','655:OR:SNTL','660:OR:SNTL','666:OR:SNTL','671:OR:SNTL','687:OR:SNTL','706:OR:SNTL','710:OR:SNTL','712:OR:SNTL','719:OR:SNTL','721:OR:SNTL','726:OR:SNTL','729:OR:SNTL','733:OR:SNTL','736:OR:SNTL','743:OR:SNTL','745:OR:SNTL','756:OR:SNTL','759:OR:SNTL','1167:OR:SNTL','767:OR:SNTL','925:OR:SNTL','789:OR:SNTL','794:OR:SNTL','800:OR:SNTL','801:OR:SNTL','1078:OR:SNTL','1077:OR:SNTL','810:OR:SNTL','812:OR:SNTL','815:OR:SNTL','821:OR:SNTL','1044:OR:SNTL','873:OR:SNTL'

#Washington : 
# '908:WA:SNTL','990:WA:SNTL','352:WA:SNTL','1080:WA:SNTL','1107:WA:SNTL','375:WA:SNTL','376:WA:SNTL','942:WA:SNTL','1109:WA:SNTL','1085:WA:SNTL','418:WA:SNTL','420:WA:SNTL','943:WA:SNTL','998:WA:SNTL','910:WA:SNTL','478:WA:SNTL','1159:WA:SNTL','1256:WA:SNTL','502:WA:SNTL','507:WA:SNTL','515:WA:SNTL','928:WA:SNTL','1129:WA:SNTL','553:WA:SNTL','591:WA:SNTL','599:WA:SNTL','606:WA:SNTL','1069:WA:SNTL','999:WA:SNTL','897:WA:SNTL','1011:WA:SNTL','642:WA:SNTL','644:WA:SNTL','648:WA:SNTL','898:WA:SNTL','941:WA:SNTL','1126:WA:SNTL','1259:WA:SNTL','672:WA:SNTL','679:WA:SNTL','681:WA:SNTL','1104:WA:SNTL','692:WA:SNTL','1263:WA:SNTL','699:WA:SNTL','702:WA:SNTL','707:WA:SNTL','711:WA:SNTL','911:WA:SNTL','728:WA:SNTL','734:WA:SNTL','1231:WA:SNTL','1068:WA:SNTL','1043:WA:SNTL','748:WA:SNTL','1257:WA:SNTL','912:WA:SNTL','985:WA:SNTL','776:WA:SNTL','777:WA:SNTL','984:WA:SNTL','788:WA:SNTL','791:WA:SNTL','804:WA:SNTL','975:WA:SNTL','1012:WA:SNTL','817:WA:SNTL','899:WA:SNTL','824:WA:SNTL','1171:WA:SNTL','832:WA:SNTL','841:WA:SNTL','974:WA:SNTL','909:WA:SNTL','863:WA:SNTL'

####HOURLY######
#%% Test URL downlaod
#url (needs to be automated)
##Updated URL with all data and QC flags 
url='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultiTimeSeriesGroupByStationReport,metric/hourly/start_of_period/848:CA:SNTL%7Cid=%22%22%7Cname/2016-10-01,2017-09-30/TOBS::value,TOBS::qcFlag,PREC::value,PREC::qcFlag,SNWD::value,SNWD::qcFlag,WTEQ::value,WTEQ::qcFlag,SMS:-2:value,SMS:-2:qcFlag,SMS:-8:value,SMS:-8:qcFlag,SMS:-20:value,SMS:-20:qcFlag,STO:-2:value,STO:-2:qcFlag,STO:-8:value,STO:-8:qcFlag,STO:-20:value,STO:-20:qcFlag?fitToScreen=false'
#Origional URL on attempt 1
# url ='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultiTimeSeriesGroupByStationReport,metric/hourly/start_of_period/428:CA:SNTL%7Cid=%22%22%7Cname/2017-10-01,2018-09-30/TOBS::value,PRCP::value,SNWD::value,WTEQ::value,SMS:-2:value,SMS:-8:value,SMS:-20:value?fitToScreen=false'
with requests.Session() as s:
    download = s.get(url) #downloads

    decoded_content = download.content.decode('utf-8') #decodes
    
    cr = csv.reader(decoded_content.splitlines(), delimiter=',') #splits lines
    my_list = list(cr) #saves to a list
    header_line = my_list[76] #This is the header line. All other lines before are NRCS metadata. May need to change this!!
    header = header_line[1].split('(') # select the second column (after Date) and split at the first ( to separate and numbers in the station name like SNT 848 Ward Creek #3)
    snotel_number=re.sub('[^0-9]','', header[1]) #this strips non numeric characters after the ( to find the snotel number
    path='/Users/anne/OneDrive/Data/SNOTEL_H/sh_'+snotel_number+'WYtest.csv' #this saves using that snotel number
    
    df=pd.DataFrame(data=my_list[77:],columns=header_line) #save list to a dataframe
    # df.to_csv(path,index=False) #save dataframe to a csv

#%% Automate URL
base='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultiTimeSeriesGroupByStationReport,metric/hourly/start_of_period/'

other ='%7Cid=%22%22%7Cname/'
date ='2000-01-01,2001-01-01/' #we will automate this below
#other variables for easy copy and paste:'WTEQ::value,TAVG::value,TMAX::value,TMIN::value,TOBS::value,PREC::value,PRCP::value,PRCPSA::value,SNWD::value,WTEQ::value,WTEQX::value,SMS:-2:value,SMV:-2:value,STO:-2:value,SNDN::value,SNRR::value' #this could be automated to loop through your list or changed manually
variable ='TOBS::value,TOBS::qcFlag,PREC::value,PREC::qcFlag,SNWD::value,SNWD::qcFlag,WTEQ::value,WTEQ::qcFlag,SMS:-2:value,SMS:-2:qcFlag,SMS:-8:value,SMS:-8:qcFlag,SMS:-20:value,SMS:-20:qcFlag,STO:-2:value,STO:-2:qcFlag,STO:-8:value,STO:-8:qcFlag,STO:-20:value,STO:-20:qcFlag'
end ='?fitToScreen=false'
station_count = 0 #which station to pull

for i in range(2022,2023): #this loops i through from WYstart (not included) to WYend (included) in 1 year chunks
    year=str(i) #beginning of period
    year2=str(i+1) #end of period
    for j in range(len(station)): #this loops j through the stations listed above
        station_id=station[j]
        date=year+'-10-01,'+year2+'-09-30/' #make timestamp
        url=base+station_id+other+date+variable+end #string together url
 
    #now we download using code from above!!!
    
        with requests.Session() as s:
            download = s.get(url) #downloads

            decoded_content = download.content.decode('utf-8') #decodes

            cr = csv.reader(decoded_content.splitlines(), delimiter=',') #splits lines
            my_list = list(cr) #saves to a list
            header_line = my_list[76] # This is the header line. All other lines before are NRCS metadata. May need to change this!!
            header = header_line[1].split('(') # select the second column (after Date) and split at the first ( to separate and numbers in the station name like SNT 848 Ward Creek #3)
            snotel_number=re.sub('[^0-9]','', header[1]) #this strips non numeric characters after the ( to find the snotel number
            path='D:/Data/SNOTEL_H/sh_'+snotel_number+'_WY'+year2+'.csv' #this saves using that snotel number

            df=pd.DataFrame(data=my_list[77:],columns=header_line) #save list to a dataframe
            df.to_csv(path, index=False) #save dataframe to a csv


#%%  DAILY
#######Test URL downlaod DAILY#####
#url (needs to be automated)
url='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultiTimeSeriesGroupByStationReport,metric/daily/start_of_period/428:CA:SNTL%7Cid=%22%22%7Cname/2019-04-01,2019-04-30/TAVG::value,TAVG::qcFlag,TMAX::value,TMAX::qcFlag,TMIN::value,TMIN::qcFlag,TOBS::value,TOBS::qcFlag,PREC::value,PREC::qcFlag,PRCP::value,PRCP::qcFlag,PRCPSA::value,PRCPSA::qcFlag,SNWD::value,SNWD::qcFlag,WTEQ::value,WTEQ::qcFlag,SMS:-2:value,SMS:-2:qcFlag,SMS:-8:value,SMS:-8:qcFlag,SMS:-20:value,SMS:-20:qcFlag,SMV:-2:value,SMV:-2:qcFlag,SMV:-8:value,SMV:-8:qcFlag,SMV:-20:value,SMV:-20:qcFlag,SMX:-2:value,SMX:-2:qcFlag,SMX:-8:value,SMX:-8:qcFlag,SMX:-20:value,SMX:-20:qcFlag,SMN:-2:value,SMN:-2:qcFlag,SMN:-8:value,SMN:-8:qcFlag,SMN:-20:value,SMN:-20:qcFlag,STV:-2:value,STV:-2:qcFlag,STV:-8:value,STV:-8:qcFlag,STV:-20:value,STV:-20:qcFlag,STX:-2:value,STX:-2:qcFlag,STX:-8:value,STX:-8:qcFlag,STX:-20:value,STX:-20:qcFlag,STN:-2:value,STN:-2:qcFlag,STN:-8:value,STN:-8:qcFlag,STN:-20:value,STN:-20:qcFlag,STO:-2:value,STO:-2:qcFlag,STO:-8:value,STO:-8:qcFlag,STO:-20:value,STO:-20:qcFlag,SNDN::value,SNDN::qcFlag,SNRR::value,SNRR::qcFlag?fitToScreen=false'
with requests.Session() as s:
    download = s.get(url) #downloads
    decoded_content = download.content.decode('utf-8') #decodes
    cr = csv.reader(decoded_content.splitlines(), delimiter=',') #splits lines
    
    my_list = list(cr) #saves to a list
    header=my_list[127] # This is the header line. All other lines before are NRCS metadata. May need to change this!!
    header = header[1].split('(') # select the second column (after Date) and split at the first ( to separate and numbers in the station name like SNT 848 Ward Creek #3)
    snotel_number=re.sub('[^0-9]','', header[1]) #this strips non numeric characters after the ( to find the snotel number
    path='/Users/anne/OneDrive/Data/SNOTEL_D/sh_'+snotel_number+'_test.csv' #this saves using that snotel number
    
    df=pd.DataFrame(data=my_list[128:],columns=header) #save list to a dataframe
    # df.to_csv(path, index=False) #save dataframe to a csv

#%% Automate URL - daily
base='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultiTimeSeriesGroupByStationReport,metric/daily/start_of_period/'
other ='%7Cid=%22%22%7Cname/'
date ='2000-01-01,2001-01-01/' #we will automate this below
variable ='TAVG::value,TAVG::qcFlag,TMAX::value,TMAX::qcFlag,TMIN::value,TMIN::qcFlag,TOBS::value,TOBS::qcFlag,PREC::value,PREC::qcFlag,PRCP::value,PRCP::qcFlag,PRCPSA::value,PRCPSA::qcFlag,SNWD::value,SNWD::qcFlag,WTEQ::value,WTEQ::qcFlag,SMS:-2:value,SMS:-2:qcFlag,SMS:-8:value,SMS:-8:qcFlag,SMS:-20:value,SMS:-20:qcFlag,SMV:-2:value,SMV:-2:qcFlag,SMV:-8:value,SMV:-8:qcFlag,SMV:-20:value,SMV:-20:qcFlag,SMX:-2:value,SMX:-2:qcFlag,SMX:-8:value,SMX:-8:qcFlag,SMX:-20:value,SMX:-20:qcFlag,SMN:-2:value,SMN:-2:qcFlag,SMN:-8:value,SMN:-8:qcFlag,SMN:-20:value,SMN:-20:qcFlag,STV:-2:value,STV:-2:qcFlag,STV:-8:value,STV:-8:qcFlag,STV:-20:value,STV:-20:qcFlag,STX:-2:value,STX:-2:qcFlag,STX:-8:value,STX:-8:qcFlag,STX:-20:value,STX:-20:qcFlag,STN:-2:value,STN:-2:qcFlag,STN:-8:value,STN:-8:qcFlag,STN:-20:value,STN:-20:qcFlag,STO:-2:value,STO:-2:qcFlag,STO:-8:value,STO:-8:qcFlag,STO:-20:value,STO:-20:qcFlag,SNDN::value,SNDN::qcFlag,SNRR::value,SNRR::qcFlag'
end ='?fitToScreen=false'
station_count = 0 #which station to pull

for i in range(2022,2023): #this loops i through from WYstart (not included) to WYend (included) in 1 year chunks
    year=str(i) #beginning of period
    year2=str(i+1) #end of period
    for j in range(len(station)): #this loops j through the stations listed above
        station_id=station[j]
        date=year+'-10-01,'+year2+'-09-30/' #make timestamp
        url=base+station_id+other+date+variable+end #string together url
 
    #now we download using code from above!!!
    
        with requests.Session() as s:
            download = s.get(url) #downloads

            decoded_content = download.content.decode('utf-8') #decodes

            cr = csv.reader(decoded_content.splitlines(), delimiter=',') #splits lines
            my_list = list(cr) #saves to a list
            header_line = my_list[127] # This is the header line. All other lines before are NRCS metadata. May need to change this!!
            header = header_line[1].split('(') # select the second column (after Date) and split at the first ( to separate and numbers in the station name like SNT 848 Ward Creek #3)
            snotel_number=re.sub('[^0-9]','', header[1]) #this strips non numeric characters after the ( to find the snotel number
            path='D:/Data/SNOTEL_D/sd_'+snotel_number+'_WY'+year2+'.csv' #this saves using that snotel number
            # path='/Users/aheggli/OneDrive/Data/SNOTEL_D/sd_'+snotel_number+'_WY'+year2+'.csv' #this saves using that snotel number


            df=pd.DataFrame(data=my_list[128:],columns=header_line) #save list to a dataframe
            df.to_csv(path, index=False) #save dataframe to a csv
