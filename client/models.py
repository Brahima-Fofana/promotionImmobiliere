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
    CNI = models.CharField(max_length=255,blank=True, null=True, unique=True)
    poste = models.CharField(max_length=255, blank=True, null=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
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
    libelle = models.CharField(max_length=255)
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