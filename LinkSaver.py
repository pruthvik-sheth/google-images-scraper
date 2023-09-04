import pandas as pd

class LinkSaver:
    
    def __init__(self) -> None:
        pass

    def save_to_csv(self, links, filename):
        df = pd.DataFrame(links, columns = ["Links"])
        df.to_csv(filename, index = False)
