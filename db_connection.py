import boto3


def create_videos_table():
    db = boto3.resource("dynamodb", endpoint_url="http://localhost:8000",
                        region_name="dummy", aws_access_key_id="dummy", aws_secret_access_key="dummy")

    _table = db.create_table(TableName="Videos",
                             KeySchema=[{
                                 "AttributeName": "subtitles",
                                 "KeyType": "HASH",
                             },
                                 {
                                     'AttributeName': "videoId",
                                     'KeyType': "RANGE"
                                 }
                             ],
                             AttributeDefinitions=[{
                                 "AttributeName": "subtitles",
                                 "AttributeType": "S"
                             },
                                 {
                                     'AttributeName': "videoId",
                                     'AttributeType': "S"
                                 }
                             ],
                             ProvisionedThroughput={
                                 "ReadCapacityUnits": 10,
                                 "WriteCapacityUnits": 10
                             })
    return _table


if __name__ == '__main__':
    table = create_videos_table()
