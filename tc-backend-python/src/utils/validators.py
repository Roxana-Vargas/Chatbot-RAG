import json
import re
from typing import Any, Dict, Tuple
import openai
from src.utils.logger import logger
import spacy
import time

nlp = spacy.load("es_core_news_sm")

# We can adjust these constraints as needed
MAX_MESSAGE_LENGTH = 500
MIN_MESSAGE_LENGTH = 10
BLOCKED_WORDS = {"hack", "attack", "drop table", "<script>"}
INVALID_CHARACTERS_PATTERN = re.compile(r'[<>$%{}[\]#^|~]')
EXTRA_SPACES_PATTERN = re.compile(r'\s+')

def validate_user_message(body):
    """
    Validates and sanitizes a user's input message before processing.

    This function checks if the message is a valid string, removes unnecessary spaces, 
    enforces length constraints, filters out prohibited characters, and blocks restricted words.

    Args:
        body (dict): The request body containing the user's message.

    Returns:
        tuple: A tuple containing:
            - (bool): True if the message is valid, False otherwise.
            - (str or None): The cleaned message if valid, otherwise None.
            - (str or None): An error message if invalid, otherwise None.
    """

    if not isinstance(body, dict):
        return False, None, "Invalid request format"

    if "message" not in body:
        return False, None, "Missing 'message' in request body"

    message = body["message"]

    if not isinstance(message, str):
        return False, None, "Message must be a string"
    
    # Remove unnecessary spaces
    message = message.strip()  

    if not message:
        return False, None, "Message cannot be empty"

    if len(message) < MIN_MESSAGE_LENGTH:
        return False, None, f"Message is too short (minimum {MIN_MESSAGE_LENGTH} characters required)"

    if len(message) > MAX_MESSAGE_LENGTH:
        return False, None, f"Message is too long (maximum {MAX_MESSAGE_LENGTH} characters allowed)"

    # Remove extra spaces
    message = EXTRA_SPACES_PATTERN.sub(' ', message)

    # Block unwanted characters
    if INVALID_CHARACTERS_PATTERN.search(message):
        return False, None, "Message contains invalid characters"

    # Check for blocked words
    lower_message = message.lower()
    if any(word in lower_message for word in BLOCKED_WORDS):
        return False, None, "Message contains prohibited content"
    
    return True, message, None

def detect_harmful_content(message):
    """
    Uses OpenAI's Moderation API to detect harmful content.

    Args:
        message (str): The user’s input message.

    Returns:
        tuple: (bool, str)
            - True, reason if harmful content is detected.
            - False, "" otherwise.
    """
    try:
        logger.info(f"Checking content moderation for message: {message}")

        response = openai.moderations.create(input=message)

        moderation_result = response.results[0]

        flagged = moderation_result.flagged
        categories = moderation_result.categories.model_dump()

        logger.info(f"Content moderation result: flagged={flagged}, categories={categories}")

        if flagged:
            # Extract flagged categories
            flagged_categories = [category for category, is_flagged in categories.items() if is_flagged]
            reason = f"Message contains harmful content: {', '.join(flagged_categories)}"
            return True, reason

        return False, ""

    except Exception as e:
        logger.error(f"Error checking content moderation: {str(e)}")
        return False, f"Error checking content moderation: {str(e)}"


def is_poorly_formed_question(question: str) -> bool:
    """
    Determines if a given question is poorly formed.

    This function uses natural language processing (NLP) to analyze the structure of the question.
    It checks for the presence of essential grammatical components such as verbs, subjects, and noun phrases.
    A question is considered poorly formed if it lacks a verb, an explicit or implicit subject, or a noun phrase.

    Args:
        question (str): The question to be analyzed.

    Returns:
        bool: True if the question is poorly formed, False otherwise.
    """
    try:
        logger.info("Validating question...")
        start_time = time.time()
        
        doc = nlp(question)

        has_explicit_subject = any(token.dep_ in {"nsubj", "nsubj:pass"} for token in doc)
        has_verb = any(token.pos_ in {"VERB", "AUX"} for token in doc)
        has_noun_phrase = any(chunk.root.pos_ == "NOUN" for chunk in doc.noun_chunks)

        has_pronoun_or_adverb = any(token.pos_ in {"PRON", "ADV"} for token in doc) or \
                                any(token.dep_ in {"mark", "advmod"} for token in doc)

        has_object = any(token.dep_ in {"dobj", "iobj"} for token in doc)
        has_prepositional_complement = any(token.dep_ == "prep" for token in doc)

        # Unify implicity subjetc condition
        has_implicit_subject = has_pronoun_or_adverb or has_object or has_prepositional_complement

        # Final evaluation
        is_poorly_formed = not (has_verb and (has_explicit_subject or has_implicit_subject) and has_noun_phrase)

        logger.info(f"Processing time: {time.time() - start_time:.4f} seconds")
        return is_poorly_formed
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return True

def parse_request_body(event: Dict[str, Any]) -> Dict[str, Any]:
    """Parses and returns the request body as a dictionary."""
    try:
        return json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in request body")
        return {}
    
def validate_request_metrics_data(body: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates if the request contains required fields."""
    if not body.get("question") or not body.get("ground_truth") or not body.get("answer") or not body.get("contexts"):
        return False, "Missing required fields"
    return True, ""