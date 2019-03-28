from bs4 import BeautifulSoup
import requests
import time

# set to your search url page
SEARCH_INITIAL_PAGE = "https://www.presidency.ucsb.edu/advanced-search?field-keywords=&field-keywords2=NATO%20%22North%20Atlantic%20Treaty%20Organization%22&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=&items_per_page=100"

# seconds between queries
TIME_BETWEEN_QUERIES = 0 # be nice!

print("Finding URLs...")

search_result_page = SEARCH_INITIAL_PAGE
documents = []

# find all documents
while search_result_page != None:
    print("Loading results from %s..." % search_result_page)
    page = requests.get(search_result_page)
    soup = BeautifulSoup(page.text, "html.parser")
    for link_block in soup.find_all("tr", {"class": ["even", "odd"]}):
        link = "https://www.presidency.ucsb.edu" + link_block.find("td", {"class": "views-field-title"}).find("a")["href"]
        print("Found link: %s" % link)
        documents.append(link)
    search_result_page_link = soup.find("a", {"title": "Go to next page"})
    if search_result_page_link != None:
        search_result_page = "https://www.presidency.ucsb.edu" + search_result_page_link["href"]
    else:
        search_result_page = None
    time.sleep(TIME_BETWEEN_QUERIES)

with open("documents.txt", "w") as outfile:
    for document in documents:
        outfile.write(document + "\n")

print("Found %s total documents." % str(len(documents)))