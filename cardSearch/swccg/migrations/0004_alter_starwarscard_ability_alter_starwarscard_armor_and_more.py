# Generated by Django 4.1.3 on 2022-11-22 15:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swccg', '0003_alter_starwarscard_darksideicons_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='starwarscard',
            name='ability',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='armor',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='characteristics',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='conceptBy',
            field=models.TextField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='destiny',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='errataVersion',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='extraText',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=200), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='forfeit',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='gametext',
            field=models.TextField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='gempId',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='hyperspeed',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='imageUrl',
            field=models.URLField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='landspeed',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='legacy',
            field=models.BooleanField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='lore',
            field=models.TextField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='maneuver',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='parsec',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='politics',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='power',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='rarity',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='set',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='side',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='sourceType',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='subType',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='title',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='type',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='starwarscard',
            name='uniqueness',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
