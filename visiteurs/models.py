# Raikage The Third

from django.db import models
from django.urls import reverse, reverse_lazy

# Create your models here.


class Message(models.Model):
    author = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now=True)
    body = models.TextField(max_length=200)

    def __str__(self) -> str:
        return self.subject



class Estimate(models.Model):
    PAYMENT_MODES = (
        ('Cash', 'Cash'),
        ('Virement bancaire', 'Virement bancaire')
    )


    name = models.CharField(max_length=20)
    required_service = models.CharField(max_length=30)
    delivery_delay = models.CharField(max_length=20)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)  # Dans le formulaire, faire en sorte d'avoir une liste de choix de paiement
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    budget = models.IntegerField()
    file  = models.FileField(upload_to='devis/%Y/%m/%d/')
    description = models.TextField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("devis")


class Subscriber(models.Model):
    email = models.EmailField(max_length=50)  #Supprimer ce commentaire après l'ajout de la contrainte d'unicité
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.email



