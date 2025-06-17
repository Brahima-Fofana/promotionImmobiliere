from django.urls import path

from client.views import inscription, connexion, deconnexion, dashboard, user_info, politique_confidentialite, \
    password_oublier, supprimer_projet_panier
from promotionImmobiliere import settings

urlpatterns = [
    path('inscription/', inscription, name="inscription"),
    path('politique_confidentialite/', politique_confidentialite, name="politique_confidentialite"),
    path('connexion/', connexion, name="connexion"),
    path('deconnexion/', deconnexion, name="deconnexion"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/user-information/', user_info, name="user_info"),
    path('dashboard/dashboard_content/<str:contenue>/', dashboard, name="dashboard"),
    path('password_oublier/', password_oublier, name="password_oublier"),
    path('supprimer_projet_panier/', supprimer_projet_panier, name="supprimer_projet_panier"),

]