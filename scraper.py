import requests
from bs4 import BeautifulSoup

# Send GET request to fetch page content
response = requests.get("https://kubernetes.io/docs/reference/glossary/?fundamental=true")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tags that may contain the required glossary terms under "fundamental"
    glossary_items = soup.select('li[data-show-count="0"]')

    # Dictionary to hold the extracted information
    glossary_terms = {}

    for item in glossary_items:
        # The term is contained in the 'b' tag within '.term-name'
        term = item.select_one('.term-name b').text

        # The main definition comes after the term name, within 'span.preview-text'
        definition = item.select_one('span.preview-text').text.strip()

        # The supplemental definition, if it exists, is within the hidden next sibling div
        supplemental_div = item.select_one('div.hide')
        if supplemental_div:
            # Use `get_text()` to extract all text within supplemental_div, 
            # separating via `\n` and removing any excess whitespace
            supplemental_definition = supplemental_div.get_text(separator='\n', strip=True)
        else:
            supplemental_definition = ""

        # Store the definitions in the glossary dictionary using the term name as the key
        glossary_terms[term] = {
            'definition': definition,
            'supplemental_definition': supplemental_definition
        }

    # Display the content in the desired format
    for term, contents in glossary_terms.items():
        print(f"Term: {term}")
        print(f"Definition: {contents['definition']}")
        supplemental = contents['supplemental_definition'].replace('\n', '\n\n')
        print(f"Supplemental definition: {supplemental}\n")
else:
    print("Failed to fetch the glossary content.")

# end of script