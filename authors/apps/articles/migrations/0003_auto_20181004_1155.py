# Generated by Django 2.1.1 on 2018-10-04 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20181003_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlesmodel',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='articlesmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='articlesmodel',
            name='slug',
            field=models.SlugField(blank=True, max_length=128, unique=True),
        ),
    ]
