from utils import CSVScraper


class LavalPersonScraper(CSVScraper):
    # https://www.donneesquebec.ca/recherche/fr/dataset/liste-des-elus
    csv_url = "https://www.donneesquebec.ca/recherche/fr/dataset/8fe69713-fade-4751-a0b4-7e57a81886b1/resource/bb38e19e-26ab-495c-a0f7-ed6b3268b6e6/download/liste-elus.csv"
    encoding = "utf-8-sig"
    locale = "fr"
    # Laval also removes accents and cedillas from data.
    corrections = {
        "district name": {
            "Concorde - Bois-de-Boulogne": "Concorde-Bois-de-Boulogne",
            "L'Abord-a-Plouffe": "Abord-à-Plouffe",
            "L'Oree-des-bois": "L'Orée-des-Bois",
            "Laval-les-Iles": "Laval-les-Îles",
            "Marc-Aurele-Fortin": "Marc-Aurèle-Fortin",
            "Saint-Francois": "Saint-François",
            "Sainte-Dorothee": "Sainte-Dorothée",
        },
        "photo url": {
            " ": None,
        },
    }

    # Absurdly, Laval has decided "les en-têtes ne comportent pas de
    # caractères accentués ou d'espaces" and includes a byte order mark.
    def header_converter(self, s):
        s = super().header_converter(s.replace("-", " "))
        return {
            "role": "primary role",
            "prenom": "first name",
            "localite": "locality",
            "telephone": "phone",
            "telecopieur": "fax",
            "url photo": "photo url",
        }.get(s, s)

    def is_valid_row(self, row):
        return row["année de à"] == "2017-2021"
