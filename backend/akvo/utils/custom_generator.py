import os
import sqlite3
import pandas as pd

from akvo.core_node.models import Node, NodeDetail
from akvo.utils.storage import Storage

storage = Storage(os.environ.get('STORAGE_PATH'))


def generate_sqlite(node: Node):
    name = node.name
    name = name.strip().lower()
    name = name.split(" ")
    name = "_".join(name)
    print(f"Generating {name}.sqlite file")

    objects = NodeDetail.objects.filter(node_id=node.id).all()
    if not len(objects):
        print(f"Node {name} doesn't have node details")
        return

    filename = f"{name}.sqlite"
    if os.path.exists(filename):
        os.remove(filename)
    if storage.check(f"sqlite/{filename}"):
        storage.delete(f"sqlite/{filename}")

    data = pd.DataFrame(list(objects.values()))
    if "parent_id" not in data.columns:
        data["parent_id"] = 0
    data["parent_id"] = data["parent_id"].fillna(0)
    data["parent"] = data["parent_id"].apply(
        lambda x: int(x) if x == x else 0
    )
    data = data[["id", "code", "name", "parent"]]
    conn = sqlite3.connect(filename)
    data.to_sql('nodes', conn, if_exists='replace', index=False)

    storage.upload(file=filename, folder="sqlite")
    os.remove(filename)

    print(f"{filename} Generated Successfully")
    conn.close()
