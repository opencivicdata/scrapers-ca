from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Mercier(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:2467045'
    division_name = 'Mercier'
    name = 'Conseil municipal de Mercier'
    url = 'http://www.ville.mercier.qc.ca'

    def get_organizations(self):  # @todo Eliminate once shapefile is found and ocd-division-ids is updated.
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Maire', label=self.division_name, division_id=self.division_id)
        for district_number in range(1, 7):
            organization.add_post(role='Conseiller', label='District {}'.format(district_number))

        yield organization
