from pathlib import Path
import datetime

import pytest
from models import Event, Gratters, consitent_uuid

from meetup.parser import parse

from pydantic_core._pydantic_core import TzInfo


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (
            {
                "id": "303599531",
                  "title": "Meetup OWASP - Paris - Octobre 2024",
                  "description": "Ce meetup se deroulera chez **GitGuardian** que nous remercions chaleureusement de leur soutien.\n\nOWASP Paris est le meetup d\u00e9di\u00e9 \u00e0 la s\u00e9curit\u00e9 applicative. Pour rappel, le meetup se veut non commercial. Il r\u00e9unit toutes personnes d\u00e9sireuses de concevoir et maintenir des logiciels plus s\u00fbrs. Si vous \u00eates int\u00e9ress\u00e9 par le sujet, que vous soyez d\u00e9butant ou expert, n'h\u00e9sitez pas \u00e0 nous rejoindre pour partager vos exp\u00e9riences ou vos probl\u00e9matiques.\nCe meetup propose des sessions organis\u00e9es en mode \"forum ouvert\". Les sujets sont propos\u00e9s par les participants lors de la s\u00e9ance. Partages de connaissances, retour d'exp\u00e9riences, exercices de type CTF, bonnes pratiques, gouvernance et organisation, ... sont au programme!\n\n**Lightning Talks:**\nLa soir\u00e9e commence par de courtes pr\u00e9sentations. Chacun peut s'il le veut proposer une pr\u00e9sentation, ce n'est pas obligatoire. Si vous avez envie de partager une technique, une opinion, une d\u00e9mo ou un retour d'exp\u00e9rience, alors vous pouvez pr\u00e9parer un lightning talk, entre une simple phrase et 10 minutes maxi et venez le pr\u00e9senter au d\u00e9but de la soir\u00e9e. Si vous n'avez jamais fait de pr\u00e9sentation avant, c'est l'occasion de commencer dans une ambiance sympa.\n\n**Workshop:**\nLa soir\u00e9e se poursuit avec des activit\u00e9s men\u00e9es en groupes. Chacun peut s'il le veut proposer un sujet, ce n'est pas obligatoire. Vous avez 30 secondes au d\u00e9but de la session pour en donner envie aux autres participants, puis tout le monde vote pour son sujet favori. Les sujets pr\u00e9f\u00e9r\u00e9s donnent lieu \u00e0 des activit\u00e9s en groupes pendant un peu plus d'une heure. Des \u00e9crans seront disponibles\n\nLe format se veut bienveillant. Pas besoin d'\u00eatre expert pour parler d'un sujet. Vous trouverez certainement d'autres personnes pour vous aider! L'accent est mis sur l'\u00e9change et le partage.\n\nL'agenda et le compte-rendu des pr\u00e9c\u00e9dents meetups est accessible ici: https://owasp.org/www-chapter-france/",
                  "eventUrl": "https://www.meetup.com/owasp-france/events/303599531/",
                  "venue": {
                      "name": "12 Rue d'Aboukir",
                      "address": "12 Rue d'Aboukir",
                      "city": "Paris",
                      "eventVenueOptions": {
                          "feeSettings": None
                      }
                  },
                  "dateTime": "2024-10-07T19:00:00+02:00",
                  "endTime": "2024-10-07T21:00:00+02:00"
            },
            Event(
                id=consitent_uuid(Gratters.MEETUP, "303599531"),
                name='Meetup OWASP - Paris - Octobre 2024',
                date_start=datetime.datetime(
                    2024, 10, 7, 19, 0, tzinfo=TzInfo(7200)
                ),
                date_end=datetime.datetime(
                    2024, 10, 7, 21, 0, tzinfo=TzInfo(7200)
                ),
                description="Ce meetup se deroulera chez **GitGuardian** que nous remercions chaleureusement de leur soutien.\n\nOWASP Paris est le meetup d\u00e9di\u00e9 \u00e0 la s\u00e9curit\u00e9 applicative. Pour rappel, le meetup se veut non commercial. Il r\u00e9unit toutes personnes d\u00e9sireuses de concevoir et maintenir des logiciels plus s\u00fbrs. Si vous \u00eates int\u00e9ress\u00e9 par le sujet, que vous soyez d\u00e9butant ou expert, n'h\u00e9sitez pas \u00e0 nous rejoindre pour partager vos exp\u00e9riences ou vos probl\u00e9matiques.\nCe meetup propose des sessions organis\u00e9es en mode \"forum ouvert\". Les sujets sont propos\u00e9s par les participants lors de la s\u00e9ance. Partages de connaissances, retour d'exp\u00e9riences, exercices de type CTF, bonnes pratiques, gouvernance et organisation, ... sont au programme!\n\n**Lightning Talks:**\nLa soir\u00e9e commence par de courtes pr\u00e9sentations. Chacun peut s'il le veut proposer une pr\u00e9sentation, ce n'est pas obligatoire. Si vous avez envie de partager une technique, une opinion, une d\u00e9mo ou un retour d'exp\u00e9rience, alors vous pouvez pr\u00e9parer un lightning talk, entre une simple phrase et 10 minutes maxi et venez le pr\u00e9senter au d\u00e9but de la soir\u00e9e. Si vous n'avez jamais fait de pr\u00e9sentation avant, c'est l'occasion de commencer dans une ambiance sympa.\n\n**Workshop:**\nLa soir\u00e9e se poursuit avec des activit\u00e9s men\u00e9es en groupes. Chacun peut s'il le veut proposer un sujet, ce n'est pas obligatoire. Vous avez 30 secondes au d\u00e9but de la session pour en donner envie aux autres participants, puis tout le monde vote pour son sujet favori. Les sujets pr\u00e9f\u00e9r\u00e9s donnent lieu \u00e0 des activit\u00e9s en groupes pendant un peu plus d'une heure. Des \u00e9crans seront disponibles\n\nLe format se veut bienveillant. Pas besoin d'\u00eatre expert pour parler d'un sujet. Vous trouverez certainement d'autres personnes pour vous aider! L'accent est mis sur l'\u00e9change et le partage.\n\nL'agenda et le compte-rendu des pr\u00e9c\u00e9dents meetups est accessible ici: https://owasp.org/www-chapter-france/",
                location='12 Rue d\'Aboukir, Paris',
                url='https://www.meetup.com/owasp-france/events/303599531/',
                mandatory_registration=True,
            ),
        ),
        (
            {
                "id": "303599531",
                  "title": "Meetup OWASP - Paris - Octobre 2024",
                  "description": "Ce meetup se deroulera chez **GitGuardian** que nous remercions chaleureusement de leur soutien.\n\nOWASP Paris est le meetup d\u00e9di\u00e9 \u00e0 la s\u00e9curit\u00e9 applicative. Pour rappel, le meetup se veut non commercial. Il r\u00e9unit toutes personnes d\u00e9sireuses de concevoir et maintenir des logiciels plus s\u00fbrs. Si vous \u00eates int\u00e9ress\u00e9 par le sujet, que vous soyez d\u00e9butant ou expert, n'h\u00e9sitez pas \u00e0 nous rejoindre pour partager vos exp\u00e9riences ou vos probl\u00e9matiques.\nCe meetup propose des sessions organis\u00e9es en mode \"forum ouvert\". Les sujets sont propos\u00e9s par les participants lors de la s\u00e9ance. Partages de connaissances, retour d'exp\u00e9riences, exercices de type CTF, bonnes pratiques, gouvernance et organisation, ... sont au programme!\n\n**Lightning Talks:**\nLa soir\u00e9e commence par de courtes pr\u00e9sentations. Chacun peut s'il le veut proposer une pr\u00e9sentation, ce n'est pas obligatoire. Si vous avez envie de partager une technique, une opinion, une d\u00e9mo ou un retour d'exp\u00e9rience, alors vous pouvez pr\u00e9parer un lightning talk, entre une simple phrase et 10 minutes maxi et venez le pr\u00e9senter au d\u00e9but de la soir\u00e9e. Si vous n'avez jamais fait de pr\u00e9sentation avant, c'est l'occasion de commencer dans une ambiance sympa.\n\n**Workshop:**\nLa soir\u00e9e se poursuit avec des activit\u00e9s men\u00e9es en groupes. Chacun peut s'il le veut proposer un sujet, ce n'est pas obligatoire. Vous avez 30 secondes au d\u00e9but de la session pour en donner envie aux autres participants, puis tout le monde vote pour son sujet favori. Les sujets pr\u00e9f\u00e9r\u00e9s donnent lieu \u00e0 des activit\u00e9s en groupes pendant un peu plus d'une heure. Des \u00e9crans seront disponibles\n\nLe format se veut bienveillant. Pas besoin d'\u00eatre expert pour parler d'un sujet. Vous trouverez certainement d'autres personnes pour vous aider! L'accent est mis sur l'\u00e9change et le partage.\n\nL'agenda et le compte-rendu des pr\u00e9c\u00e9dents meetups est accessible ici: https://owasp.org/www-chapter-france/",
                  "eventUrl": "https://www.meetup.com/owasp-france/events/303599531/",
                  "venue": {
                      "name": "12 Rue d'Aboukir",
                      "address": "12 Rue d'Aboukir",
                      "city": "Paris",
                      "eventVenueOptions": {
                          "feeSettings": {
                              "amount": 0
                          }
                      }
                  },
                  "dateTime": "2024-10-07T19:00:00+02:00",
                  "endTime": "2024-10-07T21:00:00+02:00"
            },
            Event(
                id=consitent_uuid(Gratters.MEETUP, "303599531"),
                name='Meetup OWASP - Paris - Octobre 2024',
                date_start=datetime.datetime(
                    2024, 10, 7, 19, 0, tzinfo=TzInfo(7200)
                ),
                date_end=datetime.datetime(
                    2024, 10, 7, 21, 0, tzinfo=TzInfo(7200)
                ),
                description="Ce meetup se deroulera chez **GitGuardian** que nous remercions chaleureusement de leur soutien.\n\nOWASP Paris est le meetup d\u00e9di\u00e9 \u00e0 la s\u00e9curit\u00e9 applicative. Pour rappel, le meetup se veut non commercial. Il r\u00e9unit toutes personnes d\u00e9sireuses de concevoir et maintenir des logiciels plus s\u00fbrs. Si vous \u00eates int\u00e9ress\u00e9 par le sujet, que vous soyez d\u00e9butant ou expert, n'h\u00e9sitez pas \u00e0 nous rejoindre pour partager vos exp\u00e9riences ou vos probl\u00e9matiques.\nCe meetup propose des sessions organis\u00e9es en mode \"forum ouvert\". Les sujets sont propos\u00e9s par les participants lors de la s\u00e9ance. Partages de connaissances, retour d'exp\u00e9riences, exercices de type CTF, bonnes pratiques, gouvernance et organisation, ... sont au programme!\n\n**Lightning Talks:**\nLa soir\u00e9e commence par de courtes pr\u00e9sentations. Chacun peut s'il le veut proposer une pr\u00e9sentation, ce n'est pas obligatoire. Si vous avez envie de partager une technique, une opinion, une d\u00e9mo ou un retour d'exp\u00e9rience, alors vous pouvez pr\u00e9parer un lightning talk, entre une simple phrase et 10 minutes maxi et venez le pr\u00e9senter au d\u00e9but de la soir\u00e9e. Si vous n'avez jamais fait de pr\u00e9sentation avant, c'est l'occasion de commencer dans une ambiance sympa.\n\n**Workshop:**\nLa soir\u00e9e se poursuit avec des activit\u00e9s men\u00e9es en groupes. Chacun peut s'il le veut proposer un sujet, ce n'est pas obligatoire. Vous avez 30 secondes au d\u00e9but de la session pour en donner envie aux autres participants, puis tout le monde vote pour son sujet favori. Les sujets pr\u00e9f\u00e9r\u00e9s donnent lieu \u00e0 des activit\u00e9s en groupes pendant un peu plus d'une heure. Des \u00e9crans seront disponibles\n\nLe format se veut bienveillant. Pas besoin d'\u00eatre expert pour parler d'un sujet. Vous trouverez certainement d'autres personnes pour vous aider! L'accent est mis sur l'\u00e9change et le partage.\n\nL'agenda et le compte-rendu des pr\u00e9c\u00e9dents meetups est accessible ici: https://owasp.org/www-chapter-france/",
                location='12 Rue d\'Aboukir, Paris',
                url='https://www.meetup.com/owasp-france/events/303599531/',
                mandatory_registration=True,
            ),
        ),
        (
            {
                "id": "303599531",
                  "title": "Meetup OWASP - Paris - Octobre 2024",
                  "description": "Ce meetup se deroulera chez **GitGuardian** que nous remercions chaleureusement de leur soutien.\n\nOWASP Paris est le meetup d\u00e9di\u00e9 \u00e0 la s\u00e9curit\u00e9 applicative. Pour rappel, le meetup se veut non commercial. Il r\u00e9unit toutes personnes d\u00e9sireuses de concevoir et maintenir des logiciels plus s\u00fbrs. Si vous \u00eates int\u00e9ress\u00e9 par le sujet, que vous soyez d\u00e9butant ou expert, n'h\u00e9sitez pas \u00e0 nous rejoindre pour partager vos exp\u00e9riences ou vos probl\u00e9matiques.\nCe meetup propose des sessions organis\u00e9es en mode \"forum ouvert\". Les sujets sont propos\u00e9s par les participants lors de la s\u00e9ance. Partages de connaissances, retour d'exp\u00e9riences, exercices de type CTF, bonnes pratiques, gouvernance et organisation, ... sont au programme!\n\n**Lightning Talks:**\nLa soir\u00e9e commence par de courtes pr\u00e9sentations. Chacun peut s'il le veut proposer une pr\u00e9sentation, ce n'est pas obligatoire. Si vous avez envie de partager une technique, une opinion, une d\u00e9mo ou un retour d'exp\u00e9rience, alors vous pouvez pr\u00e9parer un lightning talk, entre une simple phrase et 10 minutes maxi et venez le pr\u00e9senter au d\u00e9but de la soir\u00e9e. Si vous n'avez jamais fait de pr\u00e9sentation avant, c'est l'occasion de commencer dans une ambiance sympa.\n\n**Workshop:**\nLa soir\u00e9e se poursuit avec des activit\u00e9s men\u00e9es en groupes. Chacun peut s'il le veut proposer un sujet, ce n'est pas obligatoire. Vous avez 30 secondes au d\u00e9but de la session pour en donner envie aux autres participants, puis tout le monde vote pour son sujet favori. Les sujets pr\u00e9f\u00e9r\u00e9s donnent lieu \u00e0 des activit\u00e9s en groupes pendant un peu plus d'une heure. Des \u00e9crans seront disponibles\n\nLe format se veut bienveillant. Pas besoin d'\u00eatre expert pour parler d'un sujet. Vous trouverez certainement d'autres personnes pour vous aider! L'accent est mis sur l'\u00e9change et le partage.\n\nL'agenda et le compte-rendu des pr\u00e9c\u00e9dents meetups est accessible ici: https://owasp.org/www-chapter-france/",
                  "eventUrl": "https://www.meetup.com/owasp-france/events/303599531/",
                  "venue": {
                      "name": "12 Rue d'Aboukir",
                      "address": "12 Rue d'Aboukir",
                      "city": "Paris",
                      "eventVenueOptions": {
                          "feeSettings": {
                              "amount": 5
                          }
                      }
                  },
                  "dateTime": "2024-10-07T19:00:00+02:00",
                  "endTime": "2024-10-07T21:00:00+02:00"
            },
            None,
        ),
    ],
)
def test_parse(data: dict, expected: Event):
    assert parse(data) == expected
