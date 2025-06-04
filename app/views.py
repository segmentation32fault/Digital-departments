from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .forms import RegistrationForm
from app.models import Recipe, UserProfile
from django.contrib.auth import login


menu = [{'title': 'Популярное', 'url': 'popular_recipes'},
        {'title': 'Вход', 'url': 'login'},
        {'title': 'Регистрация', 'url': 'register'},
        ]

# Create your views here.


def profile(request: HttpRequest):
    return HttpResponse('<h1>Профиль</h1>')

def liked_recipes(request: HttpRequest, username):
    user = get_object_or_404(UserProfile, username=username)
    recipes = list(map(int, user.likes.split(', ')))
    res = list()

    for recipe_id in recipes:
        recipe_info = Recipe.objects.filter(pk=recipe_id)
        if len(recipe_info) > 0:
            res.append(recipe_info[0])

    context = {'liked_recipes': res, 'menu': menu}
    return render(request, 'app/liked.html', context=context)


#def login(request: HttpRequest):
    #return render(request, 'app/login.html', context={'menu': menu})


def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print('Форма не валидна. Ошибки: ', form.errors.as_json())
    else:
        form = RegistrationForm()
    return render(request, 'app/register.html', {'form': form})


def popular_recipes(request: HttpRequest):
    recipes = Recipe.objects.order_by('-views')[:9]
    return render(request, 'app/index.html', context={'recipes': recipes, 'menu': menu})


def search(request: HttpRequest):
    return render(request, 'app/search.html')


def recipe(request: HttpRequest, post_slug='bliny'):
    recipe_by_slug = get_object_or_404(Recipe, slug=post_slug)
    context = {'name': recipe_by_slug.title,
               'ingredients': recipe_by_slug.ingredients.split(';'),
               'desc': recipe_by_slug.description,
               'img_name': str(recipe_by_slug.id) + '.webp'
               }
    print(context['ingredients'])
    if context is None:
        #   если рецепт не нашелся, то перенаправление на гл страницу или страницу ошибки
        return redirect('popular_recipes')

    context.update({'menu': menu})
    return render(request, 'app/recipe.html', context=context)


def add_recipe(request: HttpRequest):
    context = {'menu': menu}
    return render(request, 'app/addrecipe.html', context=context)


def analytics(request: HttpRequest):
    host = request.META['HTTP_HOST']
    return HttpResponse(f'<h1>Временная аналитика</h1>\n<p>Host: {host}</p>')


def index(request: HttpRequest):
    return redirect('popular_recipes')


def page_not_found(request: HttpRequest, exception):
    context = {'menu': menu}
    return render(request, 'app/404.html', status=404)
