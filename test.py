from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from colorama import Fore

import time
import csv

from sources import CATEGORY_URLS, IMAGE_LIMIT, CSV_DOWNLOAD_PATH,IMAGE_DOWNLOAD_PATH, CATEGORIES, SAVE_BATCH_SIZE
from downloader import download_image
from email_service import send_email

wd = webdriver.Chrome()
IMG_CONTAINER_XPATH = "//div[@class='isv-r PNCib MSM1fd BUooTd']"
SHOW_MORE_BTN_XPATH = """//input[@class='LZ4I']"""
IMAGE_WINDOW_XPATH = """//img[@class='r48jcc pT0Scc iPVvYb']"""

def get_img_containers():
    try:
        print("\n🤖: Fetching image containers...")
        img_containers = wd.find_elements(By.XPATH, IMG_CONTAINER_XPATH)
        num_img_containers = len(img_containers)
        print(f"🤖: Found {num_img_containers} image containers!")
        return num_img_containers, img_containers
    except Exception as e:
        print("\n🔴🔴 Error while fetching image containers! 🔴🔴")

def load_all_thumbnails(url):
    
    wd.get(url)
    containers, img_containers = get_img_containers()

    while containers < IMAGE_LIMIT:
        print("🤖: Scrolling...")
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        containers, img_containers = get_img_containers()
        time.sleep(3)
        try:
            end_of_page = wd.find_element(By.XPATH, SHOW_MORE_BTN_XPATH).is_displayed()
            if end_of_page:
                wd.find_element(By.XPATH, SHOW_MORE_BTN_XPATH).click()
        except Exception as e:
            print("\n🔴🔴 Error finding the search more button! 🔴🔴")

    print(f"🤖: Found a total of {containers} image containers!") 
    wd.execute_script("window.scrollTo(0,0)")
    time.sleep(2)
    return containers, img_containers

def save_links(index, cache):
    print(Fore.GREEN + '📩📩 Saving to csv 📩📩')
    print(Fore.RESET)
    filename = f"./{CSV_DOWNLOAD_PATH}/{CATEGORIES[index]}.csv"
    
    try:
        with open(filename, 'a', newline='') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerows(cache)
    except Exception as e:
        print("\n🔴🔴 An error occured while saving the link into csv! 🔴🔴")
    

if __name__ == "__main__":
    
    wait = WebDriverWait(wd, 10)

    for category_index,category_url in enumerate(CATEGORY_URLS):
        load_count, img_containers = load_all_thumbnails(category_url)
        img_containers = img_containers[:IMAGE_LIMIT]
        complete_image = 0

        # while complete_image < IMAGE_LIMIT: 

        links_cache = []
        print("\nFetching Links...")
        img_count = 0

        for image in img_containers:
            image.click()
            time.sleep(2)
            try:
                img_window_check = wait.until(EC.visibility_of_element_located((By.XPATH, IMAGE_WINDOW_XPATH)))
                img_window = wd.find_element(By.XPATH, IMAGE_WINDOW_XPATH)
                # time.sleep(2)
                link = img_window.get_attribute('src')
                links_cache.append([link])
                print(Fore.CYAN + f"Link {img_count + 1}: " + link)

                if (img_count + 1) % SAVE_BATCH_SIZE == 0:
                    save_links(category_index, links_cache)
                    links_cache = []
                img_count += 1

            except Exception as e:
                print(" \n⚠️⚠️ Timeout error: An image took longer than expected to load! ⚠️⚠️")
                # print(e)
                continue
        print(Fore.RESET)
        save_links(category_index, links_cache)
        print("📧 Sending email!...")
        send_email(f"Finished scraping all {CATEGORIES[category_index]} images!")
        
    
    print("\n ✅✅✅✅ Links Scrapping Complete ✅✅✅✅ \n")
    print("🔵🔵🔵 Starting to download images 🔵🔵🔵")


    # Downloading images 
    for cat_idx, category in enumerate(CATEGORIES):
        with open(f"{CSV_DOWNLOAD_PATH}/{category}.csv", mode ='r')as file:
            print(f"\n🔻 Downloading {category} images : ")
            links_file = csv.reader(file)
            for img_index, link in enumerate(links_file):
                try:
                    download_image(link[0], category, str(img_index + 1), cat_idx)
                except Exception as e:
                    print(f"\n🔴🔴 An error occurred while downloading image no: {img_index + 1} 🔴🔴")
                    continue

            print(f"\n👍 {category} images downloaded : ")
