# Generated by Django 2.1.1 on 2018-10-17 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20181017_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='highlighted',
            name='article',
        ),
        migrations.RemoveField(
            model_name='highlighted',
            name='author',
        ),
        migrations.DeleteModel(
            name='Highlighted',
        ),
    ]