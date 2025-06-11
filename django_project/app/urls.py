from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from .views import EditRecipe

urlpatterns = [
    path('profile/<slug:username>', views.profile, name='profile'),
    # path('profile/<slug:username>', views.ProfileView.as_view(), name='profile'),
    re_path(r'likes/(?P<username>\w+)/', views.liked_recipes, name='likes'),
    # path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    # path('register/', views.register, name='register'),

    path('popular/', views.PopularRecipes.as_view(), name='popular_recipes'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('recipe/<slug:recipe_slug>/', views.RecipeView.as_view(), name='recipe'),

    path('add/', views.AddRecipe.as_view(), name='add_recipe'),
    path('edit/<slug:slug>/', EditRecipe.as_view(), name='edit_recipe'),

    path('analytics/', views.analytics, name='analytics'),

    path('home/', views.index, name='home'),
    path('', views.index),
]
