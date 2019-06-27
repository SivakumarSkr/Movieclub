# Generated by Django 2.1.7 on 2019-06-17 12:07

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('post_content_object_id', models.CharField(max_length=20)),
            ],
        ),
    ]
