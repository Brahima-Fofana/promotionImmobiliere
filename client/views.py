from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, login_not_required
from django.contrib import messages

from acceuil.models import Projet
from client.forms import InscriptionForms, UserInformationForm, PasswordOublierForm
from client.models import Client, DashboardClient, Panier
from general.models import PolitiqueConfidentialite


# Create your views here.
def inscription(request):
    form = InscriptionForms()
    if request.method == 'POST':
        form = InscriptionForms(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            login(request, user)
            return redirect('connexion')
    return render(request, 'client/inscription/inscription.html', {'form':form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print("envoie")
        if user is not None and user.is_active:
            login(request, user)
            next = request.GET.get('next') or 'dashboard'
            return redirect(next)
        else:
            messages.error(request, "Login ou mot de passe Incorrect !")
    return render(request, 'client/connexion/connexion.html')

@login_required
def deconnexion(request):
    logout(request)
    return redirect('acceuil')

def verification(request):
    user = request.user
    client = getattr(user, 'client', None)
    # Dans le cas ou l'User n'est pas associe a un compte
    if client is None:
        return redirect('connexion')
    return user, client


@login_required
def dashboard(request):
    user, client = verification(request)
    contenue = request.GET.get('contenue', 'home')  # default à 'home'
    print('valeur contenue', contenue)

    templates = {
        'home': {'libelle': 'Tableau de bord', 'url':'client/dashboard/composants/home.html', 'icon': 'fas fa-home'},
        'profile': {'libelle': 'Profile', 'url': 'client/dashboard/composants/profile.html', 'icon': ''},
        'adresse': {'libelle': 'adresse', 'url':'client/dashboard/composants/addresse.html', 'icon':''},
        'panier': {'libelle': 'Panier', 'url':'client/dashboard/composants/panier.html', 'icon':''},
    }
    composant = templates.get(contenue, templates['home'])  # fichier à inclure
    print('valeur composant', composant)

    context = {
        'user': user,
        'client': client,
        'dashboard': DashboardClient.objects.all().first(),
        'contenue_template': composant['url'],  # on passe le chemin du composant
        'contenue': contenue,  # pour activer l’onglet
        'templates': templates,
    }

    if request.htmx:
        return render(request, composant['url'], context)

    return render(request, 'client/dashboard/dashboard.html', context)

@login_required
def user_info(request):
    form = UserInformationForm()
    user, client = verification(request)
    if request.method == "POST" and request.htmx:
        form = UserInformationForm(request.POST)
        if form.is_valid():
            print('post ok')
            user.first_name = form.cleaned_data.get('nom')
            user.last_name = form.cleaned_data.get('prenom')
            user.email = form.cleaned_data.get('email')

            client.user = user
            client.poste = form.cleaned_data.get('poste')
            client.localisation = form.cleaned_data.get('localisation')
            client.CNI = form.cleaned_data.get('cni')
            client.contact1 = form.cleaned_data.get('contact1')
            client.contact2 = form.cleaned_data.get('contact2')

            user.save()
            client.save()
            print('donne save : ', client.user.first_name)

        context = {
            'user': user,
            'client': client,
            'form': form,
            'erreur': 'erreur',
        }
        print('envoie ok chez : ', user.username)
        return render(request, 'client/dashboard/composants/sous_section/user_profile.html', context)
    print('probleme')
    context = {
        'user': user,
        'client': client,
        'form': form,
    }
    return render(request, 'client/dashboard/dashboard.html', context)

def politique_confidentialite(request):
    return render(request, 'client/politique_confidentialite/confidentialite.html', {
        'confidentialite': PolitiqueConfidentialite.objects.all().first(),
    })


def password_oublier(request):
    form = PasswordOublierForm()

    if request.method == 'POST':
        form = PasswordOublierForm(request.POST)
        if form.is_valid():
            messages.success(request, "Mot de passe de renitialisation envoyez !")
            return redirect('connexion')
    return render(request, 'client/password_oublier/password_oublier.html', {'form':form})

def supprimer_projet_panier(request):
    user, client = verification(request)
    projet_id = request.GET.get('projet_id', None)

    if client is not None and user.is_active:
        projet = get_object_or_404(Projet, id=projet_id)
        Panier.objects.filter(projet=projet, client=client).delete()
        messages.success(request, f"Le Projet {projet.libelle} à été supprimé de votre panier")
        context = {
            'user': user,
            'client': client,
            'projet': projet
        }
        return render(request, 'client/panier/supprimer_panier.html')
    return redirect('acceuil')