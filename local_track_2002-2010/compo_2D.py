#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import netCDF4 as nc
import scipy.stats as stats

import matplotlib.pyplot as plt
from matplotlib import ticker, cm

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

dirin = '../tracks/ATL'

if not(os.path.exists('images')):
    os.makedirs('images')

year = 2008
yp1=year+1

data = {}
nstorm = 0

path_track = "../tracks/ATL/"
path_data="../ATL/"
path_dsn="../COMPO/ATL"
#********************************
# select sub-regions
#********************************
minlat =    7.0	# deg N
maxlat =    30.0	# deg N
minlon =  280.0	# - deg E = deg W
maxlon =  330.0	# - deg E = deg W


data_name="hurs"


#**********************************
# Definition of tracking conditions
#**********************************
VOR	=	5
RES	=	17
T	=	1
PT	=	-2
PW	=	5
REL = 200

LARG = 20
vtrsh=0.


###################################################
# Plotting tracks 

# Some configuration for the plot
# longitude must be within 0 and 360

domain = 'ATL'
#domain = 'NWPacific'
#domain = 'SWPacific'
#domain = 'NAtlantic'

if domain == 'global':
    clon = 180 # Map centered on the dateline
    lonmin = 0
    lonmax = 360 # Tricks for the longitude labels
    latmin = -60
    latmax = 60
    
    lonlabels = [0, 60, 120, 180, 240, 300, 360] # Tricks for the longitude labels
    latlabels = [-60, -30, 0, 30, 60]
    
elif domain == 'NWPacific':
    clon = 0
    lonmin = 100
    lonmax = 180
    latmin = 0
    latmax = 50
    
    lonlabels = [100, 120, 140, 160, 180]
    latlabels = [0, 10, 20, 30, 40, 50]
    
elif domain == 'SWPacific':
    clon = 180
    lonmin = 140
    lonmax = 240
    latmin = -50
    latmax = 0
    
    lonlabels = [140, 160, 180, 200, 220, 240]
    latlabels = [-50, -40, -30, -20, -10, 0]
    
elif domain == 'ATL':
    clon = 0
    lonmin = 280
    lonmax = 330
    latmin = 8
    latmax = 30
    
    lonlabels = [280, 290, 300, 310, 320, 330]
    latlabels = [10, 15, 20, 25, 30]

# Reading grid : not necessary if grid is defined from lonmin,lonmax,latmin,latmax

#fg=nc.Dataset('exemple_5x5_glob.nc')
#lon=fg['lon'][:]
#lat=fg['lat'][:]

# Reading track
data={}
data['lat'] = []
data['lon'] = []
data['vmax'] = []
data['pmin'] = []
fin = 'suiATL_{0}-{1}.vor5_res17_1_-2_5.rel200'.format(year,yp1)
f = open(os.path.join(dirin,fin))
lines = f.readlines()
f.close()
    
t0 = datetime(year, 1, 1, 6, 0)
print(t0)
    
for line in lines:
        tmp = line.split()
        if len(tmp) != 4:
            data['lon'].append(float(tmp[1]))
            data['lat'].append(float(tmp[2]))
            data['vmax'].append(float(tmp[4])) # in m s-1
            data['pmin'].append(float(tmp[5])) # in hPa

file_data=path_data+data_name+'_DOM12_CNRM-CM6-1-HR_amip_r1i1p1f2_CNRM_CNRM-ALADIN63_v1_6hrPt_'+str(year)+"01010600-"+str(yp1)+"01010000.nc".format(domain)
g=nc.Dataset(file_data)
var=g.variables[data_name]
print(np.shape(var))


xi = np.mgrid[lonmin:lonmax]
yi = np.mgrid[latmin:latmax]
xarr=np.array(xi)
yarr=np.array(yi)

nrec=len(data['lon'])
print(nrec)
for i in range(1,nrec):
  loncyc = data['lon'][i]
  latcyc = data['lat'][i]
  indx=np.absolute(loncyc-xarr).argmin()
  indy=np.absolute(latcyc-yarr).argmin()
  print(loncyc,latcyc)
  print(indx)
  print(indy)
  print(var[i,indx,indy])
  cmp[i,indx-LARG:indx+LARG,indy-LARG:indy+LARG]=var[i,indx-LARG:indx+LARG,indy-LARG:indy+LARG]
   
print(xarr)
print(yarr)




