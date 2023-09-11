import os
from django.test import TestCase
from storage import Storage


class StorageTestCase(TestCase):
    def setUp(self):
        # create a file
        self.path = "/tmp"
        self.file = "./test.txt"
        with open(self.file, "w") as f:
            f.write("test")
        self.storage = Storage(storage_path=self.path)

    def tearDown(self):
        # delete the file
        os.remove(self.file)

    def test_upload(self):
        self.storage.upload(file=self.file)
        self.assertTrue(os.path.exists(f"{self.path}/{self.file}"))

        # test upload with folder
        self.storage.upload(file=self.file, folder="testing")
        self.assertTrue(os.path.exists(f"{self.path}/testing/{self.file}"))
        # test upload with filename
        self.storage.upload(file=self.file, filename="test2.txt")
        self.assertTrue(os.path.exists(f"{self.path}/test2.txt"))

    def test_delete(self):
        self.storage.upload(file=self.file)
        self.storage.delete(url="test.txt")
        self.assertFalse(os.path.exists(f"{self.path}/{self.file}"))

    def test_check(self):
        self.storage.upload(file=self.file)
        self.assertTrue(self.storage.check(url="test.txt"))

    def test_download(self):
        self.storage.upload(file=self.file, folder="testing")
        self.assertTrue(os.path.exists(f"{self.path}/testing/{self.file}"))
        filename = self.file.split("/")[-1]
        file = self.storage.download(url="testing/test.txt")
        with open(f"{self.path}/testing/{filename}", "rb") as f:
            self.assertEqual(f.read(), file)

        # Failed Download
        file = self.storage.download(url="testing/test2.txt")
        self.assertFalse(file)
