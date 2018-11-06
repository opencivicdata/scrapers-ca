from utils import CSVScraper


class WellandPersonScraper(CSVScraper):
    # https://niagaraopendata.ca/dataset/city-of-welland-mayor-and-council-members
    csv_url = 'https://niagaraopendata.ca/dataset/b38e2f85-bcd4-43fd-95d5-f513919514d9/resource/590c9110-01f3-4256-8ac1-9c5cbeca88c5/download/city-of-welland-mayor-and-council-members.csv'
    encoding = 'windows-1252'
    many_posts_per_area = True
