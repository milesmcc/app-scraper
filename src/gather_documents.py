from bs4 import BeautifulSoup
import requests
import time
import json
from tqdm import tqdm

# set document file
DOCUMENTS_FILE = "documents.txt"
OUTPUTS_FILE = "document_contents.json"

# seconds between queries
TIME_BETWEEN_QUERIES = 0 # be nice!

print("Loading documents...")

documents = {}

try:
    with open(OUTPUTS_FILE, "r") as infile:
        documents = json.load(infile)
except:
    pass # first run; no issues -- if corrupt, will be overwritten anyway

document_links = []

with open(DOCUMENTS_FILE, "r") as infile:
    document_links = [link for link in infile.readlines() if link not in documents]

print("Loaded %s document links to process..." % str(len(document_links)))

for document_link in tqdm(document_links):
    page = requests.get(document_link)
    soup = BeautifulSoup(page.text, "html.parser")
    text = soup.find("div", {"class": "field-docs-content"}).text
    date = soup.find("span", {"class": "date-display-single"}).text
    title = soup.find("div", {"class": "field-ds-doc-title"}).text
    speaker = soup.find("h3", {"class": "diet-title"}).text
    citation = soup.find("p", {"class": "ucsbapp_citation"}).text
    documents[document_link] = {
        "text": text,
        "date": date,
        "title": title,
        "speaker": speaker,
        "citation": citation
    }

    # temporary save
    with open(OUTPUTS_FILE, "w") as outfile:
        json.dump(documents, outfile)

    time.sleep(TIME_BETWEEN_QUERIES)