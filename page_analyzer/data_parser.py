# import requests
from bs4 import BeautifulSoup


# r = requests.get("http://geoguessr.com/")

# print(r.text)

def get_url_data(data):
    soup = BeautifulSoup(data, "html.parser")

    h1 = soup.find('h1')
    if h1 is not None:
        h1 = h1.get_text()

    title = soup.title.string

    description = soup.find('meta', property="og:description")
    if description is not None:
        description = description.get('content')
    return (h1, title, description)
