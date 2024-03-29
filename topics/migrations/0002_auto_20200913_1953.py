# Generated by Django 2.2.8 on 2020-09-13 14:23

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topic',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='topics_followed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topic',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.',
                                                  through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
