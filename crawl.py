import robots
import pages
import requests
import bs4
import time
import pprint


class Crawler:
    def __init__(self, root_url: str, target_depth: int):
        print(f"Created Crawler with root {root_url}, target {target_depth}")
        self.max_depth = target_depth
        self.root = root_url
        self.policies: dict[str, robots.Policy] = {}
        self.pages: list[pages.Page] = []
        self.pages_by_name: dict[str, pages.Page] = {}
        with open("agent.txt", "r") as file:
            self.agent = file.read()
        self.header = {"User-Agent": self.agent}

        #pages to ignore to prevent redundant crawling
        self.ignore = []
    
    def start(self) -> None:
        self.crawl(self.root, 0)
    
    def crawl(self, url: str, depth: int) -> None:
        if depth > self.max_depth:
            return
        if url in self.ignore:
            #increment references to show page popularity
            if url in self.pages_by_name:
                self.pages_by_name[url].references += 1
            return
        if not url.startswith("http"):
            return
        if "wikipedia" in url:
            return

        
        print(f"\nURL: {url}\nDepth: {depth}")
        root = url.split("/")[2]
        if url.startswith("https"):
            root = "https://" + root
        else:
            root = "http://" + root
        print(f"Root: {root}")
        
        #determine appropriate robots.txt policy and apply. Make one if necessary.
        if root in self.policies:
            policy = self.policies[root]
        else:
            txt_response = requests.get(f"{root}/robots.txt", self.header)
            policy = robots.Policy(txt_response.text, self.agent) if txt_response.status_code == 200 else robots.all_allowed
            self.policies[root] = policy
            print(f"Created new policy for {root}:")
            pprint.pp(policy.clearances)
            print(f"Crawl delay: {policy.crawl_delay}")
        
        #for safety
        relative = url.replace(root, "")
        print(policy.is_allowed(relative))
        if policy.is_allowed(relative) == False:
            print(f"Path {relative} isn't allowed.")
            return
        print(f"Path {relative} is allowed.")
        print(policy.clearances)
        
        #for pure ethics and anxiety sake, put the actual fetch after clearance
        response = requests.get(url, self.header)
        if response.status_code != 200:
            print(f"Returned code {response.status_code}. Not 200.")
            print(f"Text: {response.text}")
            return
        
        #store index
        page = pages.Page(url, response.text)
        self.pages.append(page)
        self.pages_by_name[url] = page

        #to prevent reindexing
        self.ignore.append(url)

        #be a good citizen.
        #watches for <meta name="robots" contents="noindex">
        for meta in page.soup.find_all("meta"):
            if meta.get("name") == "robots" and meta.get("contents") == "noindex":
                print("Not allowed by a <meta>.")
                return

        for link in page.soup.find_all("a"):
            href: str | None = link.get("href") # type: ignore
            match href:
                case None:
                    continue
                case "/":
                    href = root
            
            #robots.txt coherence because we're good citizens
            if not policy.is_allowed(href):
                continue
            time.sleep(policy.crawl_delay)

            if href.startswith("/"):
                href = f"{root}{href}"

            self.crawl(href, depth+1)
