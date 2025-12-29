import bs4

class Page:
    def __init__(self, url: str, text: str, invalid: bool=False):
        self.url = url
        #start at one because something had to lead to it
        self.references = 1
        self.text = text
        self.soup = bs4.BeautifulSoup(text, "html.parser")
        self.invalid = invalid
        self.words = set(self.soup.get_text().lower().split())


invalid_page = Page("", "", True)


#Pretty straightforward. Not sure if that was sarcastic or not.
def rank(pages: list[Page]) -> list[Page]:
    scores = {page.references: page for page in pages}
    list_of_scores: list = list(scores.keys())
    list_of_scores.sort()
    list_of_scores.reverse()

    #most unreadable line ever written
    return [scores[score] for score in list_of_scores]
