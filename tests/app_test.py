import json
import os
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
            "/triggers/manual", base_url=self.base_url, content_type="application/json"
        )

        self.assertEquals(response.status_code, 200)

    def test_process_triggers(self):
        response = self.client.post(
            "/triggers/manual",
            query_string={"dir": ["/test/test1", "/test/test2"]},
            base_url=self.base_url,
            content_type="application/json",
        )

        self.assertEquals(response.status_code, 200)

        print(json.loads(response.data))

    def test_process_triggers_no_subdirectory(self):
        media_directory_no_subdirs = os.getenv("TEST_DIRECTORY", "/test/testdir")
        response = self.client.post(
            "/triggers/manual",
            query_string={"dir": [media_directory_no_subdirs]},
            base_url=self.base_url,
            content_type="application/json",
        )

        self.assertEquals(response.status_code, 200)

        print(json.loads(response.data))

    def test_process_triggers_with_subdirectory(self):
        media_directory = os.getenv("TEST_DIRECTORY_SUBDIR", "/test/testdir")
        response = self.client.post(
            "/triggers/manual",
            query_string={"dir": [media_directory]},
            base_url=self.base_url,
            content_type="application/json",
        )

        self.assertEquals(response.status_code, 200)

        print(json.loads(response.data))
