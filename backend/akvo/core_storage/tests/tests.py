import os
from django.test import TestCase
from akvo.utils import storage

STORAGE_PATH = os.environ.get("STORAGE_PATH")
storage = storage.Storage(storage_path=STORAGE_PATH)


def generate_image(filename: str, extension: str = "jpg"):
    filename = f"./{filename}.{extension}"
    f = open(filename, "a")
    f.write("This is a test file!")
    f.close()
    return f"./{filename}"


class ImageUploadTest(TestCase):
    def test_image_upload(self):
        filename = generate_image(filename="test", extension="png")
        file = open(filename, "rb")
        response = self.client.post(
            "/api/upload/images/",
            {"file": file},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.json()), ["message", "file"])
        uploaded_filename = response.json().get("file")
        self.assertTrue(
            storage.check(uploaded_filename),
            f"File {uploaded_filename} was not uploaded to the storage.",
        )
        os.remove(f"{STORAGE_PATH}/{uploaded_filename}")
        os.remove(filename)

    def test_wrong_extension_upload(self):
        filename = generate_image(filename="test", extension="txt")
        response = self.client.post(
            "/api/upload/images/",
            {"file": open(filename, "rb")},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            "File extension “txt” is not allowed. Allowed extensions are: jpg, png, jpeg.",  # noqa
        )
        os.remove(filename)
