# Raikage The Third

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from visiteurs.models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import EmailMessage
from personalClasses import random_phrases
from django_pandas.io import read_frame
from django.db.models import Q


# Special functions
def handle_uploaded_file(f):
    pass


# Create your views here.

# Page de connexion
def loginpage(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd['username'],
                password = cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return HttpResponse('Compte désactivé')
            else:        
                form = LoginForm()
                context = {
                    'form' : form,
                }
                messages.error(request, "Informations invalides")
                return render(request, 'admin/login.html', context)
    else:
        form = LoginForm()
        context = {
            'form' : form,
        }
    return render(request, 'admin/login.html', context )

# Fonction de déconnexion
def logoutUser(request):
    logout(request)
    return redirect('login')

# Page d'ajout d'utilisateur
@login_required(login_url='login')
def register(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Création de l'objet User sans sauvegarder
            new_user = user_form.save(commit=False)
            # Configuration du mot de passe
            new_user.set_password(user_form.cleaned_data['password'])
            # Enregistrement de l'objet User
            new_user.save()
            messages.success(request, 'Utilisateur ajouté avec succès')
            return redirect('register')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'admin/user_registration.html', {'user_form': user_form})


# Page Liste de tous les utilisateurs
@login_required(login_url='login')
def all_users(request):

    # Barre de recherche
    #q = request.GET.get('q') if request.GET.get('q') != None else ''

    if request.GET.get('q') != None:
        q = request.GET.get('q')
        p = Paginator(User.objects.filter(
            Q(username__icontains=q) |
            Q(profile__fonction__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) 
            ),5)
        page = request.GET.get('page')
        msgs = p.get_page(page)
        return render(request, 'admin/users.html', { 'pages': msgs })
    else:
        # Partie Pagination
        p = Paginator(User.objects.all(), 5)
        page = request.GET.get('page')
        msgs = p.get_page(page)
        context = {

            'pages' : msgs
        }
        return render(request, 'admin/users.html', context)


# Page supprimer un utilisateur
@login_required(login_url='login')
def user_delete(request, pk):
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "Utilisateur supprimé!")
        return redirect('all_users')
    return render(request, 'admin/delete_item.html', {'item' : user, 'objet' : "de l'utilisateur", 'model' : 'Utilisateur'})


# Page profil d'un utilisateur
@login_required(login_url='login')
def userprofile(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(user = user)
    context = {
        'user' : user,
        'profile' : profile
    }
    return render(request, 'admin/user_profile.html', context)


# Page Ajout d'un profil
@login_required(login_url='login')
def add_profile(request):
    if request.method == 'POST':
        profileForm = UserProfileForm(request.POST, request.FILES)
        if profileForm.is_valid():
            profileForm.save()
            messages.success(request, "Profil ajouté!")
            return redirect('addprofile')
    else:
        profileForm = UserProfileForm()
    return render(request, 'admin/add_profile.html', {'form' : profileForm})


# Page modification d'un profil
@login_required(login_url='login')
def edit_profile(request):
    
    if request.method == 'POST':
        profileForm = UserProfileForm(request.POST, request.FILES, instance= request.user.profile)
        if profileForm.is_valid():
            profileForm.save()
            messages.success(request, "Profil modifié!")
            return redirect('userprofile') 
    else:
        profileForm = UserProfileForm(instance=request.user.profile)
    return render(request, 'admin/edit_profile.html', {'form' : profileForm})

# Tableau de bord
@login_required(login_url='login')
def dashboard(request):

    if request.method == "POST":
        q = request.POST['q']
        visitors_messages = Message.objects.filter(
            Q(author__icontains=q)|
            Q(email__icontains=q)|
            Q(subject__icontains=q)|
            Q(body__icontains=q)
        )
        subscribers = Subscriber.objects.filter(
            Q(email__icontains=q)
        )
        users = User.objects.filter(
            Q(username__icontains=q)|
            Q(first_name__icontains=q)|
            Q(last_name__icontains=q)
        )
        publications = Publication.objects.filter(
            Q(title__icontains=q)|
            Q(message__icontains=q)
        )
        devis = Estimate.objects.filter(
            Q(name__icontains=q)|
            Q(required_service__icontains=q)|
            Q(delivery_delay__icontains=q)|
            Q(payment_mode__icontains=q)|
            Q(email__icontains=q)|
            Q(description__icontains=q)
        )
        
        context = {
            'vm' : visitors_messages ,
            'sub' : subscribers ,
            'us' : users ,
            'pu' : publications ,
            'de' : devis ,
            'query' : q
        }
        return render(request,'admin/results_page.html', context)
    
    else :
        messages_count = Message.objects.count()
        subscribers_count = Subscriber.objects.count()
        mailMessages_count = Publication.objects.count()
        devis_count = Estimate.objects.count()
        salutation = random_phrases(request.user.first_name)
        context = {
            'messages' : messages_count,
            'subscribers' : subscribers_count,
            'mailMessages' : mailMessages_count,
            'devis' : devis_count,
            'hey' : salutation,
        }

        return render(request, 'admin/dashboard.html',context)


# Page Liste de tous les messages des visiteurs
@login_required(login_url='login')
def allmessages(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        subs = Subscriber.objects.all()
        messages =  Message.objects.filter(
            Q(author__icontains=q) |
            Q(email__icontains=q) |
            Q(subject__icontains=q) |
            Q(body__icontains=q) 
        )
        # Configuration de la pagination
        p = Paginator(messages, 5)
        page = request.GET.get('page')
        msgs = p.get_page(page)


        context = {
            'msgs' : msgs,
            'subs' : subs
        }
        return render(request, 'admin/messages.html', context)
    
    else:
        subs = Subscriber.objects.all()
        messages =  Message.objects.all()
        df = read_frame(subs, fieldnames=['email'])
        mail_list = df['email'].values.tolist()
        # Configuration de la pagination
        p = Paginator(messages, 5)
        page = request.GET.get('page')
        msgs = p.get_page(page)


        context = {
            'msgs' : msgs,
            'subs' : mail_list
        }
        return render(request, 'admin/messages.html', context)

# Page détail d'un message
@login_required(login_url='login')
def message_detail(request, pk):
    message = Message.objects.get(id=pk)
    context = {
        'message' : message
    }
    return render(request, 'admin/message_detail.html', context)

# Page répondre à un message
@login_required(login_url='login')
def message_answer(request, pk):
    msg = Message.objects.get(id=pk)
    answer = AnswerMessageForm(initial = {'mail_to': msg.email, 'title' : 'Re - ' + msg.subject})
    # Ajouter ici toute la logique 
    if request.method == 'POST':
        email = EmailMessage(
            request.POST['title'],
            request.POST['body'],
            to=[request.POST['mail_to']],
        )
        email.send(fail_silently=False)
        return redirect('messages')
    context = {
        'form' : answer,
        'objet' : msg
    }
    return render(request, 'admin/message_answer.html', context)

# Page supprimer un message
@login_required(login_url='login')
def message_delete(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('messages')
    return render(request, 'admin/delete_item.html', {'item' : message, 'objet' : 'du message', 'model' : 'Message de'})

# Page Liste de tous les abonnés à la newsletter
@login_required(login_url='login')
def subscribers(request):

    p = Paginator(Subscriber.objects.all(), 5)
    page = request.GET.get('page')
    subscribers = p.get_page(page)
    context = {
        'subscribers' : subscribers
    }
    return render(request, 'admin/subscribers.html', context)


# Page d'envoi de mail à un abonné
@login_required(login_url='login')
def send_message(request, pk):

    # Ajouter ici toute la logique 
    m = Subscriber.objects.get(id=pk)
    publicationForm = AnswerMessageForm(initial={'mail_to': m.email})
    if request.method == 'POST':
        email = EmailMessage(
            request.POST['title'],
            request.POST['body'],
            to=[request.POST['mail_to']],
        )
        email.send(fail_silently=False)
        return redirect('subscribers')
    context = {
        'form' : publicationForm
    }
    return render(request, 'admin/message_answer.html', context)

# Page supprimer un abonné
@login_required(login_url='login')
def subscriber_delete(request, pk):
    subscriber = Subscriber.objects.get(id=pk)

    if request.method == 'POST':
        subscriber.delete()
        messages.success(request, "Abonné supprimé!")
        return redirect('subscribers')
    return render(request, 'admin/delete_item.html', {'item' : subscriber, 'objet' : "de l'abonné", 'model' : 'Abonné'})

# Page Liste de tous les devis
@login_required(login_url='login')
def devis_all(request):

    if request.GET.get('q') != None:
        q = request.GET.get('q')
        p = Paginator(Estimate.objects.filter(
            Q(name__icontains=q)|
            Q(required_service__icontains=q)|
            Q(delivery_delay__icontains=q)|
            Q(payment_mode__icontains=q)|
            Q(budget__icontains=q)|
            Q(description__icontains=q)
        ), 5)
        page = request.GET.get('page')
        devis = p.get_page(page)
        context = {
            'devis' : devis
        }
        return render(request, 'admin/devis_all.html', context)
    else:

        p = Paginator(Estimate.objects.all(), 5)
        page = request.GET.get('page')
        devis = p.get_page(page)
        context = {
            'devis' : devis
        }
        return render(request, 'admin/devis_all.html', context)

# Page détail d'un devis
@login_required(login_url='login')
def devis_detail(request, pk):
    devis = Estimate.objects.get(id=pk)
    context = {
        'devis' : devis
    }
    return render(request, 'admin/devis_detail.html', context)

# Page supprimer un devis
@login_required(login_url='login')
def devis_delete(request, pk):
    devis = Estimate.objects.get(id=pk)

    if request.method == 'POST':
        devis.delete()
        return redirect('devis_all')
    return render(request, 'admin/delete_item.html', {'objet' : "de la demande", 'model' : 'Demande de '+ devis.name})

# Page Newsletter
@login_required(login_url='login')
def all_publications(request):

    if request.GET.get('q') != None:
        q = request.GET.get('q')
        p = Paginator(Publication.objects.filter(
            Q(title__icontains=q)|
            Q(message__icontains=q)
        ), 5)
        page = request.GET.get('page')
        msgs = p.get_page(page)
        context = {

            'publications' : msgs
        }
        return render(request, 'admin/all_publications.html', context)

    else:
        p = Paginator(Publication.objects.all(), 5)
        page = request.GET.get('page')
        msgs = p.get_page(page)
        context = {

            'publications' : msgs
        }
        return render(request, 'admin/all_publications.html', context)

# Page Ajout d'un message de publication
@login_required(login_url='login')
def add_publication(request):
    if request.method == 'POST':
        publicationForm = PublicationForm(request.POST)
        if publicationForm.is_valid():
            publicationForm.save()
            messages.success(request, "Publication ajoutée!")
            return redirect('add_publication')
    else:
        publicationForm = PublicationForm()
    return render(request, 'admin/add_publication.html', {'form' : publicationForm})


# Page modification d'un message de publication
@login_required(login_url='login')
def edit_publication(request, pk):
    if request.method == 'POST':
        publicationForm = PublicationForm(request.POST)
        if publicationForm.is_valid():
            publicationForm.save()
            messages.success(request, "Publication modifiée!")
            return redirect('add_publication')
    else:
        p = Publication.objects.get(id=pk)
        publicationForm = PublicationForm(instance=p)
    return render(request, 'admin/edit_publication.html', {'form' : publicationForm})

# Page détail d'un publication
@login_required(login_url='login')
def publication_detail(request, pk):
    publication = Publication.objects.get(id=pk)
    context = {
        'objet' : publication
    }
    return render(request, 'admin/publication.html', context)


# Page de suppression de publication
@login_required(login_url='login')
def publication_delete(request, pk):
    p = Publication.objects.get(id=pk)

    if request.method == 'POST':
        p.delete()
        return redirect('publications')
    context = {
        'item' : ' la publication n° '+ str(p.id),
        'objet' : ' de la publication',
        'model' : 'Publication n° '+ str(p.id),
    }
    return render(request, 'admin/delete_item.html', context)


# Page de reponse à un mail en particulier et d'envoi de mail avec modification
@login_required(login_url='login')
def send_publication(request, pk):

    # Ajouter ici toute la logique 
    subs = Subscriber.objects.all()
    df = read_frame(subs, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    m = Publication.objects.get(id=pk)
    if request.method == 'POST':
        email = EmailMessage(
            m.title,
            m.message,
            bcc=mail_list,
        )
        email.send(fail_silently=False)
        m.sent_status = True
        m.save()
        return redirect('publications')
    publicationForm = PublicationForm(instance = m)
#    messages.success(request, 'Publication envoyée à tous les abonnés')
    context = {
        'form' : publicationForm
    }
    return render(request, 'admin/send_publi.html', context)


# Page de diffusion de mail à tous les abonnés
@login_required(login_url='login')
def publish_message(request, pk):
    subs = Subscriber.objects.all()
    df = read_frame(subs, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    m = Publication.objects.get(id=pk)
    email  = EmailMessage(
        m.title,
        m.message,
        'administration@lyontech.com',
        mail_list,
    )
    email.send(fail_silently=False)
    return redirect('publications')

# Page de génération de devis
@login_required(login_url='login')
def make_invoice(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            identity = form.cleaned_data['customer_identity']
            form.save()
            obj = Command.objects.get(identity=identity)
            messages.success(request, 'Devis généré!')
            return redirect('invoice')
        # Insérer la fonction de PDF ici
        
    else:
        form = CommandForm()
        context = {
            'form': form
        }
    return render(request, 'admin/add_command.html', context)