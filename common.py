from datetime import datetime
TODAYS_DATE = datetime.today().strftime('%Y-%m-%d')

CACHE_OUTPUT_PATH = "cache_viewer_files/Cache Viewer.html"
CACHE_UPDATED_PATH = "cache_viewer_files/cacheData_formatted.txt"
DATABASE_PATH = "transcript.db"
TABLE_NAME = "transcript"
ITEM_KEY = "items"
NPC_KEY = "npcs"
OBJECT_KEY = "objects"

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
FETCH_PETDIALOGUE = False
FETCH_LEVELUPMESSAGE = False
FETCH_EXAMINE = True