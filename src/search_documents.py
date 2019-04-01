import json
from tqdm import tqdm
import unicodecsv

DOCUMENTS_LOCATION = "document_contents.json"
OUTPUT_LOCATION_JSON = "search_results.json"
OUTPUT_LOCATION_CSV = "search_results.csv"

def _contains_any_term(terms, text):
    for term in terms:
        if term in text:
            return True
    return False

def _split_into_chunks(text):
    MAX_ROW_LENGTH = 30000
    return [text[i:i+MAX_ROW_LENGTH] for i in range(0, len(text), MAX_ROW_LENGTH)]

def _text(document):
    return document["title"] + " " + document["text"]

def is_match(document):
    if "nato" or "north atlantic treaty organization" in _text(document).lower():
        if _contains_any_term(["spending", "contribution", "percent of gdp", "defense budget"], _text(document).lower()): 
            if _contains_any_term(["north atlantic council", "north atlantic alliance"], _text(document).lower()):
                return True
    return False

matches = []

print("Loading documents...")
with open(DOCUMENTS_LOCATION, "r") as infile:
    documents = json.load(infile)
    print("Searching...")
    for document_url in tqdm(documents.keys()):
        document = documents[document_url]
        if is_match(document):
            document["url"] = document_url
            # It's spaghetti code, but we cannot change the past! Would have been better to store URL as a key in the first place
            matches.append(document)

print("Found %s matches!" % str(len(matches)))

if OUTPUT_LOCATION_JSON is not None:
    print("Writing json to %s..." % OUTPUT_LOCATION_JSON)
    with open(OUTPUT_LOCATION_JSON, "w") as outfile:
        json.dump(matches, outfile)

if OUTPUT_LOCATION_CSV is not None:
    print("Writing csv to %s..." % OUTPUT_LOCATION_CSV)
    with open(OUTPUT_LOCATION_CSV, "wb") as outfile:
        writer = unicodecsv.writer(outfile)
        writer.writerow(["DATE", "TITLE", "SPEAKER", "CITATION", "URL", "TEXT"])
        for match in matches:
            writer.writerow([match["date"].strip(), match["title"].strip(), match["speaker"].strip(), match["citation"].strip(), match["url"].strip(), *_split_into_chunks(match["text"].strip())])
        
print("...done!")