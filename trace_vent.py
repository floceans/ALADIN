import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

file_path = Path("/home/florent/Documents/ENM_3A/Aladin/modele_forceur/suiamip_g359_concatene.rel200")
text = file_path.read_text(encoding='utf-8', errors='ignore').replace('\r','\n')
raw_blocks = re.split(r'\n\s*\n', text.strip())

blocks=[]
for raw in raw_blocks:
    lines=[l.strip() for l in raw.split("\n") if l.strip()]
    parsed=[]
    for ln in lines:
        parts=re.split(r'\s+', ln)
        try:
            nums=[float(p) for p in parts]
            parsed.append(nums)
        except:
            pass
    if parsed:
        blocks.append(parsed)

winds=[]
for b in blocks:
    col=[]
    for row in b:
        col.append(row[5] if len(row)>=5 else np.nan)
    winds.append(np.array(col,dtype=float))

plt.figure(figsize=(10,6))

for i,w in enumerate(winds):
    # trouver premier point valide
    valid = np.where(~np.isnan(w))[0]
    if len(valid)==0: 
        continue
    start = valid[0]
    w2 = w[start:]              # couper avant
    x2 = np.arange(len(w2)) + 1 # ramener au pas de temps 1
    plt.plot(x2, w2, linewidth=2.5)

plt.xlabel("Pas de temps aligné (premier point ramené à gauche)")
plt.ylabel("Vent (colonne 5)")
plt.title("Courbes alignées — premier point ramené à gauche")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
