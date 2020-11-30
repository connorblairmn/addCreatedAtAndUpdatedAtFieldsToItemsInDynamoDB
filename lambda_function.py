import json
import boto3
import time

def connectToTable(tableName):
    '''
    Connect to DynamoDB table 

    Parameters: 
    tableName (string): Name of table
  
    Returns: 
    object: DynamoDB table object
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    return table

def addFieldsToDynamoDBTable(table):
    '''
    Adds createdAt and updatedAt fields to each item in the table.

    Parameters: 
    table (object): DynamoDB table object
  
    Returns: 
    None
    '''
    # create default unix epoch time 
    defaultUnixTime = str(int(time.time()))
    # get all items in table
    response = table.scan()
    print(f"items: {response.get('Items', [])}")
    items = response.get('Items', [])
    # add default value for createdAt and updatedAt to each item
    for item in items:
        updateItem(item, defaultUnixTime, table)
    return


def updateItem(item, defaultUnixTime, table):
    '''
    Adds createdAt and updatedAt fields to item in DynamoDB table

    Parameters: 
    item (dictionary): Item in table
    defaultUnixTime (string): Default value for reatedAt and updatedAt fields
    table (object): DynamoDB table object
  
    Returns: 
    None
    '''
    try: 
        itemId = item['id']
    except KeyError:
        print(f"ID doesnt exist for item: {item}")
        return
    response = table.update_item(
        Key={
            'id': itemId
        },
        UpdateExpression="set createdAt=:r, updatedAt=:r",
        ExpressionAttributeValues={
            ':r': defaultUnixTime
        },
        ReturnValues="UPDATED_NEW"
    )
    print(f"Response for {itemId}: {response}")
    return
        

def lambda_handler(event, context):
    '''
    Adds createdAt and updatedAt fields to each item in the table.
    '''
    # check that we have a table name
    try: 
        tableName = event['tableName']
    except KeyError: 
        return {
            'statusCode': 400,
            'body': json.dumps('Table does not exist.')
        }
    
    
    # connect to dynamoDB table
    table = connectToTable(tableName)
    # add createdAt and updatedAt fields to ever item in the table 
    addFieldsToDynamoDBTable(table)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Update completed. ')
    }
