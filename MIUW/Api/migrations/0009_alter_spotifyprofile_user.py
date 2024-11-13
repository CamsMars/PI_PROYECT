# Generated by Django 5.0.8 on 2024-11-12 06:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0008_remove_usuario_spfy_plan_remove_usuario_tokenspfy'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='spotify_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]