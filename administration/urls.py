# Raikage The Third

from django.urls import path

from .views import *

urlpatterns =[
    # Route vers la page de connexion et les pages de types "Utilisateurs"
    path('login/', loginpage ,name="login"),
    path('logout/', logoutUser ,name="logout"),
    path('register-user/', register ,name="register"),
    path('all-users/', all_users ,name="all_users"),
    path('userprofile/<int:pk>', userprofile ,name="userprofile"),
    path('add-profile/', add_profile ,name="addprofile"),
    path('edit-profile/', edit_profile ,name="editprofile"),
    path('dashboard/user-delete/<int:pk>', user_delete ,name="user_delete"),

    # Route vers le tableau de bord
    path('dashboard/', dashboard ,name="dashboard"),

    # Route vers la page des abonnés
    path('dashboard/subscribers', subscribers ,name="subscribers"),
    path('dashboard/subscriber-delete/<int:pk>', subscriber_delete ,name="subscriber_delete"),
    path('dashboard/subscriber-send-message/<int:pk>', send_message ,name="send_message"),

    # Routes vers les pages de type "Messages"
    path('dashboard/messages', allmessages ,name="messages"),
    path('dashboard/message/<int:pk>', message_detail ,name="message_detail"),
    path('dashboard/message-answer/<int:pk>', message_answer ,name="message_answer"),
    path('dashboard/message-delete/<int:pk>', message_delete ,name="message_delete"),

    # Routes vers les pages de type "Devis"
    path('dashboard/all-estimates', devis_all ,name="devis_all"),
    path('dashboard/estimate/<int:pk>', devis_detail ,name="devis_detail"),
    path('dashboard/estimate-delete/<int:pk>', devis_delete ,name="devis_delete"),

    # Routes vers les pages de la newsletter
    path('dashboard/publications', all_publications ,name="publications"),
    path('dashboard/add-publication', add_publication ,name="add_publication"),
    path('dashboard/publication/<int:pk>', publication_detail ,name="publication"),
    path('dashboard/publication-delete/<int:pk>', publication_delete ,name="publication_delete"),
    # Publication avec modification
    path('dashboard/publication-send/<int:pk>', send_publication ,name="publication_send"),
    path('dashboard/publication-edit/<int:pk>', edit_publication ,name="publication_edit"),
    # Publication sans modification
    path('dashboard/publish/<int:pk>', publish_message ,name="publish"),

    # Page de résultats de recherche générale
    path('dashboard/search-results', dashboard, name='results')

]