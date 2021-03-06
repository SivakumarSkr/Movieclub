# Generated by Django 2.1.7 on 2019-07-05 13:33

from django.db import migrations, models
import django.utils.timezone
import uuid


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
                ('time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('description', models.TextField(null=True)),
                ('slug', models.SlugField(blank=True, max_length=300, null=True)),
                ('no_of_watches', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-time',),
                'get_latest_by': 'time',
            },
        ),
    ]
