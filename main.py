from scraping import Scraper
from utils.email_sender import EmailSender
from utils.link_saver import LinkSaver
from downloader.downloader import Downloader
import yaml

def main():
    with open("./config.yaml", "r") as file:
        config = yaml.safe_load(file)

    search_queries = config['search_queries']
    sender_email = config['sender_email']
    receiver_email = config['receiver_email']
    sender_email_password = config['sender_email_password']
    images_limit = config['images_limit']
    csv_path = config['csv_path']
    image_path = config['image_path']
    send_email_bool = config['send_email']

    print("Scraping: ",search_queries)
    scraper = Scraper(num_threads = 5, show_ui = True)
    email_sender = EmailSender(
        sender = sender_email,
        receiver = receiver_email,
        sender_password = sender_email_password
    )
    link_saver = LinkSaver(path = csv_path)
    downloader = Downloader(path = image_path)

    for query in search_queries:
        scraped_links = scraper.scrape(query = query, count = images_limit)
        link_saver.save_to_csv(links = scraped_links, filename = f"{query}.csv")
        downloader.download(list(scraped_links), query)

        if send_email_bool:
            email_sender.send_email(message = f"Finished Scraping {query} images")


if __name__ == "__main__":
    main()