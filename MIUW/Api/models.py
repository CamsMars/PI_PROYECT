from django.db import models

class Token(models.Model):
    user = models.CharField(unique = True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class User(models.Model):
    Usuario = models.CharField(unique = True, max_length=50)
    Nombre = models.CharField(unique=False,max_length=25)
    Apellido = models.CharField(unique=False, max_length=25)
    Email = models.CharField(unique=True,max_length=25)
    Tpassw = models.CharField(unique=True,max_length=500)
    IA_Data = models.CharField(unique=True, max_length=700)
    User_BirthDate = models.DateField()
    UserCreateDate = models.DateTimeField()