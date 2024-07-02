from bs4 import BeautifulSoup
import requests

def get_li_text(url):
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
    text_parts = []

    for li in li_elements:
        if li.find('i') is None and li.find('a') is None and li.find('li') is None:
            text_parts.append(li.get_text().strip())


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
            text_parts.append(option.get_text().strip())
    return text_parts

# Example usage
file_path = 'your_file.html'  # Replace with your HTML file path
li_texts = get_li_text("https://oldschool.runescape.wiki/w/Transcript:Ali_the_Camel_Man")
for i,text in enumerate(li_texts):
    print(f'{i}: \n'+text)
