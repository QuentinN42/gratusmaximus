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
        'Meetup OWASP - Paris - Octobre 2024',
        'Ce meetup se deroulera chez GitGuardian que nous remercions chaleureusement de leur soutien.',
        'OWASP Paris est le meetup dédié à la sécurité applicative. Pour rappel, le meetup se veut non commercial.',
        'Il réunit toutes personnes désireuses de concevoir et maintenir des logiciels plus sûrs.',
        "Si vous êtes intéressé par le sujet, que vous soyez débutant ou expert, n'hésitez pas à nous rejoindre pour partager vos expériences ou vos problématiques.",
        'Ce meetup propose des sessions organisées en mode "forum ouvert".',
        'Les sujets sont proposés par les participants lors de la séance.',
        "Partages de connaissances, retour d'expériences, exercices de type CTF, bonnes pratiques, gouvernance et organisation, ... sont au programme!",
        'La soirée commence par de courtes présentations.',
        "Si vous avez envie de partager une technique, une opinion, une démo ou un retour d'expérience",
        ', alors vous pouvez préparer un lightning talk, entre une simple phrase et 10 minutes maxi et venez le présenter au début de la soirée.',
        "Chacun peut s'il le veut proposer une présentation, ce n'est pas obligatoire.",
        "Si vous n'avez jamais fait de présentation avant, c'est l'occasion de commencer dans une ambiance sympa.",
        'La soirée se poursuit avec des activités menées en groupes.',
        "Chacun peut s'il le veut proposer un sujet, ce n'est pas obligatoire.",
        'Vous avez 30 secondes au début de la session pour en donner envie aux autres participants, puis tout le monde vote pour son sujet favori.',
        "Les sujets préférés donnent lieu à des activités en groupes pendant un peu plus d'une heure. Des écrans seront disponibles",
        "Le format se veut bienveillant.",
        "Pas besoin d'être expert pour parler d'un sujet.",
        "Vous trouverez certainement d'autres personnes pour vous aider! L'accent est mis sur l'échange et le partage.",
        "L'agenda et le compte-rendu des précédents meetups est accessible ici: https://owasp.org/www-chapter-france/",
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
