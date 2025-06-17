import os
import uuid

from django.contrib.auth.hashers import make_password
from django.db import models

from client.models import Client, Souscription

# Create your models here.
class Timestamp(models.Model):
    ajouter_le = models.DateField(auto_now_add=True)
    modifie_le = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Projet(Timestamp):
    MODALITE = [
        ('Jour', 'JOUR'),
        ('Semaine', 'SEMAINE'),
        ('Mois', 'MOIS'),
        ('Année', 'ANNEE'),
    ]
    libelle = models.CharField(max_length=200)
    contenue = models.TextField()
    type = models.CharField(max_length=100)
    montant_investissement = models.DecimalField(max_digits=12, decimal_places=2)
    modalite_investissement = models.CharField(max_length=100, choices=MODALITE)
    cout_total = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='projet')
    client_projet = models.ManyToManyField(Client, through="client.Souscription")
    slug = models.SlugField(unique=True)
    localisation = models.CharField(max_length=190, blank=True, null=True)
    option = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle

class CaracteristiqueProjet(Timestamp):
    libelle = models.CharField(max_length=190)
    valeur = models.DecimalField(max_digits=12, decimal_places=2)
    unite = models.CharField(max_length=20, blank=True, null=True)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Projet : {self.projet.libelle} - Caracteristique : {self.libelle}"

class Plan(Timestamp):
    libelle = models.CharField(max_length=190)
    description = models.CharField(max_length=190)
    image = models.ImageField(upload_to='plan_projet/')
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.projet.libelle} - {self.libelle}"

class CaracteristiquePlan(Timestamp):
    libelle = models.CharField(max_length=190)
    valeur = models.DecimalField(max_digits=12, decimal_places=2)
    unite = models.CharField(max_length=20, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return f"Plan : {self.plan.libelle} - Caracteristique : {self.libelle}"

class Phase(Timestamp):
    libelle = models.CharField(max_length=190)
    description = models.CharField(max_length=190)
    status = models.BooleanField(default=False)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.projet.libelle} - {self.libelle}"

class Album(Timestamp):
    titre = models.CharField(max_length=190, blank=True, null=True)
    image = models.ImageField(upload_to='album')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titre or 'image'} : phase : {self.phase.libelle}"


from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
class Timestamp(models.Model):
    ajouter_le = models.DateField(auto_now_add=True)
    modifie_le = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Client(Timestamp):
    # Les autres sont contenues dans les champs par default de User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_client/', default='profile_client/default.png', blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    CNI = models.CharField(max_length=190,blank=True, null=True, unique=True)
    poste = models.CharField(max_length=190, blank=True, null=True)
    localisation = models.CharField(max_length=190, blank=True, null=True)
    contact1 = models.CharField(max_length=20, blank=True, null=True)
    contact2 = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Profile Client'

    def __str__(self):
        return self.user.username

class Commentaire(Timestamp):
    projet = models.ForeignKey('acceuil.Projet', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contenue = models.TextField()
    ajouter_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"projet : {self.projet.libelle} - commentaire : {self.contenue[:10]}"

class DashboardClient(Timestamp):
    libelle = models.CharField(max_length=190)
    description = models.TextField()
    image = models.ImageField("Photo de profile client par default", upload_to='dashboard/', blank=True, null=True)

    def __str__(self):
        return self.libelle

class Panier(Timestamp):
    projet = models.ForeignKey('acceuil.Projet', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    etat_souscription = models.BooleanField(default=0)

    def __str__(self):
        return f"Projet : {self.projet.libelle } - Client : {self.client.user.username}"

class Souscription(Timestamp):
    projet = models.ForeignKey('acceuil.Projet', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.projet.libelle} - {self.client.user.username}"

class Versement(Timestamp):
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    souscription = models.ForeignKey(Souscription, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.projet.libelle} - {self.montant}"

from django.db import models

from acceuil.models import Projet
from client.models import Commentaire


# Create your models here.
class Timestamp(models.Model):
    ajouter_le = models.DateField(auto_now_add=True)
    modifie_le = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Compagnie(Timestamp):
    denomination = models.CharField(max_length=190)
    image = models.ImageField(upload_to='compagnie/')
    description = models.CharField(max_length=190)
    localisation = models.CharField(max_length=190)
    email = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.denomination

class Contact(Timestamp):
    ICON = [
        ('icon-call', 'Telephone'),
    ]
    icon = models.CharField(max_length=100, choices=ICON)
    libelle = models.CharField(max_length=190)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)

    def __str__(self):
        return self.compagnie.denomination

class ReseauxSociaux(Timestamp):
    ICON = [
        ('fab fa-facebook-f', 'Facebook'),
        ('fab fa-google', 'Gmail'),
        ('fab fa-whatsapp', 'Whatsapp'),
    ]
    icon = models.CharField(max_length=100, choices=ICON)
    url = models.TextField()
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)

    def __str__(self):
        return self.compagnie.denomination


class Appropos(Timestamp):
    image = models.ImageField(upload_to='appropos/', blank=True, null=True)
    presentation = models.TextField()
    slogan = models.CharField(max_length=190)
    option = models.CharField(max_length=190)
    route = models.CharField(max_length=190, blank=True, null=True)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)

    def __str__(self):
        return self.compagnie.denomination

class ApproposPage(Timestamp):
    libelle = models.CharField(max_length=190)
    intitule = models.CharField(max_length=190)
    service = models.ForeignKey(Appropos, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class Prestation(Timestamp):
    ICON = [
        ('flaticon-home-2', 'Propriete Intelligent'),
        ('flaticon-mountain', 'Travaux Public'),
        ('flaticon-heart', 'Propriete Saine'),
        ('flaticon-secure', 'Securite'),
    ]
    icon = models.CharField(max_length=100, choices=ICON)
    libelle = models.CharField(max_length=190)
    compagnie = models.ForeignKey(Appropos, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class ServiceSection(Timestamp):
    libelle = models.CharField(max_length=190)
    image = models.ImageField(upload_to='appropos/', blank=True, null=True)
    contenue = models.TextField()
    option = models.CharField(max_length=190)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class ServiceSectionPage(Timestamp):
    libelle = models.CharField(max_length=190)
    intitule = models.CharField(max_length=190)
    service = models.ForeignKey(ServiceSection, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class Menu(Timestamp):
    ROUTE = [
        ('acceuil','Acceuil'),
        ('service','Service'),
        ('appropos','Appropos'),
        ('projets','Projets'),
    ]
    titre = models.CharField(max_length=100)
    slug = models.SlugField()
    route = models.CharField(max_length=190, choices=ROUTE)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titre

class Footer(Timestamp):
    SECTION_CHOICE = [
        ('presentation', 'Presentation'),
        ('compagnie', 'Compagnie'),
        ('services', 'Services'),
        ('espace_client', 'Espace Client'),
        ('mail', 'Ecrivez nous'),
    ]
    libelle = models.CharField(max_length=190)
    section_title = models.CharField(max_length=100, choices=SECTION_CHOICE)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.section_title

class FooterSection(Timestamp):
    section = models.ForeignKey(Footer, on_delete=models.CASCADE, related_name='section')
    libelle = models.CharField(max_length=190, blank=True, null=True)
    router = models.CharField(max_length=190, blank=True, null=True)
    description_email = models.CharField(max_length=190, blank=True, null=True)
    mode_payement = models.ImageField(upload_to='footer/', blank=True, null=True)

    def __str__(self):
        return f"Footer section : {self.section.section_title}"

class FooterSide(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    description = models.CharField(max_length=190, blank=True, null=True)
    lien_title = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=1)

    def __str__(self):
        return self.libelle

class FooterBottom(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    active = models.BooleanField(default=1)

    def __str__(self):
        return self.libelle

class Slide(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    description = models.CharField(max_length=190, blank=True, null=True)
    image = models.ImageField(upload_to='slider/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    active_libelle = models.BooleanField(default=1)

    def __str__(self):
        return self.libelle

class SliderVette(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    description = models.CharField(max_length=190, blank=True, null=True)
    image = models.ImageField(upload_to='projet_slider')
    order = models.PositiveIntegerField(default=0)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return self.projet.libelle

class GalerieVette(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    image = models.ImageField(upload_to='projet_slider')
    order = models.PositiveIntegerField(default=0)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return self.projet.libelle

class Compteur(Timestamp):
    ICON = [
        ('flaticon-select', 'Projet'),
        ('flaticon-office', 'Logement'),
        ('flaticon-excavator', 'Construction'),
        ('flaticon-armchair', 'Propriete'),
    ]
    type = models.CharField(max_length=100, choices=ICON)
    libelle = models.CharField(max_length=190, blank=True, null=True)
    valeur = models.PositiveIntegerField()
    intitule_valeur = models.CharField(max_length=10, blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.libelle


# APPARTEMENET VEDETTE DEBUT
class AppartementsVedette(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    description = models.CharField(max_length=190, blank=True, null=True)

    def __str__(self):
        return self.libelle

class CaracteristiqueVedette(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    appartement = models.ForeignKey(AppartementsVedette, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.libelle

class ImageAppVedette(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    image = models.ImageField(upload_to='image_app_vedette/', blank=True, null=True)
    appartement = models.ForeignKey(AppartementsVedette, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.libelle

class ImageFareVedette(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    image = models.ImageField(upload_to='image_app_vedette/', blank=True, null=True)
    appartement = models.ForeignKey(AppartementsVedette, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.libelle

# FIN

# SERVICE
class ServiceCard(Timestamp):
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    libelle = models.CharField(max_length=200)
    description = models.CharField(max_length=190)
    option = models.CharField(max_length=190, blank=True, null=True)
    slug = models.SlugField(unique=True)
    ordre = models.PositiveIntegerField(default=0)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class ServiceDetail(Timestamp):
    image = models.ImageField(upload_to='services_detail/')
    description = models.CharField(max_length=190, blank=True, null=True)
    contenue = models.TextField()
    service = models.ForeignKey(ServiceCard, on_delete=models.CASCADE)

    def __str__(self):
        return self.service.libelle

# FIN

# PLAN VEDETTE
class PlanVedette(Timestamp):
    libelle = models.CharField(max_length=190)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.libelle

# FIN

# COMMENTAIRE VEDETTE
class CommentaireVedette(Timestamp):
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.commentaire.contenue[:10]
# FIN

# PROJET TERMINE
class ProjetTerminer(Timestamp):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)
    date_de_fin = models.DateField()
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Projet : {self.projet.libelle} - FIn : {self.date_de_fin}"

# FIN

# MEMBRE DE L'EQUIPE
class MembreStaff(Timestamp):
    nom = models.CharField(max_length=190)
    prenom = models.CharField(max_length=190)
    image = models.ImageField(upload_to='staff/', blank=True, null=True)
    poste = models.CharField(max_length=190, blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Nom : {self.nom} - Prenom : {self.prenom}"

class ReseauxSociauxStaff(Timestamp):
    ICON = [
        ('fab fa-facebook-f', 'Facebook'),
        ('fab fa-google', 'Gmail'),
        ('fab fa-whatsapp', 'Whatsapp'),
    ]
    icon = models.CharField(max_length=100, choices=ICON)
    url = models.TextField()
    staff = models.ForeignKey(MembreStaff, on_delete=models.CASCADE)

    def __str__(self):
        return f"Nom : {self.staff.nom} - Prenom : {self.staff.prenom}"

class PolitiqueConfidentialite(Timestamp):
    libelle = models.CharField(max_length=190, blank=True, null=True)
    description = models.CharField(max_length=190, blank=True, null=True)
    contenue = models.TextField()

    def __str__(self):
        return f"{self.libelle or 'Politique de confidentialite'}"


# Import des modèles
from acceuil.models import (
    Projet, CaracteristiqueProjet, Plan, CaracteristiquePlan,
    Phase, Album
)
from client.models import Client, Commentaire, Souscription, Versement
from django.contrib.auth.models import User

from general.models import ReseauxSociauxStaff, MembreStaff, Prestation, Appropos, ServiceCard, Compagnie, ServiceDetail

fake = Faker('fr_FR')