from django.urls import path, re_path
from . import views
from django.contrib.auth import views as v

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    re_path(r'likes/(?P<username>\w+)/', views.liked_recipes, name='likes'),
    path('login/', v.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('register/', views.register, name='register'),

    path('popular/', views.popular_recipes, name='popular_recipes'),
    path('search/', views.search, name='search'),
    path('recipe/<slug:post_slug>/', views.recipe, name='recipe'),

    path('addrecipe/', views.add_recipe, name='add_recipe'),

    path('analytics/', views.analytics, name='analytics'),

    path('home/', views.index, name='home'),
    path('', views.index),
]
