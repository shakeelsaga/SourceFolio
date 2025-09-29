import re
import wikipedia

def clean_keyword(keyword):
    return re.sub(r'[^a-zA-Z0-9\s\(\)\+\-]', '', keyword).strip() #remove unwanted characters in the keywords

#fetching wiki data
def get_wiki_data(term, is_detailed = False):
    term = clean_keyword(term)
    try:
        if is_detailed:
            page = wikipedia.page(term, auto_suggest=False)
            return {
                "title": page.title,
                "content": page.content,
                "url": page.url
            }
        else:
            summary = wikipedia.summary(term, auto_suggest=False)
            page = wikipedia.page(term, auto_suggest=False)
            return {
                "title": page.title,
                "content": summary,
                "url": page.url
            }

    except wikipedia.exceptions.DisambiguationError as e:
        print(f"DisambiguationError: The term '{term}' may refer to multiple pages: {e.options}")
        return None
    except wikipedia.exceptions.PageError:
        print(f"PageError: The page for term '{term}' does not exist.")
        return None
    except KeyError as e:
        print(f"KeyError: Missing key {e} in Wikipedia response.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    keyword = "Halo (game)"
    data = get_wiki_data(keyword, False)
    if data:
        print(data)
    else:
        print("No data retrieved.")
