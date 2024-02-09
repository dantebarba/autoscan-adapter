import unittest
from dotenv import load_dotenv
from app import create_app

class AppTest(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = create_app()
        self.client = self.app.test_client()
        self.base_url = "http://127.0.0.1"

    def test_ping(self):
        response = self.client.head(
            "/triggers/manual",
            base_url=self.base_url,
            content_type="application/json"
        )

        self.assertEquals(response.status_code, 200)

    def test_process_triggers(self):
        response = self.client.post(
            "/triggers/manual",
            query_string={"dir": "/test/test1", "dir": "/test/test2"},
            base_url=self.base_url,
            content_type="application/json"
        )

        self.assertEquals(response.status_code, 200)