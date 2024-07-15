import unittest
import requests
from unittest.mock import patch
from unittest.mock import MagicMock
from src.utils.utils import *


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch.object(requests, 'get')
    def test_get_request(self, mock_get_request):
        '''
        Test generic test request.
        '''
        get_request = MagicMock()
        mock_get_request.return_value = get_request
        get_request.return_value = { "id": 3,
                                          "comments": [
                                            {
                                                "id": 1,
                                                "text": "Love it. Proud of you.",
                                                "polarity_score": 4.101906776428223,
                                                "sentiment": "positive",
                                                "created_at": "2024-07-13 09:52:18"
                                            },
                                            {
                                                "id": 2,
                                                "text": "Love it. Enjoy!",
                                                "polarity_score": 3.8332948684692383,
                                                "sentiment": "positive",
                                                "created_at": "2024-07-13 08:52:18"
                                            }] 
                                        }
        get_request.status_code = 200
        get_response = get_request(id=1, endpoint='http://localhost:8080/fake', verify=False, 
                                 headers=None, credentials=None, timeout=60, 
                                 proxies = {"http": "", "https": ""})
        self.assertEqual(get_response['id'], 3)

    def test_parse_datetime_string_to_utc(self):
        '''
        Test parsing datetime string to UTC.
        '''
        utc_date = parse_datetime_string_to_utc('2024-07-14 20:34:00')
        self.assertEqual(utc_date, 1720989240.0)
    
    def test_parse_utc_to_datetime_string(self):
        '''
        Test parsing UTC to datetime string
        '''
        datetime_string = parse_utc_to_datetime_string(1720982040)
        self.assertEqual(datetime_string, '2024-07-14 18:34:00')