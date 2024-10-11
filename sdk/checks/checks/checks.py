import re
import unicodedata
from typing import Callable

__WHITELISTED_CHARS = ['€']


def __build_regex(words: list) -> re.Pattern:
    return re.compile(f'({"|".join(words)})')


def __build_match(words: list) -> Callable[[str], bool]:
    _regex = __build_regex(words)

    def f(txt: str) -> bool:
        return len(_regex.findall(slug(txt))) > 0

    return f


def __build_dont_match(words: list) -> Callable[[str], bool]:
    _f = __build_match(words)

    def f(txt: str) -> bool:
        return not _f(txt)

    return f


def slug(txt: str) -> str:
    """String to only ascii chars"""
    return ''.join(
        c
        for c in unicodedata.normalize('NFD', txt)
        if (unicodedata.category(c) != 'Mn' and ord(c) < 256)
        or c in __WHITELISTED_CHARS
    ).lower()


speak_food = __build_match(
    [
        'dejeuner',
        'pizza',
        'repas',
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
)


is_free = __build_dont_match(
    [
        'price',
        'payant',
        'cost',
        'euro',
        'eur',
        'usd',
        'dollar',
        r'\$',
        '€',
    ]
)
