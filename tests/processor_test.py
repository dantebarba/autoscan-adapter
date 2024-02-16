import json
import os
import unittest

from dotenv import load_dotenv

from app import create_app


class ProcessorTest(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        load_dotenv(".processortest.env")
        self.app = create_app()
        self.client = self.app.test_client()
        self.base_url = "http://127.0.0.1"

    def test_custom_moviename_processor(self):
        media_directory = os.getenv("TEST_DIRECTORY_SUBDIR", "/test/testdir")
        response = self.client.post(
            "/triggers/manual",
            query_string={"dir": [media_directory]},
            base_url=self.base_url,
            content_type="application/json",
        )

        self.assertEquals(response.status_code, 200)

        print(json.loads(response.data))
