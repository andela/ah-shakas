from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
<<<<<<< HEAD
=======
    path('articles/', views.ArticlesList.as_view(), name='articles'),
    path('articles/<slug>', views.ArticlesDetails.as_view(),  name='article-details')
>>>>>>> [FEATURE #160577482] Add urls for comments
    path('articles/', views.ArticlesList.as_view()),
    path('articles/<slug>', views.ArticlesDetails.as_view()),
    path('articles/<slug>/comments/', views.CommentsListCreateView.as_view())
]
