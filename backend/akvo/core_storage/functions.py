from os import environ, path, mkdir
from uuid import uuid4
from akvo.utils import storage

storage = storage.Storage(storage_path=environ.get("STORAGE_PATH"))


def generate_image_file(file, filename, folder="images"):
    # create a temporary folder to store the file
    if not path.exists("./tmp"):
        mkdir("./tmp")
    temp_file = open(f"./tmp/{filename}", "wb+")
    for chunk in file.chunks():
        temp_file.write(chunk)
    storage.upload(file=f"./tmp/{filename}", filename=filename, folder=folder)
    temp_file.close()


def process_image(request):
    file = request.FILES["file"]
    extension = file.name.split(".")[-1]
    original_filename = "-".join(file.name.split(".")[:-1])
    original_filename = "_".join(original_filename.strip().split(" "))
    new_filename = f"{original_filename}-{uuid4()}.{extension}"
    generate_image_file(file, new_filename)
    return new_filename
