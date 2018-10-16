# Generated by Django 2.1.2 on 2018-10-16 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20181016_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotifications',
            name='article_link',
            field=models.URLField(blank=True, db_index=True, max_length=128, unique=True, verbose_name='Article Link'),
        ),
    ]
