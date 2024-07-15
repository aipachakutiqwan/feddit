# Feddit

This repository contains an inference service for the BERT uncased multilingual finetunned sentiment classification model. The RESTful API classifies the sentiment of the Feddit (aka. fake Reddit) comments for a given Subfeddit.

The sentiment analysis services is based on the public finetunned model: https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment. The sentiment scores goes from 1 to 5, 1 is the most negative and 5 the most positive sentiment score.


#### Online Endpoint Sentiment Analysis Microservice

A Fast API online endpoint for sentiment classification predictor was created and exposed on the port 8081. The input to the RESTful API are the following fields.

-  subfeddit_id (integer). Required subfeddit_id which it take 1, 2 or 3 as values.
- comments_start_time (string). Optional if it is required to filter the output comments by time range.
- comments_end_time (string). Optional if it is required to filter the output comments by time range.
- sort_polarity_comments (string). Optional if it is required to sort the output comments by sentiment polarity.

The output of the service will have the following structure.

```console
 {
    "id": "subfeddit_id",
    "comments": [
        {
            "id": "id_comment",
            "text": "text comment",
            "polarity_score": "sentiment score which range from 1 to 5",
            "sentiment": "positive or negative",
            "created_at": "comment creation in the format %Y-%m-%d %H:%M:%S"
        }
    ],
    "observations": "Explanation about the format applied to the output comments"
}
 ```

For activate the sentiment analysis inference enpoint it is required to follow the next steps.

- Build and run the docker containers  in the terminal.
```console
 docker compose up 
 ```

- Verify that the sentiment analysis service is running on the port 8081. Below some example logs which should appear in the terminal.

```console
feddit-inference-server-feddit-1  | [Tech] 2024-07-14 22:35:25,545 - INFO - Loaded sentiment analysis BERT model
feddit-inference-server-feddit-1  | [Tech] 2024-07-14 22:35:25,546 - INFO - Request handler initialized
feddit-inference-server-feddit-1  | [Tech] 2024-07-14 22:35:25,548 - INFO - Application startup complete.
feddit-inference-server-feddit-1  | INFO:     Application startup complete.
feddit-inference-server-feddit-1  | INFO:     Uvicorn running on http://0.0.0.0:8081 (Press CTRL+C to quit)
feddit-inference-server-feddit-1  | [Tech] 2024-07-14 22:35:25,549 - INFO - Uvicorn running on http://0.0.0.0:8081 (Press CTRL+C to quit)

 ```

- Send a post request using the integration test post request.

 ```console
 python test/integration/predict_sentiment_1.py 
 ```
- Alternativelly, it is also posible to use the curl command.
 ```console
 curl -X POST http://localhost:8081/api/subfeddit/sentiment -H 'Content-Type: application/json'  -d '{"subfeddit_id": 3}'
 ```

- Verify the sentiment analysis prediction output for the requested subfeddit_id=3. The results will be similar to the below JSON output.

 ```console
{
    "id": 3,
    "comments": [
        {
            "id": 67495,
            "text": "Love it. Proud of you.",
            "polarity_score": 4.101906776428223,
            "sentiment": "positive",
            "created_at": "2024-07-13 12:35:31"
        },
        {
            "id": 67496,
            "text": "Love it. Enjoy!",
            "polarity_score": 3.833294153213501,
            "sentiment": "positive",
            "created_at": "2024-07-13 11:35:31"
        },
        {
            "id": 67497,
            "text": "Awesome. It looks great!",
            "polarity_score": 3.928633689880371,
            "sentiment": "positive",
            "created_at": "2024-07-13 10:35:31"
        },
        {
            "id": 67498,
            "text": "Awesome. Love it.",
            "polarity_score": 3.995208740234375,
            "sentiment": "positive",
            "created_at": "2024-07-13 09:35:31"
        },
        {
            "id": 67499,
            "text": "Awesome. Awesome.",
            "polarity_score": 3.1976876258850098,
            "sentiment": "positive",
            "created_at": "2024-07-13 08:35:31"
        },
        {
            "id": 67500,
            "text": "Awesome. Well done!",
            "polarity_score": 3.6617658138275146,
            "sentiment": "positive",
            "created_at": "2024-07-13 07:35:31"
        },
        {
            "id": 67461,
            "text": "It looks great!",
            "polarity_score": 2.6681504249572754,
            "sentiment": "positive",
            "created_at": "2024-07-14 22:35:31"
        },
        {
            "id": 67462,
            "text": "Love it.",
            "polarity_score": 3.2503373622894287,
            "sentiment": "positive",
            "created_at": "2024-07-14 21:35:31"
        },
        {
            "id": 67463,
            "text": "Awesome.",
            "polarity_score": 3.054442882537842,
            "sentiment": "positive",
            "created_at": "2024-07-14 20:35:31"
        },
        {
            "id": 67464,
            "text": "Well done!",
            "polarity_score": 2.5895299911499023,
            "sentiment": "positive",
            "created_at": "2024-07-14 19:35:31"
        },
        {
            "id": 67465,
            "text": "Looks decent.",
            "polarity_score": 1.7440910339355469,
            "sentiment": "positive",
            "created_at": "2024-07-14 18:35:31"
        },
        {
            "id": 67466,
            "text": "What you did was right.",
            "polarity_score": 1.674331545829773,
            "sentiment": "positive",
            "created_at": "2024-07-14 17:35:31"
        },
        {
            "id": 67467,
            "text": "Thumbs up.",
            "polarity_score": 1.186923861503601,
            "sentiment": "positive",
            "created_at": "2024-07-14 16:35:31"
        },
        {
            "id": 67468,
            "text": "Like it a lot!",
            "polarity_score": 2.40167498588562,
            "sentiment": "positive",
            "created_at": "2024-07-14 15:35:31"
        },
        {
            "id": 67469,
            "text": "Good work.",
            "polarity_score": 2.031423568725586,
            "sentiment": "positive",
            "created_at": "2024-07-14 14:35:31"
        },
        {
            "id": 67470,
            "text": "Luckily you did it.",
            "polarity_score": 1.558504343032837,
            "sentiment": "positive",
            "created_at": "2024-07-14 13:35:31"
        },
        {
            "id": 67471,
            "text": "Proud of you.",
            "polarity_score": 3.066424608230591,
            "sentiment": "positive",
            "created_at": "2024-07-14 12:35:31"
        },
        {
            "id": 67472,
            "text": "Enjoy!",
            "polarity_score": 2.3321971893310547,
            "sentiment": "positive",
            "created_at": "2024-07-14 11:35:31"
        },
        {
            "id": 67473,
            "text": "It looks great! It looks great!",
            "polarity_score": 2.9435324668884277,
            "sentiment": "positive",
            "created_at": "2024-07-14 10:35:31"
        },
        {
            "id": 67474,
            "text": "It looks great! Love it.",
            "polarity_score": 3.6757924556732178,
            "sentiment": "positive",
            "created_at": "2024-07-14 09:35:31"
        },
        {
            "id": 67475,
            "text": "It looks great! Awesome.",
            "polarity_score": 3.657472848892212,
            "sentiment": "positive",
            "created_at": "2024-07-14 08:35:31"
        },
        {
            "id": 67476,
            "text": "It looks great! Well done!",
            "polarity_score": 2.990990161895752,
            "sentiment": "positive",
            "created_at": "2024-07-14 07:35:31"
        },
        {
            "id": 67477,
            "text": "It looks great! Looks decent.",
            "polarity_score": 2.4286184310913086,
            "sentiment": "positive",
            "created_at": "2024-07-14 06:35:31"
        },
        {
            "id": 67478,
            "text": "It looks great! What you did was right.",
            "polarity_score": 3.1648497581481934,
            "sentiment": "positive",
            "created_at": "2024-07-14 05:35:31"
        },
        {
            "id": 67479,
            "text": "It looks great! Thumbs up.",
            "polarity_score": 3.016805410385132,
            "sentiment": "positive",
            "created_at": "2024-07-14 04:35:31"
        }
    ],
    "observations": "Comments not filtered by datetime range (missing or wrong start/end datetime format %Y-%m-%d %H:%M:%S), comments not sorted by polarity score"
}
 ```

- It is possible to modify the API request query to filter comments by a specific time range. Use the below command to test this feature.

 ```console
 python test/integration/predict_sentiment_2.py 
 ```

- Also, it is possible to sort the comments results by the polarity score using the next command.

 ```console
 python test/integration/predict_sentiment_3.py 
 ```

- Play with the services changing the content of the test cases. Finally, shut down the service and close the terminal.

 ```console
 docker compose down
 ```

#### GitHub workflow to run linting checks and tests

The project contains a GitHub workflow to run linting checks and unit tests, its configuration is in .github/workflows. The last workflow running will be verified in https://github.com/aipachakutiqwan/feddit/actions.











