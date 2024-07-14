"""
Implementation predict route
"""
from fastapi import APIRouter
from starlette.requests import Request
from src.handlers.predictor import Predictor
from src.api.model.subfeddit_response import PREDICTION_RESPONSES_TYPES
from src.api.model.subfeddit import Subfeddit
from src.api.model.subfeddit_response import SubfedditResponse


ROUTER = APIRouter()

@ROUTER.post("/sentiment", response_model=SubfedditResponse, responses=PREDICTION_RESPONSES_TYPES)
async def predicting_sentiment(subfeddit: Subfeddit, request: Request):
    """
    Notifies about the arrival new request for subfeddit sentiment analysis

    Args:
        :param  sentiment: subfeddit sentiment request analysis
        :param  request: request

    Returns:
        FastAPI endpoint configured
    """
    handler: Predictor = request.app.state.predictor
    subfeddit_response = handler.predict_subfeddit_sentiment(subfeddit)
    return subfeddit_response
