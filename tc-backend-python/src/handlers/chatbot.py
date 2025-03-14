import concurrent.futures
import time
from src.constants.app_constants import MINIMUM_SCORE_CONFIDENCE, RESPONSE_FOR_LOW_CONFIDENCE, RESPONSE_FOR_UNCLEAR_QUESTION
from src.services.chat.chat_service import ChatService
from src.utils.logger import logger
from src.utils.validators import is_poorly_formed_question, parse_request_body, validate_user_message, detect_harmful_content
from src.utils.response_helpers import success_response, error_response
from src.utils.secrets import load_secrets

load_secrets()
chat_service = ChatService()

def handler(event, context):
    """
    AWS Lambda handler for processing chatbot requests.
    
    Expects a JSON request with a "message" field and returns the chatbot's response.
    """
    try:
        start_time = time.time()
        logger.info("Received request event.")
        
        # Parse request body
        body = parse_request_body(event)

        # Validate, clean and sanitize user input
        is_valid, user_message, error_msg = validate_user_message(body)

        if not is_valid:
            return error_response(400, error_msg)

        logger.info(f"Processing user input: {user_message}")

        # Execute moderation and processing tasks concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:

            future_moderation = executor.submit(detect_harmful_content, user_message)
            future_question_check = executor.submit(is_poorly_formed_question, user_message)
            future_processing = executor.submit(chat_service.process_message, user_message)

            poorly_formed = future_question_check.result()
            harmful, reason = future_moderation.result()
    
            if poorly_formed:
                logger.info("Poorly formed question detected. Requesting clarification.")
                future_moderation.cancel()
                return error_response(400, RESPONSE_FOR_UNCLEAR_QUESTION)
            
            if harmful:
                logger.info(f"Message is harmful ({reason}). Cancelling processing task.")
                future_processing.cancel()
                return error_response(400, f"Message is harmful ({reason})")

            chatbot_response = future_processing.result()

             # Verify response confidence
            if chatbot_response["response"]["confidence"] < MINIMUM_SCORE_CONFIDENCE:
                logger.info("Low confidence response. Requesting clarification.")
                chatbot_response["response"]["content"] = RESPONSE_FOR_LOW_CONFIDENCE
        
        end_time = time.time()
        total_time = end_time - start_time
        chatbot_response["response"]["processing_time"] = total_time

        return success_response(chatbot_response)

    except Exception as e:
        logger.exception("Error processing chatbot request")
        return error_response(500, str(e))
