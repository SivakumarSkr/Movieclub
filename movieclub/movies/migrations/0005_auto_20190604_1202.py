# Generated by Django 2.1.7 on 2019-06-04 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20190604_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(related_name='movies_genre', to='movies.Genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='stars',
            field=models.ManyToManyField(related_name='movies_star', to='persons.Star'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(related_name='movies_writer', to='persons.Star'),
        ),
    ]
