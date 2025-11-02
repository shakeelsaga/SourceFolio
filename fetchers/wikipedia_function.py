# This script is responsible for fetching data from Wikipedia.
# It provides functions to clean the search keyword and fetch data from Wikipedia.

import re
import wikipedia

# This function cleans the keyword by removing special characters.
# This helps to avoid errors when searching on Wikipedia.
def clean_keyword(keyword):
    return re.sub(r'[^a-zA-Z0-9\s\(\)\+\-]', '', keyword).strip()

# This function fetches data from Wikipedia for a given term.
# It can fetch either a summary or the full page content.
def get_wiki_data(term, is_detailed=False):
    term = clean_keyword(term)
    try:
        # If is_detailed is True, I'm fetching the full page content.
        if is_detailed:
            page = wikipedia.page(term, auto_suggest=False)
            return {
                "title": page.title,
                "content": page.content,
                "url": page.url
            }
        # Otherwise, I'm just fetching the summary.
        else:
            summary = wikipedia.summary(term, auto_suggest=False)
            page = wikipedia.page(term, auto_suggest=False)
            return {
                "title": page.title,
                "content": summary,
                "url": page.url
            }

    # I'm handling potential errors from the Wikipedia library.
    except wikipedia.exceptions.PageError:
        return None
        
    except wikipedia.exceptions.DisambiguationError as e:
        raise e
        
    except (KeyError, Exception):
        return None

# This block is for testing the script directly.
if __name__ == "__main__":
    keyword = "Halo (game)"
    # I'm fetching the summary for the keyword "Halo (game)".
    data = get_wiki_data(keyword, False)
    if data:
        print(data)
    else:
        print("No data retrieved.")