from django.db import models

class Token(models.Model):
    user = models.CharField(unique = True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Usuario(models.Model):
    Usuario = models.CharField(unique = True, max_length=50)
    Nombre = models.CharField(unique=False,max_length=25)
    Apellido = models.CharField(unique=False, max_length=25)
    Email = models.CharField(unique=True,max_length=25)
    tokenSPFY = models.CharField(unique=True, max_length=700)
    SPFY_plan=models.CharField(max_length=50)
    MusicalPreference = models.CharField(unique=False,max_length=700)
    Artistas_FAV = models.CharField(unique=False,null=True,max_length=700)
    Hystorial = models.CharField(unique=False,max_length=700)
    User_BirthDate = models.DateField()
    UserCreateDate = models.DateTimeField()

class CHAT(models.Model):
    ID_CHAT=models.IntegerField(primary_key=True, null=False)
    Generated_PLYST=models.CharField(max_length=700)
    SUGERIDA_PLYST=models.CharField(max_length=700)
    CREACION=models.DateField()

class MESSAGE(models.Model):
    ID_CHAT=models.IntegerField(primary_key=True, null=False)
    USER_DESCRIP=models.CharField(max_length=700)
    FECHA=models.DateField()

class PLAYLIST(models.Model):
    ID_CHAT=models.IntegerField(primary_key=True,null=False)
    LINK_PLAYLIST=models.CharField(max_length=700)

