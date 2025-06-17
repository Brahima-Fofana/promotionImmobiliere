# acceuil/management/commands/generate_full_data.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Import des modèles
from acceuil.models import (
    Projet, CaracteristiqueProjet, Plan, CaracteristiquePlan,
    Phase, Album
)
from client.models import Client, Commentaire, Souscription, Versement
from django.contrib.auth.models import User

from general.models import ReseauxSociauxStaff, MembreStaff, Prestation, Appropos, ServiceCard, Compagnie, ServiceDetail

fake = Faker('fr_FR')


class Command(BaseCommand):
    help = "Génère un jeu de données complet pour la promotion immobilière en Côte d'Ivoire"

    def handle(self, *args, **options):
        self.stdout.write("Début de la génération des données complètes...")

        # 0. Création de la compagnie principale
        compagnie = Compagnie.objects.create(
            denomination="Promotion Immobilière CI",
            image="compagnie/logo.jpg",
            description="Leader de l'immobilier en Côte d'Ivoire depuis 2010",
            localisation="Abidjan, Plateau",
            email="contact@promoimmo.ci"
        )

        # 1. Génération des services (4 services)
        services = self.create_services(4, compagnie)

        # 2. Génération du contenu À propos
        self.create_about_content(compagnie)

        # 3. Génération des membres du staff (5 membres)
        self.create_staff_members(5)

        # 4. Génération des 30 clients
        clients = self.create_clients(30)

        # 5. Génération des 30 projets avec toutes les relations
        projets = self.create_projects(30)

        # 6. Création des relations entre clients et projets
        self.create_relations(clients, projets, services)

        self.stdout.write(self.style.SUCCESS("Données complètes générées avec succès!"))

    def create_services(self, count, compagnie):
        services = []
        icons = [
            'flaticon-home-2', 'flaticon-mountain',
            'flaticon-heart', 'flaticon-secure'
        ]

        for i in range(count):
            service = ServiceCard.objects.create(
                image='services/default.jpg',
                libelle=fake.sentence(nb_words=3),
                description=fake.text(max_nb_chars=100),
                option=random.choice(['active', '']),
                slug=slugify(fake.sentence(nb_words=2)),
                ordre=i,
                compagnie=compagnie
            )

            # Détail du service
            ServiceDetail.objects.create(
                image='services_detail/default.jpg',
                description=fake.sentence(),
                contenue=fake.text(max_nb_chars=500),
                service=service
            )

            services.append(service)
        return services

    def create_about_content(self, compagnie):
        about = Appropos.objects.create(
            image='appropos/default.jpg',
            presentation=fake.text(max_nb_chars=1000),
            slogan="Votre partenaire immobilier de confiance",
            option="about",
            route="about",
            compagnie=compagnie
        )

        # Prestations
        prestations = [
            ("Propriété Intelligente", "flaticon-home-2"),
            ("Travaux Publics", "flaticon-mountain"),
            ("Sécurité", "flaticon-secure"),
            ("Environnement Sain", "flaticon-heart")
        ]

        for libelle, icon in prestations:
            Prestation.objects.create(
                icon=icon,
                libelle=libelle,
                compagnie=about
            )

    def create_staff_members(self, count):
        for i in range(count):
            membre = MembreStaff.objects.create(
                nom=fake.last_name(),
                prenom=fake.first_name(),
                image='staff/default.jpg',
                poste=fake.job(),
                ordre=i
            )

            # Réseaux sociaux
            ReseauxSociauxStaff.objects.create(
                icon='fab fa-facebook-f',
                url=f"https://facebook.com/{slugify(membre.nom)}",
                staff=membre
            )

    def create_clients(self, count):
        clients = []
        for i in range(count):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password='password123'
            )

            client = Client.objects.create(
                user=user,
                date_naissance=fake.date_of_birth(minimum_age=25, maximum_age=65),
                CNI=fake.unique.bothify(text='CI##############'),
                poste=fake.job(),
                localisation=self.get_ivoirian_location(),
                contact1=self.generate_ivoirian_phone(),
                image='profile_client/default.png'
            )
            clients.append(client)
        return clients

    def create_projects(self, count):
        projets = []
        for i in range(count):
            # Nom du projet sans accents pour le slug
            nom_projet = f"Residence {fake.street_name()}"
            slug = slugify(nom_projet)

            # Description longue (30 lignes)
            description = "\n".join([fake.paragraph() for _ in range(30)])

            projet = Projet.objects.create(
                libelle=nom_projet,
                contenue=description,
                type=random.choice(['Residentiel', 'Commercial', 'Mixte', 'Bureaux']),
                montant_investissement=Decimal(random.randint(50000000, 500000000)),
                modalite_investissement=random.choice(['Mois', 'Annee']),
                cout_total=Decimal(random.randint(100000000, 1000000000)),
                image='projet/default.jpg',
                localisation=self.get_ivoirian_location(),
                option=random.choice(['En cours', 'Termine', 'A venir']),
                slug=slug
            )

            # 5 caractéristiques par projet
            self.add_project_features(projet)

            # 3 plans par projet
            self.add_project_plans(projet)

            # Phases du projet
            self.add_project_phases(projet)

            projets.append(projet)
        return projets

    def add_project_features(self, projet):
        features = [
            ("Superficie totale", "m²", Decimal(random.uniform(500.0, 5000.0)).quantize(Decimal('0.01'))),
            ("Longueur", "m", Decimal(random.uniform(50.0, 200.0)).quantize(Decimal('0.01'))),
            ("Largeur", "m", Decimal(random.uniform(30.0, 100.0)).quantize(Decimal('0.01'))),
            ("Nombre de logements", None, random.randint(5, 50)),
            ("Espaces verts", "m²", Decimal(random.uniform(100.0, 2000.0)).quantize(Decimal('0.01')))
        ]

        for feature in features:
            CaracteristiqueProjet.objects.create(
                libelle=feature[0],
                valeur=feature[2],
                unite=feature[1],
                projet=projet
            )

    def add_project_plans(self, projet):
        plan_types = [
            ("Plan d'architecture", "Vue d'ensemble du projet"),
            ("Plan d'etage", "Details de chaque niveau"),
            ("Plan 3D", "Visualisation en trois dimensions")
        ]

        for i, (titre, desc) in enumerate(plan_types):
            plan = Plan.objects.create(
                libelle=f"{titre} - {projet.libelle}",
                description=desc,
                image='plan_projet/default.jpg',
                projet=projet,
                ordre=i
            )

            # 4 caractéristiques par plan - Valeurs décimales corrigées
            plan_features = [
                ("Longueur", "m", Decimal(random.uniform(20.0, 100.0)).quantize(Decimal('0.01'))),
                ("Largeur", "m", Decimal(random.uniform(15.0, 50.0)).quantize(Decimal('0.01'))),
                ("Echelle", None, Decimal('0.005')),  # 1:200 = 0.005
                ("Date", None, datetime.now().year)  # Utilisation de l'année comme nombre
            ]

            for feature in plan_features:
                CaracteristiquePlan.objects.create(
                    libelle=feature[0],
                    valeur=feature[2],
                    unite=feature[1],
                    plan=plan
                )

    def add_project_phases(self, projet):
        phases = [
            ("Preparation", "Travaux preliminaires et terrassement"),
            ("Fondations", "Realisation des infrastructures"),
            ("Gros oeuvre", "Construction de la structure")
        ]

        for i, (nom, desc) in enumerate(phases):
            phase = Phase.objects.create(
                libelle=f"Phase {i + 1}: {nom}",
                description=desc,
                status=random.choice([True, False]),
                projet=projet
            )

            # Album photos pour la phase
            Album.objects.create(
                titre=f"Photo {i + 1} - {phase.libelle}",
                image='album/default.jpg',
                phase=phase
            )

    def create_relations(self, clients, projets, services):
        for projet in projets:
            # Sélection de 5 à 10 clients par projet
            projet_clients = random.sample(clients, random.randint(5, 10))

            for client in projet_clients:
                # Souscription aléatoire
                if random.random() < 0.7:
                    souscription = Souscription.objects.create(
                        projet=projet,
                        client=client
                    )

                    # Versement aléatoire
                    if random.random() < 0.5:
                        Versement.objects.create(
                            montant=Decimal(random.randint(500000, 5000000)),
                            souscription=souscription
                        )

                # 3 commentaires par client/projet
                for _ in range(3):
                    Commentaire.objects.create(
                        projet=projet,
                        client=client,
                        contenue=self.generate_comment(projet.libelle)
                    )

    def get_ivoirian_location(self):
        villes = ["Abidjan", "Yamoussoukro", "Bouake", "San-Pedro", "Korhogo"]
        quartiers = ["Cocody", "Plateau", "Yopougon", "Marcory", "Riviera"]
        return f"{random.choice(villes)}, {random.choice(quartiers)}"

    def generate_ivoirian_phone(self):
        prefixes = ['01', '05', '07', '25', '27', '45', '47']
        return f"+225 {random.choice(prefixes)}{fake.numerify(text='########')}"

    def generate_comment(self, project_name):
        comments = [
            f"Le projet {project_name} correspond parfaitement a mes attentes.",
            f"J'ai visite le site de {project_name} et je suis impressionne par la qualite des travaux.",
            f"{project_name} offre un excellent rapport qualite-prix.",
            f"L'emplacement de {project_name} est strategique et les prestations sont de haut niveau.",
            f"Je recommande {project_name} a tous ceux qui cherchent un investissement fiable."
        ]
        return random.choice(comments)