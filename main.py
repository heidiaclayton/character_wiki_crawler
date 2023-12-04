from page_crawler import TokyoGhoulWikiCrawler, NarutoWikiCrawler

available_wikis = ["tokyoghoul", "naruto"]
available_categories = ["Episodes", "Chapters"]

subdomain = input("What is the subdomain of the fandom wiki? ")

if subdomain not in available_wikis:
    print(f"Invalid subdomain. Available wikis: {', '.join(available_wikis)}")
    exit(1)

category = input("What category are you searching (ex: episodes)? (case sensitive) ")

if category not in available_categories:
    print(f"Invalid category. Available categories: {', '.join(available_categories)}")
    exit(1)

character = input("What character are you looking for? ")

wiki_crawler = None

if subdomain == "tokyoghoul":
    wiki_crawler = TokyoGhoulWikiCrawler(subdomain, character, category)
elif subdomain == "naruto":
    wiki_crawler = NarutoWikiCrawler(subdomain, character, category)
else:
    print("OOPS???")
    exit(1)

pages = wiki_crawler.get_pages()

print(f"Here are the pages where {character} appears!")

for page in pages:
    print(page)
