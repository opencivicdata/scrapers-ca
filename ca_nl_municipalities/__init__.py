from utils import CanadianJurisdiction


# The municipal association lists only top-level officials.
# @see http://www.municipalnl.ca/?Content=Contact/Municipal_Directory
class NewfoundlandAndLabrador(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/todo'
  division_name = 'Newfoundland Labrador'
  name = 'Newfoundland Labrador Municipal Council'
  url = 'http://www.ma.gov.nl.ca/ma/municipal_directory/index.html'
