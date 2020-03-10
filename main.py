import yara
import boto3
import json


def analyze_lambda_handler(event, lambda_context):
    print(event)
    bucket = event["bucketName"]
    key = event["key"]

    rules = yara.load("output")

    s3 = boto3.client("s3")
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    streaming_body = s3_object["Body"]
    return json.dumps({"result": rules.match(data=streaming_body.read())})
