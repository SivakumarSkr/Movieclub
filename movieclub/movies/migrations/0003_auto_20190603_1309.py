# Generated by Django 2.1.7 on 2019-06-03 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20190602_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='stars',
            field=models.ManyToManyField(related_name='movies_star', to='persons.Star'),
        ),
    ]