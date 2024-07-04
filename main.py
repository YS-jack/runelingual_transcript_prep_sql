import sys
import re
import cacheHandler, jsonHandler, webScraper
import common


def main():
    #cacheHandler.reformatCacheViewerOutput()
    #jsonHandler.jsonFileToSQL(common.CACHE_UPDATED_PATH)
    item_names, item_examines, item_options \
        = webScraper.scrape_chisel(common.CHISEL_URL["item_main"], common.CHISEL_URL["item_main"])
    npc_names, npc_examines, npc_options \
         = webScraper.scrape_chisel(common.CHISEL_URL["npc_main"], common.CHISEL_URL["npc_examine"])
    object_names, object_examines, object_options \
        = webScraper.scrape_chisel(common.CHISEL_URL["object_main"], common.CHISEL_URL["object_examine"])
    for name_data in [item_names, npc_names, object_names]:
        jsonHandler.dictListToSQL(name_data, [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY, common.COLUMN_NAME_SUB_CATEGORY])
    for examine_data in [item_examines, npc_examines, object_examines]:
        jsonHandler.dictListToSQL(examine_data, [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY, common.COLUMN_NAME_SUB_CATEGORY])
    for option_data in [item_options, npc_options, object_options]:
        jsonHandler.dictListToSQL(option_data, [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY, common.COLUMN_NAME_SUB_CATEGORY])
                                                
    wiki_data = webScraper.scrape_wiki()
    jsonHandler.dictListToSQL(wiki_data, [common.COLUMN_NAME_ENGLISH, common.COLUMN_NAME_CATEGORY, 
                                          common.COLUMN_NAME_SUB_CATEGORY, common.COLUMN_NAME_SOURCE])

if __name__ == "__main__":
    main()