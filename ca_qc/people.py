import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.assnat.qc.ca/fr/deputes/index.html"

# Waiting for access to https://docs.google.com/spreadsheets/d/1ZV099FpBe1V9hLJNthw5bYyu6LjpC7fcjZUqEVJKhis/edit#gid=1522630662
SOCIAL_MEDIA_DATA = {
    "dufour-pierre-17823": ("https://www.facebook.com/PierreDufourCAQ/", "https://twitter.com/coalitionavenir"),
    "blais-suzanne-17825": ("https://www.facebook.com/SuzanneBlaisCAQ/", "https://twitter.com/SBlaisCAQ"),
    "st-pierre-christine-1235": ("https://www.facebook.com/csp.csp.5", "https://twitter.com/stpierre_ch"),
    "theriault-lise-1355": ("https://www.facebook.com/LiseTheriaultplq/", "https://twitter.com/LiseT_ALR"),
    "grondin-agnes-17827": ("https://www.facebook.com/AgnesGrondinCAQ/", "https://twitter.com/coalitionavenir"),
    "lefebvre-eric-16777": ("https://www.facebook.com/EricLefebvreArth/", "https://twitter.com/EricLefebvreCAQ"),
    "provencal-luc-17829": ("https://www.facebook.com/LucProvencalCAQ/", "https://twitter.com/coalitionavenir"),
    "poulin-samuel-17831": ("https://www.facebook.com/SamuelPoulinBeauce/", "https://twitter.com/poulin_samuel"),
    "reid-claude-17833": ("https://www.facebook.com/ClaudeReidCAQ/", "https://twitter.com/coalitionavenir"),
    "lachance-stephanie-17835": (
        "https://www.facebook.com/Stephanie-Lachance-Coalition-Avenir-Quebec-627820033939204/",
        "https://twitter.com/slachancecaq",
    ),
    "proulx-caroline-17837": ("https://www.facebook.com/pg/CarolineProulxCAQ", "https://twitter.com/caroaubureau"),
    "girault-nadine-17839": ("https://www.facebook.com/NadineGiraultCAQ/", "https://twitter.com/NadineGirault"),
    "laframboise-mario-15357": (
        "https://www.facebook.com/Mario.Laframboise.blainville/",
        "https://twitter.com/LaframboiseMa",
    ),
    "roy-sylvain-12163": ("https://www.facebook.com/SylvainRoyPQ/", "https://twitter.com/Roy_Bonaventure"),
    "jolin-barrette-simon-15359": (
        "https://www.facebook.com/SimonJolinBarrette.Borduas/",
        "https://twitter.com/SJB_CAQ",
    ),
    "robitaille-paule-17841": ("https://www.facebook.com/paule.robitaille.plq", "https://twitter.com/PauleRobitaille"),
    "campeau-richard-17843": ("https://www.facebook.com/RichardCampeauCAQ/", "https://twitter.com/RcampeauCAQ"),
    "charest-isabelle-17845": ("https://www.facebook.com/IsabelleCharestCAQ/", "https://twitter.com/isabellecharest"),
    "roberge-jean-francois-15361": (
        "https://www.facebook.com/roberge.chambly/",
        "https://twitter.com/coalitionavenir",
    ),
    "lebel-sonia-17847": ("https://www.facebook.com/SoniaLeBelCAQ/", "https://twitter.com/slebel19"),
    "levesque-mathieu-17851": ("https://www.facebook.com/MathieuLevesqueCAQ/", "https://twitter.com/mlevesquecaq"),
    "julien-jonatan-17855": ("https://www.facebook.com/jonatanjulien", "https://twitter.com/coalitionavenir"),
    "foster-emilie-17861": ("https://www.facebook.com/EmilieFosterCAQ/", "https://twitter.com/milie_foster"),
    "chasse-mariechantal-17865": (
        "https://www.facebook.com/MarieChantalChasseCAQ/",
        "https://twitter.com/mariechantalcha",
    ),
    "levesque-sylvain-12213": ("https://www.facebook.com/LevesqueS.CAQ/", "https://twitter.com/sylvain_caq"),
    "laforest-andree-17913": ("https://www.facebook.com/AndreeLaforestCAQ/", "https://twitter.com/AndreeLaforest"),
    "ouellette-guy-549": ("https://www.facebook.com/go5129", "https://twitter.com/Guy0uellette"),
    "picard-marc-655": ("https://www.facebook.com/marcpicard01", "https://twitter.com/MarcPicardQc"),
    "proulx-marie-eve-17915": ("https://www.facebook.com/MarieEveProulxCAQ/", "https://twitter.com/marieeveproulx_"),
    "birnbaum-david-15371": ("https://www.facebook.com/birnbaumdarcymcgee/", "https://twitter.com/DavidBirnbaum1"),
    "charette-benoit-195": ("https://www.facebook.com/Charette.DeMo/", "https://twitter.com/CharetteB"),
    "schneeberger-sebastien-5909": (
        "https://www.facebook.com/sebastien.schneeberger",
        "https://twitter.com/Sebastien_DBF",
    ),
    "tremblay-francois-17917": (
        "https://www.facebook.com/FrancoisTremblayCAQ/",
        "https://twitter.com/coalitionavenir",
    ),
    "richard-lorraine-287": ("https://www.facebook.com/LorraineRichardPQ/", "https://twitter.com/LrichardPq"),
    "sauve-monique-16493": ("https://www.facebook.com/Monique.Sauve.fabre/", "https://twitter.com/Monique_Sauve"),
    "bussiere-robert-17921": ("https://www.facebook.com/pg/RobertBussiereCAQ", "https://twitter.com/coalitionavenir"),
    "nadeau-dubois-gabriel-16827": ("https://www.facebook.com/GNadeauDubois/", "https://twitter.com/GNadeauDubois"),
    "bonnardel-francois-11": ("https://www.facebook.com/Bonnardel.coalition/", "https://twitter.com/fbonnardelCAQ"),
    "leduc-alexandre-17935": ("https://www.facebook.com/LeducAlexandreQS/", "https://twitter.com/LeducAlexandre"),
    "gaudreault-maryse-959": ("https://www.facebook.com/maryse.gaudreault.14", "https://twitter.com/MGaudreaultHull"),
    "isabelle-claire-17939": ("https://www.facebook.com/isabelle.coalition/", "https://twitter.com/IsaBelCoalition"),
    "samson-claire-15409": ("https://www.facebook.com/clairesamsoncaq/", "https://twitter.com/clairesamsoncaq"),
    "arseneau-joel-17947": ("https://www.facebook.com/joelarseneauPQ/", "https://twitter.com/joel_arseneau"),
    "kelley-gregory-17951": ("", "https://twitter.com/gharperkelley"),
    "zanetti-sol-17955": ("https://www.facebook.com/sol.zanetti.3", "https://twitter.com/SolZanetti"),
    "proulx-sebastien-5899": ("https://www.facebook.com/SebastienProulxPLQ", "https://twitter.com/SebastienProulx"),
    "rotiroti-filomena-1171": ("https://www.facebook.com/filomena.rotiroti", "https://twitter.com/FiloRotiroti"),
    "lamontagne-andre-15401": ("https://www.facebook.com/andrelamontagnecaq/", "https://twitter.com/andrelamontagn2"),
    "hivon-veronique-27": ("https://www.facebook.com/veroniquehivon/", "https://twitter.com/vhivon"),
    "gaudreault-sylvain-1001": (
        "https://www.facebook.com/sylvain.gaudreault.96",
        "https://twitter.com/SylvainGaudrea2",
    ),
    "legault-francois-4131": (
        "https://www.facebook.com/FrancoisLegaultPageOfficielle/",
        "https://twitter.com/francoislegault",
    ),
    "caire-eric-485": ("https://www.facebook.com/caire.coalition/", "https://twitter.com/ericcaire"),
    "barrette-gaetan-15397": ("https://www.facebook.com/Gaetanbarretteplq/", "https://twitter.com/drgbarrette"),
    "dube-christian-12223": ("https://www.facebook.com/ChristianDubeCAQ/", "https://twitter.com/cdube940"),
    "jeannotte-chantale-17959": (
        "https://www.facebook.com/ChantaleJeannotteCAQ/",
        "https://twitter.com/coalitionavenir",
    ),
    "girard-eric-17957": ("https://www.facebook.com/pg/EricGirardCAQ", "https://twitter.com/EricGirardMFQ"),
    "tanguay-marc-11789": ("https://www.facebook.com/m.tanguay.plq/", "https://twitter.com/marc_tanguay"),
    "menard-nicole-113": ("https://www.facebook.com/Nicole.Menard.deputee", "https://twitter.com/Nicole_Menard"),
    "fontecilla-andres-17953": ("https://www.facebook.com/AFontecillaQS/", "https://twitter.com/AFontecillaQS"),
    "polo-saul-15407": ("https://www.facebook.com/SaulJPolo/", "https://twitter.com/SaulJPolo"),
    "tardif-marie-louise-18071": (
        "https://www.facebook.com/MarieLouiseTardifCAQ/",
        "https://twitter.com/ML_Tardif_LSTM",
    ),
    "lecours-lucie-17949": ("https://www.facebook.com/LucieLecoursCAQ/", "https://twitter.com/coalitionavenir"),
    "paradis-francois-15725": ("https://www.facebook.com/francoisparadis.org/", "https://twitter.com/fparadislevis"),
    "lecours-isabelle-17945": ("https://www.facebook.com/IsabelleLecoursCAQ/", "https://twitter.com/ILecoursCAQ"),
    "guilbault-genevieve-16885": (
        "https://www.facebook.com/GenevieveGuilbaultCAQ/",
        "https://twitter.com/gguilbaultcaq",
    ),
    "david-helene-15379": ("https://www.facebook.com/plq.helenedavid/", "https://twitter.com/David_Hlne"),
    "fournier-catherine-16775": ("https://www.facebook.com/CathFournierQc/", "https://twitter.com/CathFournierQc"),
    "ciccone-enrico-17943": ("https://www.facebook.com/enrico.ciccone.plq/", "https://twitter.com/EnricoCiccone"),
    "allaire-simon-17941": ("https://www.facebook.com/SimonAllaireCAQ/", "https://twitter.com/coalitionavenir"),
    "lemay-mathieu-15403": ("https://www.facebook.com/Lemay.Masson/", "https://twitter.com/mathieu_lemay"),
    "berube-pascal-991": ("https://www.facebook.com/PascalBerubeDepute", "https://twitter.com/PascalBerube"),
    "montpetit-marie-15369": ("https://www.facebook.com/MontpetitMarie/", "https://twitter.com/Marie_Montpetit"),
    "jacques-francois-17937": ("https://www.facebook.com/FrancoisJacquesCAQ/", "https://twitter.com/coalitionavenir"),
    "ghazal-ruba-17933": ("https://www.facebook.com/RubaGhazalQS/", "https://twitter.com/RubaGhazalQS"),
    "charbonneau-francine-635": ("https://www.facebook.com/FCharbonneauMilleIles/", "https://twitter.com/mille_iles"),
    "d-amours-sylvie-15399": ("https://www.facebook.com/sdamoursmira/", "https://twitter.com/SylvieDAmours"),
    "arcand-pierre-421": ("https://www.facebook.com/arcand.pierre/", "https://twitter.com/PierreArcand"),
    "roy-nathalie-12187": ("https://www.facebook.com/nathalie.roy.1023", "https://twitter.com/NathalieRoyCAQ"),
    "simard-jean-francois-5369": (
        "https://www.facebook.com/jeanfrancoissimardcaq/",
        "https://twitter.com/coalitionavenir",
    ),
    "derraji-monsef-17923": ("https://www.facebook.com/derrajimonsef/", "https://twitter.com/monsefderraji"),
    "martel-donald-12165": ("https://www.facebook.com/MartelD.coalition/", "https://twitter.com/domartell"),
    "weil-kathleen-33": ("https://www.facebook.com/KathleenWeilNDG/", "https://twitter.com/Kathleen_Weil"),
    "belanger-gilles-17925": ("https://www.facebook.com/GillesBelangerCAQ/", "https://twitter.com/coalitionavenir"),
    "lacombe-mathieu-17927": ("https://www.facebook.com/MathieuLacombeCAQ/", "https://twitter.com/lacombemathieu"),
    "rouleau-chantal-17931": ("https://www.facebook.com/Chantal.Rouleau.CAQ/", "https://twitter.com/rouleauchantal"),
    "fortin-andre-15383": ("https://www.facebook.com/AvecAndreFortin/", "https://twitter.com/AvecAndreFortin"),
    "caron-vincent-17849": (
        "https://www.facebook.com/Vincent-Caron-1768402003211558/",
        "https://twitter.com/vincentcaroncaq",
    ),
    "blais-marguerite-1263": ("https://www.facebook.com/MargueriteBlaisCAQ/", "https://twitter.com/Marguerite_CAQ"),
    "ouellet-martin-16495": ("https://www.facebook.com/martinouelletpq/", "https://twitter.com/MartinOuellet_"),
    "lavallee-lise-15389": ("https://www.facebook.com/lise.lavallee.repentigny/", "https://twitter.com/LavalleLise"),
    "emond-jean-bernard-17857": ("https://www.facebook.com/jean.bernard.emond.caq/", "https://twitter.com/JBEmond"),
    "bachand-andre-17859": ("https://www.facebook.com/abachandCAQ/", "https://twitter.com/coalitionavenir"),
    "lebel-harold-15479": ("https://www.facebook.com/haroldrimouski/", "https://twitter.com/HLeBelRimouski"),
    "tardif-denis-17863": ("https://www.facebook.com/denistardifcaq/", "https://twitter.com/DenisTardif6"),
    "leitao-carlos-j-15391": ("https://www.facebook.com/carlos.j.leitao.qc/", "https://twitter.com/CarlosJLeitao"),
    "None": ("https://www.facebook.com/phcouillard", "https://twitter.com/phcouillard"),
    "marissal-vincent-17867": ("https://www.facebook.com/vmarissal/?ref=br_rs", "https://twitter.com/vmarissal"),
    "thouin-louis-charles-18073": (
        "https://www.facebook.com/louischarles.thouin",
        "https://twitter.com/coalitionavenir",
    ),
    "lessard-therrien-emilise-17871": ("https://www.facebook.com/ELessardTherrien/", "https://twitter.com/emiliselt"),
    "hebert-genevieve-17877": (
        "https://www.facebook.com/GenevieveHebertCoalitionAvenirQuebec/",
        "https://twitter.com/HebertGenevieve",
    ),
    "anglade-dominique-16499": ("https://www.facebook.com/dominique.anglade.90", "https://twitter.com/DomAnglade"),
    "soucy-chantal-15417": ("https://www.facebook.com/chantal.soucy.52", "https://twitter.com/ChantalSoucy2"),
    "lemieux-louis-17879": ("https://www.facebook.com/LouisLemieuxCAQ/", "https://twitter.com/LouisLemieux"),
    "chassin-youri-17881": ("https://www.facebook.com/YouriChassinCAQ/", "https://twitter.com/yourichassin"),
    "rizqy-marwah-17883": ("https://www.facebook.com/marwahrizqymtl", "https://twitter.com/marwahrizqy"),
    "masse-manon-15421": ("https://www.facebook.com/QS.ManonMasse/", "https://twitter.com/ManonMasse_Qs"),
    "skeete-christopher-17873": ("https://www.facebook.com/CALSainteRose/", "https://twitter.com/cskeete"),
    "mccann-danielle-17887": ("https://www.facebook.com/DanielleMcCannCAQ/", "https://twitter.com/coalitionavenir"),
    "labrie-christine-17889": ("https://www.facebook.com/ChristineLabrieQS/", "https://twitter.com/Christine_QS"),
    "picard-marilyne-17891": ("https://www.facebook.com/MarilynePicardCAQ/", "https://twitter.com/PicardMarilyne"),
    "carmant-lionel-17893": ("https://www.facebook.com/LionelCarmantCAQ/", "https://twitter.com/carmantlionel"),
    "dorion-catherine-17895": ("https://www.facebook.com/dorion", "https://twitter.com/cathdorion"),
    "fitzgibbon-pierre-17897": ("https://www.facebook.com/PierreFitzgibbonCAQ/", "https://twitter.com/fitzgibbonp"),
    "boulet-jean-17899": ("https://www.facebook.com/JeanBouletCAQ/", "https://twitter.com/coalitionavenir"),
    "lamothe-denis-17901": ("https://www.facebook.com/DenisLamotheCAQ/", "https://twitter.com/coalitionavenir"),
    "lafreniere-ian-17903": ("https://www.facebook.com/IanLafreniereCAQ/", "https://twitter.com/IanLafreniere"),
    "asselin-mario-17905": ("https://www.facebook.com/asselin.coalition/", "https://twitter.com/marioasselin"),
    "nichols-marie-claude-15439": (
        "https://www.facebook.com/marieclaudenicholsvaudreuil/",
        "https://twitter.com/nicholsmarieC",
    ),
    "dansereau-suzanne-17907": (
        "https://www.facebook.com/Suzanne-Dansereau-Coalition-Avenir-Quebec-721650337904964/",
        "https://twitter.com/CAQ_Vercheres",
    ),
    "melancon-isabelle-16779": ("https://www.facebook.com/isabelle.melancon.1", "https://twitter.com/Isamelancon"),
    "benjamin-frantz-17909": ("https://www.facebook.com/frantz.benjamin.plq/", "https://twitter.com/franz_benjamin"),
    "rousselle-jean-12167": ("https://www.facebook.com/Jean.Rousselle.Vimont/", "https://twitter.com/RousselleJean"),
    "maccarone-jennifer-17911": ("https://www.facebook.com/jennifer.maccarone1", "https://twitter.com/jmaccarone"),
}


class QuebecPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//*[@id="ListeDeputes"]/tbody/tr')
        headings = {
            "Circonscription": "constituency",
            "Parlement": "legislature",
            "Ministère": "office",
        }

        assert len(members), "No members found"
        for row in members:
            name_comma, division = [cell.text_content() for cell in row[:2]]

            name = " ".join(reversed(name_comma.strip().split(",")))

            division = division.replace("–", "-")  # n-dash, hyphen

            party = row[2].text_content().strip()
            if party == "Indépendante":
                party = "Indépendant"

            email = self.get_email(row[3], error=False)

            detail_url = row[0][0].attrib["href"]
            detail_page = self.lxmlize(detail_url)

            contact_url = detail_url.replace("index.html", "coordonnees.html")
            contact_page = self.lxmlize(contact_url)

            photo_url = detail_page.xpath('//img[@class="photoDepute"]/@src')

            p = Person(primary_org="legislature", name=name, district=division, role="MNA", party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)

            if photo_url:
                p.image = photo_url[0]
            if email:
                p.add_contact("email", email)

            identifier = re.search(r"/([^/]+)/index.html", detail_url).group(1)
            facebook, twitter = SOCIAL_MEDIA_DATA.get(identifier, ("", ""))
            if facebook:
                p.add_link(facebook)
            if twitter:
                p.add_link(twitter)

            for heading, note in headings.items():
                office = contact_page.xpath(f'//h3[contains(., "{heading}")]/parent::div')

                try:
                    phone = self.get_phone(office[0])
                    office_info = contact_page.xpath(
                        f'//h3[contains(., "{heading}")]/parent::div/address[1]/span/text()'
                    )
                    office_items = [item for item in office_info if item.strip()]
                    office_items = list(map(str.strip, office_items))
                    regex = re.compile(r"^Télé.+")  # remove none address items
                    address = [i for i in office_items if not regex.match(i)]
                except Exception:
                    pass  # probably just no phone number present
                else:
                    if phone:
                        p.add_contact("voice", phone, note)
                    if address:
                        p.add_contact("address", "\n".join(address), note)

            en_detail_page = self.lxmlize(detail_url.replace("/fr/", "/en/"))
            # roles = detail_page.xpath(
            #     '//ul/h4[contains(.,"Fonctions actuelles")]/following-sibling::li[preceding-sibling::h4[contains(.,"Fonctions actuelles")] and following-sibling::h4[contains(.,"Fonctions précédentes") or contains(.,"")]]/text()'
            # )
            roles = en_detail_page.xpath(
                '//ul/h4[contains(.,"Current Offices")]/following-sibling::li[preceding-sibling::h4[contains(.,"Current Offices")] and following-sibling::h4[contains(.,"Previous Offices") or contains(.,"")]]/text()'
            )
            if roles:
                # p.extras["roles"] = [role.split("depuis")[0].strip() for role in roles]
                p.extras["roles"] = [role.split("since")[0].strip() for role in roles]

            yield p
