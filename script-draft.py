import sys
import json
import datetime
import os

def main():
    # Vérifie qu'un argument a bien été passé (le chemin du fichier JSON)
    if len(sys.argv) < 2:
        print("Erreur : Aucun chemin de fichier JSON fourni.")
        sys.exit(1)

    # Récupère le chemin du fichier JSON passé par le MainController
    json_filepath = sys.argv[1]
    
    # Crée le chemin pour notre fichier de résultat (log)
    log_filepath = json_filepath + ".log.txt"

    try:
        # Lit le fichier JSON exporté par votre application
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Écrit un petit rapport dans un fichier texte
        with open(log_filepath, 'w', encoding='utf-8') as log:
            log.write(f"--- Rapport d'exécution du {datetime.datetime.now()} ---\n")
            log.write(f"Fichier reçu et analysé : {json_filepath}\n\n")
            
            # Extrait quelques informations pour prouver que le JSON est lisible
            actions = data.get('actions', [])
            clocks = data.get('clocks', [])
            locations = data.get('locations', {}) # locations est une liste ou un dict selon export_engine
            
            log.write(f"Nombre d'actions : {len(actions)}\n")
            log.write(f"Nombre d'horloges : {len(clocks)}\n")
            log.write(f"Nombre de localités : {len(locations)}\n\n")
            
            log.write("Bravo, le script tiers s'est exécuté avec succès depuis l'interface !\n")
            
        print(f"Succès ! Le fichier log a été généré : \n{log_filepath}")
            
    except Exception as e:
        # En cas d'erreur (ex: fichier introuvable, JSON invalide)
        with open(log_filepath, 'w', encoding='utf-8') as log:
            log.write(f"Une erreur est survenue lors de l'analyse du JSON :\n{e}\n")
        print(f"Une erreur est survenue : {e}")
        
    input("\nAppuyez sur Entrée pour fermer le terminal...")

if __name__ == "__main__":
    main()
