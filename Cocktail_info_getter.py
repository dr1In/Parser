
import pymorphy2
from bs4 import BeautifulSoup, Tag

import requests
from Exceptions import CantConvert

from config import IMG_CLASS, INGREDIENT_CLASS, NAME_CLASS, RECIPE_CLASS, WEBSITE_LINK


def get_info(link: str):
    resp = requests.get(WEBSITE_LINK+link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    name_tag = soup.find('h1', class_=NAME_CLASS)
    img_tag = soup.find('div', class_=IMG_CLASS)
    ingredient_tag = soup.find('ul', class_=INGREDIENT_CLASS)
    recipe_tag = soup.find_all('div', class_=RECIPE_CLASS)
    return [
        _normalize_name(name_tag),
        _normalize_ingredient(ingredient_tag),
        _normalize_img(img_tag),
        _normalize_recipe(recipe_tag)
    ]
    

def _normalize_name(unfixed_name: Tag) -> str:
    name_tag = _convert(unfixed_name)
    name = _slice(name_tag, '<h1 class="detailed" itemprop="name">', '</h1>')
    return name

def _normalize_img(img: Tag)  -> str:
    img_tag = _convert(img)
    fixed_img = img_tag.replace('"image" src="', '$')
    fixed_img = fixed_img.replace('" title=', '$!')
    f1, f2 = fixed_img.index('$'), fixed_img.index('$!')
    return fixed_img[f1+1:f2]

def _normalize_ingredient(unfixed_ingredients: Tag) -> list:
    ingredients_tag = _convert(unfixed_ingredients)
    ingredients = _slice(ingredients_tag, '<ul class="detailed_ingredients">\n', '</ul>')
    ingredients = ingredients.replace('\xa0', ' ')
    ingredients = ingredients.replace('\n', '')
    ingredients_list = ingredients.split('</li>')
    return _each_ingredient(ingredients_list)


def _normalize_recipe(steps: list) -> str:
    all_steps = list()
    for step in steps:
        fixed_step = _convert(step)
        all_steps.append(_slice(fixed_step,
            '<div class="detailed_step_description_big">',
            '</div>'))
    recipe = '$'.join(all_steps)
    if '<div class="detailed_step_description_big noPhotoStep">' in recipe:
        recipe = recipe.replace('<div class="detailed_step_description_big noPhotoStep">', '')
    if '\r' in recipe:
        recipe = recipe.replace('\r', '')
    return recipe

def _convert(tag: Tag) ->  str:
    try:
        fixed_tag = str(tag)
    except ValueError:
        raise CantConvert
    return fixed_tag

def _slice(content: str, pref: str, suf: str) -> str:
    fixed_content = content.removeprefix(pref)
    fixed_content = fixed_content.removesuffix(suf)
    return fixed_content


def _each_ingredient(tags: list) -> list:
    tags.remove('')
    ingre = list()
    for tag in tags:
        fixed_tag = _slice(tag, '<li itemprop="recipeIngredient" rel="', '</li>')
        name, quantity = fixed_tag.index('"'), fixed_tag.index('—')
        name = fixed_tag[:name]
        morph = pymorphy2.MorphAnalyzer()
        word = morph.parse(name)[0].normal_form
        ingre.append(f'{word}{fixed_tag[quantity+1:]}')
    return ingre