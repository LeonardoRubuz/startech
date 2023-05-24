# Raikage The Third

from django import forms
from .models import *

class SubscriberForm(forms.ModelForm):
    class Meta :
        model = Subscriber
        fields = '__all__'
        widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Votre adresse électronique'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].label = ''


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['author','email','subject','body']


    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].label = 'Votre nom'
        self.fields['email'].label = 'Votre mail'
        self.fields['subject'].label = 'Sujet'
        self.fields['body'].label = 'Message'


        self.fields['author'].widget.attrs.update({'class': 'form-control', 'placeholder' : 'Inscrivez votre nom'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder' : 'Inscrivez votre adresse éléctronique'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder' : 'Inscrivez le sujet de votre requête'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder' : 'Dites-nous tout...'})



class DevisForm(forms.ModelForm):

    class Meta:
        model = Estimate
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].label = 'Votre nom'
        self.fields['required_service'].label = 'De quel service avez-vous besoin?'
        self.fields['delivery_delay'].label = 'Délai de livraison'
        self.fields['payment_mode'].label = 'Modalité de paiement'
        self.fields['email'].label = 'Votre mail'
        self.fields['phone'].label = 'Votre numéro portable'
        self.fields['budget'].label = 'Quel est votre budget? (en USD)'
        self.fields['file'].label = 'Cahier de charges (.docx, .pdf)'
        self.fields['description'].label = 'Décrivez  votre projet'


        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})
        self.fields['required_service'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})
        self.fields['delivery_delay'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})
        self.fields['payment_mode'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})
        self.fields['budget'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})
        self.fields['file'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder' : ''})



