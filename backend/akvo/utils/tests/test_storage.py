import os
from django.test import TestCase
from storage import Storage


class StorageTestCase(TestCase):
    def setUp(self):
        # Create a temporary directory if it doesn't exist
        if not os.path.exists("/tmp"):
            os.mkdir("/tmp")
        # create a file
        self.file = "./test.txt"
        with open(self.file, "w") as f:
            f.write("test")
        self.storage = Storage(storage_path="/tmp")

    def test_upload(self):
        self.storage.upload(file=self.file)
        self.assertTrue(os.path.exists(self.file))

    def test_delete(self):
        self.storage.upload(file=self.file)
        self.storage.delete(url="test.txt")
        self.assertFalse(os.path.exists(self.file))

    def test_check(self):
        self.storage.upload(file=self.file)
        self.assertTrue(self.storage.check(url="test.txt"))

    def test_download(self):
        self.storage.upload(file=self.file)
        self.assertEqual(self.storage.download(url="test.txt"), self.file)
