import pysrt
import boto3
from boto3.dynamodb.conditions import Key

db = boto3.resource("dynamodb", endpoint_url="http://localhost:8000",
                    region_name="dummy", aws_access_key_id="dummy", aws_secret_access_key="dummy")
table = db.Table('Videos')


def read_srt_file(file='uploads/srts/out.srt', video_id='123456789'):
    subs = pysrt.open(file)
    for sub in subs:
        text = sub.text.strip('\n').strip('\t')
        new_text = text.replace('\n', "").replace('\t', "").lstrip()
        data = {'subtitles': new_text, 'videoId': video_id, 'start': str(sub.start), 'end': str(sub.end)}
        table.put_item(Item=data)

    print('successfully insert')
    return True


def search_subtitle(subtitle: str = '', video_id: str = '123456789'):
    # response = table.scan(TableName='Videos')
    # items = response['Items']
    # for item in items:
    #     print(item)

    resp = table.get_item(Key={'subtitles': subtitle, 'videoId': video_id})
    if 'Item' in resp:
        print(resp['Item'])
        return resp['Item']
    else:
        print('Not found')
        return False


# read_srt_file()
search_subtitle("I'D CALL THAT")
