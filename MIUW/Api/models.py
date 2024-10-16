from django.db import models

class Token(models.Model):
    user = models.CharField(unique = True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Usuario(models.Model):
    USR = models.CharField(max_length=150)
    Nombre = models.CharField(unique=False,max_length=25, blank=True)
    Apellido = models.CharField(unique=False, max_length=25, blank=True)
    Email = models.EmailField()
    tokenSPFY = models.CharField(unique=True, max_length=700, blank=True)
    SPFY_plan=models.CharField(max_length=50, blank=True)
    MusicalPreference = models.CharField(unique=False,max_length=700, blank=True)
    Artistas_FAV = models.CharField(unique=False,null=True,max_length=700, blank=True)
    Hystorial = models.CharField(unique=False,max_length=700, blank=True)
    User_BirthDate = models.DateField()
    UserCreateDate = models.DateTimeField()

class CHAT(models.Model):
    ID_CHAT=models.IntegerField(primary_key=True, null=False)
    Generated_PLYST=models.CharField(max_length=700, null=True)
    SUGERIDA_PLYST=models.CharField(max_length=700, null=True)
    CREACION=models.DateField(null=True)

class MESSAGE(models.Model):
    ID_CHAT=models.ForeignKey(CHAT,on_delete=models.CASCADE, null=False)
    USER_DESCRIP=models.TextField()
    FECHA=models.DateField()

class PLAYLIST(models.Model):
    ID_CHAT=models.ForeignKey(CHAT,on_delete=models.CASCADE, null=False)
    LINK_PLAYLIST=models.CharField(max_length=700, null=True)
