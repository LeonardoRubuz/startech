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
