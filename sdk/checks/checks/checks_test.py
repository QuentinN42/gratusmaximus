from string import ascii_lowercase, ascii_uppercase

import pytest

from checks.checks import slug, speak_food


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
