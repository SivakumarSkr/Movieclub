# Generated by Django 2.1.7 on 2019-07-26 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20190727_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
