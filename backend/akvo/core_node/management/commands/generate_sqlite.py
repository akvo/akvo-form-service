import os
import sqlite3
import pandas as pd

from django.core.management import BaseCommand
from akvo.core_node.models import Node, NodeDetail
from akvo.utils.storage import Storage

storage = Storage(os.environ.get('STORAGE_PATH'))


class Command(BaseCommand):

    def handle(self, *args, **options):
        nodes = Node.objects.all()
        for node in nodes:
            name = node.name
            name = name.strip().lower()
            name = name.split(" ")
            name = "_".join(name)
            print(f"Generating {name}.sqlite file")

            objects = NodeDetail.objects.filter(node=node).all()
            if not len(objects):
                print(f"Node {name} doesn't have node details")
                continue

            file_name = f"{name}.sqlite"
            if os.path.exists(file_name):
                os.remove(file_name)

            data = pd.DataFrame(list(objects.values()))
            if "parent_id" not in data.columns:
                data["parent_id"] = 0
            data["parent_id"] = data["parent_id"].fillna(0)
            data["parent"] = data["parent_id"].apply(
                lambda x: int(x) if x == x else 0
            )
            data = data[["id", "code", "name", "parent"]]
            conn = sqlite3.connect(file_name)
            data.to_sql('nodes', conn, if_exists='replace', index=False)

            storage.upload(file=file_name, folder="sqlite")
            os.remove(file_name)

            print(f"{file_name} Generated Successfully")
            conn.close()
