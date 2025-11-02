# This script handles the configuration for the application,
# like storing and retrieving API keys.
# It creates a .sourcefolio directory in the user's home directory to store the config file.

from pathlib import Path
import json

# I'm defining the directory and file for the configuration.
# It's good practice to keep configuration files in a hidden directory in the user's home.
CONFIG_DIR = Path.home() / ".sourcefolio"
CONFIG_FILE = CONFIG_DIR / "config.json"

# I'm creating the directory if it doesn't exist.
CONFIG_DIR.mkdir(exist_ok=True)

# This function saves the configuration data to the config file.
def save_config(data):
    # I'm opening the config file in write mode and saving the data in JSON format.
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

# This function loads the configuration data from the config file.
def load_config():
    # If the config file doesn't exist, I'm returning an empty dictionary.
    if not CONFIG_FILE.exists():
        return {}
    # I'm opening the config file in read mode and loading the JSON data.
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        # If the file is empty or corrupted, I'm returning an empty dictionary.
        except json.JSONDecodeError:
            return {}

# This function retrieves an API key from the configuration.
def get_api_key(service_name="NEWS_API_KEY"):
    # I'm loading the configuration and getting the API key for the specified service.
    config = load_config()
    return config.get(service_name)

# This function saves an API key to the configuration.
def save_api_key(key, service_name="NEWS_API_KEY"):
    # I'm loading the configuration, adding the new API key, and saving the configuration.
    config = load_config()
    config[service_name] = key
    save_config(config)
