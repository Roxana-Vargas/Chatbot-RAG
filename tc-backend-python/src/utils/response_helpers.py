import json

def create_response(status_code, data):
    """
    Creates a standardized JSON response 

    Args:
        status_code (int): HTTP status code (e.g., 200, 400, 500).
        data (dict): The response payload.

    Returns:
        dict: A properly formatted API Gateway response.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",  
            "Access-Control-Allow-Origin": "*" 
        },
        "body": json.dumps(data)
    }

import json

def success_response(data):
    """Creates a 200 OK response."""
    
    return create_response(200, data=data)

def error_response(status_code, error_message):
    """Creates an error response with a given status code and message."""
    return create_response(status_code, {"error": error_message})

def convert_documents_to_dict(documents):
    """Converts a list of Document objects to a list of dictionaries."""
    return [
        {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in documents
    ]
