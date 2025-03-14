import json
import boto3
import os
from botocore.exceptions import ClientError
from src.utils.logger import logger
from src.utils.environment import AMAZON_REGION, SECRET_NAME


def load_secrets():
    """
    Load secrets from AWS Secrets Manager only once and store them in environment variables.
    """

    client = boto3.client("secretsmanager", region_name=AMAZON_REGION)

    try:
        logger.info(f"Fetching secrets from AWS Secrets Manager: {SECRET_NAME}")

        response = client.get_secret_value(SecretId=SECRET_NAME)
        secrets = json.loads(response["SecretString"])

        # Save secrets on environment variables
        for key, value in secrets.items():
            os.environ[key] = str(value)

        logger.info("Secrets successfully loaded into environment variables.")

    except ClientError as e:
        logger.error(f"Failed to retrieve secrets: {e}")

