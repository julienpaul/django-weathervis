# Generated by Django 3.1.13 on 2021-09-17 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_auto_20210916_1156"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True, verbose_name="User biography"),
        ),
    ]
