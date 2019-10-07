import os
import simplejson as json
import boto3

def s3_file_handler(event: dict, context):
    s3_client = boto3.client('s3')
    records = event.get('Records', list())
    bucket = os.environ.get('BUCKET_NAME')
    target = f'{bucket}/Processed'
    results = list()

    for record in records:
        s3_item = record.get('s3')

        if s3_item.get('bucket', dict()).get('name') != bucket:
            continue
        key = s3_item['object']['key']
        source = {
            'Bucket': bucket,
            'Key': key
        }
        try:
            s3_client.copy_object(Bucket=target, Key=key, CopySource=source)
            results.append({
                'obj': source,
                'status': True
            })
            s3_client.delete_object(Bucket=bucket, Key=key)
        except Exception as e:
            results.append({
                'obj': source,
                'status': False,
                'msg': str(e)
            })
    res = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps(results)
    }
    return res
