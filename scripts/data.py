from django.conf import settings
import pandas as pd
import os


def find_recipe(num):
    base_dir = settings.BASE_DIR
    table = pd.read_csv(os.path.join(base_dir, 'data/recipes.csv'))
    if len(table) < num:
        return None
    ingredients = zip(table.loc[num - 1, 'Ингредиенты'], table.loc[num - 1, 'Кол-во'])
    res = {'name': table.loc[num - 1, 'Название'],
           'ingredients': dict(ingredients),
           'desc': table.loc[num - 1, 'Описание'],
           'img_name': table.loc[num - 1, 'Фото']
           }
    return res


print(find_recipe(2))
