# Generated by Django 5.0.7 on 2024-10-16 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0008_alter_usuario_usr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='CREACION',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='Generated_PLYST',
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='SUGERIDA_PLYST',
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='LINK_PLAYLIST',
            field=models.CharField(max_length=700, null=True),
        ),
    ]
