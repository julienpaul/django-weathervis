# Generated by Django 3.1.13 on 2022-08-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20220825_0933'),
        ('stations', '0006_auto_20220823_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='active_campaign',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='campaigns',
            field=models.ManyToManyField(blank=True, related_name='stations', to='campaigns.Campaign'),
        ),
    ]
