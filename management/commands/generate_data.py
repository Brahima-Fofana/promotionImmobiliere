import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

# Import de tous les modèles
from general.models import Compagnie, Contact, ReseauxSociaux
from acceuil.models import Projet, CaracteristiqueProjet, Plan, Phase
from client.models import Client, Souscription, Versement

fake = Faker('fr_FR')


class Command(BaseCommand):
    help = 'Génère des données réalistes pour toutes les applications'

    def handle(self, *args, **options):
        # 1. Création de la compagnie (general)
        compagnie = self.create_compagnie()

        # 2. Création des projets (acceuil)
        projets = self.create_projects(10)

        # 3. Création des clients (client)
        clients = self.create_clients(20)

        # 4. Création des relations
        self.create_relations(compagnie, projets, clients)

        self.stdout.write(self.style.SUCCESS("Données générées avec succès!"))

    def create_compagnie(self):
        compagnie = Compagnie.objects.create(
            denomination="Groupe Immobilier Ivoirien",
            image="compagnie/logo.jpg",
            description="Leader du marché immobilier en Côte d'Ivoire",
            localisation="Abidjan, Plateau",
            email="contact@groupe-ivoirien.ci"
        )

        # Ajout des contacts
        Contact.objects.create(
            icon="icon-call",
            libelle="+225 27 22 50 00 00",
            compagnie=compagnie
        )

        # Ajout des réseaux sociaux
        ReseauxSociaux.objects.create(
            icon="fab fa-facebook-f",
            url="https://facebook.com/groupeivoirien",
            compagnie=compagnie
        )

        return compagnie

    def create_projects(self, count):
        projets = []
        for i in range(count):
            projet = Projet.objects.create(
                libelle=f"Résidence {fake.word().capitalize()}",
                contenue=fake.text(),
                type=random.choice(['Résidentiel', 'Commercial', 'Mixte']),
                montant_investissement=random.randint(50000000, 500000000),
                modalite_investissement=random.choice(['Mois', 'Année']),
                cout_total=random.randint(100000000, 1000000000),
                image="projet/default.jpg",
                localisation=self.get_ivoirian_location(),
                option=random.choice(['En cours', 'Terminé']),
                slug=f"residence-{fake.unique.word()}"
            )

            # Ajout caractéristiques
            CaracteristiqueProjet.objects.create(
                libelle="Superficie",
                valeur=random.randint(500, 5000),
                unite="m²",
                projet=projet
            )

            projets.append(projet)
        return projets

    def create_clients(self, count):
        clients = []
        for i in range(count):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.email(),
                password='password123'
            )

            client = Client.objects.create(
                user=user,
                date_naissance=fake.date_of_birth(),
                CNI=fake.unique.bothify(text='CI##############'),
                poste=random.choice(['Entrepreneur', 'Fonctionnaire', 'Commerçant']),
                localisation=self.get_ivoirian_location(),
                contact1=self.generate_ivoirian_phone()
            )
            clients.append(client)
        return clients

    def create_relations(self, compagnie, projets, clients):
        # Souscriptions aléatoires
        for projet in projets:
            for client in random.sample(clients, random.randint(3, 8)):
                souscription = Souscription.objects.create(
                    projet=projet,
                    client=client
                )

                # Versements aléatoires
                if random.random() > 0.4:  # 60% de chance
                    Versement.objects.create(
                        montant=random.randint(500000, 5000000),
                        souscription=souscription
                    )

    def get_ivoirian_location(self):
        villes = ["Abidjan", "Yamoussoukro", "Bouaké", "San-Pédro", "Korhogo"]
        quartiers = ["Cocody", "Plateau", "Yopougon", "Marcory", "Riviera"]
        return f"{random.choice(villes)}, {random.choice(quartiers)}"

    def generate_ivoirian_phone(self):
        prefixes = ['01', '05', '07', '25', '27']
        return f"+225 {random.choice(prefixes)}{fake.numerify(text='########')}"