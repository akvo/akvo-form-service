import os
from pathlib import Path
import shutil


class Storage:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def upload(self, file: str, folder: str = None, filename: str = None):
        storage_location = self.storage_path
        if folder:
            Path(f"{storage_location}/{folder}").mkdir(parents=True, exist_ok=True)
            storage_location = f"{storage_location}/{folder}"
        if not filename:
            filename = file.split("/")[-1]
        location = f"{storage_location}/{filename}"
        shutil.copy2(file, location)
        return location

    def delete(self, url: str):
        os.remove(f"{self.storage_path}/{url}")
        return url

    def check(self, url: str):
        path = Path(f"{self.storage_path}/{url}")
        return path.is_file()

    def download(self, url: str):
        return f"{self.storage_path}/{url}"
