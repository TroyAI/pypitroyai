import requests
import pickle

from .files import StorageSystem

class ModelLoader:
    def __init__(self):
        self.storage_system = StorageSystem()
    
    def load_model(self, url: str):
        if self.storage_system.is_cached(url):
            return self.storage_system.load(url)
        else:
            return self.download_model(url)

    def download_model(self, url: str):
        # print("EXECUTING DOWNLOAD FROM SERVER")
        request = requests.get(url)
        pickled_model = request.content
        self.storage_system.save(url, pickled_model)
        return pickle.loads(pickled_model)