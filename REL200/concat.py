import os

# 1. Définir les noms des fichiers d'entrée
file_paths = [
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2002-2003.vor5_res17_1_-2_5.rel200',
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2003-2004.vor5_res17_1_-2_5.rel200',
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2004-2005.vor5_res17_1_-2_5.rel200',
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2005-2006.vor5_res17_1_-2_5.rel200',
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2006-2007.vor5_res17_1_-2_5.rel200',
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2007-2008.vor5_res17_1_-2_5.rel200',
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2008-2009.vor5_res17_1_-2_5.rel200',
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2009-2010.vor5_res17_1_-2_5.rel200'
    '/home/florent/Documents/ENM_3A/Aladin/REL200/F10_10ans/suiATL_2010-2011.vor5_res17_1_-2_5.rel200']


# 2. Définir le nom du fichier de sortie (le fichier concaténé)
output_file = '/home/florent/Documents/ENM_3A/Aladin/REL200/concat/F10_concat.rel200'

# 3. Procéder à la concaténation
try:
    # Ouvre le fichier de sortie en mode 'write' ('w'). 
    # Cela écrase le fichier s'il existe déjà.
    # Le mot clé 'with' assure que le fichier est correctement fermé.
    with open(output_file, 'w', encoding='utf-8') as outfile:
        print(f"Démarrage de la concaténation dans : {output_file}")
        
        for file_path in file_paths:
            try:
                # Ouvre chaque fichier d'entrée en mode 'read' ('r')
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # Lit tout le contenu et l'écrit immédiatement dans le fichier de sortie
                    outfile.write(infile.read())
                    print(f"  - Fichier traité : {os.path.basename(file_path)}")
                    # AJOUT OPTIONNEL : Ajoute un saut de ligne ou un séparateur si nécessaire,
                    # mais ici nous mettons le texte "à la suite" sans séparateur explicite.
            except FileNotFoundError:
                print(f"  ATTENTION : Le fichier n'a pas été trouvé : {file_path}")
            except Exception as e:
                print(f"  ERREUR lors du traitement de {file_path}: {e}")

    print("\n Concaténation terminée avec succès.")
    
except Exception as e:
    print(f"\n ERREUR FATALE lors de l'ouverture du fichier de sortie : {e}")