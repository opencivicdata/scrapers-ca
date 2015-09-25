from __future__ import unicode_literals
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

        organization.add_post(role='Maire', label='Mercier')
        for i in range(6):
            organization.add_post(role='Conseiller', label='District {}'.format(i + 1))

        yield organization
