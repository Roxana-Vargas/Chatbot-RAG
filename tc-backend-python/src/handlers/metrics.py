from typing import Any, Dict
from src.constants.app_constants import HTTP_BAD_REQUEST, HTTP_INTERNAL_SERVER_ERROR
from src.services.evaluation.evaluation_service import evaluate_question
from src.utils.logger import logger
from src.utils.response_helpers import success_response, error_response
from src.utils.secrets import load_secrets
from src.utils.validators import parse_request_body, validate_request_metrics_data

load_secrets()

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler to evaluate a RAG chatbot using the RAGAS model.

    Args:
        event (dict): The event received by the Lambda function.
        context (object): The Lambda function's context.

    Returns:
        dict: HTTP response with the evaluation results or an error message.
    """
    logger.info("Received request event.")

    body = parse_request_body(event)

    is_valid, error_message = validate_request_metrics_data(body)
    if not is_valid:
        return error_response(HTTP_BAD_REQUEST, error_message)

    question = body["question"]
    ground_truth = body["ground_truth"]
    answer = body["answer"]
    contexts = body.get("contexts") 

    try:

        logger.info(f"Answer: {answer}")

        evaluation_result = evaluate_question(question, ground_truth, answer, contexts)

        logger.info(f"Evaluation result: {evaluation_result}")

        return success_response(evaluation_result)

    except Exception as e:
        logger.exception("Error processing chatbot request")
        return error_response(HTTP_INTERNAL_SERVER_ERROR, str(e))
