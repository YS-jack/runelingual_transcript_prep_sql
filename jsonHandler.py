import json
import sqlite3
import common

def connect_to_db(db_file):
    conn = sqlite3.connect(db_file)
    return conn, conn.cursor()

def create_table(cursor):
    """Create the transcript table if it doesn't exist."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcript (
            key INTEGER PRIMARY KEY, 
            english TEXT, 
            category TEXT, 
            sub_category TEXT, 
            source TEXT, 
            widget_id INTEGER, 
            parent_widget_id INTEGER, 
            width INTEGER, 
            height INTEGER, 
            notes TEXT, 
            date_modified TEXT
        )
    ''')

    cursor.execute('''
                   CREATE INDEX IF NOT EXISTS english_index ON transcript (english)
                   ''')

def check_record_exists(c, conditions):
    """
    args:
        c: sqlite3.Cursor object
        conditions: dictionary of column-value pairs to check for existence
    """
    #base query
    query = f"SELECT 1 FROM {common.TABLE_NAME} WHERE "

    # Dynamically build the WHERE clause based on conditions
    where_clauses = []
    values = []
    for column, value in conditions.items():
        where_clauses.append(f"{column} = ?")
        values.append(value)
    
    # Join all WHERE clauses with 'AND'
    query += " AND ".join(where_clauses)
    
    # Debug: Print the query and values
    #print("Executing query:", query)
    #print("With values:", values)

    # Execute the query
    c.execute(query, tuple(values))
    
    # Retrieve the result
    result = c.fetchone()

    # Debug: Print the query, values, and return value
    #print("Executing query:", query)
    #print("With values:", values)
    #print("return value:", result is not None)
    
    # Check if any record exists based on the stored result
    return result is not None

def insert_data(conn, c, data):

    """
    Insert data in the transcript table.
    Args:
        conn: sqlite3.Connection object
        c: sqlite3.Cursor object
        entity_list_of_category: entity list for one of the categories (items, npcs, objects)
        e.g of entity_list_of_category:
            ["item":[{
            "name":"Dwarf remains",
            "examine":"The body of a Dwarf savaged by Goblins.",
            "inventoryActions":[null,null,null,null,"Destroy"]
            },{
            "name":"Toolkit",
            "examine":"Good for repairing broken cannons.",
            "inventoryActions":[null,null,null,null,"Destroy"]
            }
            ],
            "npc":[{
            "name":"Dwarf",
            "examine":"He looks like he's been working hard.",
            "actions":["Talk-to","Trade","Pickpocket"]
            },{...}],
            "object":[{
            "name":"Anvil",
            "examine":"Used for smithing metal items.",
            "actions":["Smith","Craft","Repair"]
            },{...}]
            ]
    """
    for category_type, entity_list_of_category in data.items(): #category_type = "item", "npc", "object"
        for entity in entity_list_of_category: #entity is a dictionary, of either item, npc, or object
            #source_name is the name of the entity 
            source_name = 'unknown'
            if category_type == common.ITEM_KEY:
                source_name = entity[common.ITEM_NAME_VAR_NAME]
            elif category_type == common.NPC_KEY:
                source_name = entity[common.NPC_NAME_VAR_NAME]
            elif category_type == common.OBJECT_KEY:
                source_name = entity[common.OBJECT_NAME_VAR_NAME]

            for key, value in entity.items(): #key = "name", "examine", "inventoryActions" etc
                query = f'''
                        INSERT INTO {common.TABLE_NAME} (english, category, sub_category, source, widget_id, parent_widget_id, width, height, notes, date_modified)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                # if its a name
                if key in [common.ITEM_NAME_VAR_NAME, common.NPC_NAME_VAR_NAME, common.OBJECT_NAME_VAR_NAME]\
                        and not check_record_exists(c, {"english":value}):
                    c.execute(query, (value, key, category_type, '', 0, 0, 0, 0, '', ''))

                # if its an examine
                elif key in [common.ITEM_EXAMINE_VAR_NAME, common.NPC_EXAMINE_VAR_NAME, common.OBJECT_EXAMINE_VAR_NAME]\
                        and not check_record_exists(c, {"english":value}):
                    c.execute(query, (value, key, category_type, source_name, 0, 0, 0, 0, '', ''))


                # if its an option
                elif key in [common.ITEM_OPTION_VAR_NAME, common.NPC_OPTION_VAR_NAME, common.OBJECT_OPTION_VAR_NAME]:
                    for option in value:
                        if type(option) != str or option == "Null":
                            continue
                        elif not check_record_exists(c, {"english":option, "sub_category":category_type}):
                            c.execute(query, (option, key, category_type, source_name, 0, 0, 0, 0, '', ''))
    
    conn.commit()
                        

def jsonFileToSQL(jsonFile):
    with open(jsonFile) as json_file:
        data = json.load(json_file)

    conn, c = connect_to_db(common.DATABASE_PATH)

    #create_table if it doesn't exist
    create_table(c)

    #insert data into the table
    insert_data(conn, c, data)
    

if __name__ == "__main__":
    jsonFileToSQL(common.CACHE_UPDATED_PATH)