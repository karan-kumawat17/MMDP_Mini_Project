import os
import requests
import re
import string
from bs4 import BeautifulSoup
import nltk
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("wordnet")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm


# Function to clean text using NLP preprocessing techniques:
def clean_text(text):
    text = re.sub(r'<[^>]+>', "", text)     # To remove HTML tags
    text = re.sub(r"\s+", " ", text)        # To remove extra whitespaces
    text = re.sub(r"\n+", " ", text)       # To remove extra newlines
    text = text.lower()         
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    words = word_tokenize(text)
    words = [word for word in words if word.isalnum()]

    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    text = " ".join(words)

    return text


# Format text:
def format_text(text):
    lines = text.split("\n")
    formatted_lines = []

    for line in lines:
        if line.startswith("📌") or line.startswith("📅") or line.startswith("=") or line.startswith("-"):
            formatted_lines.append(line)
        else:
            cleaned_line = clean_text(line)
            formatted_lines.append(cleaned_line)

    return "\n".join(formatted_lines)

# Function to scrape text data from the web:
def scrape_text(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string if soup.title else "No Title"

            date_tag = soup.find("time")
            pub_date = date_tag["datetime"] if date_tag else "Unknown Date"

            paragraphs = soup.find_all("p")
            content = "\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])

            if content:
                return f"\n{'='*50}\n📌 Title: {title}\n📅 Date: {pub_date}\n{'-'*50}\n{content}\n{'='*50}\n"
            else:
                return ""
        else:
            return ""
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return ""
    

# Function to process and save data for a specific category:
def process_category(category, urls):
    os.makedirs("DiverseTexts", exist_ok=True)
    file_path = os.path.join("DiverseTexts", f"{category.replace(' ', '_')}.txt")
    
    with open(file_path, "w", encoding="utf-8") as file:
        for url in tqdm(urls, desc=f"Processing {category}"):
            print(f"Scraping data from {url}...")
            article_data = scrape_text(url)
            if article_data:
                cleaned_data = format_text(article_data)
                file.write(cleaned_data + "\n")
            else:
                print(f"No relevant data found for {category} on {url}.\n")

    print(f"Data saved to {file_path}")


# Main function to automate text data collection:
def main():
    categories = {
        "technology": ["https://techcrunch.com", "https://www.wired.com", "https://arstechnica.com"],
        "science": ["https://www.sciencedaily.com", "https://www.nature.com", "https://www.scientificamerican.com"],
        "health": ["https://www.webmd.com", "https://www.healthline.com", "https://www.mayoclinic.org"],
        "business": ["https://www.bloomberg.com", "https://www.forbes.com", "https://www.cnbc.com"],
        "sports": ["https://www.espn.com", "https://www.bbc.com/sport", "https://www.si.com"],
        "politics": ["https://www.bbc.com/news/politics", "https://www.politico.com", "https://www.theguardian.com/politics"],
        "entertainment": ["https://variety.com", "https://www.hollywoodreporter.com", "https://www.rottentomatoes.com"],
        "education": ["https://www.edsurge.com", "https://www.insidehighered.com", "https://www.chronicle.com"],
        "environment": ["https://www.nationalgeographic.com/environment", "https://www.enn.com", "https://news.mongabay.com"],
        "finance": ["https://www.investopedia.com", "https://www.marketwatch.com", "https://www.fool.com"],
        "history": ["https://www.history.com", "https://www.smithsonianmag.com/history", "https://www.bbc.co.uk/history"],
        "travel": ["https://www.lonelyplanet.com", "https://www.nationalgeographic.com/travel", "https://thepointsguy.com"],
        "food": ["https://www.seriouseats.com", "https://www.bonappetit.com", "https://www.thespruceeats.com"],
        "automotive": ["https://www.motortrend.com", "https://www.caranddriver.com", "https://www.autoblog.com"],
        "fashion": ["https://www.vogue.com", "https://www.elle.com", "https://www.harpersbazaar.com"],
        "cybersecurity": ["https://krebsonsecurity.com", "https://www.darkreading.com", "https://www.bleepingcomputer.com"],
        "ai_ml": ["https://towardsdatascience.com", "https://openai.com/research", "https://ai.googleblog.com"],
        "space": ["https://www.nasa.gov", "https://www.space.com", "https://www.universetoday.com"],
        "economy": ["https://www.economist.com", "https://www.weforum.org", "https://www.ft.com"],
        "philosophy": ["https://iai.tv", "https://plato.stanford.edu", "https://www.iep.utm.edu"]
    }

    for category, urls in tqdm(categories.items(), desc="Scraping Categories"):
        process_category(category, urls)

    print("\nText data collection completed! Files saved in 'DiverseTexts/' directory.")

if __name__ == "__main__":
    main()