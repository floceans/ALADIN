#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import numpy as np
import numpy.ma as ma
import netCDF4 as nc
import scipy.stats as stats
from scipy.stats import gaussian_kde

import matplotlib.pyplot as plt
from matplotlib import ticker, cm


dirin1 = ''
dirin2 = ''

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
for iyear in range(yearmin,yearmax):
    fin1 = '/home/florent/Documents/ENM_3A/Aladin/modele_forceur/suiamip_g359_{0}.vor5_res17_1_-2_-5.rel200'.format(iyear)
    fin2 = '/home/florent/Documents/ENM_3A/Aladin/local_track_2002-2010/sui{0}_{1}-{2}.vor5_res17_1_-2_5.rel200'.format(domain,iyear,iyear+1)
#   fin2 = 'suiANTILLE_{0}-{1}.vor5_res17_1_-2_5.rel200'.format(iyear,iyear+1)
    f1 = open(os.path.join(dirin1,fin1))
    f2 = open(os.path.join(dirin2,fin2))
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    f1.close()
    f1.close()
     
    t0 = datetime(iyear, 1, 1, 0, 0)
     
    for line in lines1:
        tmp = line.split()
        if len(tmp) != 4:
            data1['lon'].append(float(tmp[1])%360)
            data1['lat'].append(float(tmp[2]))
            data1['vmax'].append(float(tmp[4])) # in m s-1
            data1['pmin'].append(float(tmp[5])) # in hPa
    for line in lines2:
        tmp = line.split()
        if len(tmp) != 4:
            data2['lon'].append(float(tmp[1])%360)
            data2['lat'].append(float(tmp[2]))
            data2['vmax'].append(float(tmp[4])) # in m s-1
            data2['pmin'].append(float(tmp[5])) # in hPa
x1=data1['lon']
y1=data1['lat']
x2=data2['lon']
y2=data2['lat']

vmax1=data1['vmax']
pmin1=data1['pmin']
vmax2=data2['vmax']
pmin2=data2['pmin']

def mask_domain(x,y,vmax,pmin):
  vmax=ma.masked_where(np.ravel(x) <= lonmin,vmax)
  vmax=ma.masked_where(np.ravel(x) >= lonmax,vmax)
  vmax=ma.masked_where(np.ravel(y) <= latmin,vmax)
  vmax=ma.masked_where(np.ravel(y) >= latmax,vmax)
  pmin=ma.masked_where(np.ravel(x) <= lonmin,pmin)
  pmin=ma.masked_where(np.ravel(x) >= lonmax,pmin)
  pmin=ma.masked_where(np.ravel(y) <= latmin,pmin)
  pmin=ma.masked_where(np.ravel(y) >= latmax,pmin)
  return vmax,pmin

vmax1,pmin1=mask_domain(x1,y1,vmax1,pmin1)
vmax2,pmin2=mask_domain(x2,y2,vmax2,pmin2)

print(ma.count(vmax1))
print(ma.count(vmax2))

#fig = plt.figure(figsize=(7, 5))
fig = plt.figure()
ax = fig.add_subplot()

plt.grid(axis='x', alpha=0.75)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Vmax')
plt.ylabel('Pmin')
plt.title('Relation Vmax-Pmin')
# Set a clean upper y-axis limit.
ax.plot(vmax1,pmin1,'o',markersize=2,color='blue')
ax.plot(vmax2,pmin2,'o',markersize=2,color='red')


plt.show()
