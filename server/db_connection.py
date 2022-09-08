import boto3
from botocore.exceptions import ClientError


def create_videos_table():
    db = boto3.resource("dynamodb", endpoint_url="http://localhost:8000",
                        region_name="dummy", aws_access_key_id="dummy", aws_secret_access_key="dummy")
    try:
        _table = db.create_table(TableName="Videos",
                                 KeySchema=[{
                                     "AttributeName": "videoId",
                                     "KeyType": "HASH",
                                 },
                                     {
                                         'AttributeName': "subtitles",
                                         'KeyType': "RANGE"
                                     }
                                 ],
                                 AttributeDefinitions=[{
                                     "AttributeName": "videoId",
                                     "AttributeType": "S"
                                 },
                                     {
                                         'AttributeName': "subtitles",
                                         'AttributeType': "S"
                                     }
                                 ],
                                 ProvisionedThroughput={
                                     "ReadCapacityUnits": 10,
                                     "WriteCapacityUnits": 10
                                 })
        return _table
    except ClientError as ce:
        # do something here as you require
        _table = db.Table('Videos')
        return _table


# if __name__ == '__main__':
#     table = create_videos_table()
