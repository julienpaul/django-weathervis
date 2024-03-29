# Generated by Django 3.1.13 on 2022-08-25 09:20

import django.contrib.postgres.fields.citext
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(error_messages={'unique': 'A campaign with that name already exists.'}, help_text='Required. 150 characters or fewer. Case insensitive.', max_length=150, unique=True, verbose_name='name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
