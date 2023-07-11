import requests
from bs4 import BeautifulSoup


def get_random_quip():
    """Returns a random quote from toolforge.org's bash.org clone."""
    url_root = "https://bash.toolforge.org"
    html_text = requests.get(url_root + "/random").text
    soup = BeautifulSoup(html_text, "html.parser")
    link = url_root + soup.find("div", class_="quote").find("a")["href"]
    quote = soup.find("div", class_="quote").find("p").text
    return (link, quote)


def post_to_fedi(link, quote):
    """Posts a quote to the fediverse."""
    # TODO: Implement this
    pass


if __name__ == "__main__":
    link, quote = get_random_quip()
    print(link)
    print(quote)
    post_to_fedi(link, quote)
