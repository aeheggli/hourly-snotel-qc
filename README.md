# hourly-snotel-qc

This workflow build on STAR★Methods published in Heggli et al., 2022 (https://doi.org/10.1016/j.isci.2022.104240). The code published here is free to use, but please cite the origional paper with the peer reviewed STAR★Methods when using the data or this code. This code reflects improvements to the original code and was presented at the 2023 Western Snow Conference. 

Data can be found on Zenodo: 10.5281/zenodo.7820056

PRIOR TO USE PLEASE UNDERSTAND:
The temperature parameter incorporates the NOAA9 9th order polynomial bias correction issued by the NRCS in the Level 1 data process. 
The code includes an experimental precipitation QC process that should be used with an abundance of caution as precipitation gauges experience snow plugs that can result in entire snowfall events being missed for days to weeks on end.
This is an evolving workflow that is a step towards improving the quality of hourly SNOTEL data. I do expect to improve upon these methods in the coming years and I hope that others will collaborate to improve the code and process so that we may all be able to make use of the rich data set. 
This data process is not an official product of the NRCS and should not be reflected as one in any research. It is just one method to make use of the SNOTEL network data.

HOW TO USE THE CODE:
These files are designed to be used consecutively. 
First, use the DownloadSNOTEL file to download hourly and daily SNOTEL data from the stations and water years of interest. 
Second, use the SNOTEL_L0_QC file to remove the daily QC'd value in the midnight stamps.
Third, use the SNOTEL_L1_L2_QC file to automate the Level 1 and Level 2 process. 

If you wish to clean the data manually (Level 3), don't hesitate to get in touch with anne.heggli@dri.edu for the Level 3 process. I am happy to share and help, but it is a bit complicated so I would prefer to walk anyone through my methods if they would like to use them. 

QA & QC FLAGS:
  Flag : Name : Description
Quality Assurance (QA) Flags
  R : Raw         : No Human Review
  F : Flagged	    : Automated QC Flag Assigned
  P : Provisional : Preliminary Human Review
  A : Approved    : Processing and Final Review Completed
Quality Control (QC) Flags
  V : Valid   : Valid observed value
  E : Edit    : Edit existing value
  S : Suspect : Suspect value
