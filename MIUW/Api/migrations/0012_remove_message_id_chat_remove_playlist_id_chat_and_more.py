# Generated by Django 5.0.8 on 2024-11-12 23:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0011_delete_spotifyprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='ID_CHAT',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='ID_CHAT',
        ),
        migrations.RemoveField(
            model_name='message',
            name='ID_USER',
        ),
        migrations.AddField(
            model_name='playlist',
            name='ID_PLAYLIST',
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='ID_USER',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.usuario'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='NOMBRE_PLAYLIST',
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.DeleteModel(
            name='CHAT',
        ),
        migrations.DeleteModel(
            name='MESSAGE',
        ),
    ]
