from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ArticlesList.as_view()),
    path('articles/<slug>', views.ArticlesDetails.as_view())
]
