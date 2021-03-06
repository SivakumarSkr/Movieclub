# Generated by Django 2.1.7 on 2019-07-05 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
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
            name='share_content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='share',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to=settings.AUTH_USER_MODEL),
        ),
    ]
