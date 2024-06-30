import sys
import re
import cacheHandler, jsonHandler, wikiScraper
import common


def main():
    #cacheHandler.reformatCacheViewerOutput()
    #jsonHandler.jsonFileToSQL(common.CACHE_UPDATED_PATH)
    wiki_data = wikiScraper.scrape_wiki()
    jsonHandler.wikiDataToSQL(wiki_data)

if __name__ == "__main__":
    main()