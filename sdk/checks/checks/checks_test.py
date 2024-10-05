from string import ascii_lowercase, ascii_uppercase

import pytest

from checks.checks import is_free, slug, speak_food


@pytest.mark.parametrize(
    ('given', 'expected'),
    [
        (ascii_lowercase, ascii_lowercase),
        (ascii_uppercase, ascii_lowercase),
        ('É', 'e'),
        ('é', 'e'),
        ('123 fôé BAR҉', '123 foe bar'),
    ],
)
def test_slug(given: str, expected: str) -> None:
    assert slug(given) == expected


@pytest.mark.parametrize(
    'txt',
    [
        'Petit-déjeuner L\'ADN Data',
    ],
)
def test_speak_food_ok(txt: str) -> None:
    assert speak_food(txt) is True


@pytest.mark.parametrize(
    'txt',
    [
        'Emilie et Mathieu, experts en direction commerciale externalisée vont vous donner des tips ultra concrets',
    ],
)
def test_speak_food_no(txt: str) -> None:
    assert speak_food(txt) is False


@pytest.mark.parametrize(
    ('price', 'expected'),
    [
        ('venez à notre événement', True),
        ('cet événement est gratuit', True),
        ('$0', False),
        ('€0', False),
        ('$10', False),
        ('€10', False),
        ('0', True),
        ('10', True),
        ('Free event', True),
        ('Événement gratuit', True),
        ('Événement payant', False),
        ('C\'est payant', False),
        ('PAYANT', False),
        ('Gratuit mais payant pour certains', False),
        ('This event has a cost', False),
        ('COST: $10', False),
        ('No cost involved', False),
        ('Free of cost', False),
        ('10 euros', False),
        ('5 dollars', False),
        ('Prix : 20 euros', False),
        ('Price in dollars: 15', False),
        ('EURO', False),
        ('DOLLAR', False),
        ('Dîner gastronomique à 50€', False),
        ('Cocktail party, tickets $20', False),
        ('Free beer, entry fee 5 euros', False),
    ],
)
def test_is_free(price: str, expected: bool) -> None:
    assert is_free(price) == expected
