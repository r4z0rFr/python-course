import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import copy

from nltk.tokenize import word_tokenize

import pprint


class Site(object):
    """dans site: mot clef, urls interne, url externe, nom de domaine, document_matrix"""

    def __init__(self, url):
        self.root_url = urlparse(url).netloc
        self.entry_point = url
        self.site_url = urlparse(url).scheme + "://" + self.root_url
        self.home_page = self.factory_page(url)

    # une factory method
    def factory_page(self, page_url):
        return Page(page_url, self.root_url, self.site_url)

    def scrap_site(self):
        print(" =================>{}<====================".format(self.site_url))
        self.home_page.get_links()
        pile = self.home_page.internal_links.copy()
        parsed = self.home_page.internal_links.copy()

        while pile != []:
            print("taille de la pile", len(pile), "taille de la liste", len(parsed))
            a = self.factory_page(pile[0])

            a.get_links()

            if a.code == 200:
                new_links = set(a.internal_links) - set(parsed)
                pile.extend(new_links)
                parsed.extend(new_links)

            pile.pop(0)


class Page(object):
    """dans page: url, page_parent, nom de domaine, urls internes, url externes, mot_clef,"""

    def __init__(self, url, root_url, site_url):
        self.url = url
        self.site_url = site_url
        self.root_url = root_url
        # print("scraping:{} ".format(self.url))
        self.soup, self.code = self.get_soup()
        print("scraping:[code: {}] {} ".format(self.code, url))

    def get_soup(self):
        try:
            r = requests.get(self.url)
            s = BeautifulSoup(r.text, 'lxml')
            print("code de la requête", r.status_code, " page: ", s.title)
            return s, r.status_code
        except:
            print("something went wrong. HTTP request code: {}".format(r.status_code))

    def get_links(self):
        '''get all links of the page (if mode internal=> only internal links)'''
        if self.code == 200:
            links = [l.get("href") for l in self.soup.find_all("a") if l.get("href") != "#"]  # --->

            intab_links = [self.site_url + l for l in links if l.startswith("/")]
            intre_links = [self.url + "/" + l for l in links if re.match(r"^(?!(http|/|#\w|mailto))", l)]
            print(intre_links)
            intex_links = [l for l in links if re.match(r"https?://{%s}.*" % self.root_url, l)]
            ext_links = [l for l in links if re.match(r"^https?(?!.*{%s}).*$" % self.root_url, l)]

            self.internal_links = list(set(intab_links + intex_links + intre_links))
            self.external_links = list(set(ext_links))

        else:
            self.internal_links = []

    def get_text(self):
        """récupère le contenu de la page"""
        div_tags = ["h{}".format(i) for i in range(1, 6)]

        p_text = [x.text.replace("\n", " ") for x in self.soup.find_all("p") if re.match(r"\w+", x.text)]
        div_text = {}

        for d in div_tags:
            div_text[d] = [x.text.replace("\n", "") for x in self.soup.find_all(d)]
        div_text["strong"] = [x.text.replace("\n", "") for x in self.soup.find_all("strong")]
        div_text["p"] = p_text

        text = " ".join(div_text["p"])

    ##############ICI########


# apply this to all n top resuslts
def main():
    site = Site("https://www.it-akademy.fr/")
    site.scrap_site()


# page = site.factory_page("https://www.it-akademy.fr/")
# page.get_links()
# page.get_text()


if __name__ == '__main__':
    main()