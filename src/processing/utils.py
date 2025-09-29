import time
import sys
import threading

def keyword_separator(keywords):
    li = []
    word = ""
    for i in range(0, len(keywords)):
        if keywords[i] != ",":
            word = word + keywords[i]
        else:
            li.append(word.strip().capitalize())
            word = ""
    if word:
        li.append(word.strip().capitalize())
    return li

def loading_dots(message, stop_event):
    while not stop_event.is_set():
        for dots in range(1, 4):
            if stop_event.is_set():
                break
            sys.stdout.write(f"\r{message}{'.' * dots}   ")
            sys.stdout.flush()
            time.sleep(0.5)
    sys.stdout.write("\r" + " " * (len(message) + 5) + "\r")

def status_update(message, success=True):
    symbol = "✔︎" if success else "✘"
    print(f"{message} {symbol}")

def fetch_with_animation(message, fetch_func, *args, **kwargs):
    stop_event = threading.Event()
    t = threading.Thread(target=loading_dots, args=(message, stop_event))
    t.start()
    try:
        result = fetch_func(*args, **kwargs)
        stop_event.set()
        t.join()
        status_update(message)
        return result
    except Exception as e:
        stop_event.set()
        t.join()
        status_update(message, success=False)
        raise e

def format_author(list):
    author = ""
    for auth in list:
        author = author + auth
    if author.strip() == "":
        author = "Unknown"

    return author