from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".sourcefolio"
CONFIG_FILE = CONFIG_DIR / "config.json"

CONFIG_DIR.mkdir(exist_ok=True)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def get_api_key(service_name="NEWS_API_KEY"):
    config = load_config()
    return config.get(service_name)

def save_api_key(key, service_name="NEWS_API_KEY"):
    config = load_config()
    config[service_name] = key
    save_config(config)
