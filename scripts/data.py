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


def get_ingredient_stats(name: str):
    ingredients_table = pd.read_csv(os.path.join(base_dir, 'data\\tablica_produktov.csv'), sep=';')
    stats = ingredients_table.loc[ingredients_table['продукт, 100 гр'].str.contains(name)]

    return stats.to_dict('records')[0]


def get_ccpf(recipe: dict):
    res = {
        'calories': 0,
        'carbohydrates': 0,
        'protein': 0,
        'fat': 0,
    }

    for i in recipe['ingredients']:
        k = recipe['ingredients'][i]
        k, amount = ' '.join(k.split()[1:]), k.split()[0]
        if k == 'ст':
            k = 200 / 100
        elif k.find('ст ложк') != -1:
            k = 10 / 100
        elif k == 'лист':
            k = 10 / 100

        else:
            k = 0

        if '/' in amount:
            amount = int(amount.split('/')[0]) / float(amount.split('/')[1])
        else:
            amount = float(amount)

        total = get_ingredient_stats(i)

        if k == 0 or len(total) == 0:
            continue

        res['calories'] = res['calories'] + total['калорийность'] * k * amount
        res['carbohydrates'] = res['carbohydrates'] + total['углеводы'] * k * amount
        res['protein'] = res['protein'] + total['белки'] * k * amount
        res['fat'] = res['fat'] + total['жиры'] * k * amount

    return res


if __name__ == '__main__':
    print(get_ccpf(find_recipe(1)))
