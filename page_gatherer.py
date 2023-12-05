from pyquery import PyQuery as pq
from utils import print_dot


# works for tokyo ghoul and naruto
def v1(base_url: str, category):
    chapters_gathered = False
    chapters_urls = set()
    glossary_url = f"{base_url}/wiki/Category:{category}"
    count = 1

    print("Gathering glossary.")

    while not chapters_gathered:
        print_dot(count, 50)
        q = pq(url=glossary_url)
        links = q("div.category-page__members a")

        for link in links:
            href = link.get('href')

            if "Discussion" in href:
                continue

            chapters_urls.add(f"{base_url}{href}")

        glossary_url = q("a.category-page__pagination-next").attr("href")
        count += 1

        if not glossary_url:
            chapters_gathered = True

    print(f"\nDone gathering glossary. Found {len(chapters_urls)} entries.")

    return chapters_urls
