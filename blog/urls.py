from django.urls import path

from rest_framework import routers

from .views import ArticleListViewSet, ArticleCreateViewSet





article_router = routers.DefaultRouter()
article_router.register('all_article', ArticleListViewSet, basename='all_article')
article_router.register('article', ArticleCreateViewSet, basename='article')