from utils import CanadianJurisdiction


# The municipal association lists only top-level officials.
# @see http://afmnb.org/municipalite_membre.cfm?id=12
class NewBrunswick(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:nb/legislature'

  def _get_metadata(self):
    return {
      'name': 'New Brunswick',
      'legislature_name': 'New Brunswick City Council',
      'legislature_url': 'http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html',
    }
