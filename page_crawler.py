from pyquery import PyQuery as pq
import re
import page_gatherer
from utils import print_dot, get_number


class CharacterWikiCrawler:
    def __init__(self, subdomain: str, character: str, category: str):
        self.character = character
        self.category = category
        self.base_url = f"https://{subdomain}.fandom.com"

    def get_glossary(self):
        return page_gatherer.v1(self.base_url, self.category)

    def crawl(self):
        pass

    def get_pages(self):
        return self.crawl()


class TokyoGhoulWikiCrawler(CharacterWikiCrawler):
    def __init__(self, subdomain, character, category):
        CharacterWikiCrawler.__init__(self, subdomain, character, category)

        self.glossary = self.get_glossary()

    def crawl(self):
        pages = []
        count = 1

        print(f"Crawling pages for {self.character}")

        for chapter in self.glossary:
            print_dot(count, 50)
            q = pq(url=chapter)

            links = q("#Characters").parent().next().children()

            for link in links:
                children = link.getchildren()
                num_children = len(children)

                if num_children < 1:
                    continue

                if self.character in children[0].text:
                    if len(children) > 1:
                        pages.append([chapter, children[1].text])
                    else:
                        pages.append([chapter, "(Appears)"])
            count += 1

        print("\nDone crawling.")

        return pages

    def get_pages(self):
        pages = self.crawl()
        cleaned_pages = []
        re_cleaned_pages = []

        for page in pages:
            split_page = page[0].split(f"{self.base_url}/wiki/")

            if len(split_page) != 2:
                cleaned_pages.append(page)
                continue

            if split_page[1].startswith("Re:"):
                re_cleaned_pages.append(f"{split_page[1].replace('_', ' ')} {page[1]}: {page[0]}")
            else:
                cleaned_pages.append(f"{split_page[1].replace('_', ' ')} {page[1]}: {page[0]}")

        return sorted(cleaned_pages, key=get_number) + sorted(re_cleaned_pages, key=get_number)


class NarutoWikiCrawler(CharacterWikiCrawler):
    def __init__(self, subdomain, character, category):
        CharacterWikiCrawler.__init__(self, subdomain, character, category)

        self.glossary = self.get_glossary()

    def crawl(self):
        pages = []
        count = 1

        print(f"Crawling pages for {self.character}")

        for chapter in self.glossary:
            print_dot(count, 50)
            q = pq(url=chapter)

            links = q("b a")

            for link in links:
                if link.text and self.character in link.text:
                    text = q("div.mw-parser-output").text()
                    matches = re.search("episode \d+ of the .+ anime", text)
                    pages.append([chapter, matches.group() if matches is not None else "Could not find episode number"])
                    break
            count += 1

        print("\nDone crawling.")

        return pages

    def get_pages(self):
        pages = self.crawl()
        original_cleaned_pages = []
        shippuden_cleaned_pages = []
        other_cleaned_pages = []

        for page in pages:
            if "of the original Naruto anime" in page[1]:
                original_cleaned_pages.append(f"{page[1]}: {page[0]}")
            elif "of the Naruto: Shippūden anime" in page[1]:
                shippuden_cleaned_pages.append(f"{page[1]}: {page[0]}")
            else:
                other_cleaned_pages.append(f"{page[1]}: {page[0]}")

        return sorted(original_cleaned_pages, key=get_number) + sorted(shippuden_cleaned_pages, key=get_number) + sorted(other_cleaned_pages, key=get_number)
