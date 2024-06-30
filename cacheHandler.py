from bs4 import BeautifulSoup
import ijson
import common

def reformatCacheViewerOutput():
    """
    After saving the cache viewer output to file stated in CACHE_OUTPUT_PATH,
    this function reads the file and reformats the data into a JSON format.
    It then saves the reformatted data to CACHE_UPDATED_PATH.
    """
    with open(common.CACHE_OUTPUT_PATH, "r", encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    div_content = soup.find_all('span', class_='string root')
    cache_data = [convert_outer_quotes(div.text.replace("\\\"","\"")) for div in div_content]


    #print(len(json_string))
    with open(common.CACHE_UPDATED_PATH, "w", encoding='utf-8') as f:
        f.write("{\n")  
        f.write("\""+common.ITEM_KEY+"\": ")       
        f.write(convert_outer_quotes(cache_data[0], ""))
        f.write(",\n")
        f.write("\""+common.NPC_KEY+"\": ")
        f.write(convert_outer_quotes(cache_data[1], ""))
        f.write(",\n")
        f.write("\""+common.OBJECT_KEY+"\": ")
        f.write(convert_outer_quotes(cache_data[2], ""))
        f.write("\n}")

    if(validate_large_json(common.CACHE_UPDATED_PATH)):
        print("Cache data reformatted successfully, saved to " + common.CACHE_UPDATED_PATH)
    else:
        print("Cache data reformatting failed!")
    

def convert_outer_quotes(string, convert_to = "'"):
    # Check if the string starts and ends with double quotes
    if (string.startswith("\"") and string.endswith("\"")) or (string.startswith("\'") and string.endswith("\'")):
        # Remove the outer double quotes and add single quotes
        return convert_to + string[1:-1] + convert_to
    return string

def validate_large_json(json_file_path):
    # Open the JSON file
    with open(json_file_path, 'rb') as file:
        # Initialize a parser to read the file in a streaming manner
        parser = ijson.parse(file)
        
        # Example validation logic
        for prefix, event, value in parser:
            # Implement validation logic here
            # For example, check for specific keys or value types
            if prefix.endswith('.key') and event == 'string':
                # Validate the value or key
                pass
            # Add more validation rules as needed

    # If the loop completes without errors, the JSON is considered valid
    # for the implemented validation rules

    return True


if __name__ == "__main__":
    reformatCacheViewerOutput()