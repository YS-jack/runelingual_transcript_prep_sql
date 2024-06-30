# scrapes data from the osrs wiki and
# returns the data in a dictionary

import common
import requests
from bs4 import BeautifulSoup

def get_data_from_wiki(url, name):
    """
    Scrapes data from the OSRS wiki and returns the data in a dictionary
    """
    # Step 1: Fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the webpage content for {name}.")
        return {}
    
    # Step 2: Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Step 3: Extract the data
    data = soup.find_all("div", class_="mw-category-group")
    # Step 4: Return the data
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
    # Step 1: Get the base URL for each category
    base_url_npc_dialogue = common.WIKI_URL["npc_dialogue"]
    base_url_pet_dialogue = common.WIKI_URL["pet_dialogue"]
    base_url_level_up_message = common.WIKI_URL["level_up_message"]

    # Step 2: Get all the URLs for every page of the category
    url_list_npc_dialogue = get_all_urls_from_category(common.WIKI_URL["base"], base_url_npc_dialogue)
    url_list_pet_dialogue = get_all_urls_from_category(common.WIKI_URL["base"], base_url_pet_dialogue)
    url_list_level_up_message = get_all_urls_from_category(common.WIKI_URL["base"], base_url_level_up_message)

    

if __name__ == "__main__":
    scrape_wiki()