from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread, Lock
from urllib import parse
from colorama import Fore
import time
import csv
class Scraper:
    
    def __init__(self, num_threads = 1, show_ui = True) -> None:
        self.__num_threads = num_threads
        self.__show_ui = show_ui
        self.__threads_pool = []
        self.__shared_index = 0
        self.__shared_index_lock = Lock()
        self.__images = set()

    def _create_threads(self):
        
        for i in range(self.__num_threads):
            thread = Thread(target = self._get_images)
            self.__threads_pool.append(thread)
            thread.start()

    def _destroy_threads(self):
        for thread in self.__threads_pool:
            thread.join()

    def _create_driver(self):
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument("incognito")
        if not self.__show_ui:
            self.__options.add_argument("headless")
        driver = webdriver.Chrome()
        return driver

    def _load_thumbnails(self, driver):
        def get_thumbnails():
            try:
                print("\n🤖: Fetching image containers...")
                thumbnails = driver.find_elements(By.XPATH, "//div[@class='isv-r PNCib MSM1fd BUooTd']")
                print(f"🤖: Found {len(thumbnails)} image containers!")
            except Exception as e:
                print("\n🔴🔴 Error while fetching image containers! 🔴🔴")
            return thumbnails
        thumbnails = get_thumbnails()

        while len(thumbnails) < self.__image_limit:
            print("🤖: Scrolling...")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            thumbnails = get_thumbnails()
            time.sleep(3)
            try:
                end_of_page = driver.find_element(By.XPATH, """//input[@class='LZ4I']""").is_displayed()
                if end_of_page:
                    driver.find_element(By.XPATH, """//input[@class='LZ4I']""").click()
            except Exception as e:
                print("\n🔴🔴 Error finding the search more button! 🔴🔴")

        print(f"🤖: Found a total of {len(thumbnails)} image containers!") 
        driver.execute_script("window.scrollTo(0,0)")
        time.sleep(2)
        return thumbnails

    def _get_images(self):
        driver = webdriver.Chrome()
        driver.get(self.__url)
        thumbnails = self._load_thumbnails(driver)
        
        wait = WebDriverWait(driver, 10)
        print("\nFetching Links...")

        while len(self.__images) < self.__image_limit:   
            self.__shared_index_lock.acquire()
            index = self.__shared_index
            self.__shared_index += 1
            self.__shared_index_lock.release()
            try:
                if not index >= self.__image_limit:
                    # print(len(self.__images))
                    thumbnails[index].click()
                    # print(index)
                    time.sleep(2)
                    wait.until(EC.visibility_of_element_located((By.XPATH, """//img[@class='r48jcc pT0Scc iPVvYb']""")))
                    img_window = driver.find_element(By.XPATH, """//img[@class='r48jcc pT0Scc iPVvYb']""")
                    # time.sleep(2)
                    link = img_window.get_attribute('src')
                    self.__images.add(link)
                    print(link)
                else:
                    print("✔️✔️✔️ Links Scraping complete! ✔️✔️✔️")
                    break
                                    
            except Exception as e:
                print(" \n🔴🔴🔴 An error occurred! 🔴🔴🔴")
                continue

    @staticmethod
    def create_url(search_query):
        parsed_query = parse.urlencode({'q': search_query})
        url = f"https://www.google.com/search?{parsed_query}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR5qK3rcbxAhXYF3IKHYiBDf8Q_AUoAXoECAEQAw&biw=1291&bih=590"
        return url

    def scrape(self, query, count):
        self.__url = self.create_url(query)
        self.__image_limit = count
        start = time.time()
        self._create_threads()
        self._destroy_threads()
        end = time.time()
        print(len(self.__images))
        
        print(f"Total elapsed time for {self.__image_limit} images is: {(end - start) / 60} mins")
        return self.__images
