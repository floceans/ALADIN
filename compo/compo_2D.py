#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import netCDF4 as nc
import scipy.stats as stats

#import matplotlib.pyplot as plt
#from matplotlib import ticker, cm

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

print("ok")
yearmin = 2001
yearmax = 2010

data = {}
nstorm = 0

data_name="tas"


RADIUS = 600    # Distance au centre des bords du domaine

LARG=int(RADIUS/20)


###################################################
# Plotting tracks 

# Some configuration for the plot
# longitude must be within 0 and 360

domain = 'ATL'
#domain = 'EP'
#domain = 'NI'
#domain = 'SI'

path_track = "../tracks/"+domain+"/"
path_data="/scratch/work/rigoudyg/TP_ALADIN/2025/ANTILLES-12-BS-10ans/outputs/assembled/"
#path_data="/scratch/work/rigoudyg/TP_ALADIN/2025/INDN12-SC-10/outputs/assembled/"
#path_data="/scratch/work/rigoudyg/TP_ALADIN/2025/IOML12V2/outputs/assembled/"
#path_data="/scratch/work/rigoudyg/TP_ALADIN/2025/PNE12-KE-10/outputs/assembled/"
path_cmp="../compo/"+domain+"/"


if domain == 'EP':
    clon = -140 # Map center
    lonmin = -171
    lonmax = -108 # Tricks for the longitude labels
    latmin = 7
    latmax = 28
    
    lonlabels = [190, 200, 210, 220, 230, 240, 250] # Tricks for the longitude labels
    latlabels = [10, 15, 20, 25, 30]
    
elif domain == 'NI':
    clon = 90
    lonmin = 69
    lonmax = 110
    latmin = 6
    latmax = 27
    
    lonlabels = [70, 80, 90, 100, 110]
    latlabels = [10, 15, 20, 25, 30]
    
elif domain == 'SI':
    clon = 55
    lonmin = 33
    lonmax = 76
    latmin = -34
    latmax = -3
    
    lonlabels = [35, 40, 45, 50, 55, 60, 65, 70, 75 ]
    latlabels = [-40, -30, -20, -10, 0]
    
elif domain == 'ATL':
    clon = 0
    lonmin = 280
    lonmax = 330
    latmin = 8
    latmax = 30
    
    lonlabels = [280, 290, 300, 310, 320, 330]
    latlabels = [10, 15, 20, 25, 30]

_FillValue=1.e+20
cmp=np.empty([10000,2*LARG+1,2*LARG+1])
cmp[:,:,:]=_FillValue


irec=0
for year in range(yearmin,yearmax): 
  print(year)
  yp1=year+1
#  Reading track
  data={}
  data['time'] = []
  data['lat'] = []
  data['lon'] = []
  data['vmax'] = []
  data['pmin'] = []
  fin = 'sui{0}_{1}-{2}.vor5_res17_1_-2_5.rel200'.format(domain,year,yp1)
  f = open(os.path.join(path_track,fin))
  lines = f.readlines()
  f.close()
  
  for line in lines:
        tmp = line.split()
        if len(tmp) != 4:
            data['lon'].append(float(tmp[1]))
            data['lat'].append(float(tmp[2]))
            data['vmax'].append(float(tmp[4])) # in m s-1
            data['pmin'].append(float(tmp[5])) # in hPa
            data['time'].append(tdeb)
            tdeb=tdeb+1
        else:
            tdeb=int(tmp[0])
# Reading netcdf data 
  file_data=path_data+data_name+'_DOM12_CNRM-CM6-1-HR_amip_r1i1p1f2_CNRM_CNRM-ALADIN63_v1_6hrPt_'+str(year)+"01010600-"+str(yp1)+"01010000.nc".format(domain)
  g=nc.Dataset(file_data)
  var=g.variables[data_name]
  timed=g.variables['time']
  lond=g.variables['lon'][:].tolist()
  lond = [round(elt, 1) for elt in lond]
  latd=g.variables['lat'][:].tolist()
  latd = [round(elt, 1) for elt in latd]
  print(lond)
  
  nlon=len(lond)
  nlat=len(latd)
  
# Calculate composites
  nrec=len(data['lon'])
  for i in range(0,nrec):
    loncyc = data['lon'][i]
    if loncyc <0:
        loncyc=loncyc+360
    latcyc = data['lat'][i]
    indx=lond.index(loncyc)
    indy=latd.index(latcyc)
    ilonn=max(0,indx-LARG)
    ilonx=min(nlon,indx+LARG+1)
    ilatn=max(0,indy-LARG)
    ilatx=min(nlat,indy+LARG+1)
     
    ideb=0
    ifin=2*LARG+1
    if (indx < LARG):
      ideb=LARG-indx
     
    if (indx >= nlon-LARG):
        ifin=2*LARG+1-(LARG+indx-nlon+1)
     
    jdeb=0
    jfin=2*LARG+1
    if (indy < LARG):
        jdeb=LARG-indy
    
    print(i,irec,data['time'][i]," ",loncyc,latcyc,indx,indy," ",ideb,ifin,jdeb,jfin,ilonn,ilonx,ilatn,ilatx)
    print(i,irec,data['time'][i]," ",loncyc,latcyc,indx,indy," ",var[data['time'][i]-1,indy,indx])
    if (indy >= (nlat-LARG)):
        jfin=2*LARG+1-(LARG+indy-nlat+1)
    
    cmp[irec,jdeb:jfin,ideb:ifin]=var[data['time'][i]-1,ilatn:ilatx,ilonn:ilonx]
    irec=irec+1
 
# Writing composites
file_out=path_cmp+'compo_2D_'+data_name+'_'+str(yearmin)+'-'+str(yearmax)+'.'+domain+'.nc'
try:
    os.remove(file_out)
except OSError:
    pass

fn = file_out
ds = nc.Dataset(fn, 'w', format='NETCDF4')
time = ds.createDimension('time', irec)
lat = ds.createDimension('lat', 2*LARG+1)
lon = ds.createDimension('lon', 2*LARG+1)
times = ds.createVariable('time', 'f4', ('time',))
times.units = ''
times.long_name = 'time'
lats = ds.createVariable('lat', 'f4', ('lat',))
lats.units = 'degrees_north'
lats.long_name = 'latitude'
lons = ds.createVariable('lon', 'f4', ('lon',))
lons.units = 'degrees_east'
lons.long_name = 'longitude'
tccmp = ds.createVariable('tccmp', 'f4', ('time', 'lat', 'lon',),fill_value=_FillValue)
tccmp.units = 'Unknown'

times[:]=np.arange(0,irec,1)
lats[:]=np.arange(-LARG, LARG+1, 1.0)
lons[:]=np.arange(-LARG, LARG+1, 1.0)
for i in range(irec):
  tccmp[i,:,:]=cmp[i,:,:]

ds.close()





