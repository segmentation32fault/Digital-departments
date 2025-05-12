from django.urls import path, re_path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    re_path(r'likes/(?P<username>\w+)/', views.liked_recipes, name='likes'),

    path('popular/', views.popular_recipes, name='popular_recipes'),
    re_path(r'^recipe/(?P<num>\d+)/', views.recipe, name='recipe'),

    path('analytics/', views.analytics, name='analytics'),
    path('home/', views.index, name='home'),
    path('', views.index),
]
