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

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

dirin = '/scratch/climat/APPS/ue_climat/tracking/data/HR6-amip'

if not(os.path.exists('images')):
    os.makedirs('images')

yearmin = 2000
yearmax = 2010

data = {}
nstorm = 0


###################################################
# Plotting tracks 

# Some configuration for the plot
# longitude must be within 0 and 360

domain = 'global'
#domain = 'NWPacific'
domain = 'SWPacific'
domain = 'NAtlantic'

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

elif domain == 'NAtlantic':
    clon = 0
    lonmin = 260
    lonmax = 360
    latmin = 0
    latmax = 50
    
    lonlabels = [260, 280, 300, 320, 340, 360]
    latlabels = [0, 10, 20, 30, 40, 50]


# Reading track
data={}
data['lat'] = []
data['lon'] = []
data['vmax'] = []
data['pmin'] = []
for iyear in range(yearmin,yearmax):
    fin = 'suiamip_g359_{0}.vor5_res17_1_-2_-5.rel200'.format(iyear)
    f = open(os.path.join(dirin,fin))
    lines = f.readlines()
    f.close()
     
    t0 = datetime(iyear, 1, 1, 0, 0)
    
    for line in lines:
        tmp = line.split()
        if len(tmp) != 4:
            data['lon'].append(float(tmp[1]))
            data['lat'].append(float(tmp[2]))
            data['vmax'].append(float(tmp[4])) # in m s-1
            data['pmin'].append(float(tmp[5])) # in hPa
x=data['lon']
y=data['lat']
vmax=data['vmax']
pmin=data['pmin']

vmax=ma.masked_where(np.ravel(x) <= lonmin,vmax)
vmax=ma.masked_where(np.ravel(x) >= lonmax,vmax)
vmax=ma.masked_where(np.ravel(y) <= latmin,vmax)
vmax=ma.masked_where(np.ravel(y) >= latmax,vmax)
pmin=ma.masked_where(np.ravel(x) <= lonmin,pmin)
pmin=ma.masked_where(np.ravel(x) >= lonmax,pmin)
pmin=ma.masked_where(np.ravel(y) <= latmin,pmin)
pmin=ma.masked_where(np.ravel(y) >= latmax,pmin)

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(121)

histv=plt.hist(vmax,bins=[17,20,23,26,29,32,35,38,41,44,47,50,53,56,59,62,65,68,71,74,77,80])

plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Distribution des Vmax')
maxfreq = 2000
# Set a clean upper y-axis limit.
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

ax = fig.add_subplot(122)
histp=plt.hist(pmin,bins=np.flip([1005,995,985,975,965,955,945,935,925,915,905,895,885,875,865]))
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Distribution des Vmax')
maxfreq = 2200
# Set a clean upper y-axis limit.
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

plt.show()
