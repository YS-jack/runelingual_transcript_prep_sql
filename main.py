import sys
import re
import cacheHandler, jsonHandler
import common


def main():
    cacheHandler.reformatCacheViewerOutput()
    jsonHandler.jsonFileToSQL(common.CACHE_UPDATED_PATH)

if __name__ == "__main__":
    main()