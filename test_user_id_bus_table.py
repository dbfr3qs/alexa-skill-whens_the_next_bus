from user_id_bus_table import put_user_bus_stop, get_user_bus_stop
from moto import mock_dynamodb2
import boto3

@mock_dynamodb2
def test_put_user_stop():
    TABLE_NAME = 'UserIDBusStop'
    conn = boto3.client('dynamodb',
                    region_name='us-east-1',
                    aws_access_key_id="ak",
                    aws_secret_access_key="sk")
    conn.create_table(TableName=TABLE_NAME,
                      KeySchema=[{'AttributeName':'UserId','KeyType':'HASH'}],
                      AttributeDefinitions=[{'AttributeName':'UserId','AttributeType':'S'}],
                      ProvisionedThroughput={'ReadCapacityUnits':20,'WriteCapacityUnits':20})
    USER_ID = 'amzn1.ask.account.AHUGXOPEDKUZKV2ABV4DPKCFGLNBUBFSF6SS5BDDMDPFHOPRINLPSJ3QWWV3RLQFBW6WIVH4HM4ZKC2DTD65YSVENUI25RJGKC3PMUJ7WIC6PH3TAUEAXAPQ7DBVHKTDTSHWSHPM3Z6HQ4TKM374VL65P6FGXD5KKCKXTKPTQH4KOR6XPGRVUGRLQNDTQIJR5ULJI2KW7UPANVY'
    STOP = 7726
    assert put_user_bus_stop(USER_ID, STOP) == True

@mock_dynamodb2
def test_get_user_stop():
    TABLE_NAME = 'UserIDBusStop'
    conn = boto3.client('dynamodb',
                    region_name='us-east-1',
                    aws_access_key_id="ak",
                    aws_secret_access_key="sk")
    conn.create_table(TableName=TABLE_NAME,
                      KeySchema=[{'AttributeName':'UserId','KeyType':'HASH'}],
                      AttributeDefinitions=[{'AttributeName':'UserId','AttributeType':'S'}],
                      ProvisionedThroughput={'ReadCapacityUnits':20,'WriteCapacityUnits':20})
    USER_ID = 'amzn1.ask.account.AHUGXOPEDKUZKV2ABV4DPKCFGLNBUBFSF6SS5BDDMDPFHOPRINLPSJ3QWWV3RLQFBW6WIVH4HM4ZKC2DTD65YSVENUI25RJGKC3PMUJ7WIC6PH3TAUEAXAPQ7DBVHKTDTSHWSHPM3Z6HQ4TKM374VL65P6FGXD5KKCKXTKPTQH4KOR6XPGRVUGRLQNDTQIJR5ULJI2KW7UPANVY'
    STOP = 7726

    response = conn.put_item(
        TableName = TABLE_NAME,
        Item = {
            'UserId': {
                'S': USER_ID,
            },
            'StopId': {
                'N': str(STOP)
            }
        }
    )

    res = get_user_bus_stop(USER_ID)
    assert res == {
        'user_id': USER_ID,
        'stop_id': STOP
    }
    

