import sys
import os
import requests
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

def test_api_predict_subfeddit_sentiment(subfeddit_id):

    payload = {"subfeddit_id": subfeddit_id
               }

    response = requests.post(
        url="http://localhost:8081/api/subfeddit/sentiment",
        json=payload,
        proxies={"https": "", "http": ""}

    )
    parsed = json.loads(response.text)
    print(f'Response predict_subfeddit_sentiment service : {json.dumps(parsed, indent=4)}')
    print(f'Status code predict_subfeddit_sentiment : {response.status_code}')
    assert response.status_code == 200

subfeddit_id = 3
test_api_predict_subfeddit_sentiment(subfeddit_id)