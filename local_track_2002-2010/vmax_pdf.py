#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

# --- Configuration du domaine ---
# Les coordonnées sont en degrés Est (0 à 360)
domain = 'NAtlantic' 

if domain == 'NAtlantic':
    # Atlantic Nord (Exemple: Ouest de l'Europe à Est des Amériques)
    lonmin = 268 # 100°W (260°E)
    lonmax = 353 # 0°E/360°E
    latmin = 8
    latmax = 30
    # Note: On n'utilise plus les variables 'clon', 'lonlabels', 'latlabels' dans cette version simplifiée d'histogramme.


# --- Lecture des données ---
yearmin = 2001
yearmax = 2010
data = {'lon': [], 'lat': [], 'vmax': [], 'pmin': []}
dirin = ''

for iyear in range(yearmin, yearmax):
    fin = f'/home/florent/Documents/ENM_3A/Aladin/modele_forceur/suiamip_g359_{iyear}.vor5_res17_1_-2_-5.rel200'
    #fin = f'/home/florent/Documents/ENM_3A/Aladin/local_track_2002-2010/suiATL_{iyear}-{iyear+1}.vor5_res17_1_-2_5.rel200'
    try:
        with open(os.path.join(dirin, fin), 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Attention : Fichier {fin} non trouvé. Poursuite avec l'année suivante.")
        continue
     
    for line in lines:
        tmp = line.split()
        # Une ligne de trajectoire contient 6 éléments (ID, lon, lat, date, vmax, pmin) ou 4 (ID, date, vmax, pmin)
        # Basé sur votre logique de lecture initiale (len(tmp) != 4), on prend les lignes de données complètes:
        if len(tmp) == 6: 
            try:
                data['lon'].append(float(tmp[1]))
                data['lat'].append(float(tmp[2]))
                data['vmax'].append(float(tmp[4])) # en m s-1
                data['pmin'].append(float(tmp[5])) # en hPa
            except ValueError:
                continue

# Conversion en tableaux numpy
x = np.array(data['lon'])
y = np.array(data['lat'])
vmax = np.array(data['vmax'])
pmin = np.array(data['pmin'])


# --- Filtrage (Masquage) des données hors Atlantique Nord ---

# Création du masque: True si HORS du domaine, False si DANS le domaine
mask_lon_out = (x < lonmin) | (x > lonmax)
mask_lat_out = (y < latmin) | (y > latmax)
# Masque combiné : True si hors de la zone Atlantique définie
mask_out = mask_lon_out | mask_lat_out

# Application du masque aux données Vmax et Pmin
vmax_atlantic = ma.masked_where(mask_out, vmax)
pmin_atlantic = ma.masked_where(mask_out, pmin)

# Les données masquées conservent uniquement les valeurs DANS l'Atlantique
# On peut les obtenir en utilisant .compressed()
vmax_filtered = vmax_atlantic.compressed()
pmin_filtered = pmin_atlantic.compressed()

print(f"\nTotal de points de données lus : {len(x)}")
print(f"Nombre de points filtrés dans l'Atlantique Nord ({lonmin}°E-{lonmax}°E, {latmin}°N-{latmax}°N) : {len(vmax_filtered)}")


# --- Tracé des Histogrammes ---
fig = plt.figure(figsize=(10, 14))
plt.suptitle(f"Distributions des Maximums de Vents (Vmax) et Pressions (Pmin)\nDomaine : {domain} ({yearmin}-{yearmax})", fontsize=14)

# --- Histogramme Vmax ---
ax1 = fig.add_subplot(121)

# Définition des bins pour Vmax (en m/s)
vmax_bins = np.arange(17, 81, 3) # [17, 20, 23, ..., 80]
histv = ax1.hist(vmax_filtered, bins=vmax_bins, edgecolor='black', alpha=0.7)

ax1.grid(axis='y', alpha=0.75, linestyle='--')
ax1.set_xlabel('Vitesse du vent maximale (m/s)')
ax1.set_ylabel('Fréquence (Nombre de points)')
ax1.set_title('Distribution des Vmax')

# Ajustement de l'axe Y
maxfreq1 = np.max(histv[0]) if len(histv[0]) > 0 else 100
ax1.set_ylim(ymax=100)#ymax=np.ceil(maxfreq1 * 1.05 / 100) * 100 if maxfreq1 > 0 else 10)
ax1.set_xlim(left=15, right=85)


# --- Histogramme Pmin ---
ax2 = fig.add_subplot(122)

# Définition des bins pour Pmin (en hPa)
# Bins inversés car la pression diminue (ex: [1005, 995, ..., 875])
pmin_bins = np.arange(875, 1015, 10)
histp = ax2.hist(pmin_filtered, bins=pmin_bins, edgecolor='black', alpha=0.7)

ax2.grid(axis='y', alpha=0.75, linestyle='--')
ax2.set_xlabel('Pression minimale (hPa)')
ax2.set_ylabel('Fréquence (Nombre de points)')
ax2.set_title('Distribution des Pmin')

# Ajustement de l'axe Y
maxfreq2 = np.max(histp[0]) if len(histp[0]) > 0 else 100
#ax2.set_ylim(ymax=np.ceil(maxfreq2 * 1.05 / 100) * 100 if maxfreq2 > 0 else 10)
ax2.set_ylim(ymax=165)#ymax= maxfreq2 + 10)
ax2.set_xlim(left=870, right=1010)


plt.tight_layout(rect=[0, 10, 0.1, 0.95]) # Ajuster pour le suptitle
plt.show()