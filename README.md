# addCreatedAtAndUpdatedAtFieldsToItemsInDynamoDB

Adds CreatedAt and UpdatedAt Fields, with a default value of the current Epoch time, to all items in DynamoDB table.

## Getting Started

1. Head over to AWS
2. Go to Lambda
3. Create new function
4. Setup IAM role to have DynamoDB permissions for ListTables, Scan, UpdateItem
5. Paste code into editor
6. Configure a test event with the following format
   {
   "tableName": "tablename"
   }
7. Press test.
