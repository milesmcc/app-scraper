# American Presidency Project Scraper
Unfortunately, no suitable tool exists for exporting search results from UCSB's database of presidential documents for aggregate use. This repository provides a collection of Python 3 scripts that, together, constitute a scraping tool for UCSB's [American Presidency Project](https://www.presidency.ucsb.edu) (APP).

Before using these scripts, note the following:

> * Scraping can put significant load on APP's servers. Choose a reasonable query delay.
> * Scraping is not a future-proof way of gathering data. These tools may break at any time.

### How To Use

Use `gather_documents.py` to scrape documents from a text file containing their URLs (one per line) located at `./documents.txt`. Use `gather_search_results.py` to scrape the search results page.

See each script's internal documentation for more information.

---

This tool is licensed under the General Public License v3. Created by Miles McCain for research with Sarah Kreps.
