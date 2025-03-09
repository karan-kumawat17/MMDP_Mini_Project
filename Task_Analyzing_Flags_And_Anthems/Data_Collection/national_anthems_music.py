import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_anthem_audio(country_code):
    os.makedirs("anthems_audio", exist_ok=True)
    file_path = os.path.join("anthems_audio", f"{country_code}.mp3")
    url = f"https://www.nationalanthems.info/{country_code}.mp3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Anthem for {country_code} saved to {file_path}.")
        else:
            print(f"Failed to fetch data for {country_code}.")
    except requests.RequestException as e:
        print(f"Failed to fetch data for {country_code}: {e}")
        return None
        

def main(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    country_codes = data.get("countries", [])
    for country_code in country_codes:
        scrape_anthem_audio(country_code)


if __name__ == "__main__":
    main(r"C:\Users\ASUS\MMDP\Task_Analyzing_Flags_And_Anthems\Data_Collection\codes.json")