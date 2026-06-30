"""
Génère un fichier passages.csv simulé pour la séance 05.
Simule des passages de bus aux arrêts avec un horodatage,
afin de pouvoir calculer des heures de pointe réalistes
(absentes du référentiel de base lignes/arrets/bus/tarifs).
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

ARRETS_PATH = "../data/referentiel/arrets.csv"
LIGNES_PATH = "../data/referentiel/lignes.csv"
OUTPUT_PATH = "passages.csv"

NB_PASSAGES = 5000
DATE_DEBUT = datetime(2026, 6, 1, 5, 30)  # début de service 5h30
DATE_FIN = datetime(2026, 6, 1, 22, 0)    # fin de service 22h00

# Heures de pointe pondérées (matin 7-9h, soir 17-19h plus fréquentes)
def heure_ponderee():
    r = random.random()
    if r < 0.35:
        # pointe du matin
        h = random.randint(6, 9)
    elif r < 0.70:
        # pointe du soir
        h = random.randint(16, 19)
    else:
        # reste de la journée
        h = random.choice([5, 10, 11, 12, 13, 14, 15, 20, 21])
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return h, m, s


def lire_ids(path, colonne):
    ids = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.append(row[colonne])
    return ids


def main():
    arret_ids = lire_ids(ARRETS_PATH, "arret_id")
    ligne_ids = lire_ids(LIGNES_PATH, "ligne_id")

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["passage_id", "arret_id", "ligne_id", "horaire", "nb_voyageurs"])

        for i in range(1, NB_PASSAGES + 1):
            arret_id = random.choice(arret_ids)
            ligne_id = random.choice(ligne_ids)
            h, m, s = heure_ponderee()
            horaire = datetime(2026, 6, 1, h, m, s)
            nb_voyageurs = random.randint(0, 45)
            writer.writerow([
                f"P{i:05d}",
                arret_id,
                ligne_id,
                horaire.strftime("%Y-%m-%d %H:%M:%S"),
                nb_voyageurs,
            ])

    print(f"[OK] {NB_PASSAGES} passages générés dans {OUTPUT_PATH}")


if __name__ == "__main__":
    main()