from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Token(models.Model):
    user = models.CharField(unique = True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class usuario(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    USR = models.CharField(max_length=150, unique=True)
    Nombre = models.CharField(unique=False, max_length=25, blank=True)
    Apellido = models.CharField(unique=False, max_length=25, blank=True)
    Email = models.EmailField(blank=True)
    MusicalPreference = models.CharField(unique=False, max_length=700, blank=True)
    Artistas_FAV = models.CharField(unique=False, null=True, max_length=700, blank=True)
    Hystorial = models.CharField(unique=False, max_length=700, blank=True)
    User_BirthDate = models.DateField(null=True, blank=True)
    UserCreateDate = models.DateTimeField(default=timezone.now, blank=True)

class CHAT(models.Model):
    ID_CHAT=models.IntegerField(primary_key=True, null=False)
    Generated_PLYST=models.CharField(max_length=700, null=True)
    SUGERIDA_PLYST=models.CharField(max_length=700, null=True)
    CREACION=models.DateField(null=True)

class MESSAGE(models.Model):
    ID_USER=models.ForeignKey(usuario, on_delete=models.CASCADE, null=True)
    ID_CHAT=models.ForeignKey(CHAT,on_delete=models.CASCADE, null=False)
    USER_DESCRIP=models.TextField()
    FECHA=models.DateField()

class PLAYLIST(models.Model):
    ID_CHAT=models.ForeignKey(CHAT,on_delete=models.CASCADE, null=False)
    LINK_PLAYLIST=models.CharField(max_length=700, null=True)

class SpotifyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="spotify_profile")
    spotify_id = models.CharField(max_length=255, unique=True)

    def _str_(self):
        return f"{self.user.username} - {self.spotify_id}"