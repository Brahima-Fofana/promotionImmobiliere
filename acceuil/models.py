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
        ('jour', 'JOUR'),
        ('semaine', 'SEMAINE'),
        ('mois', 'MOIS'),
        ('annee', 'ANNEE'),
    ]
    libelle = models.CharField(max_length=200)
    contenue = models.TextField()
    type = models.CharField(max_length=100)
    montant_investissement = models.DecimalField(max_digits=12, decimal_places=2)
    modalite_investissement = models.CharField(choices=MODALITE)
    cout_total = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='projet')
    client_projet = models.ManyToManyField(Client, through="client.Souscription")
    slug = models.SlugField(unique=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    option = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle

class CaracteristiqueProjet(Timestamp):
    libelle = models.CharField(max_length=255)
    valeur = models.DecimalField(max_digits=12, decimal_places=2)
    unite = models.CharField(max_length=20, blank=True, null=True)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Projet : {self.projet.libelle} - Caracteristique : {self.libelle}"

class Plan(Timestamp):
    libelle = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='plan_projet/')
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.projet.libelle} - {self.libelle}"

class CaracteristiquePlan(Timestamp):
    libelle = models.CharField(max_length=255)
    valeur = models.DecimalField(max_digits=12, decimal_places=2)
    unite = models.CharField(max_length=20, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return f"Plan : {self.plan.libelle} - Caracteristique : {self.libelle}"

class Phase(Timestamp):
    libelle = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.projet.libelle} - {self.libelle}"

class Album(Timestamp):
    titre = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='album')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titre or 'image'} : phase : {self.phase.libelle}"
