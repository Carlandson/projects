# Generated by Django 4.1.3 on 2022-11-22 15:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swccg', '0008_starwarscard_ferocity'),
    ]

    operations = [
        migrations.AddField(
            model_name='starwarscard',
            name='destinyValues',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=200, null=True), default=list, null=True, size=None),
        ),
    ]
