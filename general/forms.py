from django import forms
from .models import Menu, FooterSection

class FooterSectionForm(forms.ModelForm):
    class Meta:
        model = FooterSection
        fields = '__all__'

    class Media:
        js = ('js/admin_footer_fields.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['router'] = forms.ChoiceField(
            choices=[(menu.slug, menu.titre) for menu in Menu.objects.all()],
            required=False
        )

