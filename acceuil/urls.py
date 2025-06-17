from django.conf.urls.static import static
from django.urls import path

from promotionImmobiliere import settings
from .views import home, service, appropos, service_detail, projet_detail, contact, projet, ajouter_panier, \
    ajouter_commentaire

urlpatterns = [
    path('', home, name="acceuil"),
    path('service/', service, name="service"),
    path('contact/', contact, name="contact"),
    path('projets/', projet, name="projets"),
    path('appropos/', appropos, name="appropos"),
    path('detail/<slug:slug>', service_detail, name="service_detail"),
    path('projet-detail/<slug:slug>', projet_detail, name="projet_detail"),
    path('ajouter_panier/<int:projet>', ajouter_panier, name="ajouter_panier"),
    path('ajouter_commentaire/<int:projet>/', ajouter_commentaire, name="ajouter_commentaire"),

]

# Ajouter cela pour servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
