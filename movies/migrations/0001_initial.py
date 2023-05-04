# Generated by Django 2.2.8 on 2020-09-13 14:23

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import movies.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=movies.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=movies.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('released_year', models.IntegerField(null=True,
                                                      validators=[django.core.validators.MinValueValidator(1900),
                                                                  django.core.validators.MaxValueValidator(2020)])),
                ('country', models.CharField(max_length=40, null=True)),
                ('rating', models.PositiveIntegerField(default=0,
                                                       validators=[django.core.validators.MaxValueValidator(10),
                                                                   django.core.validators.MinValueValidator(0)])),
                ('thumbnail', models.ImageField(null=True, upload_to=movies.models.upload_to_movies)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rate', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10),
                                                                      django.core.validators.MinValueValidator(0)])),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings',
                                            to='movies.Movie')),
            ],
        ),
    ]
