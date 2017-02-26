from utils import CSVScraper


class MontrealPersonScraper(CSVScraper):
    # http://donnees.ville.montreal.qc.ca/dataset/listes-des-elus-de-la-ville-de-montreal
    csv_url = 'http://donnees.ville.montreal.qc.ca/dataset/381d74ca-dadd-459f-95c9-db255b5f4480/resource/ce1315a3-50ee-48d0-a0f0-9bcc15f65643/download/listeelusmontreal.csv'
    encoding = 'utf-8'
    locale = 'fr'
    corrections = {
        'primary role': {
            # Normalize to masculine role descriptor.
            'Conseillère de la ville': 'Conseiller de la ville',
            "Mairesse d'arrondissement": "Maire d'arrondissement",
            # Skip this first role (update if second role changes).
            'Chef intérimaire': 'Conseiller de la ville',
        },
        'district name': {
            'De Lorimier': 'DeLorimier',
            'la Côte-de-Liesse': 'Côte-de-Liesse',
            'Loyala': 'Loyola',
            'Mile End': 'Mile-End',
            'Saint-Henri–La Petite-Bourgogne–Pointe-Saint-Charles': 'Saint-Henri—Petite-Bourgogne—Pointe-Saint-Charles',
        },
        'party name': {
            'Indépendante': 'Indépendant',
        }
    }
    fallbacks = {
        'district name': 'arrondissement',
    }

    def header_converter(self, s):
        s = super(MontrealPersonScraper, self).header_converter(s.strip())
        return {
            'rôles': 'primary role',
            'adresse ligne 1 (arrondissement)': 'address line 1',
            'adresse ligne 2 (arrondissement)': 'address line 2',
            'localité (arrondissement)': 'locality',
            'province (arrondissement)': 'province',
            'code postal (arrondissement)': 'postal code',
            'téléphone (arrondissement)': 'phone',
        }.get(s, s)

    def is_valid_row(self, row):
        return row['primary role'] not in ("Conseiller d'arrondissement", "Conseillère d'arrondissement")
