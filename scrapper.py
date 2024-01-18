import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from sklearn.model_selection import train_test_split

# Function to fetch image URLs from Google Images
# Function to fetch image URLs from Google Images
def fetch_google_images(query, num_images=10):
    url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    
    # Use Selenium to load the page and scroll to fetch more images
    driver = webdriver.Chrome()  # Ensure you have the Chrome driver installed and in your PATH
    driver.get(url)

    image_urls = []
    while len(image_urls) < num_images:
        # Scroll down to fetch more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time based on your internet speed

        # Click the "Load more images" button
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, 'input[value="Show more results"]')
            if load_more_button:
                load_more_button.click()
        except:
            print("Load more images button not found or unable to click.")

        # Extract image URLs
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_tags = soup.find_all('img', attrs={'class': 'rg_i'})
        for img_tag in img_tags[len(image_urls):]:
            img_url = img_tag.get('src')
            if img_url:
                image_urls.append(img_url)
                if len(image_urls) == num_images:
                    break

    driver.quit()
    return image_urls

# Function to download images from URLs and split them into train and test sets
def download_images_and_split(image_urls, train_size=0.8, output_folder="downloaded_images", keyword=""):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Split the image URLs into train and test sets
    train_images, test_images = train_test_split(image_urls, train_size=train_size, random_state=42)

    # Save train images
    train_folder = os.path.join(output_folder, keyword, "train")
    if not os.path.exists(train_folder):
        os.makedirs(train_folder)
    save_images(train_images, train_folder)

    # Save test images
    test_folder = os.path.join(output_folder, keyword, "test")
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    save_images(test_images, test_folder)

def save_images(image_urls, output_folder):
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            with open(os.path.join(output_folder, f"image_{i}.jpg"), "wb") as img_file:
                img_file.write(response.content)
        except Exception as e:
            print(f"Failed to download image {i}: {str(e)}")

indian_foods = [
    # South Indian
    "Dosa",
    "Idli",
    "Sambhar",
    "Uttapam",
    "Pongal",

    # North Indian
    "Biryani",
    "Naan",
    "Butter Chicken",
    "Chole Bhature",
    "Rajma Chawal",

    # East Indian
    "Rosogolla",
    "Sorshe Ilish (Mustard Hilsa)",
    "Machher Jhol (Fish Curry)",
    "Mishti Doi (Sweet Yogurt)",
    "Sandesh",

    # West Indian
    "Vada Pav",
    "Dhokla",
    "Pav Bhaji",
    "Fafda",
    "Thepla"
]

for i in indian_foods:
    keyword = i  # Replace with the keyword you want to search for
    num_images = 500  # Number of images to fetch and download
    train_size = 0.8  # Train size (proportion)
    output_folder = "downloaded_images/" # Folder to save downloaded images

    # Fetch image URLs
    image_urls = fetch_google_images(keyword, num_images)

    # Print the image URLs
    print("Image URLs:")
    for i, url in enumerate(image_urls):
        print(f"{i+1}. {url}")

    # Download images and split into train and test sets
    download_images_and_split(image_urls, train_size, output_folder, keyword)

    print("Downloaded images saved in the train and test folders.")
