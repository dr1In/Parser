import requests
from Exceptions import CantGetLinks
from config import WEBSITE_LINK, SEARCH_FOR_A_CLASS, LINKS
from bs4 import BeautifulSoup, Tag

def get_links() -> list:
    coctail_links = list()
    for link in LINKS:
        coctail_links += _find_links(link)
    return coctail_links


def _find_links(link: str) -> list:
    response = _make_response(link)
    return _find_tags(response)


def _make_response(link: str) -> list:
    resp = requests.get(WEBSITE_LINK+'list/cocktail/'+link)
    if resp.status_code != 200:
        raise CantGetLinks
    return resp.text


def _find_tags(text: list) -> list:
    soup = BeautifulSoup(text, 'html.parser')
    tags_list = soup.find_all('a', class_=SEARCH_FOR_A_CLASS)
    return _collect_tags(tags_list)


def _collect_tags(tags: list) -> list:
    links = list()
    for tag in tags:
        links.append(_normalize_tag(tag))
    return links


def _normalize_tag(unfixed_tag: Tag) -> str:
    fixed_tag = _convert_tag(unfixed_tag)
    temp = fixed_tag.removeprefix('<a class="listRecipieTitle" href="/')
    link = temp[:temp.index('"')]
    return link

def _convert_tag(tag: Tag) -> str:
    try:
        fixed_tag = str(tag)
    except ValueError:
        raise CantGetLinks
    return fixed_tag
