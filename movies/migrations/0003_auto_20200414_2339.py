# Generated by Django 2.2.8 on 2020-04-14 18:09

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0002_auto_20200414_2325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='id',
        ),
        migrations.RemoveField(
            model_name='language',
            name='id',
        ),
        migrations.AlterField(
            model_name='genre',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='language',
            name='uuid_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
