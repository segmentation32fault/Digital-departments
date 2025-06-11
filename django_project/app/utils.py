menu = [{'title': 'Популярное', 'url': 'popular_recipes'},
        {'title': 'Вход', 'url': 'users:login'},
        {'title': 'Регистрация', 'url': 'users:register'},
        {'title': 'Поиск', 'url': 'search'},
        {'title': 'Добавить рецепт', 'url': 'add_recipe'},
        ]


class DataMixin:
    title_page = None
    extra_content = {}

    def __init__(self):
        if self.title_page:
            self.extra_content['title'] = self.title_page

        if 'menu' not in self.extra_content:
            self.extra_content['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        context['menu'] = menu
        context['tag_selected'] = None
        context.update(kwargs)

        return context
