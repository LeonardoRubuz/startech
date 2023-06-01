# Raikage The Third

from django import forms
from django.contrib.auth.models import User
from .models import Profile, Publication, Command


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : "Nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder' : 'Mot de passe'
                                                                }))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
        'class' : 'form-control'
        })
    )
    password2 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
        'class' : 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Mots de passes incompatibles')
        return cd['password2']


    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control',})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control',})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control',})
        self.fields['email'].widget.attrs.update({'class': 'form-control',})
        self.fields['password'].widget.attrs.update({'class': 'form-control',})
        self.fields['password2'].widget.attrs.update({'class': 'form-control',})

        self.fields['username'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['email'].label = ''
        self.fields['password'].label = ''
        self.fields['password2'].label = ''


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-control',})
        self.fields['sex'].widget.attrs.update({'class': 'form-control',})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control',})
        self.fields['photo'].widget.attrs.update({'class': 'form-control',})
        self.fields['fonction'].widget.attrs.update({'class': 'form-control',})
        self.fields['region'].widget.attrs.update({'class': 'form-control',})
        self.fields['country'].widget.attrs.update({'class': 'form-control',})
        self.fields['phone'].widget.attrs.update({'class': 'form-control',})

        self.fields['user'].label = ''
        self.fields['sex'].label = ''
        self.fields['date_of_birth'].label = ''
        self.fields['photo'].label = ''
        self.fields['fonction'].label = ''
        self.fields['region'].label = ''
        self.fields['country'].label = ''
        self.fields['phone'].label = ''


class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ('title', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control',})
        self.fields['message'].widget.attrs.update({'class': 'form-control',})

        self.fields['title'].label = ''
        self.fields['message'].label = ''


class AnswerMessageForm(forms.Form):
    title = forms.CharField(max_length=50)
    mail_to = forms.CharField(max_length=50)
    body = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        self.fields['mail_to'].widget.attrs.update({'class' : 'form-control'})
        self.fields['body'].widget.attrs.update({'class' : 'form-control'})


class CommandForm(forms.Form):
    class Meta:
        model = Command
        fields = '__all__'