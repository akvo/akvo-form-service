import os
import sqlite3
import pandas as pd

from django.test import TestCase
from django.core.management import call_command
from akvo.core_node.models import NodeDetail
from afs.settings import BASE_DIR

storage_path = os.environ.get('STORAGE_PATH')


class SQLiteGenerationTest(TestCase):
    def setUp(self):
        payload = {
            "name": "Example Node",
            "node_detail": [{
                "code": "JKT",
                "name": "Jakarta"
            }, {
                "code": "JKTBR",
                "name": "Jakarta Barat",
                "parent": "Jakarta"
            }, {
                "code": "JKTSL",
                "name": "Jakarta Selatan",
                "parent": "Jakarta"
            }, {
                "code": "JKTUT",
                "name": "Jakarta Utara",
                "parent": "Jakarta"
            }, {
                "code": "JKTTR",
                "name": "Jakarta Timur",
                "parent": "Jakarta"
            }, {
                "code": "JKTPT",
                "name": "Jakarta Pusat",
                "parent": "Jakarta"
            }],
        }
        self.client.post(
            "/api/node",
            payload,
            content_type="application/json",
        )
        self.example_node = NodeDetail.objects.all()

    def test_sqlite_generation_command(self):
        call_command("generate_sqlite")
        generated_example_sqlite = f"{storage_path}/sqlite/example_node.sqlite"
        self.assertTrue(os.path.exists(generated_example_sqlite))
        file_path = os.path.join(BASE_DIR, generated_example_sqlite)
        conn = sqlite3.connect(file_path)
        self.assertEqual(
            len(self.example_node),
            len(pd.read_sql_query("SELECT * FROM nodes", conn))
        )
        conn.close()
