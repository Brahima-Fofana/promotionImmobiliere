from django.contrib import admin

from client.models import Commentaire, Client, DashboardClient, Versement, Souscription, Panier


# Register your models here.
# -----------------------------
# Admin Client
# -----------------------------
class CommentaireInline(admin.StackedInline):
    model = Commentaire
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'user__first_name', 'user__last_name', 'CNI', 'date_naissance', 'poste', 'ajouter_le', 'modifie_le')
    search_fields = ('user__username','nom', 'prenom', 'NCI')
    list_filter = ('ajouter_le', 'modifie_le')
    readonly_fields = ('ajouter_le', 'modifie_le')
    inlines = [CommentaireInline]

@admin.register(DashboardClient)
class DashboardClientAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description', 'ajouter_le', 'modifie_le')
    list_filter = ('ajouter_le', 'modifie_le')
    readonly_fields = ('ajouter_le', 'modifie_le')

    def has_add_permission(self, request):
        if DashboardClient.objects.exists():
            return False
        return True

# -----------------------------
# Admin Versement
# -----------------------------
@admin.register(Versement)
class VersementAdmin(admin.ModelAdmin):
    list_display = ('souscription', 'montant', 'ajouter_le', 'modifie_le')
    readonly_fields = ['ajouter_le', 'modifie_le']

# -----------------------------
# Admin Souscription
# -----------------------------
@admin.register(Souscription)
class SouscriptionAdmin(admin.ModelAdmin):
    list_display = ('projet', 'client', 'ajouter_le', 'modifie_le')
    autocomplete_fields = ['client', 'projet']
    list_filter = ('ajouter_le',)
    readonly_fields = ['ajouter_le', 'modifie_le']

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('projet', 'client', 'etat_souscription', 'ajouter_le', 'modifie_le')
    autocomplete_fields = ['client', 'projet']
    list_filter = ('ajouter_le',)
    readonly_fields = ['ajouter_le', 'modifie_le']