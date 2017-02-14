# coding: utf-8
from __future__ import unicode_literals
from utils import CSVScraper


class LavalPersonScraper(CSVScraper):
    csv_url = 'https://www.donneesquebec.ca/recherche/dataset/8fe69713-fade-4751-a0b4-7e57a81886b1/resource/bb38e19e-26ab-495c-a0f7-ed6b3268b6e6/download/cusersapp.netappdatalocaltemp288c1490-df30-472a-8170-dd06728f449alistedeselus2013-2017.csv'
    locale = 'fr'
    # Laval also removes accents and cedillas from data.
    corrections = {
        'district name': {
            'Concorde - Bois-de-Boulogne': 'Concorde-Bois-de-Boulogne',
            "L'Abord-a-Plouffe": 'Abord-à-Plouffe',
            "L'Oree-des-bois": 'Orée-des-Bois',
            'Laval-les-Iles': 'Laval-les-Îles',
            'Marc-Aurele-Fortin': 'Marc-Aurèle-Fortin',
            'Saint-Francois': 'Saint-François',
            'Sainte-Dorothee': 'Sainte-Dorothée',
        },
    }

    # Absurdly, Laval has decided "les en-têtes ne comportent pas de
    # caractères accentués ou d'espaces" and includes a byte order mark.
    def header_converter(self, s):
        s = super(LavalPersonScraper, self).header_converter(s.replace('-', ' '))
        return {
            'ï»¿nom du district': 'district name',
            'role': 'primary role',
            'prenom': 'first name',
            'localite': 'locality',
            'telephone': 'phone',
            'telecopieur': 'fax',
            'url photo': 'photo url',
        }.get(s, s)
