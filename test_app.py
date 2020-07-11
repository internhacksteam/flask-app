from app import app 
from flask import json

def test_app():
	response = app.test_client().post(
		'/api/updateLevel',
		data = json.dumps({'UserID': 1}),
		content_type='application/json',
	)
	
	data = json.loads(response.get_data(as_text=True))

	assert response.status_code == 200
	assert data['level'] == data['updatedLevel'] - 1
