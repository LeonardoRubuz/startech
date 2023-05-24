# Raikage The Third
# J'utiliserais les vues en fonctions

#from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.views.generic import CreateView
#from multiforms import MultiFormsView
from django.urls import reverse, reverse_lazy
from django.conf import settings


# Create your views here.

# Function based views

# Fonction de la page d'acceuil

def homepage(request):
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form.save()
            messages.success(request, "Message envoyé avec succès!" )
            return redirect('home')
    else:
        message_form = MessageForm()
    context = {
        'form' : message_form
    }
    return render(request, 'index.html', context)

# Fonction de la page de demande de devis
class DevisPageView(CreateView):
    model = Estimate
    form_class = DevisForm
    template_name = 'devis.html'




# Fonction de la page de développement de logiciel
def softwares(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Abonnement effectué!')
            #return redirect('home')  La redirection n'est pas capitale pour l'abonnement
    else:
        form = SubscriberForm()
    context ={
        'subscriber' : form,
    }

    return render(request, 'creationdelogiciel.html', context)


# Fonction de la page de développement mobile
def mobile(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Abonnement effectué!')
            #return redirect('home')  La redirection n'est pas capitale pour l'abonnement
    else:
        form = SubscriberForm()
    context ={
        'subscriber' : form,
    }

    return render(request, 'mobileapp.html', context)


# Fonction de la page marketing
def marketing(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Abonnement effectué!')
            #return redirect('home')  La redirection n'est pas capitale pour l'abonnement
    else:
        form = SubscriberForm()
    context ={
        'subscriber' : form,
    }

    return render(request, 'marketing.html', context)


# Fonction de la page de développement web
def website(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Abonnement effectué!')
            #return redirect('home')  La redirection n'est pas capitale pour l'abonnement
    else:
        form = SubscriberForm()
    context ={
        'subscriber' : form,
    }

    return render(request, 'siteweb.html', context)


# Fonction de redirection vers la page 404
def error_404_view(request, exception):
    return render(request, '404.html', {})
















# Un mode de création qui se veut facile mais qui en réalité est hyper chelou

"""
class HomePageView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'index.html'


def devis(request):

    devisForm = DevisForm(request.POST or None, request.FILES or None)
    subscribeForm = SubscriberForm(request.POST or None)


    if all([devisForm.is_valid(), subscribeForm.is_valid()]):
        devisForm.save()
        subscribeForm.save()
        messages.success(request, 'Opération effectuée')
    context = {
        'devis' : devisForm,
        'subscriber': subscribeForm
    }
    return render(request, 'devis.html', context)



class SubscriptionView(CreateView):
    model = Subscriber
    form_class  = SubscriberForm
    template_name = 'newsletter.html'
    success_url = reverse_lazy('')



class DevisPageView(MultiFormsView):
    template_name = 'devis.html'
    form_classes = {
        'devis': DevisForm,
        'subscriber': SubscriberForm,
    }

    success_urls = {
        'devis' : reverse_lazy('home'),
        'subscriber' : reverse_lazy('home')
    }

    def devis_form_valid(self, form):
        name = form.cleaned_data.get('name')
        form_name = form.cleaned_data.get('action')
        print(name)
        return HttpResponseRedirect(self.get_success_url(form_name))

    def subscriber_form_valid(self, form):
        email = form.cleaned_data.get('email')
        form_name = form.cleaned_data.get('action')
        print(email)
        return HttpResponseRedirect(self.get_success_url(form_name))





class SoftwareCreationPageView(TemplateView):
    template_name = 'creationdelogiciel.html'

class MarketingPageView(TemplateView):
    template_name = 'marketing.html'

class MobileAppPageView(TemplateView):
    template_name = 'mobileapp.html'

class WebDevPageView(TemplateView):
    template_name = 'siteweb.html'


"""
