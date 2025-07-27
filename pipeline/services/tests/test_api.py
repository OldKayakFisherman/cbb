from services.api import (
    APIResponse,
    CBPCountyAPIClient,
    CBPStateAPIClient
)
import unittest

class CBPCountyAPIClientTests(unittest.TestCase):

    def test_poll(self):

        client: CBPCountyAPIClient = CBPCountyAPIClient()
        response: APIResponse = client.poll(2023)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)


class CBPStateAPIClientTests(unittest.TestCase):

    def test_poll(self):

        client: CBPStateAPIClient = CBPStateAPIClient()
        response: APIResponse = client.poll(2023)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)


        client: CBPStateAPIClient = CBPStateAPIClient()
        response: APIResponse = client.poll(2015)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
