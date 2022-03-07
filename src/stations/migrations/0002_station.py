# Generated by Django 3.1.13 on 2022-03-01 10:09

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('margins', '0002_auto_20220301_0952'),
        ('stations', '0001_postgres_extensions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(error_messages={'unique': 'That name already exists.'}, max_length=50, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True, verbose_name='Station Adress')),
                ('geom', django.contrib.gis.db.models.fields.PointField(dim=3, srid=4326)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('station_id', django.contrib.postgres.fields.citext.CICharField(blank=True, error_messages={'unique': 'That station_id already exists.'}, help_text='Station identifier', max_length=50, null=True, unique=True)),
                ('wmo_id', django.contrib.postgres.fields.citext.CICharField(blank=True, error_messages={'unique': 'That wmo_id already exists.'}, help_text='WMO identifier', max_length=5, null=True, unique=True)),
                ('description', models.TextField(blank=True, help_text='Add information about the station')),
                ('margin_geom', django.contrib.gis.db.models.fields.PolygonField(dim=3, srid=4326)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('margin', models.ForeignKey(help_text='Offset around station location', on_delete=django.db.models.deletion.RESTRICT, related_name='stations', to='margins.margin')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
