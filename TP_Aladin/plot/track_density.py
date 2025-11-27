#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from datetime import datetime, timedelta
import numpy as np
import netCDF4 as nc
import scipy.stats as stats
from scipy.stats.kde import gaussian_kde

import matplotlib.pyplot as plt
from matplotlib import ticker, cm

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter



dirin = 'C:\\Users\\flore\\Documents\\cours\\N7_ENM_3A\\Aladin\\local_track_2002-2010\\'


if not(os.path.exists('images')):
    os.makedirs('images')

yearmin = 2002
yearmax = 2010

data = {}
nstorm = 0


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
for iyear in range(yearmin,yearmax):
    yp1=iyear+1
    fin = 'suiATL_{0}-{1}.vor5_res17_1_-2_5.rel10'.format(iyear,yp1)
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

nech=len(x)
# To express results in nb of TC days per 10y per 5x5deg
coef=nech/4*25

k = gaussian_kde(np.vstack([x, y]))
xi, yi = np.mgrid[lonmin:lonmax,latmin:latmax]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))*coef

#fig = plt.figure(figsize=(7, 5))
#ax = fig.add_subplot(131)
#
## Define used projection
proj = ccrs.PlateCarree()
projcl = ccrs.PlateCarree(central_longitude=clon)
#
ax = plt.axes(projection=projcl)
#
## Add a title to the plot
ax.set_title('Track density [{0}-{1}]'.format(yearmin,yearmax))
#
## Define domain of the plot
ax.set_extent([lonmin, lonmax, latmin, latmax], crs=projcl)
#
# Formatting of longitude/latitude labels
lon_formatter = LongitudeFormatter(zero_direction_label=False)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter) 
ax.yaxis.set_major_formatter(lat_formatter)
#
ax.set_xticks(lonlabels, crs=proj)
ax.set_yticks(latlabels, crs=proj)
#
#plt.contourf(lon, lat, dgrid, 60, transform=proj)

#ax.pcolormesh(xi, yi, zi.reshape(xi.shape), alpha=0.5)
#plt.contourf(xi, yi, zi.reshape(xi.shape), alpha=1.0)
cs=ax.contourf(xi, yi, zi.reshape(xi.shape), 60, transform=proj)
plt.colorbar(cs,ax=ax,shrink=0.6)

# Add coastlines
ax.coastlines()
#plt.show()
# Save the plot in a png file
plt.savefig('images/density_{0}-{1}_{2}.pdf'.format(yearmin,yearmax,domain))
# Erase the plot
#plt.close()

