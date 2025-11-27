import numpy as np
import matplotlib.pyplot as plt

nbr_bat = [21, 333, 2843, 4024, 4240, 4309]
alti = [1, 2, 4, 6, 8, 10]

plt.plot(nbr_bat, alti, marker='o')
plt.xlabel("Nombre de batiments")
plt.ylabel("Elevation du niveau d'eau (m)")
plt.title("Nombre de batiments touchés selon élévation du niveau d'eau")
plt.show()