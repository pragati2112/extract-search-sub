import pysrt
from boto3.dynamodb.conditions import Key
from db_connection import create_videos_table
videos_table = create_videos_table()


def read_srt_file(file='uploads/srts/out.srt', video_id='123456789'):
    subs = pysrt.open(file)
    for sub in subs:
        text = sub.text.strip('\n').strip('\t')
        new_text = text.replace('\n', "").replace('\t', "").lstrip()
        data = {'subtitles': new_text, 'videoId': video_id, 'start': str(sub.start), 'end': str(sub.end)}
        videos_table.put_item(Item=data)

    print('successfully insert!')
    return True


def search_subtitle(subtitle: str = '', video_id: str = '123456789'):
    # response = videos_table.scan(TableName='Videos')
    # items = response['Items']
    # for item in items:
    #     print(item)

    resp = videos_table.get_item(Key={'subtitles': subtitle, 'videoId': video_id})
    if 'Item' in resp:
        print(resp['Item'])
        return resp['Item']
    else:
        print('Not found')
        return False


# read_srt_file()
# search_subtitle("I'D CALL THAT")
