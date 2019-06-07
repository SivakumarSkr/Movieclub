# Generated by Django 2.1.7 on 2019-06-01 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.URLField(null=True)),
                ('twitter', models.URLField(null=True)),
                ('instagram', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField()),
                ('country', models.CharField(max_length=30)),
                ('biography', models.TextField()),
                ('social_media', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='star', to='persons.SocialMedia')),
            ],
        ),
    ]
