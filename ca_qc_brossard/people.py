import json
import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

DATA_PAGE = "https://www.brossard.ca/in/rest/public/contentGraphByPath?locale=fr&path=/elus-municipaux&propertyFilter=backup,site"
COUNCIL_PAGE = "https://www.brossard.ca/elus-municipaux"


class BrossardPersonScraper(CanadianScraper):
    def scrape(self):
        def index_by_id(element_list):
            result = {}
            for element in element_list:
                id = element["id"]
                result[id] = element
            return result

        # Gets the ids of all children elements recursively
        def get_children(parent_id, element_dict):
            return_list = []
            element = element_dict[parent_id]
            if element.get("children"):
                for child in element.get("children"):
                    if not re.search(r"^\d+$", child):
                        continue
                    return_list.append(child)
                    if get_children(child, element_dict):
                        return_list.extend(get_children(child, element_dict))
            return return_list

        # The whole page is rendered in javascript and stored as a massive json object
        page = self.get(DATA_PAGE)
        page = json.loads(page.content)
        containers = page["content"].values()
        for container in containers:
            if container.get("contentType") != "CMSPage":
                continue
            elements = index_by_id(container["properties"]["content"]["data"])

        councillors = [
            element
            for element in elements.values()
            if isinstance(element.get("children"), dict)
            and re.search(r"DISTRICT \d+\s+[-|]\sSecteur", element.get("children").get("fr"))
        ]

        assert councillors, "No councillors found"
        for councillor in councillors:
            district = re.search(r"DISTRICT (\d+)", councillor["children"]["fr"]).group(0).title()
            parent_id = councillor["parent"]
            children = get_children(parent_id, elements)
            name = None
            phone = None
            for id in children:
                child = elements[id]
                if child["tag"] == "Link":
                    email = child["props"]["link"]["options"]["url"]["fr"].split(":")[1]
                elif child["tag"] == "Image":
                    photo = "https://www.brossard.ca/in/rest/public/AttachmentThumb?id=" + child["children"]["fr"]
                elif child["tag"] == "TextBox":
                    if not isinstance(child["children"], dict) or "DISTRICT" in child["children"]["fr"]:
                        continue
                    text = re.search(r"(?<=>).+(?=<)", child["children"]["fr"]).group(0)
                    if child["parent"] == parent_id and "Conseill" not in text:
                        name = text.replace("&nbsp;", "")
                    elif not phone:
                        phone_pattern = re.search(r"\d{3} \d{3}-\d{4}(, poste \d{4})?", text)
                        if phone_pattern:
                            phone = phone_pattern.group(0)

            p = Person(primary_org="legislature", name=name, district=district, role="Conseiller", image=photo)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)

            yield p

        for element in elements.values():
            if (
                isinstance(element.get("children"), dict)
                and re.search(r"MAIRE", element.get("children").get("fr"))
                and not element.get("children").get("en")
            ):
                mayor = element
        parent_id = mayor["parent"]
        children = get_children(parent_id, elements)
        name = None
        phone = None
        for id in children:
            child = elements[id]
            if child["tag"] == "Image":
                photo = "https://www.brossard.ca/in/rest/public/AttachmentThumb?id=" + child["children"]["fr"]
            elif child["tag"] == "TextBox":
                if not isinstance(child["children"], dict) or "MAIRE" in child["children"]["fr"]:
                    continue
                text = re.search(r"(?<=>).+(?=<)", child["children"]["fr"]).group(0)
                if child["parent"] == parent_id:
                    name = text.replace("&nbsp;", "")
                elif not phone:
                    phone_pattern = re.search(r"\d{3} \d{3}-\d{4}(, poste \d{4})?", text)
                    if phone_pattern:
                        phone = phone_pattern.group(0)
        p = Person(primary_org="legislature", name=name, district="Brossard", role="Maire", image=photo)
        p.add_contact("voice", phone, "legislature")
        p.add_source(COUNCIL_PAGE)
        yield p
