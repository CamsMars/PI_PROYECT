# Generated by Django 5.1.2 on 2024-11-11 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0002_alter_usuario_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='USR',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='UserCreateDate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='User_BirthDate',
            field=models.DateField(blank=True),
        ),
    ]