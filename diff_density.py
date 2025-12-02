#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import scipy.stats as stats
from scipy.stats import gaussian_kde

import matplotlib.pyplot as plt
from matplotlib import ticker, cm

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# --- CONFIGURATION ---
dirin2 = '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/'
dirin1 = '/home/florent/Documents/ENM_3A/Aladin/REL200/D10_10ans/'

if not(os.path.exists('images')):
    os.makedirs('images')

yearmin = 2002
yearmax = 2010

# --- DOMAIN SETUP ---
#domain = 'global'
domain = 'NAtlantic'
#domain = 'SWPacific'

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
    clon = 30
    lonmin = 260
    lonmax = 360
    latmin = 0
    latmax = 50
    lonlabels = [260, 280, 300, 320, 340, 360]
    latlabels = [0, 10, 20, 30, 40, 50]

# --- DATA READING ---
data1 = {'lat': [], 'lon': [], 'vmax': [], 'pmin': []}
data2 = {'lat': [], 'lon': [], 'vmax': [], 'pmin': []}

for iyear in range(yearmin, yearmax):
    fin1 = 'suiATL_{0}-{1}.vor5_res17_1_-2_5.rel200'.format(iyear, iyear+1)
    fin2 = 'suiATL_{0}-{1}.vor5_res17_1_-2_5.rel200'.format(iyear, iyear+1)
    
    path1 = os.path.join(dirin1, fin1)
    path2 = os.path.join(dirin2, fin2)
    
    # Lecture dataset 1
    if os.path.exists(path1):
        with open(path1, 'r') as f1:
            for line in f1:
                tmp = line.split()
                if len(tmp) != 4:
                    data1['lon'].append(float(tmp[1]))
                    data1['lat'].append(float(tmp[2]))
                    data1['vmax'].append(float(tmp[4]))
                    data1['pmin'].append(float(tmp[5]))
    
    # Lecture dataset 2
    if os.path.exists(path2):
        with open(path2, 'r') as f2:
            for line in f2:
                tmp = line.split()
                if len(tmp) != 4:
                    data2['lon'].append(float(tmp[1]))
                    data2['lat'].append(float(tmp[2]))
                    data2['vmax'].append(float(tmp[4]))
                    data2['pmin'].append(float(tmp[5]))

x1, y1 = np.array(data1['lon']), np.array(data1['lat'])
x2, y2 = np.array(data2['lon']), np.array(data2['lat'])

if len(x1) == 0 or len(x2) == 0:
    print("Erreur: Données insuffisantes pour le calcul.")
    exit()

# --- KDE CALCULATION ---
nech1 = len(x1)
nech2 = len(x2)

coef1 = nech1/4*25
coef2 = nech2/4*25

k1 = gaussian_kde(np.vstack([x1, y1]))
k2 = gaussian_kde(np.vstack([x2, y2]))

xi, yi = np.mgrid[lonmin:lonmax, latmin:latmax]

# Calcul sur la grille
zi1 = k1(np.vstack([xi.flatten(), yi.flatten()])) * coef1
zi2 = k2(np.vstack([xi.flatten(), yi.flatten()])) * coef2
zi = zi2 - zi1

# Reshape important pour contourf
zi = zi.reshape(xi.shape)

# --- PLOTTING (STYLE APPLIED FROM SNIPPET) ---
proj = ccrs.PlateCarree()
projcl = ccrs.PlateCarree(central_longitude=clon)

fig = plt.figure(figsize=(10, 7))
ax = plt.axes(projection=projcl)

# Titre adapté pour refléter que c'est une différence, mais format demandé
ax.set_title('Track Density Difference [{0}-{1}] (Days/Area)'.format(yearmin, yearmax))
ax.set_extent([lonmin, lonmax, latmin, latmax], crs=proj)

lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter) 
ax.yaxis.set_major_formatter(lat_formatter)

ax.set_xticks(lonlabels, crs=proj)
ax.set_yticks(latlabels, crs=proj)

# --- FIXED COLORBAR RANGE 0–15 ---
# Note: Comme c'est une difference, cela montrera surtout les anomalies positives
levels = np.linspace(0, 15, 15)

cs = ax.contourf(
    xi, yi, zi,
    levels=levels,
    transform=proj,
    cmap=plt.cm.jet,
    vmin=0, vmax=15
)

# S'assurer que l'objet mappable a bien la plage
cs.set_clim(0, 15)

cbar = plt.colorbar(cs, ax=ax, shrink=0.6, label='Density Diff (0–15)')

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

# Save
#output_filename = 'images/diff_density_{0}-{1}_{2}_jet_0-15.pdf'.format(yearmin, yearmax, domain)
#fig.savefig(output_filename)

