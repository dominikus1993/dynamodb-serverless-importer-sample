import json
from typing import Any
import boto3
import logging
import os
import dataclasses

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
bucket_name = os.environ['BUCKET_NAME']
dynamodb = boto3.resource('dynamodb')

recipts_table = dynamodb.Table('Recipts')

def _write_recipt(recipt: Any) -> None: 
    resp = recipts_table.put_item(
        Item={
            'customer_id': recipt['customer_id'],
            'bought_at': recipt['bought_at'],
            'items': [product for product in recipt['items']],
            'total': recipt['total'],
            'store_id': recipt['store_id']
        },       
    )
    logger.info("Insert product response: %s", resp)


def write_recipts(event, context):
    """Write all recipts from json file to dynamodb."""
    records = event["Records"]
    for record in records:
        filename = record["s3"]["object"]["key"]
        obj = s3.get_object(Bucket=bucket_name, Key=filename)
        recipts = json.loads(obj["Body"].read().decode("utf-8"))
        for recipt in recipts:
            logger.info(f"Writing recipt: {recipt}")
            _write_recipt(recipt)
            logger.info(f"Wrote recipt: {recipt}")
        s3.delete_object(Bucket=bucket_name, Key=filename)
