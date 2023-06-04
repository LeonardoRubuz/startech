# Raikage The Third

from django.db import models
from django.conf import settings

# Fonction de définition de route d'un fichier
def user_directory_path(instance):

    # L'image sera envoyée vers MEDIA_ROOT/users_<username>
    return 'users{0}/'.format(instance.user.username)

# Create your models here.
class Publication(models.Model):
    title = models.CharField(max_length=100, null=True)
    message = models.TextField()
    sent_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    SEX_OPTIONS = (
        ('Femme', 'Femme'),
        ('Homme', 'Homme')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    sex = models.CharField(max_length=5, choices=SEX_OPTIONS, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/photos/",null=True, blank=True)
    fonction = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=50,null=True)
    country = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username

class Command(models.Model):
    # Différents choix 
    PAYMENT_MODES = (
        ('Cash', 'Cash'),
        ('Virement bancaire', 'Virement bancaire'),
        ('Orange-Money', 'Orange-Money')
    )
    SITE_TYPES = (
        ('Application Web','Application Web'),
        ('Blog','Blog'),
        ('E-commerce','E-commerce'),
        ('Forum','Forum'),
        ('One Page','One Page'),
        ('Portfolio','Portfolio'),
        ('Vitrine','Vitrine')
    )
    DATABASE_CATEGORIES = (
        ('Classique','Classique'),
        ('Avancée','Avancéé')

    )
    DOMAIN_EXTENSIONS = (
        ('.com','.com'),
        ('.org','.org'),
        ('.cd','.cd')
    )
    HOSTING_CATEGORIES = (
        ('Simple','Simple'),
        ('Mutualisé','Mutualisé'),
        ('WordPress','WordPress'),
        ('VPS','VPS')

    )
    MAINTENANCE_CATEGORIES = (
        ('Mensuelle','Mensuelle'),
        ('Trimestrielle','Trimestrielle'),
        ('Semestrielle','Semestrielle')
    )
    HOSTING_PERIODS = (
        ('5 ans','5 ans'),
        ('2 ans','2 ans'),
        ('1 an','1 an'),
        ('6 mois','6 mois'),
        ('3 mois','3 mois'),
        ('1 mois','1 mois'),
    )
    SITE_CATEGORIES=(
        ('Simple','Simple'),
        ('Intermédiaire','Intermédiaire'),
        ('Avancé','Avancé')
    )
    DOMAIN_PERIODS = (
        ('5 ans','5 ans'),
        ('4 ans','4 ans'),
        ('3 ans','3 ans'),
        ('2 ans','2 ans'),
        ('1 an','1 an')
    )

    ## Informations propres au client
    customer_identity = models.CharField(max_length=25, null=False)
    address = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, null=False)
    phone = models.CharField(max_length=15, null=False)
    payment_mode = models.CharField(max_length=50, null=False, choices=PAYMENT_MODES)
    ## Informations de la commande
    # Type de site
    site_type = models.CharField( max_length=50, null=False, choices=SITE_TYPES)
    site_category = models.CharField( max_length=50, null=False, choices=SITE_CATEGORIES)
    site_quantity = models.PositiveSmallIntegerField(null=False)
    site_cost = models.FloatField(null=False)
    # Base de données
    db_exist = models.BooleanField(default=False, blank=True, null=True)
    db_category = models.CharField(max_length=50, null=True, choices=DATABASE_CATEGORIES)
    db_quantity = models.PositiveSmallIntegerField(null=True)
    db_cost = models.FloatField(null=True)
    # Nom de domaine
    domain_exist = models.BooleanField(default=False, null=True)
    domain_extension = models.CharField(max_length=50, null=True, choices=DOMAIN_EXTENSIONS)
    domain_period = models.CharField(max_length=50,null=True, choices=DOMAIN_PERIODS)
    domain_quantity = models.PositiveSmallIntegerField(null=True)
    domain_cost = models.FloatField(null=True)
    # Hébergement
    hosting_exist = models.BooleanField(default=False, null=True)
    hosting_type = models.CharField(max_length=50, null=True, choices=HOSTING_CATEGORIES)
    hosting_period = models.CharField(max_length=50,null=True, choices=HOSTING_PERIODS)
    hosting_quantity = models.PositiveSmallIntegerField(null=True)
    hosting_cost = models.FloatField(null=True)
    
    # Maintenance
    maintenance_exist = models.BooleanField(default=False, null=True)
    maintenance_category = models.CharField(null=True, max_length=50, choices=MAINTENANCE_CATEGORIES)
    maintenance_quantity = models.PositiveSmallIntegerField(null=True)
    maintenance_cost = models.FloatField(null=True)
