#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import numpy.ma as ma
import netCDF4 as nc
import scipy.stats as stats
from scipy.stats import linregress 

import matplotlib.pyplot as plt
from matplotlib import ticker, cm

# --- FONCTION MODIFIÉE ---
def mask_domain(x,y,vmax,pmin):
  # 1. Convertir les listes en tableaux NumPy pour une manipulation facile
  x = np.array(x)
  y = np.array(y)
  vmax = np.array(vmax)
  pmin = np.array(pmin)

  # 2. Créer le masque initial basé sur les limites du domaine
  # Le masque est True (masqué) là où la condition est remplie.
  mask_lon_min = x <= lonmin
  mask_lon_max = x >= lonmax
  mask_lat_min = y <= latmin
  mask_lat_max = y >= latmax
  
  # Combiner tous les masques : True si AU MOINS UNE condition est remplie (doit être masqué)
  combined_mask = mask_lon_min | mask_lon_max | mask_lat_min | mask_lat_max
  
  # 3. Appliquer le masque aux tableaux de données
  vmax_masked = ma.masked_array(vmax, mask=combined_mask)
  pmin_masked = ma.masked_array(pmin, mask=combined_mask)
  
  return vmax_masked, pmin_masked
# -------------------------


dirin1 = '/home/florent/Documents/ENM_3A/Aladin/REL200/global_10ans'
dirin2 = '/home/florent/Documents/ENM_3A/Aladin/REL200/D10_10ans'
dirin3 = '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans'
dirin4 = '/home/florent/Documents/ENM_3A/Aladin/REL200/reference_10ans'

if not(os.path.exists('images')):
    os.makedirs('images')

yearmin = 2002
yearmax = 2009

data = {}
nstorm = 0


###################################################
# Plotting tracks 

# Some configuration for the plot
# longitude must be within 0 and 360

domain = 'ATL'
#domain = 'NAtlantic'

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
data1['lat'] = []
data1['lon'] = []
data1['vmax'] = []
data1['pmin'] = []

data2={}
data2['lat'] = []
data2['lon'] = []
data2['vmax'] = []
data2['pmin'] = []

data3={}
data3['lat'] = []
data3['lon'] = []
data3['vmax'] = []
data3['pmin'] = []

data4={}
data4['lat'] = []
data4['lon'] = []
data4['vmax'] = []
data4['pmin'] = []

for iyear in range(yearmin,yearmax):
    fin1 = 'suiamip_g359_{0}.vor5_res17_1_-2_-5.rel200'.format(iyear)
    fin2 = 'sui{0}_{1}-{2}.vor5_res17_1_-2_5.rel200'.format(domain,iyear,iyear+1)
    fin3 = 'sui{0}_{1}-{2}.vor5_res17_1_-2_5.rel200'.format(domain,iyear,iyear+1)
    fin4 = 'sui{0}_{1}-{2}.vor5_res17_1_-2_5.rel200'.format(domain,iyear,iyear+1)

    try:
        f1 = open(os.path.join(dirin1,fin1))
        f2 = open(os.path.join(dirin2,fin2))
        f3 = open(os.path.join(dirin3,fin3))
        f4 = open(os.path.join(dirin4,fin4))
    except FileNotFoundError:
        continue
        
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    lines3 = f3.readlines()
    lines4 = f4.readlines()
    f1.close()
    f2.close()
    f3.close()
    f4.close()
     
    t0 = datetime(iyear, 1, 1, 0, 0)
     
    for lines, data_dict in zip([lines1, lines2, lines3, lines4], [data1, data2, data3, data4]):
        for line in lines:
            tmp = line.split()
            # The condition `if len(tmp) != 4:` suggests the data line has a different format than a header/separator, 
            # and that indices 1, 2, 4, and 5 correspond to lon, lat, vmax, and pmin. 
            if len(tmp) != 4 and len(tmp) >= 6: 
                try:
                    data_dict['lon'].append(float(tmp[1])%360)
                    data_dict['lat'].append(float(tmp[2]))
                    data_dict['vmax'].append(float(tmp[4])) # in m s-1
                    data_dict['pmin'].append(float(tmp[5])) # in hPa
                except ValueError:
                    # Skip lines with non-numeric data in these columns
                    continue


x1=data1['lon']
y1=data1['lat']
x2=data2['lon']
y2=data2['lat']
x3=data3['lon']
y3=data3['lat']
x4=data4['lon']
y4=data4['lat']

vmax1=data1['vmax']
pmin1=data1['pmin']
vmax2=data2['vmax']
pmin2=data2['pmin']
vmax3=data3['vmax']
pmin3=data3['pmin']
vmax4=data4['vmax']
pmin4=data4['pmin']

# Apply masking
vmax1,pmin1=mask_domain(x1,y1,vmax1,pmin1)
vmax2,pmin2=mask_domain(x2,y2,vmax2,pmin2)
vmax3,pmin3=mask_domain(x3,y3,vmax3,pmin3)
vmax4,pmin4=mask_domain(x4,y4,vmax4,pmin4)

print("--- Data Point Counts (After Domain Masking) ---")
print(f"Count (Vmax1 - Arpège): {ma.count(vmax1)}")
print(f"Count (Vmax2 - D10): {ma.count(vmax2)}")
print(f"Count (Vmax3 - F10): {ma.count(vmax3)}")
print(f"Count (Vmax4 - Reference): {ma.count(vmax4)}")


# --- Linear Regression Calculation ---
# Filter out masked values before calculation

# D10 Data
# Extraction des données non masquées
vmax2_data = vmax2.compressed()
pmin2_data = pmin2.compressed()
print(f"D10 (vmax2_data) points used for regression (compressed): {len(vmax2_data)}")

# Regression for D10 (vmax2 vs pmin2)
if len(vmax2_data) > 1:
    slope2, intercept2, r_value2, p_value2, std_err2 = linregress(vmax2_data, pmin2_data)
    # Generate the line for D10
    vmax2_fit = np.array([np.min(vmax2_data), np.max(vmax2_data)])
    pmin2_fit = slope2 * vmax2_fit + intercept2
else:
    slope2, intercept2 = None, None
    print("Warning: Not enough data points for D10 linear regression.")

# F10 Data
# Extraction des données non masquées
vmax3_data = vmax3.compressed()
pmin3_data = pmin3.compressed()
print(f"F10 (vmax3_data) points used for regression (compressed): {len(vmax3_data)}")

# Regression for F10 (vmax3 vs pmin3)
if len(vmax3_data) > 1:
    slope3, intercept3, r_value3, p_value3, std_err3 = linregress(vmax3_data, pmin3_data)
    # Generate the line for F10
    vmax3_fit = np.array([np.min(vmax3_data), np.max(vmax3_data)])
    pmin3_fit = slope3 * vmax3_fit + intercept3
else:
    slope3, intercept3 = None, None
    print("Warning: Not enough data points for F10 linear regression.")

# --- Plotting ---
fig = plt.figure()
ax = fig.add_subplot()

plt.grid(axis='x', alpha=0.75)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Vmax (m/s)')
plt.ylabel('Pmin (hPa)')
plt.title('Relation Vmax-Pmin (Domain: {0})'.format(domain))

# Plot scatter points
#h_scatter_1, = ax.plot(vmax1,pmin1,'.',markersize=1,color='green', label='Arpège (Points)')
h_scatter_2, = ax.plot(vmax2,pmin2,'v',markersize=1,color='red', label='D10 (Points)')
h_scatter_3, = ax.plot(vmax3,pmin3,'^',markersize=1,color='blue', label='F10 (Points)')
#h_scatter_4, = ax.plot(vmax4,pmin4,'o',markersize=1,color='purple', label='Reference (Points)')

# Lists for legend handles and labels
legend_handles = [ h_scatter_2, h_scatter_3]
legend_labels = ['D10', 'F10']


# Plot regression lines
if slope2 is not None:
    h_reg_2, = ax.plot(vmax2_fit, pmin2_fit, '-', color='red', linewidth=2)
    legend_handles.append(h_reg_2)
    legend_labels.append(f'D10 Reg. (m={slope2:.2f}, c={intercept2:.2f})')

if slope3 is not None:
    h_reg_3, = ax.plot(vmax3_fit, pmin3_fit, '--', color='blue', linewidth=2)
    legend_handles.append(h_reg_3)
    legend_labels.append(f'F10 Reg. (m={slope3:.2f}, c={intercept3:.2f})')

# Update legend
plt.legend(legend_handles, legend_labels, loc='best', markerscale=5)

plt.show()