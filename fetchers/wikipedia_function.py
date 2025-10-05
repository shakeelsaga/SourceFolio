import re
import wikipedia

def clean_keyword(keyword):
    return re.sub(r'[^a-zA-Z0-9\s\(\)\+\-]', '', keyword).strip()

def get_wiki_data(term, is_detailed=False):
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

    except wikipedia.exceptions.PageError:
        return None
        
    except wikipedia.exceptions.DisambiguationError as e:
        raise e
        
    except (KeyError, Exception):
        return None

if __name__ == "__main__":
    keyword = "Halo (game)"
    data = get_wiki_data(keyword, False)
    if data:
        print(data)
    else:
        print("No data retrieved.")