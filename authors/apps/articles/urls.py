from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ArticlesList.as_view(), name='articles'),
    path('articles/<slug>', views.ArticlesDetails.as_view(),  name='article-details')
    path('articles/<slug>/comments/', views.CommentsListCreateView.as_view())
]
