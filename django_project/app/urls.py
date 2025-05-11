from django.urls import path, re_path
from . import views

urlpatterns = [
    path('profile/', views.profile),
    path('login/', views.login),
    path('register/', views.register),

    path('popular/', views.popular_recipes),
    re_path(r'^recipe/(?P<num>\d+)', views.recipe),

    path('analytics/', views.analytics),
    path('home/', views.index, name='home'),
    path('', views.index),
]
