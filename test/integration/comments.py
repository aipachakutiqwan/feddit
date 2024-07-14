import sys
import os
import requests
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

def test_api_subfeddit_comments(subfeddit_id):

    response = requests.get(
        url=f"http://0.0.0.0:8080/api/v1/comments/?subfeddit_id={subfeddit_id}&skip=0&limit=25",
        proxies={"https": "", "http": ""}
    )
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4))
    print(f'Status code test_api_subfeddit_comments : {response.status_code}')
    assert response.status_code == 200

subfeddit_id = 1
test_api_subfeddit_comments(subfeddit_id)