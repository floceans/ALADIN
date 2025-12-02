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

# --- CONFIGURATION ---
dirin_forceur = '/home/florent/Documents/ENM_3A/Aladin/REL200/global_10ans/'
dirin_ref = '/home/florent/Documents/ENM_3A/Aladin/REL200/reference_10ans/'
dirin_D10 = '/home/florent/Documents/ENM_3A/Aladin/REL200/D10_10ans/'
dirin_F10 = '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/'

dirin = dirin_D10

if not(os.path.exists('images')):
    os.makedirs('images')

yearmin = 2002
yearmax = 2010

data = {}
nstorm = 0

# --- DOMAIN SETUP ---
#domain = 'global'
#domain = 'NWPacific'
#domain = 'SWPacific'
domain = 'NAtlantic'

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

elif domain == 'NAtlantic':
    clon = 320
    lonmin = 280
    lonmax = 330
    latmin = 8
    latmax = 30
    lonlabels = [280, 290, 300, 310, 320, 330]
    latlabels = [0, 10, 20, 30, 40]

# --- DATA READING ---
data['lat'] = []
data['lon'] = []
data['vmax'] = []
data['pmin'] = []

for iyear in range(yearmin, yearmax):
    ip = iyear+1
    #fin = 'suiamip_g359_{0}.vor5_res17_1_-2_-5.rel200'.format(iyear)
    # Si besoin de changer le nom de fichier, décommentez ci-dessous:
    fin = 'suiATL_{iyear}-{ip}.vor5_res17_1_-2_5.rel200'.format(iyear=iyear, ip=ip)
    
    filepath = os.path.join(dirin, fin)
    
    # Vérification basique si le fichier existe pour éviter un crash
    if os.path.exists(filepath):
        f = open(filepath)
        lines = f.readlines()
        f.close()
         
        for line in lines:
            tmp = line.split()
            if len(tmp) != 4:
                data['lon'].append(float(tmp[1]))
                data['lat'].append(float(tmp[2]))
                data['vmax'].append(float(tmp[4])) # in m s-1
                data['pmin'].append(float(tmp[5])) # in hPa
    else:
        print(f"Attention: Le fichier {filepath} n'existe pas.")

x = np.array(data['lon'])
y = np.array(data['lat'])

# --- MASKING & KDE CALCULATION ---
# Mask domain outside of the basin of interest
mask = (x >= lonmin) & (x <= lonmax) & (y >= latmin) & (y <= latmax)
x_filt = x[mask]
y_filt = y[mask]

nech = len(x_filt)
if nech == 0:
    print("Aucune donnée trouvée dans le domaine sélectionné.")
    exit()

# To express results in nb of TC days per 10y per 5x5deg
coef = nech/4*25

k = gaussian_kde(np.vstack([x_filt, y_filt]))
xi, yi = np.mgrid[lonmin:lonmax, latmin:latmax]
zi = k(np.vstack([xi.flatten(), yi.flatten()])) * coef

# IMPORTANT: Reshape zi pour qu'il corresponde à la grille (nécessaire pour contourf)
zi = zi.reshape(xi.shape)

# --- PLOTTING (NEW SECTION) ---

# Define used projection
proj = ccrs.PlateCarree()
projcl = ccrs.PlateCarree(central_longitude=clon)

fig = plt.figure(figsize=(10, 7))
ax = plt.axes(projection=projcl)

ax.set_title('Track density [{0}-{1}] (Days/Area)'.format(yearmin, yearmax-1))
ax.set_extent([lonmin, lonmax, latmin, latmax], crs=proj)

lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter) 
ax.yaxis.set_major_formatter(lat_formatter)

ax.set_xticks(lonlabels, crs=proj)
ax.set_yticks(latlabels, crs=proj)

# --- FIXED COLORBAR RANGE 0–150 ---
levels = np.linspace(0, 16, 17)

cs = ax.contourf(
    xi, yi, zi,
    levels=levels,
    transform=proj,
    cmap=plt.cm.jet,
    vmin=0, vmax=15
)

# S'assurer que l'objet mappable a bien la plage
cs.set_clim(0, 15)

cbar = plt.colorbar(cs, ax=ax, shrink=0.6, label='Track Density (0–150)')

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

plt.show()

# Save the plot
output_filename = 'images/density_{0}-{1}_{2}_jet_contours.pdf'.format(yearmin, yearmax, domain)
fig.savefig(output_filename)
print(f"Image sauvegardée sous : {output_filename}")