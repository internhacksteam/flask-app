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

#Displaying levels (in World 1 for version 1)
@app.route('/api/displayLevels', methods=['GET'])
def display_levels():
  #get service resource 
  dynamodb = boto3.resource('dynamodb')
  #instance of table without creating it 
  table = dynamodb.Table('Worlds')

  response = table.get_item(
    Key={
      'WorldID': 1
    })
  levels = str(response['Item']['Levels'])

  return jsonify(levels)

#Displaying achievements (in World 1 for version 1)
@app.route('/api/displayAchievements', methods=['GET'])
def display_achievments():
  if not request.json:
    abort(400)
  #get service resource 
  dynamodb = boto3.resource('dynamodb')
  #instance of table without creating it 
  table = dynamodb.Table('Achievements')

  json_data = request.get_json()
  level= json_data['Level']

  response = table.get_item(
    Key={
      'AchievementID': level
    })
  achievements = str(response['Item']['Text'])

  return jsonify(achievements)

@app.route('/api/evaluatingAnswer', methods=['POST'])
def evaluatingAnswer():
    if request.method == 'POST':
        json_data = request.get_json()
        answer= json_data['Answer']


        q1answers = {
            'print("Hello World!")',
            'print("Hello world!")',
            'print("hello world!")',
            'print("hello World!")'
        }

        if answer in q1answers:
            return {'response': "Correct!"}
        else:
            return {'response': "Sorry, try again!"}

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


