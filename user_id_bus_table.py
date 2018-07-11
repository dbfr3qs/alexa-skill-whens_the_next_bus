import boto3

TABLE_NAME = 'UserIDBusStop'


def put_user_bus_stop(user_id, stop):
    print("Putting {0} into table".format(user_id))
    conn = boto3.client('dynamodb', 
                        region_name='us-east-1')
    response = conn.put_item(
        TableName = TABLE_NAME,
        Item = {
            'UserId': {
                'S': user_id,
            },
            'StopId': {
                'N': str(stop)
            }
        }
    )
    return True if response['ResponseMetadata']['HTTPStatusCode'] else False

def get_user_bus_stop(user_id):
    print("getting {} from table".format(user_id))
    conn = boto3.client('dynamodb', 
                    region_name='us-east-1')

    response = conn.get_item(
        TableName = TABLE_NAME,
        Key={
            'UserId':{
                'S': user_id
            }
        }
    )

    item = {}
    print(response)
    if 'Item' in response:
        if 'UserId' in response['Item']:
            item = {
                'user_id': response['Item']['UserId']['S'],
                'stop_id': int(response['Item']['StopId']['N'])
            }
    print("item: {}".format(item))
    return item