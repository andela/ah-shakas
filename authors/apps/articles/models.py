from django.db import models
from authors.apps.authentication.models import User

# Create your models here.


class ArticlesModel(models.Model):
    """ This class defines the model for creating articles"""
    slug = models.SlugField(db_index=True, max_length=128, unique=True)
    title = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=120, blank=False)
    body = models.TextField(blank=False)
    createdAt = models.DateTimeField(auto_now_add=True, auto_now=False)
    updatedAt = models.DateTimeField(auto_now=True, auto_now_add=False)
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    #Todo
    # -Slugify slug
