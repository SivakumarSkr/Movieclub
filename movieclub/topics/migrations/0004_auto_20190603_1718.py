# Generated by Django 2.1.7 on 2019-06-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20190603_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='no_of_watches',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
