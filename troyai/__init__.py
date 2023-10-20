from .download import ModelLoader
from .upload import upload_model

model_downloader = ModelLoader()
load_model = model_downloader.load_model