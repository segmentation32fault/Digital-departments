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


menu = [{'title': 'Популярное', 'url': 'popular_recipes'},
        {'title': 'Вход', 'url': 'login'},
        {'title': 'Регистрация', 'url': 'register'},
        ]

# Create your views here.


def profile(request: HttpRequest):
    return HttpResponse('<h1>Профиль</h1>')

def liked_recipes(request: HttpRequest, username):
    context = {'liked_recipes': get_liked_recipes(username=username), 'menu': menu}
    return render(request, 'app/liked.html', context=context)


def login(request: HttpRequest):
    return render(request, 'app/login.html', context={'menu': menu})


def register(request: HttpRequest):
    return render(request, 'app/register.html', context={'menu': menu})


def popular_recipes(request: HttpRequest):
    recipes = get_popular_recipes(9)
    return render(request, 'app/index.html', context={'recipes': recipes, 'menu': menu})


def search(request: HttpRequest):
    # return render(request, 'app/search.html')
    return HttpResponse('<h1>Поиск рецепта</h1>')


def recipe(request: HttpRequest, num=1):
    context = find_recipe(int(num))
    if context is None:
        #   если рецепт не нашелся, то перенаправление на гл страницу или страницу ошибки
        return redirect('popular_recipes')

    context.update({'menu': menu})
    return render(request, 'app/recipe.html', context=context)


def add_recipe(request: HttpRequest):
    return HttpResponse('<h1>Добавление рецепта</h1>')


def analytics(request: HttpRequest):
    host = request.META['HTTP_HOST']
    return HttpResponse(f'<h1>Временная аналитика</h1>\n<p>Host: {host}</p>')


def index(request: HttpRequest):
    return redirect('popular_recipes')


def page_not_found(request: HttpRequest, exception):
    context = {'menu': menu}
    return render(request, 'app/404.html', status=404)
