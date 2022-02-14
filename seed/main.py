import json
import boto3

dynamodb = boto3.resource('dynamodb')
recipts = dynamodb.Table("Recipts")
# recipts = dynamodb.create_table(

#     TableName='Recipts',
#     KeySchema=[
#         {
#             'AttributeName': 'customer_id',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName': 'bought_at',
#             'KeyType': 'RANGE'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'customer_id',
#             'AttributeType': 'N'
#         },
#         {
#             'AttributeName': 'bought_at',
#             'AttributeType': 'N'
#         }
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 1,
#         'WriteCapacityUnits': 1,
#     })

print("Table status:", recipts.table_status)
f = open("./recipts.json", "r", encoding="utf-8")
data = json.load(f)

for recipt in data:
    resp = recipts.put_item(
        Item={
            'customer_id': recipt['customer_id'],
            'bought_at': recipt['bought_at'],
            'items': [product for product in recipt['items']],
            'total': recipt['total'],
            'store_id': recipt['store_id']
        }
    )
    print("Insert product response:", resp)

f.close()
