import json
import unittest
import tempfile
import requests
from unittest.mock import patch
from unittest.mock import mock_open
from src.api.core import config
from unittest.mock import MagicMock
from src.handlers.predictor import Predictor


class TestPredictor(unittest.TestCase):

    def setUp(self):
        self.app_config = {}
        self.model_path_sentiment_analysis = 'model_path'

    def tearDown(self):
        pass

    def test_sort_by_polarity_score(self):
        '''
        Test sorting output comments by polarity score
        '''
        array_comments = { "id": 2,
                           "comments": [
                                {
                                    "id": 67495,
                                    "text": "Love it",
                                    "polarity_score": 4.101906776428223,
                                    "sentiment": "positive",
                                    "created_at": "2024-07-13 09:52:18"
                                },
                                {
                                    "id": 67496,
                                    "text": "Enjoy",
                                    "polarity_score": 3.8332948684692383,
                                    "sentiment": "positive",
                                    "created_at": "2024-07-13 08:52:18"
                                },
                                {
                                    "id": 67497,
                                    "text": "Awesome",
                                    "polarity_score": 1.9286322593688965,
                                    "sentiment": "positive",
                                    "created_at": "2024-07-13 07:52:18"
                                }
                            ]
                        }
        self_env_variables = MagicMock()
        self_env_variables.model_path_sentiment_analysis = MagicMock()
        sorted_comments, observations = Predictor.sort_by_polarity_score(self_env_variables, array_comments, False)
        self.assertEqual(sorted_comments, array_comments)


