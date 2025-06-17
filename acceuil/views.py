import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from acceuil.models import Projet, Phase, Album, Plan
from client.models import Panier, Commentaire
from general.models import Slide, Compteur, AppartementsVedette, PlanVedette, CommentaireVedette, \
    ProjetTerminer, Appropos, ServiceCard, ServiceSectionPage, ServiceSection, ApproposPage, MembreStaff, ServiceDetail


# Create your views here.
def home(request):
    type_projet = Projet.objects.values_list('type', flat=True).distinct()
    localisation_projet = Projet.objects.values_list('localisation', flat=True).distinct()
    statut_projet = Projet.objects.values_list('option', flat=True).distinct()
    context = {
        'slider': Slide.objects.all().order_by('ordre'),
        'appropos': Appropos.objects.all().first(),
        'compteur': Compteur.objects.all().order_by('ordre'),
        'appartement': AppartementsVedette.objects.all().first(),
        'services': ServiceCard.objects.all().order_by('ordre'),
        'projet': Projet.objects.all().order_by('-modifie_le')[:6],
        'plan': PlanVedette.objects.all().order_by('ordre'),
        'commentaire': CommentaireVedette.objects.all().order_by('ordre'),
        'projet_terminer': ProjetTerminer.objects.all().order_by('ordre'),
        'type_projet': type_projet,
        'localisation_projet': localisation_projet,
        'statut_projet': statut_projet,
     }
    return render(request, 'acceuil/index.html', context)


def service(request):
    context = {
        'section_info': ServiceSectionPage.objects.all().first(),
        'service_section': ServiceSection.objects.all().first(),

        'services': ServiceCard.objects.all().order_by('ordre'),
        'projet_terminer': ProjetTerminer.objects.all().order_by('ordre'),
    }
    return render(request, 'acceuil/pages/service/service.html', context)


def appropos(request):
    context = {
        'section_info': ApproposPage.objects.all().first(),
        'appropos': Appropos.objects.all().first(),
        'services': ServiceCard.objects.all().order_by('ordre'),
        'staff': MembreStaff.objects.all().order_by('ordre'),
        'commentaire': CommentaireVedette.objects.all().order_by('ordre'),
        'projet_terminer': ProjetTerminer.objects.all().order_by('ordre'),
    }
    return render(request, 'acceuil/pages/appropos/appropos.html', context)

def service_detail(request, slug):
    service_card = get_object_or_404(ServiceCard, slug=slug)
    service_detail = ServiceDetail.objects.filter(service=service_card).first()

    section_info = {
        'libelle': service_card.description ,
        'intitule': service_card.libelle,
    }
    context = {
        'section_info': section_info,
        'service_detail': service_detail,
        'service_card': ServiceCard.objects.exclude(id=service_card.id).order_by('ordre'),
        'services': ServiceCard.objects.all().order_by('ordre'),
        'projet_terminer': ProjetTerminer.objects.all().order_by('ordre'),

    }
    return render(request, 'acceuil/pages/service_details/service_detail.html', context)

def projet_detail(request, slug):
    projet = get_object_or_404(Projet, slug=slug)
    statut_projet = ProjetTerminer.objects.filter(projet=projet).exists()
    projet_select = None

    if statut_projet :
        projet_select = ProjetTerminer.objects.filter(projet=projet).first()

    album = Album.objects.filter(phase__projet=projet)

    projetterminer = ProjetTerminer.objects.values_list('projet_id', flat=True)
    projet_all = Projet.objects.exclude(id=projet.id).exclude(id__in=projetterminer).order_by('-modifie_le')[:6]

    commentaires_non_trier = Commentaire.objects.filter(projet=projet).order_by('-ajouter_le')[:10]
    commentaires = sorted(commentaires_non_trier, key=lambda c: c.ajouter_le)

    section_info = {
        'libelle': "Détails du projet" ,
        'intitule': "Détails du projet",
    }
    context = {
        'section_info': section_info,

        'album' : album,
        'projet': projet,
        'plan': Plan.objects.filter(projet=projet),
        'statut_projet': statut_projet,
        'projet_all': projet_all,
        'projet_select': projet_select,
        'commentaire': commentaires,
        'projet_terminer': ProjetTerminer.objects.all().order_by('ordre'),
    }
    return render(request, 'acceuil/pages/projet_detail/projet_detail.html', context)

def contact(request):
    section_info = {
        'libelle': "Contactez-nous",
        'intitule': 'Contacte',
    }
    context = {
        'section_info': section_info,

    }
    return render(request, 'acceuil/pages/contact/contact.html', context)


from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render


def projet(request):
    # Récupération des données
    projets = Projet.objects.all().order_by('-modifie_le')
    types = Projet.objects.values_list('type', flat=True).distinct()
    localisation_projet = Projet.objects.values_list('localisation', flat=True).distinct()
    statut_projet = Projet.objects.values_list('option', flat=True).distinct()

    # Filtre
    statut_send = request.GET.get('statut_projet')
    type_send = request.GET.get('type_projet')
    localisation_send = request.GET.get('localisation_projet')
    print(statut_send, type_send, localisation_send)

    if statut_send :
        projets = projets.filter(option=statut_send)

    if type_send :
        projets = projets.filter(type=type_send)

    if localisation_send :
        projets = projets.filter(localisation=localisation_send)

    search = request.GET.get('search')
    if search :
        projets = projets.filter(libelle__icontains=search)

    search_header = request.GET.get('search_header')
    send_header = request.GET.get('send_header')
    if search_header and send_header  :
        projets = projets.filter(libelle__icontains=search_header)


    # Pagination
    paginator = Paginator(projets, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.htmx:

        return render(request, 'acceuil/pages/produits/section_produit/sous_section_produit/projet_card.html', {
            'projet': page_obj,
            'page': page_obj,

        })


    context = {
        'section_info': {
            'libelle': "Nos Propriétés",
            'intitule': 'Propriété'
        },
        'types': types,
        'localisation_projet': localisation_projet,
        'statut_projet': statut_projet,
        'projet': page_obj,
        'page': page_obj,
        'search_header': search_header,
        'statut_projet_acceuil': statut_send,
        'types_acceuil': type_send,
        'localisation_projet_acceuil': localisation_send,
    }

    return render(request, 'acceuil/pages/produits/projets.html', context)



def ajouter_panier(request, projet):
    user = request.user
    client = getattr(user, 'client', None)
    if client is not None and user.is_active:
        projet = get_object_or_404(Projet, id=projet)

        if not Panier.objects.filter(projet=projet, client=client).exists():
            Panier.objects.create(client=client, projet=projet)
            messages.success(request, "Projet ajouter au panier")
        else:
            messages.error(request, "Projet a deja été ajouter dans votre panier !")

        if request.htmx:
             return render(request, 'acceuil/pages/projet_detail/ajouter_panier_htmx.html', {
                'projet': projet
            })

    return redirect('connexion')


def ajouter_commentaire(request, projet):
    user = request.user
    client = getattr(user, 'client', None)

    if client is not None and user.is_active:
        projet = get_object_or_404(Projet, id=projet)
        contenue = request.POST.get('contenue')
        if not contenue :
            messages.error(request,"Vous ne pouvez pas envie un commentaire vide !")
            return render(request, 'acceuil/pages/projet_detail/section_projet/commentaire_error.html', {
                'commentaire': Commentaire.objects.filter(projet=projet).order_by('-ajouter_le')[:10],
            })

        Commentaire.objects.create(projet=projet, client=client, contenue=contenue)
        commentaires_non_trier = Commentaire.objects.filter(projet=projet).order_by('-ajouter_le')[:10]
        commentaires = sorted(commentaires_non_trier, key=lambda c: c.ajouter_le)
        context = {
            'user': user,
            'client': client,
            'commentaire': commentaires,
        }

        return render(request, 'acceuil/pages/projet_detail/section_projet/commentaire.html', context)

    if request.htmx:
        response = HttpResponse(status=403)
        response['HX-Redirect'] = reverse('connexion')
        return response
    return redirect('connexion')