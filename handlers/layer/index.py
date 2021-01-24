import json
import os
import uuid
import arrow

def main(event, context):
    utc = arrow.utcnow()
    return_object = {
        "success": True,
        "utc": utc.format('YYYY-MM-DD HH:mm:ss ZZ'),
        "utc_timestamp": utc.timestamp
    }
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': os.environ['CORS_ORIGIN'],
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(return_object)
    }