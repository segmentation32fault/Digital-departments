from django.conf import settings
import pandas as pd
import os
import psycopg2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
base_dir = settings.BASE_DIR


def find_recipe(num):
    table = pd.read_csv(os.path.join(base_dir, 'data\\recipes.csv'))
    if len(table) < num:
        return None
    ingredients = zip(table.loc[num - 1, 'Ингредиенты'].split(', '), table.loc[num - 1, 'Кол-во'].split(', '))
    res = {'name': table.loc[num - 1, 'Название'],
           'ingredients': dict(ingredients),
           'desc': table.loc[num - 1, 'Описание'],
           'img_name': table.loc[num - 1, 'Фото']
           }
    return res


def get_popular_recipes(count):
    table = pd.read_csv(os.path.join(base_dir, 'data\\recipes.csv'))
    res = table.sort_values(by=['Просмотры'], ascending=False)
    res = res.head(count)
    res = res.to_dict(orient='records')
    return res


def get_liked_recipes(username: str):
    users_table = pd.read_csv(os.path.join(base_dir, 'data\\users.csv'))
    recipes_table = pd.read_csv(os.path.join(base_dir, 'data\\recipes.csv'))

    liked = users_table.loc[users_table['Username'] == username]['Saved'].tolist()
    liked = list(map(int, liked[0].split(', ')))

    res = list(filter(lambda recipe: recipe['ID'] in liked, recipes_table.to_dict(orient='records')))
    return res


if __name__ == '__main__':
    print(get_liked_recipes('ramilische'))
