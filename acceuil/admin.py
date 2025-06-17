from django.contrib import admin

from client.models import Souscription
from general.models import SliderVette, GalerieVette
from .models import Client, Projet, Plan, Phase, Album, CaracteristiqueProjet, \
    CaracteristiquePlan


# -----------------------------
# Inlines pour Projet
# -----------------------------

class SouscriptionInline(admin.TabularInline):
    model = Souscription
    extra = 1
    autocomplete_fields = ['client']

class PlanInline(admin.StackedInline):
    model = Plan
    extra = 1

class PhaseInline(admin.TabularInline):
    model = Phase
    extra = 1

class CaracteristiqueProjetInline(admin.StackedInline):
    model = CaracteristiqueProjet
    extra = 1

class CaracteristiquePlanInline(admin.StackedInline):
    model = CaracteristiquePlan
    extra = 1

# -----------------------------
# Inlines pour Phase
# -----------------------------
class AlbumInline(admin.TabularInline):
    model = Album
    extra = 1

# -----------------------------
# Admin Projet avec plusieurs inlines
# -----------------------------
class SliderVetteInline(admin.StackedInline):
    model = SliderVette
    extra = 1

class GalerieVetteInline(admin.StackedInline):
    model = GalerieVette
    extra = 1

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'type', 'montant_investissement', 'cout_total', 'slug', 'ajouter_le', 'modifie_le')
    search_fields = ('libelle', 'type')
    list_filter = ('type', 'ajouter_le')
    prepopulated_fields = {'slug':('libelle',),}
    inlines = [SouscriptionInline, PlanInline, PhaseInline, CaracteristiqueProjetInline, SliderVetteInline,
               GalerieVetteInline]

# -----------------------------
# Admin Phase avec Album inline
# -----------------------------
@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'projet', 'status', 'ajouter_le', 'modifie_le')
    list_filter = ('status', 'ajouter_le')
    inlines = [AlbumInline]
    autocomplete_fields = ['projet']
    search_fields = ('libelle', 'projet__libelle')

# -----------------------------
# Admin Plan
# -----------------------------
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'projet', 'ajouter_le', 'modifie_le')
    search_fields = ('libelle', 'projet__libelle')
    list_filter = ('ajouter_le',)
    autocomplete_fields = ['projet']
    inlines = [CaracteristiquePlanInline]

# -----------------------------
# Admin Album seul (en plus de l'inline)
# -----------------------------
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titre', 'phase', 'ajouter_le', 'modifie_le')
    search_fields = ('titre', 'phase__libelle')
    autocomplete_fields = ['phase']

