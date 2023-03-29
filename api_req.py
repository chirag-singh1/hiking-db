import requests
import sys
import re

ind = 0
count = 0
reg = re.compile('data-href=\".*?\"')

def get_urls():
    global ind

    x = requests.get(f'https://www.hikingproject.com/ajax/area/8011070/trails?idx={ind}')
    urls = reg.findall(x.json()['markup'])
    ind += 1
    return urls

urls = get_urls()
while urls:
    for u in urls:
        print(u[u.find("\"")+1:-1])
    count+= len(urls)
    sys.stderr.write(str(count))
    sys.stderr.write('\n')
    sys.stderr.flush()
    urls = get_urls()