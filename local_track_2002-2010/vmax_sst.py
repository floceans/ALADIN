#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import numpy.ma as ma
import netCDF4 as nc
import scipy.stats as stats
from scipy.stats.kde import gaussian_kde

import matplotlib.pyplot as plt
from matplotlib import ticker, cm


dirin1 = '/home/newton/ienm2025/puyf/Documents/TP_aladin/data_chauvin/tracks/ATL/'
#dirdat = '/scratch/work/rigoudyg/TP_ALADIN/2025/ANTILLES-12-BS-10ans/outputs/assembled'
dirdat = '/home/newton/ienm2025/puyf/Documents/TP_aladin/data_chauvin/ATL'#/codes_perso/track_aladin_200/'


if not(os.path.exists('images')):
    os.makedirs('images')

yearmin = 2001
yearmax = 2003

data = {}
nstorm = 0

def closest(arry,arrx,lat,lon):
     
     nlat=len(arry)
     nlon=len(arrx)
     lstx = np.asarray(arrx)
     lsty = np.asarray(arry)
     idx = (np.abs(lstx - lon)).argmin()
     idy = (np.abs(lsty - lat)).argmin()
     print(idx,idy)
     return [idy,idx]

###################################################
# Plotting tracks 

# Some configuration for the plot
# longitude must be within 0 and 360

domain = 'ATL'

if domain == 'global':
    clon = 180 # Map centered on the dateline
    lonmin = 0
    lonmax = 320 # Tricks for the longitude labels
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


# Reading track
data1={}
data2={}
data1['time'] = []
data1['lat'] = []
data1['lon'] = []
data1['vmax'] = []
data1['pmin'] = []
data1['sst'] = []
for iyear in range(yearmin,yearmax):
    fin1 = 'suiATL_{0}-{1}.vor5_res17_1_-2_5.rel200'.format(iyear,iyear+1)
    sstf1 = 'ts_DOM12_CNRM-CM6-1-HR_amip_r1i1p1f2_CNRM_CNRM-ALADIN63_v1_6hrPt_{0}01010600-{1}01010000.nc'.format(iyear,iyear+1)
    f1 = open(os.path.join(dirin1,fin1))
    fsst1 = nc.Dataset(os.path.join(dirdat,sstf1))
    lines1 = f1.readlines()
    sst=fsst1.variables['ts'][:].data
    lon=fsst1.variables['lon'][:].data
    lat=fsst1.variables['lat'][:].data
    f1.close()
     
    t0 = datetime(iyear, 1, 1, 0, 0)
     
    for line in lines1:
        tmp = line.split()
        if len(tmp) == 4:
            it=int(tmp[0]) 
        else:
            data1['time'].append((it))
            data1['lon'].append(float(tmp[1])%360)
            data1['lat'].append(float(tmp[2]))
            data1['vmax'].append(float(tmp[4])) # in m s-1
            data1['pmin'].append(float(tmp[5])) # in hPa
            
            posloc=closest(lat,lon,float(tmp[2]),float(tmp[1])%360)
            data1['sst'].append(sst[it,posloc[0],posloc[1]]) # in hPa
            it=it+1

t1=data1['time']
x1=data1['lon']
y1=data1['lat']

vmax1=data1['vmax']
pmin1=data1['pmin']
sstf1=data1['sst']



def mask_domain(x,y,vmax,sst):
  vmax=ma.masked_where(np.ravel(x) <= lonmin,vmax)
  vmax=ma.masked_where(np.ravel(x) >= lonmax,vmax)
  vmax=ma.masked_where(np.ravel(y) <= latmin,vmax)
  vmax=ma.masked_where(np.ravel(y) >= latmax,vmax)
  sst=ma.masked_where(np.ravel(x) <= lonmin,sst)
  sst=ma.masked_where(np.ravel(x) >= lonmax,sst)
  sst=ma.masked_where(np.ravel(y) <= latmin,sst)
  sst=ma.masked_where(np.ravel(y) >= latmax,sst)
  return vmax,sst

vmax1,sstf1=mask_domain(x1,y1,vmax1,sstf1)

print(ma.count(vmax1))

#fig = plt.figure(figsize=(7, 5))
fig = plt.figure()
ax = fig.add_subplot()

plt.grid(axis='x', alpha=0.75)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Vmax')
plt.ylabel('SST')
plt.title('Relation Vmax-SST')
# Set a clean upper y-axis limit.
ax.plot(vmax1,sstf1,'o',markersize=1,mec='blue', mfc='None', label='ALD2')
plt.legend()


plt.savefig('vmax_sst_{0}-{1}_{2}.png'.format(yearmin,yearmax,domain))
