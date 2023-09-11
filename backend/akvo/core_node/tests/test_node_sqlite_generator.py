import os
import sqlite3
import pandas as pd

from django.test import TestCase
from django.core.management import call_command
from akvo.core_node.models import NodeDetail


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
        generated_example_sqlite = "./source/sqlite/example_node.sqlite"
        self.assertTrue(os.path.exists(generated_example_sqlite))
        conn = sqlite3.connect(generated_example_sqlite)
        self.assertEqual(
            len(self.example_node),
            len(pd.read_sql_query("SELECT * FROM nodes", conn))
        )
        conn.close()

    def test_sqlite_file_endpoint(self):
        call_command("generate_sqlite")
        generated_example_sqlite = "./source/sqlite/example_node.sqlite"
        self.assertTrue(os.path.exists(generated_example_sqlite))
        file = generated_example_sqlite.split("/")[-1]
        endpoint = f"/api/device/sqlite/{file}"
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
