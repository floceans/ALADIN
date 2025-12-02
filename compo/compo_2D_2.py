import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
# import cartopy.crs as ccrs # Non utilisé ici car les coordonnées sont relatives au centre

# 1. Configuration du fichier d'entrée (Résultat de compo_2D.py)
file_in = '/home/florent/Documents/ENM_3A/Aladin/compo/AA_compo_2D_tas_2002-2010.ATL.nc'
VARIABLE_NAME = 'tas'

print(f"Lecture du fichier : {file_in}")
ds = nc.Dataset(file_in, 'r')

# 2. Lecture des variables et prétraitement
tas_data = ds.variables[VARIABLE_NAME][:]
lats = ds.variables['lat'][:]
lons = ds.variables['lon'][:]

# Calcul de la moyenne temporelle (pour obtenir la structure composite moyenne 2D)
if tas_data.ndim == 3:
    print("Calcul de la moyenne temporelle (axis=0)...")
    tas_mean = np.mean(tas_data, axis=0)
else:
    tas_mean = tas_data

# Conversion Kelvin (K) -> Celsius (°C). 
# On suppose que 'tas' est en Kelvin si la moyenne est supérieure à 200.
if np.nanmean(tas_mean) > 200:
    tas_celsius = tas_mean - 273.15
    unit_label = "°C"
else:
    tas_celsius = tas_mean
    unit_label = VARIABLE_NAME # Afficher le nom de la variable si pas de conversion

ds.close()

# 3. Génération de la Carte avec Isolignes et Colormap 'jet'
print("Génération du graphique avec colormap 'jet' et isolignes...")
fig, ax = plt.subplots(figsize=(10, 8))

# A. Tracé du fond coloré (ContourF) avec la colormap 'jet'
cf = ax.contourf(lons, lats, tas_celsius, levels=25, cmap='jet', extend='both')
cbar = plt.colorbar(cf, ax=ax, label=f'Température ({unit_label})')

# B. Tracé des Isolignes (Contour)
# On choisit 10 lignes pour la clarté, en noir pour le contraste
CS = ax.contour(lons, lats, tas_celsius, levels=10, colors='black', linewidths=0.7)

# C. Ajout des valeurs sur les lignes (clabel)
# fmt='%1.1f' : pour afficher une décimale
ax.clabel(CS, inline=True, fontsize=9, fmt='%1.1f', colors='black')

# D. Mise en forme
ax.set_title(f'Composite {VARIABLE_NAME} Moyen\nCarte de couleurs "jet" avec isolignes')
ax.set_xlabel('Longitude relative')
ax.set_ylabel('Latitude relative')
ax.grid(True, linestyle='--', alpha=0.5)

# Sauvegarde et affichage
output_name = f'plot_{VARIABLE_NAME}_jet_isolignes.png'
plt.savefig(output_name, dpi=300)
print(f"Carte générée : {output_name}")
plt.show()