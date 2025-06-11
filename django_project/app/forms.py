from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Recipe, Tag


class RegistrationForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'slug', 'description', 'ingredients', 'tags', 'calories', 'steps')
        widgets = {
            'title': forms.TextInput(),
            'slug': forms.TextInput(),
            'description': forms.Textarea(),
            'ingredients': forms.Textarea(),
            'tags': forms.MultipleChoiceField(),
            'calories': forms.NumberInput(),
            'steps': forms.Textarea(),

        }
    title = forms.CharField(max_length=255, label='Название')
    slug = forms.SlugField(max_length=255, label='URL')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
    ingredients = forms.CharField(widget=forms.Textarea, label='Ингредиенты')
    calories = forms.IntegerField(widget=forms.NumberInput, required=False, label='Калории')
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, label='Теги')
    steps = forms.CharField(widget=forms.Textarea, required=False, label='Шаги приготовления')


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 500px; height: 50px; border-radius: 8px;'}),
                                                   label='Поиск')
