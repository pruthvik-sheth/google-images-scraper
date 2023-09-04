from scraper import Scraper
from config import SEARCH_QUERIES, IMAGES_LIMIT



if __name__ == "__main__":
    sc = Scraper(num_threads = 5, show_ui = True)
    sc.scrape(query = "living room", count = 200)


