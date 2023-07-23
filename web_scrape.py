import requests
from bs4 import BeautifulSoup
import json
import re

def web_scrape(inputs: dict) -> str:
    url = inputs["url"]
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")

    # 1, list of all names
    # 2, dictionary from name to link

    names = []
    name_to_link = {}

    for i, link in enumerate(links):
        if i < 76:
            continue
        if i > 237:
            continue
        name = link.get_text()
        name = re.sub("[\(\[].*?[\)\]]", "", name)
        name = name.replace('®', '')
        name = name.replace('\u00ae', '')
        name = name.replace('©', '')
        name = name.replace('\u00a9', '')
        name = name.strip()
        names += [name]
        name_to_link[name] = link.get("href")
    
    with open('therapy_categories.txt', 'w') as f:
        for name in names:
            f.write(f'{name}\n')
    
    name_to_link_json = json.dumps(name_to_link)
    with open('therapy_categories_to_links.txt', 'w') as f:
        f.write(name_to_link_json)

    return

if __name__ == "__main__":
    web_scrape({"url": "https://www.goodtherapy.org/learn-about-therapy/types"})