# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.parl.gc.ca/Parliamentarians/en/members?view=ListAll'


class CanadaPersonScraper(Scraper):
  """
  The CSV at http://www.parl.gc.ca/Parliamentarians/en/members/export?output=CSV
  accessible from http://www.parl.gc.ca/Parliamentarians/en/members has no
  contact information or photo URLs.
  """

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    rows = page.xpath('//div[@class="main-content"]//tr')[1:]
    for row in rows:
      name_cell = row.xpath('./td[1]')[0]
      last_name = name_cell.xpath('string(.//span[1])')
      first_name = name_cell.xpath('string(.//span[2])')
      name = '%s %s' % (first_name, last_name)
      constituency = row.xpath('string(./td[2])')
      province = row.xpath('string(./td[3])')
      party = row.xpath('string(./td[4])')

      url = name_cell.xpath('string(.//a/@href)')
      mp_page = lxmlize(url)
      email = mp_page.xpath('string(//span[@class="caucus"]/'
                            'a[contains(., "@")])')
      photo = mp_page.xpath('string(//div[@class="profile overview header"]//'
                            'img/@src)')

      m = Legislator(name=name, post_id=constituency, role='MP', chamber='lower', party=party)
      m.add_source(COUNCIL_PAGE)
      m.add_source(url)
      twitter = TWITTER.get(name)
      if twitter:
        m.add_link('https://twitter.com/%s' % twitter.get('screen_name'))
      # @see http://www.parl.gc.ca/Parliamentarians/en/members/David-Yurdiga%2886260%29
      if email:
        m.add_contact('email', email, None)
      elif name == 'Adam Vaughan':
        m.add_contact('email', 'Adam.Vaughan@parl.gc.ca', None)
      m.image = photo

      if mp_page.xpath('string(//span[@class="province"][1])') == u'Québec':
        m.add_contact('address', 'Chambre des communes\nOttawa ON  K1A 0A6', 'legislature')
      else:
        m.add_contact('address', 'House of Commons\nOttawa ON  K1A 0A6', 'legislature')
      voice = mp_page.xpath('string(//div[@class="hilloffice"]//span[contains(text(), "Telephone:")])')
      if voice:
        m.add_contact('voice', voice.replace('Telephone: ', ''), 'legislature')
      fax = mp_page.xpath('string(//div[@class="hilloffice"]//span[contains(text(), "Fax:")])').replace('Fax: ', '')
      if fax:
        m.add_contact('fax', fax, 'legislature')

      for li in mp_page.xpath('//div[@class="constituencyoffices"]//li'):
        spans = li.xpath('./span[not(@class="spacer")]')
        m.add_contact('address', '\n'.join([
          spans[0].text_content(), # address line 1
          spans[1].text_content(), # address line 2
          spans[2].text_content(), # city, region
          spans[3].text_content(), # postal code
        ]), 'constituency')
        voice = li.xpath('string(./span[contains(text(), "Telephone:")])').replace('Telephone: ', '')
        if voice:
          m.add_contact('voice', voice, 'constituency')
        fax = li.xpath('string(./span[contains(text(), "Fax:")])').replace('Fax: ', '')
        if fax:
          m.add_contact('fax', fax, 'constituency')

      yield m


# @see https://github.com/opennorth/scrapers-ca-ruby
# It's possible for an MP to change their screen name, and for another person to
# take the old screen name. We track the Twitter ID to detect such seizures.
TWITTER = {
  "Bruce Hyer": {
    "id": 103772503,
    "screen_name": "brucehyer"
  },
  "Gerry Byrne": {
    "id": 110396108,
    "screen_name": "Gerry_Byrne"
  },
  "Wladyslaw Lizon": {
    "id": 1137765446,
    "screen_name": "MPWLizon"
  },
  "Sana Hassainia": {
    "id": 119932406,
    "screen_name": "SanaNPD"
  },
  "Tony Clement": {
    "id": 121483664,
    "screen_name": "TonyclementCPC"
  },
  "Laurie Hawn": {
    "id": 121858468,
    "screen_name": "MPLaurieHawn"
  },
  "Dean Del Mastro": {
    "id": 124478275,
    "screen_name": "mpdeandelmastro"
  },
  "Joyce Bateman": {
    "id": 1278988074,
    "screen_name": "JoyceBatemanMP"
  },
  "Kerry-Lynne D. Findlay": {
    "id": 1283934079,
    "screen_name": "KerryLynneFindl"
  },
  "Mike Lake": {
    "id": 129395750,
    "screen_name": "MikeLakeMP"
  },
  "Rob Nicholson": {
    "id": 1340289319,
    "screen_name": "HonRobNicholson"
  },
  "Jean Rousseau": {
    "id": 1362037146,
    "screen_name": "JeanRousseauNPD"
  },
  "Dany Morin": {
    "id": 137444494,
    "screen_name": "drdanymorin"
  },
  "Gary Schellenberger": {
    "id": 80160605,
    "screen_name": "GSchellenberger"
  },
  "Judy Sgro": {
    "id": 1390883714,
    "screen_name": "JudySgroMP"
  },
  "Jay Aspin": {
    "id": 139407582,
    "screen_name": "JayAspinMP"
  },
  "Justin Trudeau": {
    "id": 14260960,
    "screen_name": "JustinTrudeau"
  },
  "Gerald Keddy": {
    "id": 143460822,
    "screen_name": "GeraldKeddy"
  },
  "K. Kellie Leitch": {
    "id": 1449023288,
    "screen_name": "KellieLeitch"
  },
  "Peter Kent": {
    "id": 1449320024,
    "screen_name": "KentThornhillMP"
  },
  "Michelle Rempel": {
    "id": 14538949,
    "screen_name": "MichelleRempel"
  },
  "Mike Sullivan": {
    "id": 15205787,
    "screen_name": "MikeSullivanMP"
  },
  "Blaine Calkins": {
    "id": 156288226,
    "screen_name": "blainecalkinsmp"
  },
  "Bryan Hayes": {
    "id": 1580429754,
    "screen_name": "BryanHayesMP"
  },
  "Joyce Murray": {
    "id": 16180205,
    "screen_name": "joycemurray"
  },
  "Don Davies": {
    "id": 16189107,
    "screen_name": "DonDavies"
  },
  "Elizabeth May": {
    "id": 16220555,
    "screen_name": "ElizabethMay"
  },
  "Dan Albas": {
    "id": 16278177,
    "screen_name": "DanAlbas"
  },
  "Nathan Cullen": {
    "id": 16307818,
    "screen_name": "nathancullen"
  },
  "Shelly Glover": {
    "id": 1638538464,
    "screen_name": "ShellyGloverMIN"
  },
  "Larry Maguire": {
    "id": 1686740173,
    "screen_name": "LarryMaguireMP"
  },
  "Mark Adler": {
    "id": 169227763,
    "screen_name": "MarkAdlerMP"
  },
  "Scott Simms": {
    "id": 171977015,
    "screen_name": "Scott_Simms"
  },
  "Ed Holder": {
    "id": 172786343,
    "screen_name": "EdHolder_MP"
  },
  "Paul Dewar": {
    "id": 17314758,
    "screen_name": "PaulDewar"
  },
  "Steven Fletcher": {
    "id": 17485622,
    "screen_name": "stevenjfletcher"
  },
  "Bob Zimmer": {
    "id": 176207343,
    "screen_name": "bobzimmermp"
  },
  "Ben Lobb": {
    "id": 1851503720,
    "screen_name": "BenLobbMP"
  },
  "Mylène Freeman": {
    "id": 18585980,
    "screen_name": "MyleneFreeman"
  },
  "Niki Ashton": {
    "id": 18654401,
    "screen_name": "nikiashton"
  },
  "Mathieu Ravignat": {
    "id": 1872363637,
    "screen_name": "MRavignat"
  },
  "Ralph Goodale": {
    "id": 188359178,
    "screen_name": "RalphGoodale"
  },
  "Nina Grewal": {
    "id": 191898945,
    "screen_name": "MPNinaGrewal"
  },
  "Scott Armstrong": {
    "id": 195112832,
    "screen_name": "Armstrong_MP"
  },
  "Peter Julian": {
    "id": 19557595,
    "screen_name": "MPJulian"
  },
  "Tim Uppal": {
    "id": 195820437,
    "screen_name": "MinTimUppal"
  },
  "Rosane Doré Lefebvre": {
    "id": 196159502,
    "screen_name": "RosaneDL"
  },
  "Alexandre Boulerice": {
    "id": 196717787,
    "screen_name": "alexboulerice"
  },
  "Brian Masse": {
    "id": 19750015,
    "screen_name": "BrianMasseMP"
  },
  "Laurin Liu": {
    "id": 19881863,
    "screen_name": "laurinliu"
  },
  "Francis Scarpaleggia": {
    "id": 200100603,
    "screen_name": "ScarpaleggiaMP"
  },
  "Julian Fantino": {
    "id": 201394249,
    "screen_name": "JulianFantino"
  },
  "Peter Braid": {
    "id": 20159038,
    "screen_name": "peterbraid"
  },
  "Paulina Ayala": {
    "id": 204796709,
    "screen_name": "paulinaayalaNPD"
  },
  "Devinder Shory": {
    "id": 205448899,
    "screen_name": "NortheastShory"
  },
  "James Lunney": {
    "id": 206307515,
    "screen_name": "jameslunneymp"
  },
  "Kevin Lamoureux": {
    "id": 208750527,
    "screen_name": "Kevin_Lamoureux"
  },
  "Joe Preston": {
    "id": 21123463,
    "screen_name": "Joe_Preston"
  },
  "LaVar Payne": {
    "id": 211948412,
    "screen_name": "LaVarMP"
  },
  "David Anderson": {
    "id": 212295349,
    "screen_name": "DavidAndersonSK"
  },
  "Jason Kenney": {
    "id": 21525682,
    "screen_name": "kenneyjason"
  },
  "Stéphane Dion": {
    "id": 2153005170,
    "screen_name": "HonStephaneDion"
  },
  "Charlie Angus": {
    "id": 215632349,
    "screen_name": "CharlieAngusMP"
  },
  "Glenn Thibeault": {
    "id": 21594028,
    "screen_name": "GlennThibeault"
  },
  "Bal Gosal": {
    "id": 218677733,
    "screen_name": "BalGosal"
  },
  "Parm Gill": {
    "id": 22244391,
    "screen_name": "ParmGill"
  },
  "Andrew Saxton": {
    "id": 226344619,
    "screen_name": "AndrewSaxton1"
  },
  "Pierre-Luc Dusseault": {
    "id": 22785676,
    "screen_name": "PLDusseault"
  },
  "John Duncan": {
    "id": 2303650022,
    "screen_name": "JohnDuncanMP"
  },
  "Ray Boughen": {
    "id": 2305372206,
    "screen_name": "RayBoughenMP"
  },
  "André Bellavance": {
    "id": 2328085010,
    "screen_name": "AndreBellavance"
  },
  "John McCallum": {
    "id": 233561717,
    "screen_name": "JohnMcCallumMP"
  },
  "John Rafferty": {
    "id": 23604951,
    "screen_name": "JohnRaffertyMP"
  },
  "Rob Moore": {
    "id": 237281828,
    "screen_name": "RobMoore_CPC"
  },
  "Robert Chisholm": {
    "id": 239388939,
    "screen_name": "RobertNDP"
  },
  "Greg Rickford": {
    "id": 2413537274,
    "screen_name": "HonGregRickford"
  },
  "Blake Richards": {
    "id": 24171225,
    "screen_name": "BlakeRichardsMP"
  },
  "Pierre Poilievre": {
    "id": 242827267,
    "screen_name": "PierrePoilievre"
  },
  "Jean Crowder": {
    "id": 243690594,
    "screen_name": "JeanCrowder"
  },
  "Dean Allison": {
    "id": 243709627,
    "screen_name": "DeanAllisonMP"
  },
  "James Rajotte": {
    "id": 243847328,
    "screen_name": "JamesRajotte"
  },
  "Ted Opitz": {
    "id": 24403218,
    "screen_name": "TedOpitz"
  },
  "Jinny Jogindera Sims": {
    "id": 244196762,
    "screen_name": "jinnysims"
  },
  "Paul Calandra": {
    "id": 24474900,
    "screen_name": "PaulCalandra"
  },
  "Malcolm Allen": {
    "id": 245039169,
    "screen_name": "Malcolm_AllenMP"
  },
  "John McKay": {
    "id": 245954929,
    "screen_name": "JohnMcKayLib"
  },
  "Mike Allen": {
    "id": 246455540,
    "screen_name": "mpmikea"
  },
  "Judy Foote": {
    "id": 2471250308,
    "screen_name": "JudyFooteMP"
  },
  "Brent Rathgeber": {
    "id": 24738102,
    "screen_name": "brentrathgeber"
  },
  "Royal Galipeau": {
    "id": 24757140,
    "screen_name": "GalipeauOrleans"
  },
  "Brad Butt": {
    "id": 251116380,
    "screen_name": "BradButtMP"
  },
  "Hedy Fry": {
    "id": 25127782,
    "screen_name": "HedyFry"
  },
  "Larry Miller": {
    "id": 2516160571,
    "screen_name": "LarryMillerMP"
  },
  "Frank Valeriote": {
    "id": 254152481,
    "screen_name": "FrankValeriote"
  },
  "Greg Kerr": {
    "id": 256099374,
    "screen_name": "MPGregKerr"
  },
  "Andrew Scheer": {
    "id": 256360738,
    "screen_name": "andrewscheer"
  },
  "Sean Casey": {
    "id": 256775505,
    "screen_name": "SeanCaseyMP"
  },
  "Claude Gravelle": {
    "id": 2579033064,
    "screen_name": "ClaudeGravelle"
  },
  "Lynne Yelich": {
    "id": 259329872,
    "screen_name": "Lynne_Yelich"
  },
  "Ryan Cleary": {
    "id": 261913059,
    "screen_name": "ClearyNDP"
  },
  "Barry Devolin": {
    "id": 262352090,
    "screen_name": "BarryDevolin_MP"
  },
  "Chris Charlton": {
    "id": 26279847,
    "screen_name": "ChrisCharltonMP"
  },
  "Libby Davies": {
    "id": 26282371,
    "screen_name": "LibbyDavies"
  },
  "Rodger Cuzner": {
    "id": 266635199,
    "screen_name": "RodgerCuzner"
  },
  "Randall Garrison": {
    "id": 266855812,
    "screen_name": "r_garrison"
  },
  "Gary Goodyear": {
    "id": 266908514,
    "screen_name": "GaryGoodyearMP"
  },
  "Rick Norlock": {
    "id": 267390627,
    "screen_name": "RickNorlock"
  },
  "Rodney Weston": {
    "id": 267588644,
    "screen_name": "rodneywestonsj"
  },
  "Christian Paradis": {
    "id": 269187135,
    "screen_name": "christianparad"
  },
  "John Weston": {
    "id": 270637108,
    "screen_name": "JohnWestonMP"
  },
  "Hélène Laverdière": {
    "id": 270938299,
    "screen_name": "HLaverdiereNPD"
  },
  "Kirsty Duncan": {
    "id": 271073165,
    "screen_name": "KirstyDuncanMP"
  },
  "Chungsen Leung": {
    "id": 271222307,
    "screen_name": "csleungmp"
  },
  "Bev Shipley": {
    "id": 271505228,
    "screen_name": "BevShipleyMP"
  },
  "Nycole Turmel": {
    "id": 271745470,
    "screen_name": "nycole_turmel"
  },
  "Phil McColeman": {
    "id": 271959297,
    "screen_name": "Phil4Brant"
  },
  "Ron Cannan": {
    "id": 272056371,
    "screen_name": "RonCannan"
  },
  "John Baird": {
    "id": 272172091,
    "screen_name": "HonJohnBaird"
  },
  "Bruce Stanton": {
    "id": 272183541,
    "screen_name": "bruce_stanton"
  },
  "Anne-Marie Day": {
    "id": 272234584,
    "screen_name": "AnneMarieDay"
  },
  "Robert Aubin": {
    "id": 272436944,
    "screen_name": "RobertAubinNPD"
  },
  "Earl Dreeshen": {
    "id": 272617171,
    "screen_name": "earl_dreeshen"
  },
  "Dave Van Kesteren": {
    "id": 2726686742,
    "screen_name": "DVK_MP"
  },
  "David McGuinty": {
    "id": 272903688,
    "screen_name": "DavidMcGuinty"
  },
  "Terence Young": {
    "id": 273067760,
    "screen_name": "TerenceYoungMP"
  },
  "Bernard Valcourt": {
    "id": 273203853,
    "screen_name": "Min_BValcourt"
  },
  "François Pilon": {
    "id": 273654460,
    "screen_name": "francoispilon"
  },
  "Gail Shea": {
    "id": 274190395,
    "screen_name": "CPCGailShea"
  },
  "Jack Harris": {
    "id": 274231222,
    "screen_name": "JackHarrisNDP"
  },
  "François Lapointe": {
    "id": 274305156,
    "screen_name": "F_Lapointe"
  },
  "Deepak Obhrai": {
    "id": 274328258,
    "screen_name": "deepakobhrai"
  },
  "Randy Kamp": {
    "id": 274722044,
    "screen_name": "RandyKamp_com"
  },
  "Mark Strahl": {
    "id": 274831602,
    "screen_name": "markstrahl"
  },
  "Matthew Kellway": {
    "id": 275026205,
    "screen_name": "MatthewKellway"
  },
  "Françoise Boivin": {
    "id": 275185537,
    "screen_name": "FBoivinNPD"
  },
  "Sylvain Chicoine": {
    "id": 275313660,
    "screen_name": "sylvainchicoine"
  },
  "Pierre Nantel": {
    "id": 275600932,
    "screen_name": "pierrenantel"
  },
  "Brad Trost": {
    "id": 275821378,
    "screen_name": "BradTrostCPC"
  },
  "Harold Albrecht": {
    "id": 276234003,
    "screen_name": "Albrecht4KitCon"
  },
  "Jamie Nicholls": {
    "id": 276595482,
    "screen_name": "JPNichollsNPD"
  },
  "Dennis Bevington": {
    "id": 276657926,
    "screen_name": "nwtdennis"
  },
  "Raymond Côté": {
    "id": 276718773,
    "screen_name": "RCoteNPD"
  },
  "Rona Ambrose": {
    "id": 277155475,
    "screen_name": "MinRonaAmbrose"
  },
  "Kennedy Stewart": {
    "id": 27823555,
    "screen_name": "kennedystewart"
  },
  "Brian Storseth": {
    "id": 279137282,
    "screen_name": "BrianStorseth"
  },
  "Keith Ashfield": {
    "id": 279208924,
    "screen_name": "KeithAshfield11"
  },
  "Peter MacKay": {
    "id": 280523158,
    "screen_name": "MacKayCPC"
  },
  "Dan Harris": {
    "id": 280831905,
    "screen_name": "danharrisndp"
  },
  "Scott Reid": {
    "id": 283179858,
    "screen_name": "ScottReidCPC"
  },
  "Eve Adams": {
    "id": 284725852,
    "screen_name": "MPEveAdams"
  },
  "Marjolaine Boutin-Sweet": {
    "id": 286229457,
    "screen_name": "MarjBoutinSweet"
  },
  "Kelly Block": {
    "id": 28804785,
    "screen_name": "KellyBlockcpc"
  },
  "Matthew Dubé": {
    "id": 288970758,
    "screen_name": "MattDube"
  },
  "Rod Bruinooge": {
    "id": 28922499,
    "screen_name": "rodbruinooge"
  },
  "Russ Hiebert": {
    "id": 292067263,
    "screen_name": "HiebertRuss"
  },
  "Erin O'Toole": {
    "id": 296553576,
    "screen_name": "Erin_M_OToole"
  },
  "Charmaine Borg": {
    "id": 299816095,
    "screen_name": "mpcharmaineborg"
  },
  "Guy Caron": {
    "id": 304991157,
    "screen_name": "GuyCaronNPD"
  },
  "Ruth Ellen Brosseau": {
    "id": 305695167,
    "screen_name": "RE_Brosseau"
  },
  "Lois Brown": {
    "id": 30775031,
    "screen_name": "MPLoisBrown"
  },
  "Jonathan Tremblay": {
    "id": 313297696,
    "screen_name": "JTremblayNPD"
  },
  "Jonathan Genest-Jourdain": {
    "id": 321663386,
    "screen_name": "GenestJourdain"
  },
  "Kyle Seeback": {
    "id": 32444591,
    "screen_name": "KyleSeeback"
  },
  "Isabelle Morin": {
    "id": 325555085,
    "screen_name": "IsabelleMorinMP"
  },
  "Anne Minh-Thu Quach": {
    "id": 327038655,
    "screen_name": "AnneMTQuach"
  },
  "Tarik Brahmi": {
    "id": 330995093,
    "screen_name": "TarikBrahmi"
  },
  "Romeo Saganash": {
    "id": 334802268,
    "screen_name": "RomeoSaganash"
  },
  "Hélène LeBlanc": {
    "id": 335497387,
    "screen_name": "HeleneLeBlanc"
  },
  "Manon Perreault": {
    "id": 335953858,
    "screen_name": "MPerreaultNPD"
  },
  "Lawrence Toet": {
    "id": 339692762,
    "screen_name": "lawrencetoetMP"
  },
  "Djaouida Sellah": {
    "id": 340381029,
    "screen_name": "DSellahNPD"
  },
  "James Moore": {
    "id": 34041396,
    "screen_name": "JamesMoore_org"
  },
  "Randy Hoback": {
    "id": 35018890,
    "screen_name": "MPRandyHoback"
  },
  "Tyrone Benskin": {
    "id": 356378265,
    "screen_name": "tbenskin"
  },
  "Leona Aglukkaq": {
    "id": 35764984,
    "screen_name": "leonaaglukkaq"
  },
  "Rick Dykstra": {
    "id": 35781335,
    "screen_name": "RickDykstra"
  },
  "Patrick Brown": {
    "id": 35826823,
    "screen_name": "brownbarrie"
  },
  "Claude Patry": {
    "id": 363697539,
    "screen_name": "claude_patry"
  },
  "Thomas Mulcair": {
    "id": 363997684,
    "screen_name": "ThomasMulcair"
  },
  "Alexandrine Latendresse": {
    "id": 369088384,
    "screen_name": "ALatendresseNPD"
  },
  "Mark Eyking": {
    "id": 378207083,
    "screen_name": "MarkEyking_MP"
  },
  "Marie-Claude Morin": {
    "id": 382790334,
    "screen_name": "MC_Morin_NPD"
  },
  "Costas Menegakis": {
    "id": 398241429,
    "screen_name": "CostasMenegakis"
  },
  "Carolyn Bennett": {
    "id": 40550119,
    "screen_name": "Carolyn_Bennett"
  },
  "Annick Papillon": {
    "id": 407261547,
    "screen_name": "AnnickPapillon"
  },
  "Joy Smith": {
    "id": 413423918,
    "screen_name": "MPJoySmith"
  },
  "Pierre Dionne Labelle": {
    "id": 421336331,
    "screen_name": "DionneLabelleMP"
  },
  "David Wilks": {
    "id": 42164584,
    "screen_name": "DavidJohnWilks"
  },
  "Craig Scott": {
    "id": 434271579,
    "screen_name": "CraigScottNDP"
  },
  "Cheryl Gallant": {
    "id": 43545966,
    "screen_name": "cherylgallant"
  },
  "James Bezan": {
    "id": 44718864,
    "screen_name": "jamesbezan"
  },
  "Joe Oliver": {
    "id": 45631939,
    "screen_name": "joeoliver1"
  },
  "Joan Crockatt": {
    "id": 45637133,
    "screen_name": "Crockatteer"
  },
  "Chris Warkentin": {
    "id": 45923631,
    "screen_name": "chriswarkentin"
  },
  "François Choquette": {
    "id": 464871646,
    "screen_name": "F_Choquette"
  },
  "Megan Leslie": {
    "id": 46710447,
    "screen_name": "MeganLeslieMP"
  },
  "Jacques Gourde": {
    "id": 47135309,
    "screen_name": "JacquesGourde"
  },
  "Pierre Jacob": {
    "id": 472064608,
    "screen_name": "PJacobNPD"
  },
  "Diane Ablonczy": {
    "id": 47964234,
    "screen_name": "DianeAblonczy"
  },
  "Rob Merrifield": {
    "id": 487553158,
    "screen_name": "RobMerrifieldMP"
  },
  "Jasbir Sandhu": {
    "id": 52447427,
    "screen_name": "jasbirsandhu"
  },
  "Ève Péclet": {
    "id": 529665584,
    "screen_name": "evepeclet"
  },
  "Joe Comartin": {
    "id": 54572255,
    "screen_name": "joecomartin"
  },
  "Fin Donnelly": {
    "id": 54962166,
    "screen_name": "FinDonnelly"
  },
  "Lisa Raitt": {
    "id": 55687338,
    "screen_name": "lraitt"
  },
  "Jean-François Fortin": {
    "id": 56132313,
    "screen_name": "fortjf"
  },
  "Peter Goldring": {
    "id": 56415147,
    "screen_name": "PeterGoldring"
  },
  "Corneliu Chisu": {
    "id": 57309123,
    "screen_name": "cchisu"
  },
  "Ted Hsu": {
    "id": 59084035,
    "screen_name": "tedhsu"
  },
  "Carol Hughes": {
    "id": 60916234,
    "screen_name": "CarolHughesMP"
  },
  "Christine Moore": {
    "id": 620605132,
    "screen_name": "MooreNpd"
  },
  "Linda Duncan": {
    "id": 62909691,
    "screen_name": "LindaDuncanMP"
  },
  "Colin Carrie": {
    "id": 63210367,
    "screen_name": "ColinCarrie"
  },
  "Wayne Easter": {
    "id": 65624152,
    "screen_name": "WayneEaster"
  },
  "David Sweet": {
    "id": 68452445,
    "screen_name": "DavidSweetMP"
  },
  "Cathy McLeod": {
    "id": 68995519,
    "screen_name": "Cathy_McLeod"
  },
  "Daryl Kramp": {
    "id": 69050763,
    "screen_name": "darylkramp"
  },
  "Hoang Mai": {
    "id": 69671596,
    "screen_name": "hoangmai_npd"
  },
  "Rob Clarke": {
    "id": 71001729,
    "screen_name": "Rob_Clarke_MP"
  },
  "Susan Truppe": {
    "id": 72652039,
    "screen_name": "SusanTruppe"
  },
  "Irene Mathyssen": {
    "id": 72663989,
    "screen_name": "irenemathyssen"
  },
  "Stephen Harper": {
    "id": 7401202,
    "screen_name": "pmharper"
  },
  "Mike Wallace": {
    "id": 74208784,
    "screen_name": "MikeWallaceMP"
  },
  "Stephen Woodworth": {
    "id": 75229026,
    "screen_name": "WoodworthMP"
  },
  "Bernard Trottier": {
    "id": 75443458,
    "screen_name": "btrottier"
  },
  "Steven Blaney": {
    "id": 75459502,
    "screen_name": "MinStevenBlaney"
  },
  "Scott Andrews": {
    "id": 75928120,
    "screen_name": "ScottAndrewsMP"
  },
  "John Carmichael": {
    "id": 76068728,
    "screen_name": "JohnBCarmichael"
  },
  "Geoff Regan": {
    "id": 76143039,
    "screen_name": "geoffregan"
  },
  "David Tilson": {
    "id": 76233932,
    "screen_name": "davidtilson"
  },
  "Scott Brison": {
    "id": 76710096,
    "screen_name": "scottbrison"
  },
  "Jean-François Larose": {
    "id": 76738942,
    "screen_name": "jflarose"
  },
  "Chris Alexander": {
    "id": 76918775,
    "screen_name": "calxandr"
  },
  "Andrew Cash": {
    "id": 77298060,
    "screen_name": "Cash4TO"
  },
  "Denis Blanchette": {
    "id": 77374359,
    "screen_name": "DenisBlanchette"
  },
  "Murray Rankin": {
    "id": 796675838,
    "screen_name": "MurrayRankin"
  },
  "Wai Young": {
    "id": 80475670,
    "screen_name": "WaiYoung"
  },
  "Marc Garneau": {
    "id": 80702644,
    "screen_name": "MarcGarneau"
  },
  "Candice Bergen": {
    "id": 833988769,
    "screen_name": "CandiceBergenMP"
  },
  "Jim Hillyer": {
    "id": 843843476,
    "screen_name": "JimHillyerMP"
  },
  "Dave MacKenzie": {
    "id": 897770628,
    "screen_name": "DaveMacKenzieMP"
  },
  "Peggy Nash": {
    "id": 92091739,
    "screen_name": "PeggyNashNDP"
  },
  "Rathika Sitsabaiesan": {
    "id": 92651574,
    "screen_name": "RathikaS"
  },
  "Mark Warawa": {
    "id": 99334624,
    "screen_name": "MPmarkwarawa"
  }
}
