# Generated by Django 3.1.13 on 2022-08-11 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0002_domainsplot'),
        ('domains', '0002_domain_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='plots',
            field=models.ManyToManyField(blank=True, related_name='domains', to='plots.DomainsPlot'),
        ),
    ]
