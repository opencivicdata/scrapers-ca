import json
import re

import requests

from utils import CanadianPerson as Person
from utils import CanadianScraper

DATA_PAGE = "https://www.brossard.ca/in/rest/public/contentGraphByPath?locale=fr&path=/elus-municipaux&propertyFilter=backup,site"
COUNCIL_PAGE = "https://www.brossard.ca/elus-municipaux"


class BrossardPersonScraper(CanadianScraper):
    def scrape(self):
        def indexById(elementList):
            result = {}
            for element in elementList:
                id = element["id"]
                result[id] = element
            return result

        # Gets the ids of all children elements recursively
        def getChildren(parentId, elementDict):
            returnList = []
            element = elementDict[parentId]
            if element.get("children"):
                for child in element.get("children"):
                    if not re.search(r"^\d+$", child):
                        continue
                    returnList.append(child)
                    if getChildren(child, elementDict):
                        returnList.extend(getChildren(child, elementDict))
            return returnList

        # The whole page is rendered in javascript and stored as a massive json object
        page = requests.get(DATA_PAGE)
        page = json.loads(page.content)
        containers = page["content"].values()
        for container in containers:
            if container.get("contentType") != "CMSPage":
                continue
            elements = indexById(container["properties"]["content"]["data"])

        councillors = []
        for element in elements.values():
            if isinstance(element.get("children"), dict) and re.search(
                r"DISTRICT \d+\s+[-|]\sSecteur", element.get("children").get("fr")
            ):
                councillors.append(element)

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district = re.search(r"DISTRICT (\d+)", councillor["children"]["fr"]).group(0).title()
            parent_id = councillor["parent"]
            children = getChildren(parent_id, elements)
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
        children = getChildren(parent_id, elements)
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
