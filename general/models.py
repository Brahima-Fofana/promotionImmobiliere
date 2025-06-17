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
    denomination = models.CharField(max_length=255)
    image = models.ImageField(upload_to='compagnie/')
    description = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)
    email = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.denomination

class Contact(Timestamp):
    ICON = [
        ('icon-call', 'Telephone'),
    ]
    icon = models.CharField(max_length=100, choices=ICON)
    libelle = models.CharField(max_length=255)
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
    slogan = models.CharField(max_length=255)
    option = models.CharField(max_length=255)
    route = models.CharField(max_length=255, blank=True, null=True)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)

    def __str__(self):
        return self.compagnie.denomination

class ApproposPage(Timestamp):
    libelle = models.CharField(max_length=255)
    intitule = models.CharField(max_length=255)
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
    libelle = models.CharField(max_length=255)
    compagnie = models.ForeignKey(Appropos, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class ServiceSection(Timestamp):
    libelle = models.CharField(max_length=255)
    image = models.ImageField(upload_to='appropos/', blank=True, null=True)
    contenue = models.TextField()
    option = models.CharField(max_length=255)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class ServiceSectionPage(Timestamp):
    libelle = models.CharField(max_length=255)
    intitule = models.CharField(max_length=255)
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
    route = models.CharField(max_length=255, choices=ROUTE)
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
    libelle = models.CharField(max_length=255)
    section_title = models.CharField(max_length=100, choices=SECTION_CHOICE)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.section_title

class FooterSection(Timestamp):
    section = models.ForeignKey(Footer, on_delete=models.CASCADE, related_name='section')
    libelle = models.CharField(max_length=255, blank=True, null=True)
    router = models.CharField(max_length=255, blank=True, null=True)
    description_email = models.CharField(max_length=255, blank=True, null=True)
    mode_payement = models.ImageField(upload_to='footer/', blank=True, null=True)

    def __str__(self):
        return f"Footer section : {self.section.section_title}"

class FooterSide(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    lien_title = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=1)

    def __str__(self):
        return self.libelle

class FooterBottom(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=1)

    def __str__(self):
        return self.libelle

class Slide(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='slider/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    active_libelle = models.BooleanField(default=1)

    def __str__(self):
        return self.libelle

class SliderVette(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='projet_slider')
    order = models.PositiveIntegerField(default=0)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return self.projet.libelle

class GalerieVette(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
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
    libelle = models.CharField(max_length=255, blank=True, null=True)
    valeur = models.PositiveIntegerField()
    intitule_valeur = models.CharField(max_length=10, blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.libelle


# APPARTEMENET VEDETTE DEBUT
class AppartementsVedette(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.libelle

class CaracteristiqueVedette(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
    appartement = models.ForeignKey(AppartementsVedette, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.libelle

class ImageAppVedette(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='image_app_vedette/', blank=True, null=True)
    appartement = models.ForeignKey(AppartementsVedette, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.libelle

class ImageFareVedette(Timestamp):
    libelle = models.CharField(max_length=255, blank=True, null=True)
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
    description = models.CharField(max_length=255)
    option = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)
    ordre = models.PositiveIntegerField(default=0)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class ServiceDetail(Timestamp):
    image = models.ImageField(upload_to='services_detail/')
    description = models.CharField(max_length=255, blank=True, null=True)
    contenue = models.TextField()
    service = models.ForeignKey(ServiceCard, on_delete=models.CASCADE)

    def __str__(self):
        return self.service.libelle

# FIN

# PLAN VEDETTE
class PlanVedette(Timestamp):
    libelle = models.CharField(max_length=255)
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
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    image = models.ImageField(upload_to='staff/', blank=True, null=True)
    poste = models.CharField(max_length=255, blank=True, null=True)
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
    libelle = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    contenue = models.TextField()

    def __str__(self):
        return f"{self.libelle or 'Politique de confidentialite'}"