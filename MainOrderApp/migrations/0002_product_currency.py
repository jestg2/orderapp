# Generated by Django 5.0.1 on 2024-02-01 19:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainOrderApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(default=django.utils.timezone.now, max_length=3),
            preserve_default=False,
        ),
    ]
