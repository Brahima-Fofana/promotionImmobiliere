from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .forms import FooterSectionForm
from .models import Compagnie, Menu, Footer, FooterSection, FooterSide, FooterBottom, Slide, Compteur, \
    AppartementsVedette, ImageAppVedette, ImageFareVedette, CaracteristiqueVedette, ServiceCard, PlanVedette, \
    CommentaireVedette, ProjetTerminer, Prestation, Contact, ReseauxSociaux, Appropos, ServiceSection, \
    ServiceSectionPage, ApproposPage, MembreStaff, ReseauxSociauxStaff, ServiceDetail, PolitiqueConfidentialite


class PrestationInline(admin.StackedInline):
    model = Prestation
    extra = 1

class ContactInline(admin.StackedInline):
    model = Contact
    extra = 1

class ReseauxSociauxInline(admin.StackedInline):
    model = ReseauxSociaux
    extra = 1

class ServiceCardInline(admin.StackedInline):
    model = ServiceCard
    extra = 1

class ServiceSectionInline(admin.StackedInline):
    model = ServiceSection
    extra = 1

    def has_add_permission(self, request, obj):
        if ServiceSection.objects.exists() :
            return False
        return True

@admin.register(Compagnie)
class CompagnieAdmin(admin.ModelAdmin):
    list_display = ('description', 'localisation', 'email', 'ajouter_le', 'modifie_le')
    search_fields = ('description', 'localistation', 'email')
    readonly_fields = ('ajouter_le', 'modifie_le')
    list_filter = ('ajouter_le', 'modifie_le')
    inlines = [ContactInline, ReseauxSociauxInline, ServiceCardInline, ServiceSectionInline]
    
    def has_add_permission(self, request):
        if Compagnie.objects.exists():
            return False
        return True

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('titre', 'slug', 'route', 'order', 'ajouter_le', 'modifie_le')
    search_fields = ('titre', 'slug')
    list_filter = ('ajouter_le', 'modifie_le')
    ordering = ('order',)
    prepopulated_fields = {'slug':('titre',),}
    readonly_fields = ('ajouter_le', 'modifie_le')

class FooterSectionInline(admin.TabularInline):
    model = FooterSection
    extra = 1

@admin.register(Footer)
class FooterAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('section_title', 'libelle', 'active', 'order', 'ajouter_le', 'modifie_le')
    list_filter = ('section_title', 'active')
    ordering = ('order',)
    readonly_fields = ('ajouter_le', 'modifie_le')
    inlines = [FooterSectionInline]

@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    form = FooterSectionForm
    list_display = ('get_section', 'libelle', 'router', 'description_email', 'ajouter_le', 'modifie_le')
    search_fields = ('libelle', 'router', 'description_email')
    readonly_fields = ('ajouter_le', 'modifie_le')
    list_filter = ('section__section_title',)

    def get_section(self, obj):
        return obj.section.section_title
    get_section.short_description = 'Section'

@admin.register(FooterSide)
class FooterSideAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description', 'lien_title', 'active', 'ajouter_le', 'modifie_le')
    list_filter = ('libelle',)
    ordering = ('active',)
    readonly_fields = ('ajouter_le', 'modifie_le')

    def has_add_permission(self, request):
        if FooterSide.objects.exists():
            return False
        return True

@admin.register(FooterBottom)
class FooterBottomAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'active', 'ajouter_le', 'modifie_le')
    list_filter = ('libelle',)
    ordering = ('active',)
    readonly_fields = ('ajouter_le', 'modifie_le')

    def has_add_permission(self, request):
        if FooterBottom.objects.exists():
            return False
        return True

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description', 'active_libelle',  'ordre', 'ajouter_le', 'modifie_le')
    list_filter = ('libelle',)
    ordering = ('ordre',)
    readonly_fields = ('ajouter_le', 'modifie_le')

@admin.register(Compteur)
class CompteurAdmin(admin.ModelAdmin):
    list_display = ('type', 'libelle', 'valeur', 'ordre', 'ajouter_le', 'modifie_le')
    list_filter = ('libelle',)
    ordering = ('ordre',)
    readonly_fields = ('ajouter_le', 'modifie_le')


class ImageAppVedetteInline(admin.StackedInline):
    model = ImageAppVedette
    extra = 1

class ImageFareVedetteInline(admin.StackedInline):
    model = ImageFareVedette
    extra = 1

class CaracteristiqueVedetteInline(admin.StackedInline):
    model = CaracteristiqueVedette
    extra = 1


@admin.register(AppartementsVedette)
class AppartementsVedetteAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description', 'ajouter_le', 'modifie_le')
    list_filter = ('libelle',)
    readonly_fields = ('ajouter_le', 'modifie_le')
    inlines = [CaracteristiqueVedetteInline, ImageAppVedetteInline, ImageFareVedetteInline]

    def has_add_permission(self, request):
        if AppartementsVedette.objects.exists():
            return False
        if ImageAppVedette.objects.exists():
            return False
        return True

class ServiceDetailInline(admin.StackedInline):
    model = ServiceDetail
    extra = 1

@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description', 'option', 'slug', 'ordre', 'ajouter_le', 'modifie_le')
    list_filter = ('libelle',)
    ordering = ('ordre',)
    prepopulated_fields = {'slug':('libelle',),}
    readonly_fields = ('ajouter_le', 'modifie_le')
    inlines = [ServiceDetailInline]

@admin.register(PlanVedette)
class PlanVedetteAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'projet', 'ajouter_le', 'modifie_le')
    list_filter = ('libelle',)
    ordering = ('ordre',)
    readonly_fields = ('ajouter_le', 'modifie_le')

@admin.register(CommentaireVedette)
class CommentaireVedetteAdmin(admin.ModelAdmin):
    list_display = ('commentaire', 'ajouter_le', 'modifie_le')
    ordering = ('ordre',)
    readonly_fields = ('ajouter_le', 'modifie_le')

@admin.register(ProjetTerminer)
class ProjetTerminerAdmin(admin.ModelAdmin):
    list_display = ('projet', 'date_de_fin', 'option', 'ajouter_le', 'modifie_le')
    ordering = ('ordre',)
    readonly_fields = ('ajouter_le', 'modifie_le')

class ApproposPageInline(admin.StackedInline):
    model = ApproposPage
    extra = 1

    def has_add_permission(self, request, obj):
        if ApproposPage.objects.exists() :
            return False
        return True

@admin.register(Appropos)
class ApproposAdmin(admin.ModelAdmin):
    list_display = ('compagnie__denomination', 'presentation', 'slogan', 'ajouter_le', 'modifie_le')
    readonly_fields = ('ajouter_le', 'modifie_le')
    inlines = [PrestationInline, ApproposPageInline]

    def has_add_permission(self, request):
        if Appropos.objects.exists():
            return False
        return True

class ServiceSectionPageInline(admin.StackedInline):
    model = ServiceSectionPage
    extra = 1

    def has_add_permission(self, request, obj):
        if ServiceSectionPage.objects.exists():
            return False
        return True

@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    list_display = ( 'libelle', 'contenue', 'option', 'ajouter_le', 'modifie_le')
    readonly_fields = ('ajouter_le', 'modifie_le')
    inlines = [ServiceSectionPageInline]

    def has_add_permission(self, request):
        if ServiceSection.objects.exists():
            return False
        return True

class ReseauxSociauxStaffInline(admin.StackedInline):
    model = ReseauxSociauxStaff
    extra = 1

@admin.register(MembreStaff)
class MembreStaffAdmin(admin.ModelAdmin):
    list_display = ( 'nom', 'prenom', 'poste', 'ordre', 'ajouter_le', 'modifie_le')
    ordering = ('ordre',)
    readonly_fields = ('ajouter_le', 'modifie_le')
    inlines = [ReseauxSociauxStaffInline]

@admin.register(PolitiqueConfidentialite)
class PolitiqueConfidentialiteAdmin(admin.ModelAdmin):
    list_display = ( 'libelle', 'description', 'contenue', 'ajouter_le', 'modifie_le')
    readonly_fields = ('ajouter_le', 'modifie_le')

    def has_add_permission(self, request):
        if PolitiqueConfidentialite.objects.exists():
            return False
        return True




