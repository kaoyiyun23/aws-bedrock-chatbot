import boto3

dynamodb = boto3.client('dynamodb', region_name='us-west-2')

def getdata(nodeid):

    s = nodeid
    response = dynamodb.get_item(
        TableName='nodedata',
        Key={
            'nodeId': {'S': s},
        }
    )
    ls = response['Item']['val']['M']['value']['S']
    li = list(ls.split("]")) 
    return li
    