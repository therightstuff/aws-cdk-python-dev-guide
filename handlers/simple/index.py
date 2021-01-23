import json
import os

def main(event, context):
    return_object = {
        "success": True,
        "querystring": event.get("queryStringParameters"),
        "environmentVariables": os.environ['GREETING']
    }
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': os.environ['CORS_ORIGIN'],
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(return_object)
    }