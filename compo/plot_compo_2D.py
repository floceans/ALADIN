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

yearmin = 2002
yearmax = 2010

data_name="psl"


###################################################

# Some configuration for the plot
# longitude must be within 0 and 360

domain = 'ATL'
#domain = 'EP'
#domain = 'NI'
#domain = 'SI'

path_track = "../tracks/{0}/".format(domain)
path_data="../{0}/".format(domain)
path_dsn="../COMPO/{0}/".format(domain)

LARG=30
clon=0
lonmin=-LARG
lonmax=LARG
lonlabels = [-30, -20, -10, 0, 10, 20, 30] # Tricks for the longitude labels
latmin=-LARG
latmax=LARG
latlabels = [-30, -20, -10, 0, 10, 20, 30] # Tricks for the latgitude labels

# Raeding composites

file_data='../compo/'+domain+'/compo_2D_'+data_name+'_'+str(yearmin)+'-'+str(yearmax)+'.'+domain+'.nc'
print(file_data)
g=nc.Dataset(file_data)
var=g.variables['tccmp']
time=g.variables['time']
lon=g.variables['lon']
lat=g.variables['lat']

nlon=len(lon)
nlat=len(lat)
  
varmean=np.average(var,axis=0)
varstd=np.std(var[:,:,:],axis=0)

# Plotting figure
xi, yi = np.mgrid[lonmin:lonmax+1,latmin:latmax+1]
zi = varmean
## Define used projection
proj = ccrs.PlateCarree()
projcl = ccrs.PlateCarree(central_longitude=clon)
#
ax = plt.axes(projection=projcl)
#
## Add a title to the plot
ax.set_title('Composite for {0} [{1}-{2}]'.format(data_name,yearmin,yearmax))
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
#plt.show()
# Save the plot in a pdf file
plt.savefig('PDF/compo_2D_{0}_{1}-{2}_{3}.pdf'.format(data_name,yearmin,yearmax,domain))
# Erase the plot
#plt.close()

