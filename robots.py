import re

#Hold all info about a robots.txt file
class Policy:
    def __init__(self, file_text: str, user: str):
        self.raw = file_text
        self.user_agent = user
        self.allow_all = False
        self.disallow_all = False
        self.crawl_delay = 0
        self.process_file()
    
    #check if a url is allowed or disallowed by robots.txt
    def is_allowed(self, url: str) -> bool:
        if url in self.clearances:
            return self.clearances[url]
        for i in self.clearances.keys():
            if url.startswith(i) or re.search(i, url):
                return self.clearances[i]
        if self.disallow_all:
            return False
        if self.allow_all:
            return True

        return True
    
    def process_file(self) -> dict[str, bool]:
        clearances = {}
        discussed_agent = ""

        for line in self.raw.split("\n"):
            #skip blank lines and comments
            if line == "":
                continue
            if line.startswith("#"):
                continue

            #if a user agent is addressed,
            # set the agent recieving clearances to the last word in line
            if line.lower().startswith("user-agent"):
                discussed_agent = line.split()[1]
            elif discussed_agent in ("*", self.user_agent):
                #wildcard support with regexes
                line = line.replace("*", ".*")

                words = line.split()

                #if a path is allowed, the clearance for the
                #path is set to True
                match words[0].lower():
                    case "allow:":
                        #allow for disallow all
                        if len(words) == 1 or words[1] == "/":
                            self.allow_all = True
                            self.disallow_all = False
                        else:
                            clearances[words[1]] = True
                    case "disallow:":
                        if len(words) == 1 or words[1] == "/":
                            self.disallow_all = True
                            self.allow_all = False
                        else:
                            clearances[words[1]] = False
                    case "crawl-delay:":
                        self.crawl_delay = int(words[1])
        self.clearances = clearances
        return clearances


#generic policy to stand in for sites without robots.txt
all_allowed = Policy("", "*")
