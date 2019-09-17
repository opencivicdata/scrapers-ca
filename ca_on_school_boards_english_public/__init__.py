from utils import CanadianJurisdiction
from opencivicdata.divisions import Division
from pupa.scrape import Organization


class OntarioEnglishPublicSchoolBoards(CanadianJurisdiction):
    classification = 'legislature'  # just to avoid clash
    division_id = 'ocd-division/country:ca/province:on'
    division_name = 'Ontario English Public School Board boundary"'
    name = 'Ontario English Public School Boards'
    url = 'http://www.edu.gov.on.ca/eng/sbinfo/boardList.html'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division in Division.get(self.division_id).children('school_district'):
            organization.add_post(role='Representative', label=division.name, division_id=division.id)

        yield organization
