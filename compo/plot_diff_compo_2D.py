#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import netCDF4 as nc
import scipy.stats as stats

import matplotlib.pyplot as plt
from matplotlib import ticker, cm
plt.style.use('RdBu')

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

yearmin = 2001
yearmax = 2010

data_name="psl"


###################################################

# Some configuration for the plot
# longitude must be within 0 and 360

domain1 = 'ATL'
domain2 = 'EP'
#domain = 'NI'
#domain = 'SI'

path_data="../compo/"

LARG=30
clon=0
lonmin=-LARG
lonmax=LARG
lonlabels = [-30, -20, -10, 0, 10, 20, 30] # Tricks for the longitude labels
latmin=-LARG
latmax=LARG
latlabels = [-30, -20, -10, 0, 10, 20, 30] # Tricks for the latgitude labels

# Raeding composites

file_data1='{1}/compo_2D_{0}_{2}-{3}.{1}.nc'.format(data_name,domain1,yearmin,yearmax)
file_data2='{1}/compo_2D_{0}_{2}-{3}.{1}.nc'.format(data_name,domain2,yearmin,yearmax)
g1=nc.Dataset(path_data+file_data1)
g2=nc.Dataset(path_data+file_data2)
var1=g1.variables['tccmp']
var2=g2.variables['tccmp']
time=g1.variables['time']
lon=g1.variables['lon']
lat=g1.variables['lat']

nlon=len(lon)
nlat=len(lat)
  
nt1=var1.shape[0]
nt2=var2.shape[0]
varm1=np.average(var1,axis=0)
varm2=np.average(var2,axis=0)
vard=varm2-varm1
varv1=np.var(var1[:,:,:],axis=0)
varv2=np.var(var2[:,:,:],axis=0)
varv=(nt1*varv1+nt2*varv2)/(nt1+nt2)
stud=vard/varv*np.sqrt(nt1*nt2/(nt1+nt2))

# Plotting figure
xi, yi = np.mgrid[lonmin:lonmax+1,latmin:latmax+1]
zi = vard
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
plt.savefig('PDF/compo_2D_{0}_{3}-{4}_{2}-{1}.pdf'.format(data_name,domain1,domain2,yearmin,yearmax))
# Erase the plot
#plt.close()

