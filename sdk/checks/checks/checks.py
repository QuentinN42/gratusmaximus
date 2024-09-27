import re
import unicodedata


def slug(txt: str) -> str:
    """String to only ascii chars"""
    return ''.join(
        (
            c
            for c in (
                c
                for c in unicodedata.normalize('NFD', txt)
                if unicodedata.category(c) != 'Mn'
            )
            if ord(c) < 256
        )
    ).lower()


_FOOD_WORDS = [
    'dejeuner',
    'repa',
    'restauration',
    'collation',
    'apero',
    'cocktail',
    'biere',
    'buffet',
    'cuisine',
    'menu',
    'bistrot',
    'diner',
    'brunch',
    'nourriture',
    'lunch',
    'beer',
    'dinner',
    'meal',
    'food',
    'restaurant',
    'snack',
    'breakfast',
]
_FOOD_REGEX = re.compile(f'({"|".join(_FOOD_WORDS)})')


def speak_food(txt: str) -> bool:
    res = _FOOD_REGEX.findall(slug(txt))
    return len(res) > 0
