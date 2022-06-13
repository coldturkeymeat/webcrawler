from bs4 import BeautifulSoup


import requests
from time import sleep
from tqdm import tqdm


def get_agreeance_text(ratio):
    if ratio > 3: return "absolutely agrees"
    elif 2 < ratio <= 3: return "strongly agrees"
    elif 1.5 < ratio <= 2: return "agrees"
    elif 1 < ratio <= 1.5: return "somewhat agrees"
    elif ratio == 1: return "neutral"
    elif .67 < ratio < 1 : return "somewhat disagrees"
    elif 0.5 < ratio <= .67: return "disagrees"
    elif 0.33 < ratio <= .5: return "strongly disagrees"
    elif ratio <= 0.33: return "absolutely disagrees"


data = []
url = 'https://www.allsides.com/media-bias/ratings?page='

for i in range(1):

    r = requests.get(url+str(i))
    soup = BeautifulSoup(r.content,'html.parser')
    rows = soup.select('tbody tr')

    for row in rows:
        d = dict()

        d['name'] = row.select_one('.source-title').text.strip()

        d['allsides_page'] = 'https://allsides.com' + row.select_one('.source-title a')['href']

        d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]

        d['agree'] = int(row.select_one('.agree').text)

        d['disagree'] = int(row.select_one('.disagree').text)

        d['ratio'] = d['agree'] / d['disagree']

        d['agreeance_text'] = get_agreeance_text(d['ratio'])

        data.append(d)
    sleep(10)

for d in tqdm(data):
    r = requests.get(d['allsides_page'])
    soup = BeautifulSoup(r.content, 'html.parser')

    try:
        website = soup.select_one('.www')['href']
        d['website'] = website
    except TypeError:
        print('No website for '+d['name'])
        pass
    sleep(10)

for j in data:
    print(j['name'],j['agreeance_text'])
