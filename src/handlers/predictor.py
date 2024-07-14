'''
Predictor class manages the endpoint preprocessing, inference and postprocessing of the models.
'''
import os
import sys
import time
import json
import logging
import joblib
import torch
import requests
from typing import List
from datetime import datetime
from transformers import pipeline
from src.utils.utils import *
from src.api.model.subfeddit import Subfeddit
from src.api.model.subfeddit_response import SubfedditResponse
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class Predictor:

    def __init__(self, app_config) -> None:
        logging.info("Initializing predictor class")
        self.sentiment_name = { 1: 'positive',
                                0: 'Negative'
                              }
        self.tokenizer = AutoTokenizer.from_pretrained('./models/nlptown/bert-base-multilingual-uncased-sentiment')
        self.model = AutoModelForSequenceClassification.from_pretrained('./models/nlptown/bert-base-multilingual-uncased-sentiment')
        self.endpoint_comments = f"http://0.0.0.0:8080/api/v1/comments/?subfeddit_id=subfeddit_id_request&skip=0&limit=25"
        logging.info("Loaded sentiment analysis BERT model")

    def predict_subfeddit_sentiment(self, subfeddit: Subfeddit):
        """
        Analize sentiment for subfeddit's comments.
        Args:
            :param sentiment: pydantic class with subfeddit information
        Returns:
            array_response_comments: List of comments with their sentiment information.
        """
        start_processing = time.time()
        subfeddit_id = subfeddit.subfeddit_id
        logging.info(f'arrived to predict_subfeddit_sentiment : subfeddit_id = {subfeddit_id}')
        self.endpoint_comments = self.endpoint_comments.replace("subfeddit_id_request", str(subfeddit_id))
        subfeddit_comment_response = get_request(subfeddit_id, self.endpoint_comments, verify=False, 
                                                 headers=None, credentials=None, timeout=60)
        parsed_subfeddit_response = None
        if subfeddit_comment_response.status_code == 200:
            logging.info(f"Response subfeddit_comment_response microservice: {subfeddit_comment_response.json()} : subfeddit_id={subfeddit_id}")
            parsed_subfeddit_response =  subfeddit_comment_response.json()
        else:
            raise Exception(f"ERROR RESPONSE {subfeddit_comment_response.status_code} SUBFEDDIT COMMENT : subfeddit_id={subfeddit_id}")
        logging.info(f'subfeddit_response: {json.dumps(parsed_subfeddit_response, indent=4)} : subfeddit_id={subfeddit_id}')
        array_response_comments = []
        for dict_comment in parsed_subfeddit_response['comments']:
            self.analize_comment_sentiment(array_response_comments, dict_comment, subfeddit_id)
        logging.info(f'array_response_comments: {json.dumps(array_response_comments, indent=4)} : subfeddit_id={subfeddit_id}')
        formatted_comments, observations = self.format_output(array_response_comments, subfeddit)
        response = SubfedditResponse(id=subfeddit_id, comments = formatted_comments, observations=observations)
        logging.info(f'Processing time subfeddit sentiment analysis: {time.time()- start_processing}: subfeddit_id={subfeddit_id}')
        return response
        
    def analize_comment_sentiment(self, array_response_comments: List, comment: dict, subfeddit_id: str):
        """
        Analize sentiment for specific comment text.
        Args:
            :param array_response_comments: accumulator sentiment comment list
            :param comment: dict with comment information
            :param subfeddit_id: subfeddit_id 
        Returns:
            array_response_comments: added sentiment to comment list.
        """
        logging.info(f'processing comment: {comment} : subfeddit_id = {subfeddit_id}')
        tokens = self.tokenizer.encode(comment['text'], return_tensors='pt')
        model_output = self.model(tokens)
        logging.info(f'model_output: {model_output} : subfeddit_id = {subfeddit_id}')
        class_number = int(torch.argmax(model_output.logits))
        sentiment_id = 1 if class_number>=2 else 0
        polarity_score = float(torch.max(model_output.logits))
        logging.info(f'polarity_score: {polarity_score} : subfeddit_id = {subfeddit_id}')
        logging.info(f'class_number: {class_number} : subfeddit_id = {subfeddit_id}')
        array_response_comments.append({
            'id': comment['id'],
            'text': comment['text'],
            'polarity_score': polarity_score,
            'sentiment': self.sentiment_name[sentiment_id],
            'created_at':  parse_utc_to_datetime_string(comment['created_at'])
        })

    def format_output(self, array_response_comments: List, subfeddit: Subfeddit):
        """
        Apply some format to the output comments response. The format will be the following:
        -   Filter comments by a specific time range 
        -	Sort the results by the comments polarity score.
        Args:
            :param array_response_comments: list comment response without format
            :param subfeddit: subfeddit with format requests paramenters
        Returns:
            array_response_comments: Formatted output list comments response.
            observations: Explanation about format applied.
        """
        filtered_comments, observations_filtered = self.filter_by_time_range(array_response_comments, 
                                                                           subfeddit.comments_start_time, 
                                                                           subfeddit.comments_end_time)
        
        sorted_comments, observations_sorted = self.sort_by_polarity_score(filtered_comments, 
                                                                           subfeddit.sort_polarity_comments)
        return sorted_comments, observations_filtered + ', ' + observations_sorted


    def filter_by_time_range(self, array_response_comments: List, comments_start_time: str, comments_end_time: str):
        """
        Filter the output comments response by a specific time range.
        Args:
            :param array_response_comments: list comments
            :param comments_start_time_range: start datetime
            :param comments_end_time_range: end datetime
        Returns:
            filtered_comments: Filtered comments by date range (if it was applied).
            observations: Observations about filtering applied.
        """
        observations = ''
        unix_comments_start_time = parse_datetime_string_to_utc(comments_start_time)
        unix_comments_end_time = parse_datetime_string_to_utc(comments_end_time)
        filtered_comments = []
        if unix_comments_start_time and unix_comments_end_time:
            if unix_comments_end_time > unix_comments_start_time:
                for comment in array_response_comments:
                    if parse_datetime_string_to_utc(comment['created_at']) >= unix_comments_start_time and \
                       parse_datetime_string_to_utc(comment['created_at']) <= unix_comments_end_time:
                        filtered_comments.append(comment)  
                observations = f'Comments filtered by datetime >= {comments_start_time} and <= {comments_end_time}'
                return filtered_comments, observations
            else:
                observations = 'Comments not filtered by datetime range (end datetime is lower or equalt to start datetime)'
        else:
            observations = 'Comments not filtered by datetime range (missing or wrong start/end datetime format %Y-%m-%d %H:%M:%S)'
        return array_response_comments, observations
    
    def sort_by_polarity_score(self, array_comments: List, sort_polarity_comments: bool):
        """
        Sort output by polarity score.
        Args:
            :param array_comments: list comments
            :param sort_polarity_comments: flag for sorting
        Returns:
            sorted_comments: Sorted comments by polarity score (if it was applied)
            observations: Observations about sorted applied.
        """
        observations = ''
        sorted_comments = None
        if sort_polarity_comments == True:
            sorted_comments = sorted(array_comments, 
                                     key=lambda comment: comment['polarity_score'])
            observations = 'comments sorted by polarity score'
            return sorted_comments, observations
        else:
            observations = 'comments not sorted by polarity score'
            return array_comments, observations
        



