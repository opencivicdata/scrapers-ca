from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.laval.ca/Pages/Fr/A-propos/conseillers-municipaux.aspx'


class LavalPersonScraper(CSVScraper):
    csv_url = 'https://www.donneesquebec.ca/recherche/dataset/8fe69713-fade-4751-a0b4-7e57a81886b1/resource/bb38e19e-26ab-495c-a0f7-ed6b3268b6e6/download/cusersapp.netappdatalocaltemp288c1490-df30-472a-8170-dd06728f449alistedeselus2013-2017.csv'
    # Absurdly, Québec has decided "les en-têtes ne comportent pas de caractères accentués ou d'espaces".
    # @todo Waiting for Laval to restore accents and cedillas. (2016-08-01)
    header_converter = lambda self, s: {
        'Prenom': 'first name',
        'Nom': 'last name',
        'Genre': 'gender',
        'Role': 'primary role',
        'ï»¿Nom-du-district': 'district name',
        'Nom-du-parti': 'party name',
        'Adresse-ligne-1': 'address line 1',
        'Adresse-ligne-2': 'address line 2',
        'Localite': 'locality',
        'Province': 'province',
        'Code-postal': 'postal code',
        'Telephone': 'phone',
        'Telecopieur': 'fax',
        'Courriel': 'email',
        "URL-d'une-photo": 'photo url',
        'URL-source': 'source url',
    }.get(s, s)
