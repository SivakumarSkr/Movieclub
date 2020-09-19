# Generated by Django 2.2.8 on 2020-09-13 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shares', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='liked',
            field=models.ManyToManyField(related_name='shares_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='share',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]