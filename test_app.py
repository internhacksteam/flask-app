from app import app 
from flask import json

def test_app():
	response = app.test_client().post(
		'/api/updateLevel',
		data = json.dumps({'UserID': 1}),
		content_type='application/json',
	)

	response2 = app.test_client().post(
		'/api/evaluatingAnswer',
		data = json.dumps({'Answer': 'print("Hello World!")'}),
		content_type='application/json',
		)

	response3 = app.test_client().get(
		'/api/displayLevels')

	data = json.loads(response.get_data(as_text=True))
	data2 = json.loads(response2.data)
	data3 = json.loads(response3.data)


	assert response.status_code == 200
	assert data['level'] == data['updatedLevel'] - 1

	assert response2.status_code == 200
	assert data2['response'] == 'Correct!'

	assert response3.status_code == 200

