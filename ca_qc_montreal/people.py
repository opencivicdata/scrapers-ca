from utils import CSVScraper

BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
)


class MontrealPersonScraper(CSVScraper):
    # http://donnees.ville.montreal.qc.ca/dataset/listes-des-elus-de-la-ville-de-montreal
    csv_url = "https://donnees.montreal.ca/dataset/381d74ca-dadd-459f-95c9-db255b5f4480/resource/211f6903-1440-438a-9f6c-9718ecf2d3ee/download/liste_elus_montreal.csv"
    encoding = "utf-8"
    locale = "fr"
    corrections = {
        "primary role": {
            # Normalize to masculine role descriptor.
            "Conseillère de la ville": "Conseiller de la ville",
            "Conseiller(ère) de la ville": "Conseiller de la ville",
            "Conseiller(ère) de la Ville": "Conseiller de la ville",
            "Mairesse d'arrondissement": "Maire d'arrondissement",
            "Maire(sse) d'arrondissement": "Maire d'arrondissement",
            "Mairesse de la Ville de Montréal": "Maire de la Ville de Montréal",
            "Maire(sse)": "Maire de la Ville de Montréal",
            "Mairesse suppl\u00e9ante d'arrondissement": "Conseiller de la ville",
        },
        "arrondissement": {
            # Articles.
            "Ile-Bizard - Sainte-Genevi\u00e8ve": "L'Île-Bizard—Sainte-Geneviève",
            # Hyphens.
            "Côte-des-Neiges - Notre-Dame-de-Grâce": "Côte-des-Neiges—Notre-Dame-de-Grâce",
            "Mercier - Hochelaga-Maisonneuve": "Mercier—Hochelaga-Maisonneuve",
            "Rivière-des-Prairies - Pointe-aux-Trembles": "Rivière-des-Prairies—Pointe-aux-Trembles",
            "Rosemont-La Petite-Patrie": "Rosemont—La Petite-Patrie",
            "Villeray - Saint-Michel - Parc-Extension": "Villeray—Saint-Michel—Parc-Extension",
            # Name.
            "Ville de Montr\u00e9al": "Montr\u00e9al",
        },
        "district name": {
            "Champlain—L'Île-des-Sœurs": "Champlain—L'Île-des-Soeurs",
            "De Lorimier": "DeLorimier",
            "Saint-Henri-Est–Petite-\nBourgogne–Pointe-Saint-\nCharles–Griffintown": "Saint-Henri—Petite-Bourgogne—Pointe-Saint-Charles",
            "Saint-Paul–Émard– \nSaint-Henri-Ouest": "Saint-Paul—Émard",
            # Hyphens.
            "Maisonneuve-Longue-Pointe": "Maisonneuve—Longue-Pointe",
            "Norman McLaren": "Norman-McLaren",
            "Saint-Léonard Ouest": "Saint-Léonard-Ouest",
            "Saint-Léonard Est": "Saint-Léonard-Est",
        },
        "party name": {
            "Indépendante": "Indépendant",
            "Ind\u00e9pendant(e)": "Indépendant",
        },
        "gender": {
            "Madame": "female",
            "Monsieur": "male",
        },
    }
    fallbacks = {
        "district name": "arrondissement",
    }

    def header_converter(self, s):
        s = super().header_converter(s).strip()
        return {
            # Current column names (2024+ CSV format)
            "fonction élective": "primary role",
            "appellation": "gender",
            "district": "district name",
            "parti": "party name",
            "téléphone": "phone",
            "courriel officiel": "email",
            # Legacy column names (pre-2024)
            "rôles": "primary role",
            "adresse ligne 1 (arrondissement)": "address line 1",
            "adresse ligne 2 (arrondissement)": "address line 2",
            "localité (arrondissement)": "locality",
            "province (arrondissement)": "province",
            "code postal (arrondissement)": "postal code",
            "téléphone (arrondissement)": "phone",
        }.get(s, s)

    def is_valid_row(self, row):
        return row["primary role"] not in (
            "Conseiller d'arrondissement",
            "Conseillère d'arrondissement",
            "Conseiller(\u00e8re) d'arrondissement",
        )

    def scrape(self):
        # donnees.montreal.ca intermittently rejects non-browser user agents.
        self.user_agent = BROWSER_USER_AGENT
        yield from super().scrape()
