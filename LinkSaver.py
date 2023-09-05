import pandas as pd

class LinkSaver:
    
    def __init__(self, path) -> None:
        self.__path = path

    def save_to_csv(self, links, filename):
        df = pd.DataFrame(links, columns = ["Links"])
        df.to_csv(f"{self.__path}/{filename}", index = False)
