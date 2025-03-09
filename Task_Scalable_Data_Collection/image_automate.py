import os
import csv
import time
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup WebDriver with options
def setup_driver():
    driver_path = r"C:\Users\ASUS\MMDP\Task_Scalable_Data_Collection\drivers\chromedriver-win32\chromedriver.exe"
    service = Service(driver_path)  # Adjust the path to your ChromeDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Ensure headless is being added as an argument
    options.add_argument("--disable-gpu")  # This option is often recommended to run headless
    options.add_argument("--window-size=1920,1080")  # Specify the window size
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    options.add_argument("--log-level=OFF")
    options.add_argument("--disable-logging")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # This option specifically targets ChromeDriver logs.
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Search images on Google per query 50 images
def search_images(driver, query, num_images=50):
    driver.get("https://www.google.com/imghp?hl=en")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query + Keys.RETURN)
    time.sleep(5)  # Adjust timing based on your testing
    
    image_urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(image_urls) < num_images:
        # images = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
        images = driver.find_elements(By.CSS_SELECTOR, "img")
        for img in images:
            try:
                # img.click()
                # time.sleep(2)
                # # full_image = driver.find_element(By.CSS_SELECTOR, "img.n3VNCb")
                # full_image = WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, "img.n3VNCb"))
                # )
                
                src = img.get_attribute("src") or img.get_attribute("data-src")
                if src and src.startswith("http") and src not in image_urls:
                    image_urls.add(src)
                if len(image_urls) >= num_images:
                    break
            except Exception as e:
                print(f"Error fetching image {img} for {query}: {e}")

            
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return list(image_urls)[:num_images]


# Create directory structure to store images for each category:
def create_directories(categories):
    os.makedirs("DiverseVisuals", exist_ok=True)
    for category in categories:
        folder_path = os.path.join("DiverseVisuals", category.replace(" ", "_"))
        os.makedirs(folder_path, exist_ok=True)


# Save images to the respective category folders:
def download_images(image_urls, category):
    folder_path = os.path.join("DiverseVisuals", category.replace(" ", "_"))
    metadata = []

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code == 200:
                filename = f"{category.replace(' ', '_')}_{i+1}.jpg"
                file_path = os.path.join(folder_path, filename)
                img = Image.open(BytesIO(response.content))
                img.save(file_path, "PNG")
                resolution = f"{img.width}x{img.height}"
                metadata.append([category, filename, url, resolution])
        except Exception as e:
            print(f"Error downloading image {i} for {category}: {e}")
    return metadata


# Save metadata to a CSV file:
def save_metadata(metadata):
    with open("DiverseVisuals/metadata.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Filename", "URL", "Resolution"])
        writer.writerows(metadata)

def main():
    categories = [
        "Vintage Cameras", "Underwater Coral Reefs", "Street Art Murals",
        "Astronaut Suits", "Ancient Ruins", "Futuristic Cities",
        "Exotic Fruits", "Handmade Pottery", "Wildlife in Snow",
        "Abstract Paintings", "Hot Air Balloons", "Lush Green Valleys",
        "Robotic Arms", "Traditional Festivals", "Crystal Caves",
        "Desert Landscapes", "Vintage Typewriters", "Aurora Borealis",
        "Steampunk Gadgets", "Zen Gardens"
    ]

    driver = setup_driver()
    create_directories(categories)
    all_metadata = []

    for category in categories:
        print(f"Fetching images for {category}...")
        image_urls = search_images(driver, category)
        print(f"Downloading {len(image_urls)} images for {category}...")
        metadata = download_images(image_urls, category)
        all_metadata.extend(metadata)

    save_metadata(all_metadata)
    driver.quit()
    print("Image collection completed successfully!")

if __name__ == "__main__":
    main()


