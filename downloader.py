from threading import Thread, Lock
import requests as req
import io
from PIL import Image
import os
import time

class Downloader:

    def __init__(self, path, min_num_threads = 5) -> None:
        self.__path = path
        self.__min_num_threads = min_num_threads

    def _create_threads(self):
        num_batches = self.__min_num_threads
        total_links = len(self.__image_links)
        batch_size = total_links // num_batches
        leftover = total_links % batch_size

        for i in range(self.__min_num_threads):
            start_idx = i * batch_size
            end_idx = (i + 1) * batch_size
            thread = Thread(target = self.download_image, args = (i+1, start_idx, end_idx))
            self.__threads_pool.append(thread)

        if leftover > 0:
            start_idx = num_batches * batch_size
            end_idx = total_links
            thread = Thread(target = self.download_image, args = (i+2, start_idx, end_idx))
            self.__threads_pool.append(thread)
        
        for thread in self.__threads_pool:
            thread.start()
    
    def _destroy_threads(self):
        for thread in self.__threads_pool:
            thread.join()

    def download(self, image_links, category):
        self.__threads_pool = []
        self.__image_links = image_links
        self.__category = category

        check_path = f"{self.__path}/{self.__category}"
        if not os.path.exists(check_path):
            os.makedirs(check_path)

        self._create_threads()
        self._destroy_threads()
        
    def download_image(self, thread_num,  start_idx, end_idx):
            print(f"Thread {thread_num} running: ")
            # for link in enumerate(self.__image_links):
            for i in range(start_idx, end_idx):
                try:
                    file_name = f"{self.__category}_{i + 1}.jpg"
                    image_content = req.get(self.__image_links[i], timeout = 10).content
                    image_file = io.BytesIO(image_content)
                    pil_image = Image.open(image_file)
                except Exception as e:
                    print(f"🔴🔴🔴 Error while downloading the image: {i + 1}! 🔴🔴🔴")
                    continue

                if len(pil_image.getbands()) == 3:
                    try:
                        file_path = f"{self.__path}/{self.__category}/{file_name}"
                        with open(file_path, "wb") as f:
                            pil_image.save(f)
                        print("Downloaded: ", file_name)
                    except Exception as e:
                        print(f"🔴🔴🔴 Error while saving the image no: {i + 1} 🔴🔴🔴")
                else:
                    print("🔵🔵 An image with alpha channel found, hence discarding it!! 🔵🔵")

