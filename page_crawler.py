from pyquery import PyQuery as pq
import page_gatherer
from utils import print_dot


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
                        pages.append([chapter, "Appears"])
            count += 1

        print("\nDone crawling.")

        return pages

    def get_pages(self):
        pages = self.crawl()
        cleaned_pages = []

        for page in pages:
            split_page = page[0].split(f"{self.base_url}/wiki/")

            if len(split_page) != 2:
                cleaned_pages.append(page)
                continue

            cleaned_pages.append(f"{split_page[1].replace('_', ' ')} ({page[1]}): {page[0]}")

        return sorted(cleaned_pages)


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
                    pages.append(chapter)
                    break
            count += 1

        print("\nDone crawling.")

        return pages
