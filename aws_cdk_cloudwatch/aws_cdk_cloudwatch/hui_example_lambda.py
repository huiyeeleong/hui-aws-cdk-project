import json
import logging
import os

def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getlogger()
    LOGGER.setLevel(level=os.getenv("LOG_LEVEL", "DEBUG").upper())

    LOGGER.info(f"received_event:{event}")

    return{
        "statusCode": 200,
        "body": json.dumps({
            "message": event
        })
    }