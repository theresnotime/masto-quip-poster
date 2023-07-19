import config
import requests
from bs4 import BeautifulSoup
from mastodon import Mastodon


def get_random_quip():
    """Returns a random quote from toolforge.org's bash.org clone."""
    url_root = "https://bash.toolforge.org"
    html_text = requests.get(url_root + "/random").text
    soup = BeautifulSoup(html_text, "html.parser")
    link = url_root + soup.find("div", class_="quote").find("a")["href"]
    quote = soup.find("div", class_="quote").find("p").text
    return (link, quote)


def post_to_fedi(link: str, quote: str):
    """Posts a quote to the fediverse."""
    status = f"{quote}\n\nvia: {link}"
    if len(status) > config.MAX_QUOTE_LENGTH:
        print(
            f"Status too long ({len(status)} > {config.MAX_QUOTE_LENGTH}). Not posting."
        )
        main()
        return False
    if config.DRY_RUN:
        print(f"[DRY] Would have posted:\n{status}")
        return True
    mastodon = Mastodon(access_token=config.ACCESS_TOKEN, api_base_url=config.API_URL)
    print(f"Posted:\n{status}")
    return mastodon.status_post(status, visibility=config.POST_VISIBILITY)


def main():
    """Do the thing."""
    link, quote = get_random_quip()
    post_to_fedi(link, quote)


if __name__ == "__main__":
    print(f"Max quote length: {config.MAX_QUOTE_LENGTH}")
    if config.DRY_RUN:
        print("Dry run enabled. No posts will be made.")
    main()
