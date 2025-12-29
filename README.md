# bear-crawler
bear-crawler is a local, small, semi-reliable web crawler that obeys robots.txt. It runs locally and allows for quick searching.

Main.py is a simple implementation that crawls a user-chosen website. simple-search-engine.py performs a similar crawl, but then give the user a simple CLI to search for keywords and phrases.

You can also use components of bear-crawler in your Python projects. crawl.py is the main crawl logic, but it needs pages.py and robots.py.

__NOTE: Asterisks (\*) are not experimentally supported in `robots.txt`. So paths like /a/b/\*/c may not be processed correctly.__

## To use the preconfigured setup
1. Run `git clone https://github.com/left-alert-chaos/bear-crawler.git` to download the repo.
2. Run `cd bear-crawler` to move to the repo directory.
3. Run `python -m venv venv` to create a virtual environment.
4. Run `venv/Scripts/activate` to activate the environment.
5. Run `pip install -r requirements.txt` to download bear-crawler's dependencies.
6. Run `python main.py` to use bear-crawler.

Note: You only need to do steps 1-5 once.

# crawl.py
Crawl.py is the main implementation of the web crawler. It's recursive and uses a user-definable User-Agent (read from agent.txt).

## Crawler()
The Crawler class takes only a few arguments to its constructor: `root_url`, and `target_depth`. The root url is the URL to start crawling from. Pretty simple. The target depth is the maximum depth to crawl. Really all that means is that `Crawler.crawl()` is recursive, so it's the maximum number of recursive calls to preform while crawling.

### start()
The best way to use the crawler is to just create it and run `.start()`. After the very very time consuming crawl, the results will be in `.pages`, which is a list, and `.pages_by_name`, which is a dictionary of URLs to pages.

# pages.py
Pages.py is a short file (they all are, really) that just provides a structure and type for processed and crawled pages. The user only needs to care about the `Page` type when processing results.

## Page()
This is a simple, almost self-documenting type providing structure for data about crawled pages.

### text
The HTML (or other format) of text retrieved from the server.

### soup
A `bs4.BeautifulSoup` object that is used to process the page.

### words
A Python set of all words encountered in a page.

### references
An integer that represents how many times a page was linked from other pages. This is good if you want to sort pages (you can use pages.py's `rank()` function, too).

### url
The URL the page was fetched from.

# robots.py
This file provides support for `robots.txt`.

## Policy()
This is a type that represents a web page's `robots.txt` file for easy link blocking. Its constructor only takes two arguments: `file_text` and `user`. The file text is the text of the `robots.txt` file and the user is the user agent to process for.

### is_allowed()
This is a function that takes a relative path as a string an returns a boolean. The path is formatted as a path from a website's root and the return value represents whether a page is allowed under `robots.txt`. If the bool returned is True, the page is allowed. If it's False, the page is disallowed.