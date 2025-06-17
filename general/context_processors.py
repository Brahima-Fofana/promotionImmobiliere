from django.urls import NoReverseMatch, reverse

from general.models import Compagnie, Menu, FooterSection, Footer, FooterSide, FooterBottom
from promotionImmobiliere.settings import DEBUG

def header_footer(request):
    footer = Footer.objects.filter(active=True).prefetch_related('section').order_by('order')

    # Determine active menu
    menu_active = None
    current_path = request.path
    all_menus = Menu.objects.all()
    menu_trouver = None

    for menu in all_menus:
        if menu.route:
            try:
                menu_url = reverse(menu.route)
                if (current_path == menu_url) or (
                        menu_url != '/' and current_path.startswith(menu_url + '/')
                ):
                    menu_active = menu.id
                    menu_trouver = menu
                    break
            except NoReverseMatch:
                continue

    context = {
        'debug': DEBUG,
        'compagny': Compagnie.objects.all().first(),
        'menu': Menu.objects.all(),
        'footer': footer,
        'footer_side': FooterSide.objects.all().filter(active=True).first(),
        'footer_bottom': FooterBottom.objects.filter(active=True).first(),
        'menu_active': menu_active,
        'menu_trouver': menu_trouver,
     }
    return context
