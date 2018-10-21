# Generated by Django 2.1.2 on 2018-10-16 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('articles', '0002_articlesmodel_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.TextField()),
                ('read_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='articles.ArticlesModel', to_field='slug')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_id+', to='articles.ArticlesModel')),
                ('recipient', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='profiles.Profile')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]