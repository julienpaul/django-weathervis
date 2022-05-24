# Generated by Django 3.1.13 on 2022-05-23 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surface_meteograms", "0002_auto_20220329_0956"),
    ]

    operations = [
        migrations.AddField(
            model_name="surfacemeteogram",
            name="img_path",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="surfacemeteogram",
            name="subtext",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="smpoints",
            name="name",
            field=models.CharField(
                choices=[
                    ("HERE", "Point location"),
                    ("ALL", "All points"),
                    ("LAND", "Land points"),
                    ("SEA", "Sea points"),
                ],
                default="HERE",
                max_length=4,
            ),
        ),
    ]