import requests
from bs4 import BeautifulSoup
import json
import time
import traceback

STATE_NAME = 'alaska'

infile = open(f'./urls/{STATE_NAME}.txt', 'r')
outfile = open(f'./trails/{STATE_NAME}.txt', 'w')
outfile.write('[\n')
num_url = 0
num_title = 0
num_diff = 0
num_th = 0
num_gpx = 0
num_overview = 0
num_descr = 0
num_ft = 0
num_cond = 0
num_photo = 0
num_rated = 0
num_dist = 0
num_alt = 0
num_dalt = 0
num_grade = 0
st = time.time()
for url in infile.readlines():
    if num_url != 0:
        outfile.write(',\n')
    num_url += 1
    x = requests.get(url.strip())
    soup = BeautifulSoup(x.text, 'html.parser')
    stats = [s.get_text().strip() for s in soup.find(id="trail-stats-bar").findAll('h3')]
    trail = {}
    trail['url'] = url.strip()

    try:
        trail['title'] = soup.find('h1', {"id": "trail-title"}).get_text().strip()
        num_title += 1
    except:
        print('No title')

    try:
        trail['difficulty'] = soup.find('span', {"class": "difficulty-text"}).get_text()
        num_diff += 1
    except:
        print('No difficulty')

    try:
        trail['trailhead'] = soup.find('a', {'data-gtm-id': 'trail-page-driving-directions'})['href']
        num_th += 1
    except:
        print('No trailhead')

    try:
        trail['gpx'] = soup.find('a', string='Download GPX File')['href']
        num_gpx += 1
    except:
        print('No gpx')

    tt = soup.find('div', {'id': 'trail-text'})
    trail['info-text'] = {}
    try:
        trail['info-text']['overview'] = tt.find(lambda t: t.name == 'h3' and 'Overview' in t.text).find_next_siblings()[0].get_text().strip()
        num_overview +=1
    except:
        print('No overview')

    try:
        trail['info-text']['description'] = tt.find(lambda t: t.name == 'h3' and 'Description' in t.text).find_next_siblings()[0].get_text().strip()
        num_descr += 1
    except:
        print('No description')

    try:
        trail['info-text']['features'] = tt.find(lambda t: t.name == 'h3' and 'Features' in t.text).find('span').get_text().strip()
        num_ft += 1
    except:
        print('No features')

    try:
        trail['info-text']['condition'] = soup.find('span', {'class': 'condition'}).get_text().strip()
        num_cond += 1
    except:
        print('No condition')

    try:
        trail['photo'] = soup.find('a', {'class': 'photo-link'})['href']
        num_photo += 1
    except:
        print('No photo')

    try:
        slist = soup.find('span', {'id': 'title-stars'}).get_text().strip().split(' ')
        rating = float(slist[0])
        num_reviewers = int(slist[1][1:-1])
        trail['ratings'] = {
            'rating': rating,
            'num_reviewers': num_reviewers
        }

        num_rated += 1
    except:
        print('No ratings')

    trail['stats'] = {}
    stats = soup.find('div', {'id': 'trail-stats-bar'}).findChildren(recursive=False)
    try:
        dist = float(stats[0].find('span', {'class': 'imperial'}).get_text().strip().split(' ')[0])
        dist_type = stats[0].find_all('h3')[-1].get_text().strip()
        trail['stats']['dist'] = dist
        trail['stats']['dist-type'] = dist_type
        num_dist += 1

    except:
        print('No distance')

    try:
        alt_range = [int(s.get_text().strip().split(' ')[0][:-1].replace(',', '')) for s in stats[1].find_all('span', {'class': 'imperial'})]
        assert len(alt_range) == 2
        trail['stats']['alt-range'] = alt_range

        num_alt += 1
    except:
        print('No altitude range')

    try:
        alt_change = [int(s.get_text().strip().split(' ')[0][:-1].replace(',', '')) for s in stats[2].find_all('span', {'class': 'imperial'})]
        assert len(alt_change) == 2
        trail['stats']['alt-change'] = alt_change

        num_dalt += 1
    except:
        traceback.print_exception()
        print('No altitude change')

    try:
        grade = [float(s.get_text().strip()[:-1]) for s in stats[3].find_all('h3')]
        assert len(grade) == 2
        trail['stats']['avg-grade'] = grade[0]
        trail['stats']['max-grade'] = grade[1]
        num_grade += 1
    except:
        print('No grade')

    outfile.write(json.dumps(trail))

outfile.write('\n]')
infile.close()
outfile.close()

print(f'{num_url} processed in {time.time() - st} seconds')
print('Percent available:')
print(f'Difficulty: {num_diff/num_url}')
print(f'Trailhead: {num_th/num_url}')
print(f'GPX: {num_gpx/num_url}')
print(f'Overview: {num_overview/num_url}')
print(f'Description: {num_descr/num_url}')
print(f'Features: {num_ft/num_url}')
print(f'Condition: {num_cond/num_url}')
print(f'Photo: {num_photo/num_url}')
print(f'Rating: {num_rated/num_url}')
print(f'Distance: {num_dist/num_url}')
print(f'Altitude: {num_alt/num_url}')
print(f'Altitude Change: {num_dalt/num_url}')
print(f'Grade: {num_grade/num_url}')