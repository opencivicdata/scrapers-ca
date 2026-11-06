import re

from utils import CUSTOM_USER_AGENT, CSVScraper


def phone(value):
    # "Tél.  : 514-328-4000\nposte 5573\nCell. : 514-…\nFax  : 514-…"
    match = re.search(r"^Tél\. *: *(\S.*)(?:\n(poste .+))?", value, flags=re.MULTILINE)
    if not match:
        return ""
    return " ".join(group for group in match.groups() if group)


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
            "Le Plateau-Mont-Royal": "Plateau-Mont-Royal",
            "Le Sud-Ouest": "Sud-Ouest",
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
            "Saint-Paul–Émard–\nSaint-Henri-Ouest": "Saint-Paul—Émard",
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
        "phone": phone,
    }
    fallbacks = {
        "district name": "arrondissement",
    }

    def header_converter(self, s):
        s = super().header_converter(s).strip()
        return {
            "appellation": "gender",
            "fonction élective": "primary role",
            "district": "district name",
            "parti": "party name",
            "bureau": "address line 1",
            "courriel officiel": "email",
        }.get(s, s)

    def is_valid_row(self, row):
        # The CSV ends with a "Départs d'élus" section, listing elected officials who left office.
        if row["gender"] == "Départs d'élus":
            self.departures = True
        # The CSV omits this councillor's last name.
        if row["email"] == "maeva.vilain@montreal.ca" and not row["last name"]:
            row["last name"] = "Vilain"
        return (
            not self.departures
            and row["primary role"]  # blank rows
            and row["primary role"]
            not in (
                "Conseiller d'arrondissement",
                "Conseillère d'arrondissement",
                "Conseiller(\u00e8re) d'arrondissement",
            )
        )

    def scrape(self):
        # donnees.montreal.ca returns 403 to the default python-requests user agent.
        self.user_agent = CUSTOM_USER_AGENT
        self.departures = False
        yield from super().scrape()
