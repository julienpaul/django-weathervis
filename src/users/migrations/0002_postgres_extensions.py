# Generated by Django 3.1.13 on 2021-09-16 11:38
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        CITextExtension()
    ]
