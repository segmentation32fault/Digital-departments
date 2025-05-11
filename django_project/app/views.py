from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, Http404
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.conf import settings
import os

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Tag, User
from .serializers import PostSerializer, TagSerializer, UserSerializer, RegistrationSerializer
from scripts.data import find_recipe

# Create your views here.


def index(request: HttpRequest):
    return HttpResponse('<h1>Главная страница</h1>')


def profile(request: HttpRequest):
    return HttpResponse('<h1>Профиль</h1>')


def login(request: HttpRequest):
    return render(request, 'app/login.html')


def register(request: HttpRequest):
    return render(request, 'app/register.html')


def popular_recipes(request: HttpRequest):
    return render(request, 'app/index.html')


def recipe(request: HttpRequest, num=1):
    recipe_info = find_recipe(int(num))

    if recipe_info is None:
        #   если рецепт не нашелся, то перенаправление на гл страницу или страницу ошибки
        return redirect('home')

    return render(request, 'app/recipe.html', context=recipe_info)


def analytics(request: HttpRequest):
    host = request.META['HTTP_HOST']
    return HttpResponse(f'<h1>Временная аналитика</h1>\n<p>Host: {host}</p>')


def page_not_found(request: HttpRequest, exception):
    return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')
