import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import os
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

# --- Configuration du fichier et de la carte ---
# Assurez-vous que ce fichier se trouve dans le même dossier que votre script Python
filename = 'C:\\Users\\flore\\Documents\\cours\\N7_ENM_3A\\Aladin\\modele_forceur\\suiamip_g359_concatene.rel200' 
tracks = {}
current_track_id = None

# --- 1. Lecture, Parsing et Conversion des données ---
print(f"Lecture des données depuis le fichier : {filename}")

if not os.path.exists(filename):
    print(f"Erreur : Le fichier '{filename}' est introuvable. Veuillez vérifier son emplacement.")
    exit()

with open(filename, 'r') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        
        # Nettoyage des artefacts d'affichage si le contenu a été copié/collé
        if '[' in line and ']' in line:
            line = line.split(']', 1)[1].strip()

        # line.split() gère les espaces simples ou multiples (y compris les tabulations) 
        # comme séparateurs, en traitant les éléments comme des colonnes distinctes.
        parts = line.split()
        
        # Détection d'une nouvelle trajectoire (En-tête : lignes courtes comme '6 6 0 0')
        # Ces lignes sont utilisées UNIQUEMENT pour identifier un nouveau groupe, puis ignorées.
        if len(parts) > 0 and len(parts) < 5:
            # On utilise le premier nombre (ex: '6') comme identifiant de la trajectoire
            current_track_id = parts[0]
            tracks[current_track_id] = {'lat': [], 'lon': [], 'press': []}
            continue # <--- La ligne d'en-tête est ignorée comme point à tracer
        
        # Détection des données (Lignes longues avec coordonnées)
        if len(parts) >= 5 and current_track_id:
            try:
                # Colonne 2 = Longitude, Colonne 3 = Latitude, Dernière colonne = Pression
                lon_val = float(parts[1])
                lat_val = float(parts[2])
                pressure_val = float(parts[-1]) 
                
                # Conversion Longitude 0-360 vers -180/180
                if lon_val > 180:
                    lon_val = lon_val - 360
                if pressure_val > 930 and pressure_val < 1100:
                    tracks[current_track_id]['lon'].append(lon_val)
                    tracks[current_track_id]['lat'].append(lat_val)
                    tracks[current_track_id]['press'].append(pressure_val)
            except ValueError:
                # Ignore les lignes qui ne sont pas des données numériques valides
                continue

# --- 2. Configuration de la Carte avec OpenStreetMap (Cartopy) ---
if not tracks:
    print("Aucune donnée de trajectoire valide n'a pu être extraite.")
    exit()

# Choix du fournisseur de tuiles (OSM) et de la projection
request_tiler = cimgt.OSM()
plt.figure(figsize=(12, 10))
ax = plt.axes(projection=request_tiler.crs)

# Détermination des limites de la carte
all_lons = [lon for t in tracks.values() for lon in t['lon']]
all_lats = [lat for t in tracks.values() for lat in t['lat']]
margin = 5 
ax.set_extent([min(all_lons)-margin, max(all_lons)+margin, 
               min(all_lats)-margin, max(all_lats)+margin], 
              crs=ccrs.PlateCarree())

# Ajout du fond de carte OSM
ax.add_image(request_tiler, 4)

# --- 3. Tracé des segments multicolores (Intensité/Pression) ---

# Normalisation globale de la pression pour l'échelle de couleurs
all_pressures = [p for t in tracks.values() for p in t['press']]
norm = plt.Normalize(min(all_pressures), max(all_pressures))

for track_id, data in tracks.items():
    if len(data['lon']) < 2:
        continue 

    # Préparation des données pour LineCollection
    x = np.array(data['lon'])
    y = np.array(data['lat'])
    p = np.array(data['press'])

    # Création des segments
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Création de la LineCollection
    lc = LineCollection(segments, cmap='jet_r', norm=norm, 
                        transform=ccrs.PlateCarree()) 
    
    # La couleur de chaque segment est basée sur la pression au début du segment
    lc.set_array(p[:-1])
    lc.set_linewidth(2)
    ax.add_collection(lc)

# --- 4. Finalisation et Affichage ---

# Barre de couleur (légende de la pression)
sm = plt.cm.ScalarMappable(cmap='jet_r', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.02)
cbar.set_label('Pression atmosphérique (hPa) - Rouge = Intense')

# Configuration de la grille
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5, crs=ccrs.PlateCarree())
gl.top_labels = False
gl.right_labels = False

plt.title("Trajectoires d'événements (Pression) sur fond OpenStreetMap")
plt.show()