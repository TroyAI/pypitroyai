import os
import pickle
from urllib.parse import quote_plus, unquote_plus

class StorageSystem:
    FOLDER_NAME = "./.troyai_cache"
    
    def __init__(self):
        if not os.path.exists(self.FOLDER_NAME):
            os.mkdir(self.FOLDER_NAME)
        
    def is_cached(self, url: str):
        return url in self.saved_urls
    
    @property
    def saved_urls(self):
        return [unquote_plus(url) for url in os.listdir(self.FOLDER_NAME)]

    @classmethod
    def url_to_path(cls, url: str):
        return f"{cls.FOLDER_NAME}/{quote_plus(url)}"
    
    def save(self, url: str, pickled_model):
        with open(StorageSystem.url_to_path(url), "wb") as f:
            f.write(pickled_model)
    
    def load(self, url: str):
        # print("LOADING FROM LOCAL CACHE")
        with open(StorageSystem.url_to_path(url), "rb") as f:
            return pickle.load(f)
    
    