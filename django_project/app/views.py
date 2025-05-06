from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.conf import settings
import os

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Tag, User
from .serializers import PostSerializer, TagSerializer, UserSerializer, RegistrationSerializer

# Create your views here.


def index(request: HttpRequest):
    return HttpResponse('<h2>Главная страница</h2>')


def profile(request: HttpRequest):
    return HttpResponse('<h2>Профиль</h2>')


def login(request: HttpRequest):
    return render(request, 'login.html')


def register(request: HttpRequest):
    return render(request, 'register.html')


def popular_recipes(request: HttpRequest):
    return render(request, 'index.html')


def recipe(request: HttpRequest, num=1):
    # recipe_info = find_recipe(num)

    recipe_info = {'name': 'Блины',
                   'ingredients': {'молоко': '1 ст',
                                   'яйца': '2 шт',
                                   'мука': '100 гр',
                                   'соль': '1 щепотка',
                                   'сахар': '2 ст ложки'},
                   'desc': 'Описание',
                   'img_name': 'bliny.jpg'}

    if recipe_info is None:
        #   надо придумать что-то если рецепт не нашелся. наверное перенаправление на гл страницу
        return HttpResponsePermanentRedirect('/popular')

    return render(request, 'recipe.html', context=recipe_info)


def analytics(request: HttpRequest):
    host = request.META['HTTP_HOST']
    return HttpResponse(f'<h2>Временная аналитика</h2>\n<p>Host: {host}</p>')
