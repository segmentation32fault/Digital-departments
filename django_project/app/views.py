from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import RegistrationForm, AddRecipeForm, SearchForm
from app.models import Recipe, UserProfile
from .utils import DataMixin

menu = [{'title': 'Популярное', 'url': 'popular_recipes'},
        {'title': 'Вход', 'url': 'users:login'},
        {'title': 'Регистрация', 'url': 'users:register'},
        {'title': 'Поиск', 'url': 'search'},
        {'title': 'Добавить рецепт', 'url': 'add_recipe'},
        ]

# Create your views here.


def liked_recipes(request: HttpRequest, username):
    user = get_object_or_404(UserProfile, username=username)
    recipes = user.likes.all()
    res = list()

    for recipe_id in recipes:
        recipe_info = Recipe.published.filter(pk=recipe_id)
        if len(recipe_info) > 0:
            res.append(recipe_info[0])

    context = {'liked_recipes': res, 'menu': menu}
    return render(request, 'app/liked.html', context=context)


def profile(request: HttpRequest, username):
    user = get_object_or_404(UserProfile, username=username)
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    recipes = user.likes.all()

    context = {'menu': menu, 'username': username, 'first_name': first_name, 'last_name': last_name, 'liked_recipes': recipes}
    return render(request, 'app/profile.html', context)


class ProfileView(DataMixin, DetailView):
    model = UserProfile
    template_name = 'app/profile.html'
    slug_url_kwarg = 'username_slug'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = context['user'].likes.all()

        return self.get_mixin_context(context,
                                      liked_recipes=recipes,
                                      username=context['user'].username,
                                      first_name=context['user'].first_name,
                                      last_name=context['user'].last_name
                                      )

    def get_object(self, queryset=None):
        user = get_object_or_404(UserProfile, username=self.kwargs[self.slug_url_kwarg])



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


class SearchView(DataMixin, View):
    template_name = 'app/search.html'

    def get(self, request):
        form = SearchForm()
        context = {'menu': menu, 'form': form, 'title': 'Поиск'}
        return render(request, 'app/search.html', context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('query')
            queryset = Recipe.published.order_by('-views')
            result = []
            for i in queryset:
                if name.lower() in i.title.lower():
                    result.append(i)
            if len(result) != 0:
                return render(request, 'app/search.html', {'menu': menu, 'recipes': result, 'form': form, 'title': 'Поиск'})
            else:
                return render(request, 'app/search.html', {'menu': menu, 'form': form, 'title': 'Поиск'})
        else:
            print('Форма не валидна. Ошибки: ', form.errors.as_json())
        return render(request, 'app/search.html', context={'menu': menu, 'form': form, 'title': 'Поиск'})



class PopularRecipes(DataMixin, ListView):
    model = Recipe
    template_name = 'app/index.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Популярные рецепты')

    def get_queryset(self):
        return Recipe.published.order_by('-views')[:9]


class RecipeTag(DataMixin, ListView):
    template_name = 'app/index.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = context['recipes'][0].tag
        return self.get_mixin_context(context, title=tag.name, tag_selected=tag.id)

    def get_queryset(self):
        return Recipe.published.filter(tag__slug=self.kwargs['tag_slug']).order_by('-views')


class RecipeView(DataMixin, DetailView):
    model = Recipe
    template_name = 'app/recipe.html'
    slug_url_kwarg = 'recipe_slug'
    context_object_name = 'rec'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context['rec']
        recipe.views += 1
        print(recipe.views)
        recipe.save()
        return self.get_mixin_context(context,
                                      title=recipe.title,
                                      ingredients=recipe.ingredients.split('\n'),
                                      steps = recipe.steps.strip().split('\n')
                                      )

    def get_object(self, queryset=None):
        return get_object_or_404(Recipe.published, slug=self.kwargs[self.slug_url_kwarg])


class AddRecipe(DataMixin, CreateView):
    form_class = AddRecipeForm
    template_name = 'app/addrecipe.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return self.get_mixin_context(context, title='Добавление рецепта')


class EditRecipe(DataMixin, UpdateView):
    model = Recipe
    fields = ('title', 'slug', 'description', 'ingredients', 'tags', 'calories', 'steps')
    template_name = 'app/addrecipe.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return self.get_mixin_context(context, title='Изменение рецепта')


def analytics(request: HttpRequest):
    host = request.META['HTTP_HOST']
    return HttpResponse(f'<h1>Временная аналитика</h1>\n<p>Host: {host}</p>')


def index(request: HttpRequest):
    return redirect('popular_recipes')


def page_not_found(request: HttpRequest, exception):
    context = {'menu': menu}
    return render(request, 'app/404.html', status=404)
