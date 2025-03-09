import json
import os
import requests
from bs4 import BeautifulSoup


def scrape_anthem(country_code):
    url = f"https://www.nationalanthems.info/{country_code}.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data for {country_code}: {e}")
        return None
      
    soup = BeautifulSoup(response.text, "html.parser")

    english_translation_div = soup.find("div", title=lambda x: x and "English" in x)
    if not english_translation_div:
        print(f"No English anthem found for {country_code}.")
        return None
    
    anthem_text = english_translation_div.find_next_sibling("div")

    if not anthem_text:
        print(f"No anthem text found for {country_code}.")
        return None
    
    anthem_text = anthem_text.get_text(separator="\n", strip=True)
    return anthem_text


def save_anthem(country_code, anthem_text):
    os.makedirs("anthems", exist_ok=True)
    file_path = os.path.join("anthems", f"{country_code}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(anthem_text)
    print(f"Anthem for {country_code} saved to {file_path}.")


def main(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    country_codes = data.get("countries", [])
    for country_code in country_codes:
        anthem_text = scrape_anthem(country_code)
        if anthem_text:
            save_anthem(country_code, anthem_text)


if __name__ == "__main__":
    main(r"C:\Users\ASUS\MMDP\Task_Analyzing_Flags_And_Anthems\Data_Collection\codes.json")