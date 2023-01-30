from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianJurisdiction


class OntarioEnglishPublicSchoolBoards(CanadianJurisdiction):
    classification = "school"  # just to avoid clash
    division_id = "ocd-division/country:ca/province:on"
    division_name = 'Ontario English Public School Board boundary"'
    name = "Ontario English Public School Boards"
    url = "http://www.edu.gov.on.ca/eng/sbinfo/boardList.html"

    def get_organizations(self):
        organization = Organization(self.name, classification="committee")
        organization.add_source(self.url)

        for division in Division.get(self.division_id).children("school_district"):
            organization.add_post(role="Chair", label=division.name, division_id=division.id)
            for i in range(0, 22):  # XXX made-up number
                organization.add_post(
                    role="Trustee", label="{} (seat {})".format(division.name, i), division_id=division.id
                )

        yield organization
