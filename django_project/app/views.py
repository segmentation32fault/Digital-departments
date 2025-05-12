from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, Http404
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.conf import settings
import os
from scripts.data import find_recipe, get_popular_recipes, get_liked_recipes

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Tag, User
from .serializers import PostSerializer, TagSerializer, UserSerializer, RegistrationSerializer


# Create your views here.


def index(request: HttpRequest):
    return redirect('popular_recipes')


def profile(request: HttpRequest):
    return HttpResponse('<h1>Профиль</h1>')


def login(request: HttpRequest):
    return render(request, 'app/login.html')


def register(request: HttpRequest):
    return render(request, 'app/register.html')


def popular_recipes(request: HttpRequest):
    recipes = get_popular_recipes(9)
    return render(request, 'app/index.html', context={'recipes': recipes})


def recipe(request: HttpRequest, num=1):
    recipe_info = find_recipe(int(num))

    if recipe_info is None:
        #   если рецепт не нашелся, то перенаправление на гл страницу или страницу ошибки
        return redirect('popular_recipes')

    return render(request, 'app/recipe.html', context=recipe_info)


def analytics(request: HttpRequest):
    host = request.META['HTTP_HOST']
    return HttpResponse(f'<h1>Временная аналитика</h1>\n<p>Host: {host}</p>')


def liked_recipes(request: HttpRequest, username):
    context = {'liked_recipes': get_liked_recipes(username=username)}
    return render(request, 'app/liked.html', context=context)

def page_not_found(request: HttpRequest, exception):
    return render(request, 'app/404.html', status=404)
