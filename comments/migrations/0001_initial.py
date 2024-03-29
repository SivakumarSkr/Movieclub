# Generated by Django 2.2.8 on 2020-09-13 14:23

import uuid

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('text', models.TextField()),
                ('edited', models.BooleanField(blank=True, default=False, verbose_name='Edited')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('object_id', models.CharField(blank=True, max_length=40)),
                ('content_type',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-time',),
            },
        ),
    ]
