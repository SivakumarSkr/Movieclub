# Generated by Django 2.2.8 on 2020-04-14 17:55

import uuid

import django.utils.timezone
import markdownx.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(max_length=500)),
                ('type_of_group',
                 models.CharField(choices=[('O', 'Open'), ('C', 'Closed')], max_length=1, verbose_name='Type')),
            ],
        ),
        migrations.CreateModel(
            name='GroupBlog',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('watched', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1)),
                ('contents', markdownx.models.MarkdownxField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='contents/%(class)/%Y/%m/%d')),
                ('heading', models.CharField(max_length=300)),
                ('published', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('requested_time', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
            ],
        ),
    ]
