# scrapes data from the osrs wiki and
# returns the data in a dictionary
# npc_dialogue includes dialogue, every option in option dialogue as different entry, and overhead

import common
import requests
from bs4 import BeautifulSoup
import re

def get_data_from_wiki_page(url, category):
    """
    Scrapes data from the OSRS wiki and returns the data in a list of dictionary
    return:
    [
    {"english": dialogue, "category":"dialogue", "sub_category":entity_name, "source":speaker "notes":"may be one of options in option dialogue"},
    {"english": dialogue, "notes":""},
    {"english": dialogue, "notes":"may be an overhead"},
    ...
    ]

    """
    # Step 1: Fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the webpage content for {url}.")
        return {}
    
    # Step 2: Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')

    # get target entity (name of npc, object, etc.)
    if category == common.WIKI_URL["npc_dialogue"]:
        entity_name = soup.find("h1", class_="firstHeading").get_text().replace("Dialogue for ", "")
        print(entity_name)

    data = {entity_name: []}
    # Step 3: Extract the data
    mw_parser_output = soup.find("div", class_="mw-parser-output")

    # Check if mw_parser_output exists
    if mw_parser_output is None:
        print("Div with class 'mw-parser-output' not found.")
        return {}
    
    list_items = mw_parser_output.find_all("li")

    # Step 4: retrieve the dialogue text and insert to raw_text_list[]
    raw_text_list = []

    if category == common.WIKI_URL["npc_dialogue"]:
        # Find all <b> tags for the speaker's dialogue
        for b_tag in mw_parser_output.find_all("b"):
            sibling_texts = []
            next_sibling = b_tag.next_sibling
            while next_sibling:
                if next_sibling.name:
                    sibling_texts.append(next_sibling.get_text(strip=True))
                else:  
                    sibling_texts.append(next_sibling.strip())
                next_sibling = next_sibling.next_sibling
            full_text = " ".join(sibling_texts).strip()
            raw_text = (b_tag.get_text(strip=True), full_text)
            print(raw_text)
            raw_text_list.append(raw_text)

        # Find all <div class="transcript-opt"> for the player's options
        for div_tag in mw_parser_output.find_all("div", class_="transcript-opt"):
            raw_text = div_tag.get_text(strip=True)
            if re.match(r"Dialogue \d+", raw_text.strip()):
                continue
            print(raw_text)
            raw_text_list.append(raw_text)

    # Step 5: reformat the raw texts in raw_text_list[] and insert to data{}
    for raw_text in raw_text_list:
        # Check if the raw text is a tuple
        if isinstance(raw_text, tuple):
            speaker, dialogue = raw_text
            # Check if the dialogue is not empty
            if dialogue:
                data[entity_name].append({"english": dialogue, "category":"dialogue", "sub_category":entity_name, "source":speaker, "notes":""})
        else:
            # Check if the raw text is not empty
            if raw_text:
                data[entity_name].append({"english": raw_text, "category":"dialogue", "sub_category":entity_name, "source":"player", "notes":"may be one of options in option dialogue"})

    return data

def get_all_urls_from_category(base_url, url):
    """
    Get all the URLs for every page of the category
    """
    # Step 1: Fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the webpage content for {url}.")
        return []

    links = [url]

    # Step 2: Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')
    nextpage_tag = soup.find("a", string="next page")

    # Check if the 'next page' tag exists
    if not nextpage_tag:
        return links

    # Step 3: get the 'next page' url path
    next_url_path = soup.find("a", string="next page")["href"]
    next_page_link = base_url + next_url_path

    return links + get_all_urls_from_category(base_url, next_page_link)

def scrape_wiki():
    """
    1. get the base url for list for each category
    2. get all the urls for every page of the category
    3. get the data from each page in dictionary form, to tell what entity we are interacting with
    4. return the data
    """
    data = {}
    if common.FETCH_NPCDIALOGUE:
        # Step 1: Get the base URL for each category
        #base_url_npc_dialogue = common.WIKI_URL["npc_dialogue"]
        # Step 2: Get all the URLs for every page of the category
        #url_list_npc_dialogue = get_all_urls_from_category(common.WIKI_URL["base"], base_url_npc_dialogue)
        # Step 3: Get the data from each page in dictionary form
        dialgogue_data = get_data_from_wiki_page("https://oldschool.runescape.wiki/w/Transcript:Banker", common.WIKI_URL["npc_dialogue"])
        #print(dialgogue_data)
        """for url in url_list_npc_dialogue:
            dialogue_data = get_data_from_wiki_page(url, common.WIKI_URL["npc_dialogue"])
            data.update(dialogue_data)"""

    if common.FETCH_PETDIALOGUE:
        base_url_pet_dialogue = common.WIKI_URL["pet_dialogue"]
        url_list_pet_dialogue = get_all_urls_from_category(common.WIKI_URL["base"], base_url_pet_dialogue)

    if common.FETCH_LEVELUPMESSAGE:
        base_url_level_up_message = common.WIKI_URL["level_up_message"]
        url_list_level_up_message = get_all_urls_from_category(common.WIKI_URL["base"], base_url_level_up_message)



if __name__ == "__main__":
    scrape_wiki()