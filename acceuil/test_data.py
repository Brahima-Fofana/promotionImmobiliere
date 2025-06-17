import os
import django
import random
from datetime import date, timedelta
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ton_projet.settings')  # remplace par le nom réel de ton projet
django.setup()

from .models import (
    Client, Projet, Souscription, Versement, Phase,
    Plan, CaracteristiqueProjet, Commentaire
)

# ------------------ 1. CLIENTS ------------------
clients = []
for i in range(5):
    client = Client.objects.create(
        login=f"user{i}",
        mot_pass="pass1234",
        nom=f"NOM{i}",
        prenom=f"Prenom{i}",
        date_naissance=date(1990 + i, 1, 1),
        NCI=f"CI00{i}ABCD",
        poste=f"poste{i}",
        contacts_1=f"+2250700000{i}",
        contacts_2=f"+2250100000{i}"
    )
    clients.append(client)

# ------------------ 2. PROJETS ------------------
projets = []
for i in range(3):
    projet = Projet.objects.create(
        libelle=f"Résidence Prestige {i}",
        contenue=f"Un projet immobilier haut standing à Abidjan {i}",
        type="Appartement",
        montant_investissement=10000000 + i * 1000000,
        modalite_investissement="mois",
        cout_total=15000000 + i * 1500000,
        image="projet/default.jpg",  # assure-toi qu’un fichier dummy existe
        slug=slugify(f"residence-prestige-{i}"),
        localisation="Abidjan Cocody",
        option="Avec piscine"
    )
    projets.append(projet)

# ------------------ 3. SOUSCRIPTIONS + VERSEMENTS ------------------
for projet in projets:
    for client in clients:
        Souscription.objects.create(projet=projet, client=client)
        # Chaque client paie 3 fois
        for j in range(3):
            Versement.objects.create(
                montant=200000 + j * 50000,
                date_payement=date.today() - timedelta(days=30 * j),
                projet=projet,
                client=client
            )

# ------------------ 4. PHASES ------------------
for projet in projets:
    Phase.objects.create(libelle="Terrassement", description="Préparation du terrain", status=True, projet=projet)
    Phase.objects.create(libelle="Élévation", description="Murs montés", status=False, projet=projet)

# ------------------ 5. PLANS ------------------
for projet in projets:
    for i in range(2):
        Plan.objects.create(
            libelle=f"Plan étage {i+1}",
            description="Plan architectural du bâtiment",
            image="plan_projet/default.jpg",
            projet=projet,
            ordre=i
        )

# ------------------ 6. CARACTÉRISTIQUES PROJET ------------------
for projet in projets:
    CaracteristiqueProjet.objects.create(
        libelle="Surface",
        valeur=150.0 + random.randint(0, 50),
        unite="m²",
        projet=projet
    )
    CaracteristiqueProjet.objects.create(
        libelle="Nombre de pièces",
        valeur=5 + random.randint(0, 3),
        unite="",
        projet=projet
    )

# ------------------ 7. COMMENTAIRES ------------------
for projet in projets:
    for client in clients:
        Commentaire.objects.create(
            projet=projet,
            client=client,
            contenue=f"Très bon projet {projet.libelle} !"
        )

print("✅ Données insérées avec succès !")
