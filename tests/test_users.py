from fastapi.testclient import TestClient
from app.mainalchemy import app
from app import schemas

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == "Hello World"
    
# use -x flag in pytest to stop when test is failed

def test_create_user():
    response = client.post('/users/', json = {"email": "test@gmail.com", "password": "test@123"})
    assert response.status_code == 201
    # test keys
    print(111,response.json(), schemas.UserResponse)
    assert response.json().get('email') == "test@gmail.com"