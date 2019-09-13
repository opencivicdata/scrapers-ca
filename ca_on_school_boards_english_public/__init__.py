from utils import CanadianJurisdiction


class OntarioEnglishPublicSchoolBoards(CanadianJurisdiction):
    classification = 'legislature'  # just to avoid clash
    division_id = 'ca_on_school/en_public'
    division_name = 'Ontario English Public School Board boundary"'
    name = 'Ontario English Public School Boards'
    url = 'http://www.edu.gov.on.ca/eng/sbinfo/boardList.html'
    #skip_null_valid_from = True
    #valid_from = '2019-05-31'

