from django.urls import path, re_path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    re_path(r'likes/(?P<username>\w+)/', views.liked_recipes, name='likes'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    path('popular/', views.popular_recipes, name='popular_recipes'),
    path('search/', views.search, name='search'),
    re_path(r'^recipe/(?P<num>\d+)/', views.recipe, name='recipe'),
    path('addrecipe/', views.add_recipe, name='add_recipe'),

    path('analytics/', views.analytics, name='analytics'),

    path('home/', views.index, name='home'),
    path('', views.index),
]
