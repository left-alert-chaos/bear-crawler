import crawl
import gc
import os
import pages

url = input("Please enter url:\n>")

#quick and dirty implementation
crawler = crawl.Crawler(url, 8)
input("About to start crawl at webscraper.io. Press ^C to stop crawl. Press enter to start.")
try:
    crawler.start()
except KeyboardInterrupt:
    gc.collect()

print("Done!")

#super simple search engine
while True:
    query = input("Please enter a query (single words or phrases work best):\n>").lower()
    query_words = set(query.split())
    results: list[pages.Page] = []
    for i in crawler.pages:
        if len(i.words.intersection(query_words)) > 0:
            results.append(i)
    results = pages.rank(results)
    for res in results:
        print(f"{res.url} with {res.references} pointers")