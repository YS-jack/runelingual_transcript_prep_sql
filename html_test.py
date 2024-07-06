# scrapes data from the osrs wiki and
# returns the data in a dictionary
# npc_dialogue includes dialogue, every option in option dialogue as different entry, and overhead

import common
import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import json

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
        return []
    
    # Step 2: Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')
    main_content = soup.find('div', class_='mw-parser-output')
    if not main_content:
        return []
    
    #the dialogue part
    li_elements = main_content.find_all('li')
    text_part_list = []

    entity_name = ''
    if category == common.WIKI_URL["npc_dialogue"]:
        entity_name = soup.find("h1", class_="firstHeading").get_text().replace("Dialogue for ", "").strip()

    
        for li in li_elements:
            if li.find('i') is None and li.find('a') is None and li.find('li') is None:
                b_tag = li.find('b')
                if b_tag:
                    speaker_name = b_tag.get_text().strip()
                    dialogue = li.get_text(strip=True).replace(speaker_name, '',1)
                    speaker_name = speaker_name.replace(":", "").strip()
                    text_part_list.append((speaker_name, dialogue))
                else:
                    #print("no b tag found for"+li.get_text().strip())
                    text_part_list.append((entity_name,li.get_text().strip()))


        #the option part
        option_elements = main_content.find_all('div', class_='transcript-opt')
        for option in option_elements:
            # Remove all <i> tags from the option element
            for i_tag in option.find_all('i'):
                i_tag.decompose()
            
            # Remove all <a> tags from the option element
            for a_tag in option.find_all('a'):
                a_tag.decompose()

            if option.find('li') is None:
                option_text = option.get_text().strip()
                if re.match(r"Dialogue \d+", option_text):
                    continue
                text_part_list.append(option_text)
        #print("number of raw text : ", len(raw_text_list))

        
        
        # Step 5: reformat the raw texts in raw_text_list[] and insert to data[]
        data_normal = []
        data_option = []
        for raw_text in text_part_list:
            # Check if the raw text is a tuple
            if isinstance(raw_text, tuple):
                speaker, dialogue = raw_text
                
                speaker = speaker.replace(":", "").replace("[sic]", "").strip()
                # Use re.sub to remove >[%s] at the beginning of dialogue
                dialogue = dialogue.replace("[sic]", "").strip()

                # Check if the dialogue is not empty
                if dialogue:
                    data_normal.append({common.COLUMN_NAME_ENGLISH: dialogue, 
                                common.COLUMN_NAME_CATEGORY:common.NPC_DIALOGUE_VAR_NAME, 
                                common.COLUMN_NAME_SUB_CATEGORY:entity_name, 
                                common.COLUMN_NAME_SOURCE:speaker, 
                                common.COLUMN_NAME_NOTES:"",
                                common.COLUMN_NAME_DATE_MODIFIED:common.TODAYS_DATE,
                                common.COLUMN_NAME_WIKI_URL:url})
            else:
                # Check if the raw text is not empty
                if raw_text:
                    raw_text = raw_text.replace("[sic]", "").strip()
                    data_option.append({common.COLUMN_NAME_ENGLISH: raw_text, 
                                common.COLUMN_NAME_CATEGORY:common.NPC_DIALOGUE_VAR_NAME, 
                                common.COLUMN_NAME_SUB_CATEGORY:entity_name, 
                                common.COLUMN_NAME_SOURCE:entity_name, 
                                common.COLUMN_NAME_NOTES:"probably an option",
                                common.COLUMN_NAME_DATE_MODIFIED:common.TODAYS_DATE,
                                common.COLUMN_NAME_WIKI_URL:url})
        data = data_normal + data_option
    
    return data

def get_all_urls_of_entity(base_url, url):
    """
    Get all the URLs from every page of the category
    """
    # Step 1: Fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the webpage content for {url}.")
        return []


    # Step 2: Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')
    nextpage_tag = soup.find("a", string="next page")

    links = get_all_urls_in_page(soup, base_url)

    # Check if the 'next page' tag exists
    if not nextpage_tag:
        return links

    # Step 3: get the 'next page' url path
    next_url_path = soup.find("a", string="next page")["href"]
    next_page_link = base_url + next_url_path

    return links + get_all_urls_of_entity(base_url, next_page_link)

def get_all_urls_in_page(soup, base_url):
    """
    gets all urls in the page thats starts with "/w/Transcript:"
    args:
    soup: BeautifulSoup object

    return:
    list of urls in the page
    """
    links = []
    for link in soup.find_all("a"):
        if link.get("href") and link.get("href").startswith("/w/Transcript:"):
            links.append(base_url + link.get("href"))
    return links

def scrape_wiki(): 
    """
    1. get the base url for list for each category
    2. get all the urls for every page of the category
    3. get the data from each page in dictionary form, to tell what entity we are interacting with
    4. return the data
    """
    data_npc_dialogue = []
    if common.FETCH_NPCDIALOGUE:
        # Step 1: Get the base URL for each category
        base_url_npc_dialogue = common.WIKI_URL["npc_dialogue"]

        # Step 2: Get all the URLs for every page of the npc's dailogue, like "Banker (Al Kharid)" etc.
        url_list_npc_dialogue = get_all_urls_of_entity(common.WIKI_URL["base"], base_url_npc_dialogue)
        #print("number of npcs: ",len(url_list_npc_dialogue))
        
        # Step 3: Get the data from each page in dictionary form
        for url in url_list_npc_dialogue:
            print("fetching from : ", url)
            dialogue_data = get_data_from_wiki_page(url, common.WIKI_URL["npc_dialogue"])
            data_npc_dialogue += dialogue_data
            #print(dialogue_data)
        
        """#for debugging
        dialogue_data = get_data_from_wiki_page("https://oldschool.runescape.wiki/w/Transcript:Ali_the_Camel_Man", common.WIKI_URL["npc_dialogue"])
        for dialogue in dialogue_data:
            print(dialogue['english'])
            print()
        print(len(dialogue_data))"""
        
    data_pet_dialogue = []
    if common.FETCH_PETDIALOGUE:
        base_url_pet_dialogue = common.WIKI_URL["pet_dialogue"]
        url_list_pet_dialogue = get_all_urls_of_entity(common.WIKI_URL["base"], base_url_pet_dialogue)
        for url in url_list_pet_dialogue:
            print("fetching from : ", url)
            dialogue_data = get_data_from_wiki_page(url, common.WIKI_URL["npc_dialogue"])
            data_pet_dialogue += dialogue_data

    """if common.FETCH_LEVELUPMESSAGE:
        base_url_level_up_message = common.WIKI_URL["level_up_message"]
        url_list_level_up_message = get_all_urls_of_entity(common.WIKI_URL["base"], base_url_level_up_message)"""
    for data in data_pet_dialogue:
        print(data)
    return data_pet_dialogue



if __name__ == "__main__":
    scrape_wiki()
    #scrape_chisel(common.CHISEL_URL["item_main"], common.CHISEL_URL["items_main"])
    #scrape_chisel(common.CHISEL_URL["npc_main"], common.CHISEL_URL["npc_examine"])
    #scrape_chisel(common.CHISEL_URL["object_main"], common.CHISEL_URL["object_examine"])