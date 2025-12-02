import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuration des fichiers
file_u = '/home/florent/Documents/ENM_3A/Aladin/compo/AA_compo_2D_uas_2002-2010.ATL.nc'
file_v = '/home/florent/Documents/ENM_3A/Aladin/compo/AA_compo_2D_vas_2002-2010.ATL.nc'

# 2. Chargement des données
print("Chargement des fichiers...")
ds_u = nc.Dataset(file_u, 'r')
ds_v = nc.Dataset(file_v, 'r')

# On récupère les coordonnées (supposées identiques pour les deux fichiers)
# Note: Dans les composites, lat/lon sont souvent des distances relatives au centre
lats = ds_u.variables['lat'][:]
lons = ds_u.variables['lon'][:]

# On récupère les variables de vent (Temps, Lat, Lon)
# Le nom de la variable interne est souvent le même que le nom physique, ou 'var'
# Ici on suppose 'uas' et 'vas' basés sur les noms de fichiers standards
try:
    u_data = ds_u.variables['uas'][:]
    v_data = ds_v.variables['vas'][:]
except KeyError:
    # Fallback si les variables s'appellent différemment (ex: 'var')
    print("Variables 'uas'/'vas' non trouvées, tentative avec les clés disponibles...")
    u_key = list(ds_u.variables.keys())[-1] # Souvent la dernière variable ajoutée
    v_key = list(ds_v.variables.keys())[-1]
    u_data = ds_u.variables[u_key][:]
    v_data = ds_v.variables[v_key][:]

# 3. Calcul de la vitesse du vent (Module)
# Formule : sqrt(u² + v²)
print("Calcul de la vitesse du vent...")
wind_speed = np.sqrt(u_data**2 + v_data**2)

# 4. Moyenne Temporelle (Composite Moyen)
# Les fichiers 'compo' contiennent souvent plusieurs pas de temps (ou plusieurs tempêtes).
# On fait la moyenne sur l'axe 0 (le temps/les enregistrements) pour avoir une carte unique.
u_mean = np.mean(u_data, axis=0)
v_mean = np.mean(v_data, axis=0)
ws_mean = np.mean(wind_speed, axis=0)

ds_u.close()
ds_v.close()

# 5. Création de la Carte (Plot)
print("Génération du graphique...")
fig, ax = plt.subplots(figsize=(10, 8))

# Tracé des contours de la vitesse du vent (couleur)
# On utilise 'jet' ou 'viridis' comme colormap
cf = ax.contourf(lons, lats, ws_mean, levels=20, cmap='jet', extend='both')
cbar = plt.colorbar(cf, ax=ax, label='Vitesse du vent (m/s)')

# Ajout des vecteurs (flèches) pour montrer la direction
# On sous-échantillonne (step) pour ne pas avoir trop de flèches (ex: 1 sur 4)
step = 4 
Q = ax.quiver(lons[::step], lats[::step], 
              u_mean[::step, ::step], v_mean[::step, ::step], 
              color='white', scale=None, alpha=0.8)

# Mise en forme
ax.set_title(f'Composite Vent Moyen (2002-2010)\nModule (couleurs) et Direction (flèches)')
ax.set_xlabel('Longitude relative (deg)')
ax.set_ylabel('Latitude relative (deg)')
ax.grid(True, linestyle='--', alpha=0.5)

# Sauvegarde et affichage
plt.savefig('carte_vent_resultat.png', dpi=300)
plt.show()

print("Terminé. Carte sauvegardée sous 'carte_vent_resultat.png'")