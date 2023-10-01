import csv

# ---------------------------------------------------------------
#       Fonctions d'affichage et de statistiques
# ---------------------------------------------------------------
def afficher_statistiques_fichier(fichier, lignes, valeurs_manquantes):
    """
    Affiche des statistiques après avoir lu un fichier.
    """
    print("📂📊 ----------------------------------------------------------------------------------------------------------------")
    print(f"📂 Fichier {fichier} lu avec succès. 🎉")
    print(f"📌 Nombre de colonnes: {len(lignes[0])}")
    print(f"📌 Nombre de lignes: {len(lignes)}")
    print(f"⚠️ Nombre de valeurs manquantes: {valeurs_manquantes}")
    print("--------------------------------------------------------------------------------------------------------------------")

def afficher_statistiques_finales(data_final):
    print("📊 ----------------------------------------------------------------------------------------------------------------")
    print("🌎 Statistiques des pays retenus:")
    print("--------------------------------------------------------------------------------------------------------------------")
    print(f"🌐 Nombre total de pays retenus: {len(data_final)}")
    annees_totales = set()
    for data_pays in data_final.values():
        annees_totales.update(data_pays.keys())
    print("--------------------------------------------------------------------------------------------------------------------")
    print(f"📅 Nombre total d'années retenues: {len(annees_totales)}")
    print("--------------------------------------------------------------------------------------------------------------------")
    print("📅 Années retenues:")
    print(sorted(list(annees_totales)))
    print("--------------------------------------------------------------------------------------------------------------------")

def afficher_top_n(titre, data, n=10):
    print("🔝 ----------------------------------------------------------------------------------------------------------------")
    print(titre)
    print("--------------------------------------------------------------------------------------------------------------------")
    for rang, (entite, valeur) in enumerate(sorted(data.items(), key=lambda x: x[1], reverse=True)[:n], 1):
        print(f"🥇 Rang {rang}. {entite}: {valeur}")
    print("--------------------------------------------------------------------------------------------------------------------")

def afficher_bottom_n(titre, data, n=10):
    print("🔝 ----------------------------------------------------------------------------------------------------------------")
    print(titre)
    print("--------------------------------------------------------------------------------------------------------------------")
    for rang, (entite, valeur) in enumerate(sorted(data.items(), key=lambda x: x[1])[:n], 1):
        print(f"🥉 Rang {rang}. {entite}: {valeur}")
    print("--------------------------------------------------------------------------------------------------------------------")

def afficher_pays_communs(pays_communs):
    if pays_communs:
        print("✅ Les pays qu'on retrouve dans les listes d'augmentation ou élévation sont:", ", ".join(pays_communs))
        print("--------------------------------------------------------------------------------------------------------------------")
    else:
        print("❌ Aucun pays n'est retrouvé dans les listes d'augmentation ou élévation.")
        print("--------------------------------------------------------------------------------------------------------------------")

def afficher_pays_communs_bottom(pays_communs):
    if pays_communs:
        print("✅ Les pays qu'on retrouve dans les listes de faible croissance sont:", ", ".join(pays_communs))
        print("--------------------------------------------------------------------------------------------------------------------")
    else:
        print("❌ Aucun pays n'est retrouvé dans les listes de faible croissance.")
        print("--------------------------------------------------------------------------------------------------------------------")

def afficher_resultats(annee_augmentation_max, augmentation_max):
    print("📊 ----------------------------------------------------------------------------------------------------------------")
    print(f"🌡️ L'année avec la plus forte augmentation de température mondiale est {annee_augmentation_max}.")
    print(f"🔺 Augmentation moyenne: {augmentation_max:.2f}°C")
    print("--------------------------------------------------------------------------------------------------------------------")

def affichage(message, pays_valides=None, data=None, index_choisi=None):
    if message == "intro":
        return input("🌍 Tous nos calculs sont terminés. Voulez-vous choisir un pays spécifique pour afficher ses données? (Y/N) ").strip().upper()
    elif message == "liste_pays":
        largeur_max = max([len(pays) for pays in pays_valides]) + 5 
        for idx, pays in enumerate(pays_valides, 1):
            print(f"{idx}. {pays}".ljust(largeur_max), end="")
            if idx % 5 == 0: 
                print()
        print()
    elif message == "choix_pays":
        return input("\nEntrez le numéro du pays : ").strip()
    elif message == "donnees_pays":
        print("\nDonnées pour", pays_valides[index_choisi], ":")
        print(data[pays_valides[index_choisi]])
        print("--------------------------------------------------------------------------------------------------------------------")
    elif message == "reponse":
        return input("Voulez-vous choisir un autre pays? (Y/N) ").strip().upper()
    elif message == "merci":
        print("--------------------------------------------------------------------------------------------------------------------")
        print("🙏 Merci d'avoir utilisé notre service. Au revoir! 🚀")
        print("--------------------------------------------------------------------------------------------------------------------")
    elif message == "choix_non_valide":
        print("❌ Choix non valide. Veuillez entrer un numéro de la liste.")
        print("--------------------------------------------------------------------------------------------------------------------")


# ---------------------------------------------------------------
#               Lecture du fichier:gdp_data
# ---------------------------------------------------------------
def lire_gdp_data():
    fichier = "gdp_data.csv"
    data = {}
    valeurs_manquantes = 0

    colonnes_attendues = [
        "Country",
        "Year",
        "GDP",
        "GDP-Growth",
        "GDP-Per-Capita",
        "Code",
    ]

    with open(fichier, "r") as f:
        reader = csv.DictReader(f)

        for col in reader.fieldnames:
            if col not in colonnes_attendues:
                print(f"Avertissement: Colonne {col} non attendue dans {fichier}")

        lignes = list(reader)
        for row in lignes:
            pays = row.get("Country")
            annee = row.get("Year")

            if not pays or not annee:
                continue

            annee = int(annee)

            if pays not in data:
                data[pays] = {}

            data[pays][annee] = {
                "GDP": row.get("GDP"),
                "GDP-Growth": row.get("GDP-Growth"),
                "GDP-Per-Capita": row.get("GDP-Per-Capita"),
                "Code": row.get("Code")
            }

            for key, value in row.items():
                if not value:
                    valeurs_manquantes += 1

    afficher_statistiques_fichier(fichier, lignes, valeurs_manquantes)
    return (
        data,
        set(data.keys()),
        {year for country_data in data.values() for year in country_data.keys()},
    )

# ---------------------------------------------------------------
#               Lecture du fichier: temperatures
# ---------------------------------------------------------------

def lire_temperatures():
    fichier = "GlobalLandTemperaturesByCountry.csv"
    data = {}
    valeurs_manquantes = 0

    colonnes_attendues = [
        "Country",
        "dt",
        "AverageTemperature",
        "AverageTemperatureUncertainty",
    ]

    with open(fichier, "r") as f:
        reader = csv.DictReader(f)

        for col in reader.fieldnames:
            if col not in colonnes_attendues:
                print(f"Avertissement: Colonne {col} non attendue dans {fichier}")

        lignes = list(reader)
        for row in lignes:
            pays = row.get("Country")
            annee = row.get("dt", "").split("-")[0]

            if not pays or not annee:
                continue

            annee = int(annee)

            if pays not in data:
                data[pays] = {}

            data[pays][annee] = {
                "AverageTemperature": row.get("AverageTemperature"),
                "AverageTemperatureUncertainty": row.get("AverageTemperatureUncertainty")
            }

            for key, value in row.items():
                if not value:
                    valeurs_manquantes += 1

    afficher_statistiques_fichier(fichier, lignes, valeurs_manquantes)
    return (
        data,
        set(data.keys()),
        {year for country_data in data.values() for year in country_data.keys()},
    )

# ---------------------------------------------------------------
#               Lecture du fichier: population
# ---------------------------------------------------------------

def lire_population():
    fichier = "World-population-by-countries-dataset.csv"
    data = {}
    valeurs_manquantes = 0

    colonnes_minimales_attendues = ["Country Name"]

    with open(fichier, "r") as f:
        reader = csv.DictReader(f)

        for col in colonnes_minimales_attendues:
            if col not in reader.fieldnames:
                print(f"Avertissement: Colonne {col} manquante dans {fichier}")

        lignes = list(reader)
        for row in lignes:
            pays = row.get("Country Name")

            if not pays:
                continue

            if pays not in data:
                data[pays] = {}

            for annee, valeur in row.items():
                if annee.isdigit():
                    annee_int = int(annee)
                    if annee_int not in data[pays]:
                        data[pays][annee_int] = {}
                    data[pays][annee_int][annee] = valeur if valeur else None

                    if not valeur:
                        valeurs_manquantes += 1

    afficher_statistiques_fichier(fichier, lignes, valeurs_manquantes)
    return (
        data,
        set(data.keys()),
        {year for country_data in data.values() for year in country_data.keys()},
    )


# ---------------------------------------------------------------
#                   Rassembler les données
# ---------------------------------------------------------------

def rassembler_donnees(gdp_data, temp_data, pop_data, pays_communs, annees_communes):
    data_final = {}

    for pays in pays_communs:
        data_final[pays] = {}

        for annee in annees_communes:
            if (
                annee in gdp_data.get(pays, {})
                and annee in temp_data.get(pays, {})
                and annee in pop_data.get(pays, {})
            ):
                data_final[pays][annee] = {
                    "temperature": temp_data[pays][annee].get("AverageTemperature"),
                    "population": pop_data[pays][annee].get(
                        str(annee)
                    ),  # conversion de l'année en chaîne pour l'utiliser comme clé
                    "gdp": gdp_data[pays][annee].get("GDP"),
                }

    return data_final


# ---------------------------------------------------------------
#          calculs d'indices statistiques pour les pays
# ---------------------------------------------------------------
def top_10_pays_par_croissance_population(dictionnaire_final):
    croissance_population = {}

    for pays, donnees in dictionnaire_final.items():
        annees = sorted(donnees.keys())
        if len(annees) < 2:
            continue
        population_initiale = float(donnees[annees[0]]['population'] or 0)
        population_finale = float(donnees[annees[-1]]['population'] or 0)
        croissance = population_finale - population_initiale
        croissance_population[pays] = croissance

    # Utilisez la fonction afficher_top_n pour afficher les résultats
    afficher_top_n("Les 10 pays avec la plus forte croissance en nombre de personnes", croissance_population)


def bottom_10_pays_par_croissance_population(dictionnaire_final):
    croissance_population = {}

    for pays, donnees in dictionnaire_final.items():
        annees = sorted(donnees.keys())
        if len(annees) < 2:
            continue
        population_initiale = float(donnees[annees[0]]['population'] or 0)
        population_finale = float(donnees[annees[-1]]['population'] or 0)
        croissance = population_finale - population_initiale
        croissance_population[pays] = croissance

    # Triez les pays par croissance de la population en ordre croissant et prenez les 10 premiers
    bottom_10_croissance = dict(sorted(croissance_population.items(), key=lambda x: x[1])[:10])

    # Utilisez la fonction afficher_bottom_n pour afficher les résultats
    afficher_bottom_n("Les 10 pays avec la plus faible croissance en nombre de personnes", bottom_10_croissance)


def top_10_pays_par_augmentation_PIB_par_habitant(dictionnaire_final):
    augmentation_PIB_par_habitant = {}

    for pays, donnees in dictionnaire_final.items():
        annees = sorted(donnees.keys())
        if len(annees) < 2:
            continue
        
        PIB_initial = float(donnees[annees[0]]['gdp'] or 0)
        population_initiale = float(donnees[annees[0]]['population'] or 0)
        PIB_per_capita_initial = PIB_initial / population_initiale if population_initiale else 0

        PIB_final = float(donnees[annees[-1]]['gdp'] or 0)
        population_finale = float(donnees[annees[-1]]['population'] or 0)
        PIB_per_capita_final = PIB_final / population_finale if population_finale else 0

        augmentation = PIB_per_capita_final - PIB_per_capita_initial
        augmentation_PIB_par_habitant[pays] = augmentation

    # Triez les pays par augmentation du PIB par habitant en ordre décroissant et prenez les 10 premiers
    top_10_augmentation = dict(sorted(augmentation_PIB_par_habitant.items(), key=lambda x: x[1], reverse=True)[:10])

    # Utilisez la fonction afficher_top_n pour afficher les résultats
    afficher_top_n("Les 10 pays avec la plus forte augmentation du PIB par habitant", top_10_augmentation)



def bottom_10_pays_par_augmentation_PIB_par_habitant(dictionnaire_final):
    augmentation_PIB_par_habitant = {}

    for pays, donnees in dictionnaire_final.items():
        annees = sorted(donnees.keys())
        if len(annees) < 2:
            continue
        
        PIB_initial = float(donnees[annees[0]]['gdp'] or 0)
        population_initiale = float(donnees[annees[0]]['population'] or 0)
        PIB_per_capita_initial = PIB_initial / population_initiale if population_initiale else 0

        PIB_final = float(donnees[annees[-1]]['gdp'] or 0)
        population_finale = float(donnees[annees[-1]]['population'] or 0)
        PIB_per_capita_final = PIB_final / population_finale if population_finale else 0

        augmentation = PIB_per_capita_final - PIB_per_capita_initial
        augmentation_PIB_par_habitant[pays] = augmentation

    # Triez les pays par augmentation du PIB par habitant en ordre croissant et prenez les 10 premiers
    bottom_10_augmentation = dict(sorted(augmentation_PIB_par_habitant.items(), key=lambda x: x[1])[:10])

    # Utilisez la fonction afficher_bottom_n pour afficher les résultats
    afficher_bottom_n("Les 10 pays avec la plus faible augmentation du PIB par habitant", bottom_10_augmentation)


def top_10_pays_par_augmentation_temperature(dictionnaire_final):
    augmentation_temperature = {}

    for pays, donnees in dictionnaire_final.items():
        annees = sorted(donnees.keys())
        if len(annees) < 2:
            continue

        temp_initial = float(donnees[annees[0]]['temperature'] or 0)
        temp_final = float(donnees[annees[-1]]['temperature'] or 0)
        augmentation = temp_final - temp_initial
        augmentation_temperature[pays] = augmentation

    # Triez les pays par augmentation de température en ordre décroissant et prenez les 10 premiers
    top_10_augmentation = dict(sorted(augmentation_temperature.items(), key=lambda x: x[1], reverse=True)[:10])

    # Utilisez la fonction afficher_top_n pour afficher les résultats
    afficher_top_n("Les 10 pays avec la plus forte augmentation en température", top_10_augmentation)

def bottom_10_pays_par_augmentation_temperature(dictionnaire_final):
    augmentation_temperature = {}

    for pays, donnees in dictionnaire_final.items():
        annees = sorted(donnees.keys())
        if len(annees) < 2:
            continue

        temp_initial = float(donnees[annees[0]]['temperature'] or 0)
        temp_final = float(donnees[annees[-1]]['temperature'] or 0)
        augmentation = temp_final - temp_initial
        augmentation_temperature[pays] = augmentation

    # Triez les pays par augmentation de température en ordre croissant et prenez les 10 premiers
    bottom_10_augmentation = dict(sorted(augmentation_temperature.items(), key=lambda x: x[1])[:10])

    # Utilisez la fonction afficher_bottom_n pour afficher les résultats
    afficher_bottom_n("Les 10 pays avec la plus faible augmentation en température", bottom_10_augmentation)

def top_n_pays(dictionnaire_final, cle_donnee, n=10, inverse=False):
    """
    Retourne les n premiers pays selon la clé fournie.
    """
    evolution = {
        pays: float(donnees[sorted(donnees.keys())[-1]][cle_donnee] or 0) - float(donnees[sorted(donnees.keys())[0]][cle_donnee] or 0)
        for pays, donnees in dictionnaire_final.items()
        if len(donnees.keys()) > 1
    }
    
    return set(sorted(evolution, key=evolution.get, reverse=not inverse)[:n])

def pays_communs_dans_top_10(dictionnaire_final):
    top_population = top_n_pays(dictionnaire_final, 'population')
    top_PIB_par_habitant = top_n_pays(dictionnaire_final, 'gdp')  # Notez que ceci ne calcule pas réellement le PIB par habitant
    top_temperature = top_n_pays(dictionnaire_final, 'temperature')
    
    return top_population & top_PIB_par_habitant & top_temperature


def pays_communs_dans_bottom_10(dictionnaire_final):
    bottom_population = top_n_pays(dictionnaire_final, 'population', inverse=True)
    bottom_PIB_par_habitant = top_n_pays(dictionnaire_final, 'gdp', inverse=True)  # Encore une fois, cela suppose que 'gdp' est le PIB par habitant
    bottom_temperature = top_n_pays(dictionnaire_final, 'temperature', inverse=True)
    
    return bottom_population & bottom_PIB_par_habitant & bottom_temperature

def top_10_pays_par_score(dictionnaire_final, w1=0.3, w2=0.2, w3=0.5):
    scores = {}

    for pays, donnees in dictionnaire_final.items():
        annees = sorted(donnees.keys())
        if len(annees) < 2:
            continue
        
        population_initiale = float(donnees[annees[0]]['population'] or 0)
        population_finale = float(donnees[annees[-1]]['population'] or 0)
        croissance_population = population_finale - population_initiale

        PIB_initial = float(donnees[annees[0]]['gdp'] or 0)
        population_initiale = float(donnees[annees[0]]['population'] or 0)
        PIB_per_capita_initial = PIB_initial / population_initiale if population_initiale else 0

        PIB_final = float(donnees[annees[-1]]['gdp'] or 0)
        population_finale = float(donnees[annees[-1]]['population'] or 0)
        PIB_per_capita_final = PIB_final / population_finale if population_finale else 0

        augmentation_PIB_par_habitant = PIB_per_capita_final - PIB_per_capita_initial

        temp_initial = float(donnees[annees[0]]['temperature'] or 0)
        temp_final = float(donnees[annees[-1]]['temperature'] or 0)
        augmentation_temperature = temp_final - temp_initial

        # Calcul du score en utilisant la formule donnée
        score = (w1 * croissance_population + w2 * augmentation_PIB_par_habitant - w3 * augmentation_temperature) / (w1 + w2 + w3)
        scores[pays] = score

    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10])

def afficher_top_10_pays_par_score(dictionnaire_final):
    top_10_pays = top_10_pays_par_score(dictionnaire_final)
    afficher_top_n("Les 10 pays en tête du classement par score", top_10_pays)


def annee_avec_plus_forte_augmentation_moyenne(dictionnaire_final):
    """
    Trouve et affiche l'année où l'augmentation moyenne de la température mondiale a été la plus forte.
    :param dictionnaire_final: Données consolidées par pays et par année.
    """
    
    # Rassemble toutes les années présentes dans dictionnaire_final
    toutes_les_annees = {annee for pays in dictionnaire_final for annee in dictionnaire_final[pays]}
    augmentations_moyennes = {}

    for annee in sorted(toutes_les_annees):
        if annee + 1 in toutes_les_annees:  # Vérifie que l'année suivante existe
            somme_augmentations = 0
            compteur_pays = 0
            
            for pays, donnees_pays in dictionnaire_final.items():
                if annee in donnees_pays and annee + 1 in donnees_pays:
                    temperature_annee = donnees_pays[annee]['temperature']
                    temperature_annee_suivante = donnees_pays[annee + 1]['temperature']

                    # Assurez-vous que les deux chaînes ne sont pas vides avant de les convertir
                    if temperature_annee and temperature_annee_suivante:
                        temperature_annee = float(temperature_annee)
                        temperature_annee_suivante = float(temperature_annee_suivante)
                    
                        somme_augmentations += temperature_annee_suivante - temperature_annee
                        compteur_pays += 1

            # Calcul de l'augmentation moyenne pour cette année
            if compteur_pays != 0:
                augmentations_moyennes[annee + 1] = somme_augmentations / compteur_pays

    # Trouver l'année avec la plus forte augmentation moyenne
    annee_augmentation_max = max(augmentations_moyennes, key=augmentations_moyennes.get)
    augmentation_max = augmentations_moyennes[annee_augmentation_max]
    return annee_augmentation_max, augmentation_max

# ---------------------------------------------------------------
#    Obtention des donnees pour pays choisi par l'utilisateur
# ---------------------------------------------------------------

def obtenir_donnees_pour_pays(data_final):
    reponse = affichage("intro")
    if reponse != 'Y':
        affichage("merci")
        return

    pays_valides = sorted(list(data_final.keys()))

    while True:
        affichage("liste_pays", pays_valides=pays_valides)
        choix = affichage("choix_pays")

        if choix.isdigit():
            index_choisi = int(choix) - 1
            if 0 <= index_choisi < len(pays_valides):
                affichage("donnees_pays", pays_valides=pays_valides, data=data_final, index_choisi=index_choisi)
                reponse = affichage("reponse")
                if reponse != 'Y':
                    affichage("merci")
                    break
            else:
                affichage("choix_non_valide")
        else:
            affichage("choix_non_valide")

# ---------------------------------------------------------------
#                     POINT D'ENTRÉE DU CODE
# ---------------------------------------------------------------
if __name__ == "__main__":

    # la liste des pays présents dans le fichier GDP et les années disponibles.
    gdp_data, gdp_pays, gdp_annees = lire_gdp_data()
    # la liste des pays présents dans le fichier des températures et les années disponibles.
    temp_data, temp_pays, temp_annees = lire_temperatures()
    # la liste des pays présents dans le fichier de population et les années disponibles.
    pop_data, pop_pays, pop_annees = lire_population()
    # Cela donne une liste de pays présents dans tous les fichiers.
    pays_communs = gdp_pays.intersection(temp_pays).intersection(pop_pays)
    # Cela donne une liste d'années présentes dans tous les fichiers.
    annees_communes = gdp_annees.intersection(temp_annees).intersection(pop_annees)
    # Rassemble toutes les données des trois fichiers en un seul dictionnaire en utilisant uniquement les pays et les années communs.
    dictionnaire_final = rassembler_donnees(
        gdp_data, temp_data, pop_data, pays_communs, annees_communes
    )
    # Affiche les statistiques finales basées sur le dictionnaire consolidé.
    afficher_statistiques_finales(dictionnaire_final)

    # Ajoutez cet appel après l'affichage des statistiques finales ou après obtenir_donnees_pour_pays.
    top_10_pays_par_croissance_population(dictionnaire_final)
    bottom_10_pays_par_croissance_population(dictionnaire_final)
    top_10_pays_par_augmentation_PIB_par_habitant(dictionnaire_final)
    bottom_10_pays_par_augmentation_PIB_par_habitant(dictionnaire_final)
    top_10_pays_par_augmentation_temperature(dictionnaire_final)
    pays_communs = pays_communs_dans_top_10(dictionnaire_final)
    afficher_pays_communs(pays_communs)
    pays_communs = pays_communs_dans_bottom_10(dictionnaire_final)
    afficher_pays_communs_bottom(pays_communs)
    afficher_top_10_pays_par_score(dictionnaire_final)
    resultats = annee_avec_plus_forte_augmentation_moyenne(dictionnaire_final)
    afficher_resultats(*resultats)
    # Demande à l'utilisateur de choisir un pays depuis une liste numérotée et affiche les données associées à ce pays.
    obtenir_donnees_pour_pays(dictionnaire_final)