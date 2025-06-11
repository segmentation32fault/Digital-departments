from django.contrib import admin
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from unicodedata import category


# Create your models here.


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Recipe.Status.PUBLISHED)


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0
        PUBLISHED = 1

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    ingredients = models.TextField(blank=True)
    calories = models.IntegerField(default=0)
    photos_count = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    views = models.IntegerField(default=0)

    tags = models.ManyToManyField('Tag', related_name='recipes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")

    objects = models.Manager()
    published = PublishedModel()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'recipe_slug': self.slug})

    def get_image_url(self):
        return f'images/{self.id}.webp'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'views')
    list_display_links = ('title', )
    list_editable = ('is_published', )
    list_filter = ('is_published', 'tags__name')
    list_per_page = 10
    ordering = ['-created_at', 'title']
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'tags__name']

    fields = ('title', 'slug', 'ingredients', 'description', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title', )}

    @admin.action(description='Опубликовать выбранные рецепты')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Recipe.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} рецепта(ов).')

    @admin.action(description='Снять с публикации выбранные рецепты')
    def set_draft(self, request, queryset):
        count = queryset.update(is_draft=Recipe.Status.DRAFT)
        self.message_user(request, f'{count} рецепта(ов) снято с публикации.')


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    likes = models.ManyToManyField(Recipe, related_name='liked_recipes')
    isadmin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_display_links = ('username', )
    search_fields = ('username', 'first_name', 'last_name', 'email')
