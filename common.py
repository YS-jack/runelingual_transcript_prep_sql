from datetime import datetime
TODAYS_DATE = datetime.today().strftime('%Y-%m-%d')

CACHE_OUTPUT_PATH = "cache_viewer_files/Cache Viewer.html"
CACHE_UPDATED_PATH = "cache_viewer_files/cacheData_formatted.txt"
DATABASE_PATH = "transcript.db"
CSV_FILE_DIR = "./manual_data/"
TABLE_NAME = "transcript"

# KEYs are the values in column
ITEM_KEY = "item"
NPC_KEY = "npc"
OBJECT_KEY = "object"

# VAR_NAMEs are static values inserted to the database
ITEM_NAME_VAR_NAME = "name"
NPC_NAME_VAR_NAME = "name"
OBJECT_NAME_VAR_NAME = "name"

ITEM_EXAMINE_VAR_NAME = "examine"
NPC_EXAMINE_VAR_NAME = "examine"
OBJECT_EXAMINE_VAR_NAME = "examine"

ITEM_OPTION_VAR_NAME = "inventoryActions"
NPC_OPTION_VAR_NAME = "actions"
OBJECT_OPTION_VAR_NAME = "actions"

NPC_DIALOGUE_VAR_NAME = "dialogue"
LEVEL_UP_VAR_NAME = "lvl_up_msg"

#COLUMN_NAMEs are the column names in the database
COLUMN_NAME_ENGLISH = "english"
COLUMN_NAME_CATEGORY = "category"
COLUMN_NAME_SUB_CATEGORY = "sub_category"
COLUMN_NAME_SOURCE = "source"
COLUMN_NAME_WIDGET_ID = "widget_id"
COLUMN_NAME_PARENT_WIDGET_ID = "parent_widget_id"
COLUMN_NAME_WIDTH = "width"
COLUMN_NAME_HEIGHT = "height"
COLUMN_NAME_NOTES = "notes"
COLUMN_NAME_DATE_MODIFIED = "date_modified"
COLUMN_NAME_WIKI_URL = "wiki_url"

WIKI_URL = {"npc_dialogue" : "https://oldschool.runescape.wiki/w/Category:NPC_dialogue",
            "pet_dialogue" : "https://oldschool.runescape.wiki/w/Category:Pet_dialogue",
            "level_up_message" : "https://oldschool.runescape.wiki/w/Category:Level_up_messages",
            "examine" : "https://oldschool.runescape.wiki/w/",
            "base" : "https://oldschool.runescape.wiki"}
FETCH_NPCDIALOGUE = True
FETCH_PETDIALOGUE = True
FETCH_LEVELUPMESSAGE = True
FETCH_EXAMINE = True
FETCH_ITEM_NPC_OBJECT_URLS = False

CHISEL_URL = {"item_main" : "https://chisel.weirdgloop.org/moid/data_files/itemsmin.js",
              "npc_main" : "https://chisel.weirdgloop.org/moid/data_files/npcsmin.js",
              "object_main" : "https://chisel.weirdgloop.org/moid/data_files/objectsmin.js",
              "npc_examine": "https://chisel.weirdgloop.org/moid/data_files/npc_examinesmin.js",
              "object_examine": "https://chisel.weirdgloop.org/moid/data_files/object_examinesmin.js",}


# DONT CHANGE unless the chisel data changes
CHISEL_CATEGORY_NAME = {'item' : 'items', 'npc' : 'npcs', 'object' : 'objects', 'name': 'name',\
                        'examine' : 'examine', 'action_item' : 'actInv',\
                        'action_npc' : 'actions', 'action_object' : 'actions'}

WIKI_SEARCH_BASE_URL = {"npc" : "https://oldschool.runescape.wiki/?title=Special%3ASearchByProperty&property=NPC+ID&value=",
                        "object" : "https://oldschool.runescape.wiki/?title=Special%3ASearchByProperty&property=Object+ID&value=",
                        "item" : "https://oldschool.runescape.wiki/?title=Special%3ASearchByProperty&property=Item+ID&value="}