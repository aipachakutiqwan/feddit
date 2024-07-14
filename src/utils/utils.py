import time
import datetime
import requests
import logging

def get_request(id: str, endpoint, verify, headers=None, credentials=None, timeout=60, proxies = {"http": "", "https": ""}):
    """
    Parameterized get request function.
    """
    start_time = time.time()
    response = requests.get(
        url=endpoint,
        verify=verify,
        headers=headers,
        auth=credentials,
        timeout=timeout, 
        proxies=proxies
    )
    end_time = time.time()
    logging.info(f"Response time GET endpoint {endpoint} service for id={id}: {end_time - start_time}")
    return response

def post_request(id: str, endpoint, json, verify, credentials, timeout=60, proxies = {"http": "", "https": ""}):
    """
    Parameterized post request function.
    """
    start_time = time.time()
    response = requests.post(
        url=endpoint,
        json=json,
        verify=verify,
        auth=credentials,
        timeout=timeout,
        proxies=proxies
    )
    end_time = time.time()
    logging.info(f"Response time POST endpoint {endpoint} service for id={id}: {end_time - start_time}")
    return response 

def parse_datetime_string_to_utc(datetime_string: str):
    """
    Convert datetime string ('%Y-%m-%d %H:%M:%S') to Unix timestamp.
    """
    if datetime_string:
        datetime_format = datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
        unix_datetime = datetime.datetime.timestamp(datetime_format)
        return unix_datetime
    else:
        return None

def parse_utc_to_datetime_string(datetime_unix: int):
    """
    Convert Unix timestamp to datetime string ('%Y-%m-%d %H:%M:%S')
    """
    if datetime_unix:
        datetime_string = datetime.datetime.fromtimestamp(datetime_unix).strftime('%Y-%m-%d %H:%M:%S') 
        return datetime_string
    else:
        return None