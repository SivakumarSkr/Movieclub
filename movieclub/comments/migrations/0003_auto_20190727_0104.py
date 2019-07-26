# Generated by Django 2.1.7 on 2019-07-26 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('comments', '0002_auto_20190705_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_content_object_id',
            new_name='object_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post_content_type',
        ),
        migrations.AddField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]