# Generated by Django 2.1.2 on 2018-11-14 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20181113_2233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favourite',
            options={'ordering': ('created_at',)},
        ),
    ]
