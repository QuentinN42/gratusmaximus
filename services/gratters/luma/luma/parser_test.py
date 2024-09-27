import datetime
from pathlib import Path

import pytest
from models import Event, Gratters, consitent_uuid

from luma.parser import parse

assets = Path(__file__).parent.parent / "assets"


@pytest.mark.parametrize(
    ("file", "expected"),
    [
        (
            'evt-1Ah5VleTtMDiezj.json',
            Event(
                id=consitent_uuid(Gratters.LUMA, "evt-1Ah5VleTtMDiezj"),
                name='Inclusive Hour SISTA x DASTORE - Comment créer et gérer une relation commerciale avec un grand groupe ?',
                date_start=datetime.datetime(
                    2024, 10, 2, 10, 0, tzinfo=datetime.timezone.utc
                ),
                date_end=datetime.datetime(
                    2024, 10, 2, 12, 30, tzinfo=datetime.timezone.utc
                ),
                description="""INCLUSIVE HOURS

L’Inclusive Hour est un événement co-organisé par SISTA et Carrefour via son fonds Dastore. Cette rencontre vise à mettre en lumière des entrepreneurs du portefeuille de Dastore, ainsi que des représentants de Carrefour, autour d'un sujet crucial pour leur développement : \"Comment créer et gérer une relation commerciale avec un grand groupe".

Objectifs de l'événement

Éducation et partage d'expérience : Fournir aux entrepreneuses de SISTA les connaissances et les bonnes pratiques (do & don'ts) pour établir et maintenir une relation commerciale fructueuse avec une grande entreprise.

Leverage sur le Corporate Venture Capital (CVC) : Montrer comment les entrepreneurs peuvent tirer parti des ressources et des opportunités offertes par les fonds de CVC comme Dastore.



Intervenants

Startups : Les dirigeants des startups partenaires de Carrefour et leurs équipes, telles que Stockly, Ida et Underdog, partageront leurs expériences et perspectives.


Représentants de Carrefour : Des responsables internes de Carrefour fourniront un aperçu de leurs attentes et processus internes.

Public Cible

Cet événement est ouvert au public et sera particulièrement bénéfique pour les fondatrices et fondateurs de startups cherchant à comprendre et à améliorer leurs relations commerciales avec de grandes entreprises.

Déroulé de l'événement 

12H - 12H30 : Accueil dans les locaux de Carrefour
12h30 - 13h30 : Table ronde et échanges
13h30 - 14h30 : Networking et cocktail déjeunatoire""",
                location='93 Av. de Paris, 91300 Massy, France',
                url='https://lu.ma/lzl1nxxz',
                mandatory_registration=True,
            ),
        ),
        (
            'evt-i2lYpvfGZTy3p0U.json',
            Event(
                id=consitent_uuid(Gratters.LUMA, "evt-i2lYpvfGZTy3p0U"),
                name='Climate Coffee in Paris',
                date_start=datetime.datetime(
                    2024, 10, 3, 6, 30, tzinfo=datetime.timezone.utc
                ),
                date_end=datetime.datetime(
                    2024, 10, 3, 8, 30, tzinfo=datetime.timezone.utc
                ),
                description="""Founders Future & Techstars Sustainability Paris are inviting you to Climate Coffee that this time will take place at Techstars' office in Paris

Climate Coffee is built on the idea of creating an open community for anyone interested in climate, whether you’re operating, investing, studying in or just exploring the space.

This is based on the belief that time is of the essence when it comes to tackling climate change, and that by fostering connections and helping to develop local ecosystems, we might be able to increase the pace of change and adoption of new technologies and new ideas across the world.

Here the supporters helping getting this initiative off the ground:

Thomas Bajas @Founders Future - a French early stage VC investing in European tech startups and supporting founders into building the backbone of their business. Climate Tech is one of the two main pillars of the thesis with a focus on circular economy (Bibak, auum, Campsider, Underdog, Twice, 900care, food (Yuka, Bon Vivant, Olala), and electrification (Zenride, Yespark, Bohr Énergie, Beev, Tilt, Daze).


Rebecca Ravenni & Raphaele Leyendecker @Techstars Sustainability Paris - French antenna of Techstars, Techstars Sustainability Paris invests worldwide in state-of-the-art Climate tech ventures (Tech and Sector agnostic) and support founders through three-month hybrid accelerator programs.""",
                location='48.86750 2.34250',
                url='https://lu.ma/f5uzlkr4',
                mandatory_registration=True,
            ),
        ),
    ],
)
def test_parse(file: str, expected: Event):
    with open(assets / file) as f:
        data = f.read()
    assert parse(data) == expected
