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

domain = 'ATL'

path_track = "/home/florent/Documents/ENM_3A/Aladin/local_track_2002-2010"
#path_data="compo/AA_compo_2D_tas_2002-2010.ATL.nc"
path_dsn="compo/AA_compo_2D_tas_2002-2010.ATL.nc"

LARG=30
clon=0
lonmin=-LARG
lonmax=LARG
lonlabels = [-30, -20, -10, 0, 10, 20, 30]
latmin=-LARG
latmax=LARG
latlabels = [-30, -20, -10, 0, 10, 20, 30]

# Read data
file_data='/home/florent/Documents/ENM_3A/Aladin/compo/AA_compo_2D_pr_2002-2010.ATL.nc'
print(file_data)
g = nc.Dataset(file_data)
var = g.variables['tccmp']
time = g.variables['time']
lon = g.variables['lon']
lat = g.variables['lat']

nlon = len(lon)
nlat = len(lat)

varmean = np.average(var, axis=0)
varstd  = np.std(var[:,:,:], axis=0)

# Plot
xi, yi = np.mgrid[lonmin:lonmax+1, latmin:latmax+1]
zi = varmean*3600

proj = ccrs.PlateCarree()
projcl = ccrs.PlateCarree(central_longitude=clon)

ax = plt.axes(projection=projcl)
ax.set_title('Composite for {0} [{1}-{2}]'.format(data_name, yearmin, yearmax))

ax.set_extent([lonmin, lonmax, latmin, latmax], crs=projcl)

lon_formatter = LongitudeFormatter(zero_direction_label=False)
lat_formatter = LatitudeFormatter()

ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

ax.set_xticks(lonlabels, crs=proj)
ax.set_yticks(latlabels, crs=proj)

# --- Contourf avec colormap JET ---
cs = ax.contourf(
    xi, yi, zi.reshape(xi.shape),
    60, cmap='jet', transform=proj
)

# --- Tracé des isolignes ---
contours = ax.contour(
    xi, yi, zi.reshape(xi.shape),
    levels=15, colors='black', linewidths=0.7, transform=proj
)

# --- Labels des isolignes ---
ax.clabel(contours, inline=True, fontsize=8, fmt="%.1f")

# Colorbar
plt.colorbar(cs, ax=ax, shrink=0.6, label=data_name)
plt.tight_layout()
plt.show()

# Save
#plt.savefig('PDF/compo_2D_{0}_{1}-{2}_{3}.pdf'.format(data_name, yearmin, yearmax, domain))
