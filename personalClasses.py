from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
import random

class MultipleFormsMixin(FormMixin):


    form_classes = {}

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self, form_classes):
        return dict([(key,klass(**self.get_form_kwargs())) for key, klass in form_classes.items()])

    def get_context_data(self, **kwargs):
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms()
        return super().get_context_data(**kwargs)

    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)

    def forms_invalid(self, forms) :
        return self.render_to_response(self.get_context_data(forms=forms))


class ProcessMultipleFormsView(ProcessFormView):

    def get(self, request, *args, **kwargs):
        forms_classes = self.get_form_classes()
        forms = self.get_forms(forms_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        forms_classes = self.get_form_classes()
        forms = self.get_forms(forms_classes)
        if all(form.is_valid() for form in forms.values()):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """

class MultipleFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A  view for displaying several forms qnd rendering a template response.
    """

def random_phrases(objet) :
    sentences = [
        objet +' dans la maison!',
        'Hey '+ objet +'!',
        'Tranquille ou quoi '+ objet +'?',
        'Alors, qu\'est-ce qu\'on fait aujourd\'hui '+ objet +'?',
        'Bienvenue '+ objet,
        'Pfff... Encore toi '+ objet,
        'Content de te revoir '+ objet +'!',
        'S/O '+ objet +'!',
        'Ooh '+objet+', morale?',
        'Regardez qui est là? '+ objet + '!',
        'Et bien ' + objet + ', je t\'ai manqué?'

    ]
    return random.choice(sentences)