# Generated by Django 5.0.7 on 2024-10-15 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0003_user_gustos'),
    ]

    operations = [
        migrations.CreateModel(
            name='CHAT',
            fields=[
                ('ID_CHAT', models.IntegerField(primary_key=True, serialize=False)),
                ('Generated_PLYST', models.CharField(max_length=700)),
                ('SUGERIDA_PLYST', models.CharField(max_length=700)),
                ('CREACION', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MESSAGE',
            fields=[
                ('ID_CHAT', models.IntegerField(primary_key=True, serialize=False)),
                ('USER_DESCRIP', models.CharField(max_length=700)),
                ('FECHA', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PLAYLIST',
            fields=[
                ('ID_CHAT', models.IntegerField(primary_key=True, serialize=False)),
                ('LINK_PLAYLIST', models.CharField(max_length=700)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Usuario', models.CharField(max_length=50, unique=True)),
                ('Nombre', models.CharField(max_length=25)),
                ('Apellido', models.CharField(max_length=25)),
                ('Email', models.CharField(max_length=25, unique=True)),
                ('tokenSPFY', models.CharField(max_length=700, unique=True)),
                ('SPFY_plan', models.CharField(max_length=50)),
                ('MusicalPreference', models.CharField(max_length=700)),
                ('Artistas_FAV', models.CharField(max_length=700, null=True)),
                ('Hystorial', models.CharField(max_length=700)),
                ('User_BirthDate', models.DateField()),
                ('UserCreateDate', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
