import os
import pages
import crawl

root_url = input("Please input URL to start from:\n>")

while True:
    depth = input("Please enter max depth: (10 is a lot more than you'd think)\n>")
    if not depth.isdecimal():
        print("That's not an integer.")
    else:
        depth = int(depth)
        break

crawler = crawl.Crawler(root_url, depth)
input("About to start crawl. Press ^C to stop crawl and download pages. It can take a lot of space to store pages after crawl, and it uses a fair amount of RAM and time to do the crawl. Press enter to start.")
crawler.start()
if not os.path.isdir("scrapes"):
    os.mkdir("scrapes")
os.chdir("scrapes")

for page in crawler.pages:
    #filter non-html pages
    if len(page.soup.get_text()) == 0:
        continue
    fname = page.url.replace("/", "").replace(".", "_").replace("?", "_").replace(":", "")
    with open(fname, "w") as file:
        file.write(page.text)