# Generated by Django 2.2.8 on 2020-04-14 17:55

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('head', models.CharField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=300)),
                ('no_of_watches', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-time',),
                'get_latest_by': 'time',
            },
        ),
    ]
