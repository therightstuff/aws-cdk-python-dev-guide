import json
import os
import uuid

def main(event, context):
    return_object = {
        "success": True,
        "response_id": str(uuid.uuid4()),
        "querystring": event.get("queryStringParameters"),
        "environment_variables": os.environ['GREETING']
    }
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': os.environ['CORS_ORIGIN'],
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(return_object)
    }