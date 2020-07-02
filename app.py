from flask import Flask, jsonify

app = Flask(__name__)

#temporary database for influencial women in tech
womenInTech = [
    {
        'name': 'Grace Hopper',
        'description' : 'Grace Hopper Description'
        },
    {
        'name': 'Ada Lovelace',
        'description' : 'Ada Lovelace Description'
        }
]

@app.route('/api/womenInTech', methods=['GET'])
def get_womenInTech():
    return (jsonify(womenInTech))
    
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    app.run(debug=True)

