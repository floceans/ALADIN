import csv
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx

# --- 1) Lecture manuelle du fichier texte ---
file_path = "C:\\Users\\flore\\Documents\\cours\\N7_ENM_3A\\Aladin\\modele_forceur\\suiamip_g359_concatene.rel200"

longitudes = []
latitudes = []
pressures = []

with open(file_path, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # ignorer lignes vides ou commentaires

        parts = line.split()
        if len(parts) < 4:
            continue  # ligne trop courte -> on ignore

        # Colonne 2 = longitude (index 1)
        # Colonne 3 = latitude  (index 2)
        # Dernière colonne = pression
        try:
            lon = float(parts[1])
            lat = float(parts[2])
            pres = float(parts[-1])
        except ValueError:
            continue  # ligne non numérique → sauter
        
        if pres >930 and pres <1100:  # Filtrer les pressions réalistes
            longitudes.append(lon)
            latitudes.append(lat)
            pressures.append(pres)

# --- 2) Création de la GeoDataFrame ---
geoms = [Point(lon, lat) for lon, lat in zip(longitudes, latitudes)]
gdf = gpd.GeoDataFrame({"pressure": pressures}, geometry=geoms, crs="EPSG:4326")

# Reprojection pour OSM
gdf_3857 = gdf.to_crs(epsg=3857)

# --- 3) Tracé ---
fig, ax = plt.subplots(figsize=(10, 8))

x = gdf_3857.geometry.x
y = gdf_3857.geometry.y

scatter = ax.scatter(
    x, y, c=gdf_3857["pressure"],
    cmap="rainbow_r", s=10, alpha=0.9, edgecolor="none"
)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label("Pression")

# Fond OpenStreetMap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Zoom automatique
ax.set_xlim(x.min(), x.max())
ax.set_ylim(y.min(), y.max())

ax.set_axis_off()
plt.tight_layout()
plt.show()
