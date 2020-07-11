from flask import Flask, jsonify, request
import boto3

app = Flask(__name__)

#given the level id it increases its level by one 
@app.route('/api/updateLevel', methods=['POST'])
def update_user():
  if not request.json:
    abort(400)

  #get service resource 
  dynamodb = boto3.resource('dynamodb')
  #instance of table without creating it 
  table = dynamodb.Table('Users')
  #gets the information 
  json_data = request.get_json()
  userID= json_data['UserID']
  response = table.get_item(
    Key={
      'UserID':userID
    })
  level = response['Item']['Level']
  updatedLevel= level + 1

  #updates the level 
  table.update_item(
  Key={
    'UserID': userID,
    },
    UpdateExpression='SET #level = :vall',
    ExpressionAttributeValues={
      ':vall': updatedLevel
    },
    ExpressionAttributeNames={
    "#level": "Level"
  }
  )

  return jsonify({'level':int(level), 'updatedLevel':int(updatedLevel)})

@app.route('/')
def home():
    return "hello there! This is working"
    
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


