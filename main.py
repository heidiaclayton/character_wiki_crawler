import inquirer
from page_crawler import TokyoGhoulWikiCrawler, NarutoWikiCrawler, JJKWikiCrawler, DungeonMeshiWikiCrawler

available_wikis = ["tokyoghoul", "naruto", "jujutsu-kaisen", "delicious-in-dungeon"]
available_categories = ["Episodes", "Chapters"]

questions = [
    inquirer.List('subdomain', message="Which wiki do you want to search?", choices=available_wikis),
    inquirer.List('category', message='Which category are you searching?', choices=available_categories)
]
answers = inquirer.prompt(questions)
subdomain = answers['subdomain']
category = answers['category']

character = input("What character are you looking for?\n")

wiki_crawler = None

if subdomain == available_wikis[0]:
    wiki_crawler = TokyoGhoulWikiCrawler(subdomain, character, category)
elif subdomain == available_wikis[1]:
    wiki_crawler = NarutoWikiCrawler(subdomain, character, category)
elif subdomain == available_wikis[2]:
    wiki_crawler = JJKWikiCrawler(subdomain, character, category)
elif subdomain == available_wikis[3]:
    wiki_crawler = DungeonMeshiWikiCrawler(subdomain, character, category)
else:
    print("OOPS???")
    exit(1)

pages = wiki_crawler.get_pages()

print(f"Here are the pages where {character} appears or is mentioned!")

for page in pages:
    print(page)
