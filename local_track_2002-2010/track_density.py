#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import netCDF4 as nc
import scipy.stats as stats
from scipy.stats import gaussian_kde

import matplotlib.pyplot as plt
from matplotlib import ticker, cm

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

print("Creating images directory if it does not exist...")

dirin = ''

if not(os.path.exists('images')):
    os.makedirs('images')

yearmin = 2002
yearmax = 2010

data = {}
nstorm = 0

###################################################
# Plotting tracks 

domain = 'ATL'

if domain == 'global':
    clon = 180
    lonmin = 0
    lonmax = 360
    latmin = -60
    latmax = 60
    
    lonlabels = [0, 60, 120, 180, 240, 300, 360]
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
    clon = 20
    lonmin = 280
    lonmax = 330
    latmin = 8
    latmax = 30
    
    lonlabels = [280, 290, 300, 310, 320, 330]
    latlabels = [10, 15, 20, 25, 30]

# Reading track
data = {'lat': [], 'lon': [], 'vmax': [], 'pmin': []}

for iyear in range(yearmin, yearmax):
    yp1 = iyear + 1
    
    fin = '/home/florent/Documents/ENM_3A/Aladin/modele_forceur/suiamip_g359_{0}.vor5_res17_1_-2_-5.rel200'.format(iyear)
    #fin = '/home/florent/Documents/ENM_3A/Aladin/local_track_2002-2010/suiATL_{0}-{1}.vor5_res17_1_-2_5.rel200'.format(iyear, yp1)
    try:
        f = open(os.path.abspath(fin))
    except FileNotFoundError:
        print(f"Erreur: Le fichier {fin} n'a pas été trouvé pour l'année {iyear}. Le saut est effectué.")
        continue

    lines = f.readlines()
    f.close()
    
    t0 = datetime(iyear, 1, 1, 0, 0)
    
    for line in lines:
        tmp = line.split()
        if len(tmp) != 4:
            lon_val = float(tmp[1]) % 360
            data['lon'].append(lon_val)
            data['lat'].append(float(tmp[2]))
            data['vmax'].append(float(tmp[4]))
            data['pmin'].append(float(tmp[5]))

x = np.array(data['lon'])
y = np.array(data['lat'])

nech = len(x)

if nech == 0:
    print("Aucune donnée de trajectoire trouvée pour la période/le domaine spécifié.")
    exit()

# To express results in nb of TC days per 10y per 5x5deg
coef = nech / 4 *2

# Filtering for KDE domain
mask = (x >= lonmin) & (x <= lonmax) & (y >= latmin) & (y <= latmax)
x_filt = x[mask]
y_filt = y[mask]

if len(x_filt) < 2:
    print("Pas assez de points valides dans le domaine pour calculer la densité (KDE).")
    exit()

k = gaussian_kde(np.vstack([x_filt, y_filt]))

# Grid
xi, yi = np.mgrid[lonmin:lonmax, latmin:latmax]
zi = k(np.vstack([xi.flatten(), yi.flatten()])) * coef
zi = zi.reshape(xi.shape)

# Figure
fig = plt.figure()

proj = ccrs.PlateCarree()
projcl = ccrs.PlateCarree(central_longitude=clon)

ax = plt.axes(projection=projcl)

ax.set_title('Track density [{0}-{1}] (Days/Area)'.format(yearmin, yearmax-1))
ax.set_extent([lonmin, lonmax, latmin, latmax], crs=proj)

lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter) 
ax.yaxis.set_major_formatter(lat_formatter)

ax.set_xticks(lonlabels, crs=proj)
ax.set_yticks(latlabels, crs=proj)

# --- FIXED COLORBAR RANGE 0–14 ---
levels = np.linspace(0, 14, 15)

cs = ax.contourf(
    xi, yi, zi,
    levels=levels,
    transform=proj,
    cmap=plt.cm.jet,
    vmin=0, vmax=15
)

# S'assurer que l'objet mappable a bien la plage
cs.set_clim(0, 15)

cbar = plt.colorbar(cs, ax=ax, shrink=0.6, label='Track Density (0–14)')

# Contour lines + labels
ct = ax.contour(
    xi, yi, zi,
    levels=np.linspace(0, 15, 10),
    colors='black',
    linewidths=0.5,
    transform=proj
)
ax.clabel(ct, inline=True, fontsize=8, fmt='%1.1f')

# Coastlines + grid
ax.coastlines(resolution='50m')
ax.gridlines(crs=proj, draw_labels=False, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

# Save figure
plt.savefig('images/density_{0}-{1}_{2}_labeled.pdf'.format(yearmin, yearmax-1, domain))

plt.show()
