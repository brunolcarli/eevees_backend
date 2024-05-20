import requests
from bs4 import BeautifulSoup


def read_paste_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Error requesting pokepaste at ', url)
    return r.text


def get_team(html):
    """"
    Extract pokemon names from a team hosted in pokepaste
    Return <dict>
    """
    soup = BeautifulSoup(html, 'html.parser')
    pre = soup.findAll('pre')
    t = {}
    n = 1
    for i in pre:
        raw = i.text.split('\n')[0].strip()
        hidden_start = raw.find('(')
        hidden_end = raw.find(')')
        if (hidden_start + hidden_end) == -2:
            raw = raw
        if (hidden_end - hidden_start) == 2:
            raw = raw.split('(')[0].strip()
        if (hidden_end - hidden_start) > 2:
            raw = raw[hidden_start+1:hidden_end]
        if '@' in raw:
            raw = raw.split('@')[0].strip()
        t[f'poke{n}'] = raw
        n += 1
        
    return t
