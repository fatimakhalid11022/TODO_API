import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from app import settings  # assuming your settings are in a file named settings.py
from app.main import todo, get_session, todos  # assuming your FastAPI app is in a file named main.py

# Setup the Test Database
connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_string)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_session dependency
def override_get_session():
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()

todo.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="module")
def test_client():
    SQLModel.metadata.create_all(bind=engine)
    client = TestClient(todo)
    yield client
    SQLModel.metadata.drop_all(bind=engine)

def test_hello_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "mylady"}

def test_create_todo_endpoint(test_client):
    todo_data = {
        "title": "Test Todo"
    }
    response = test_client.post("/todo", json=todo_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"



# smple practice

# from fastapi.testclient import TestClient
# from app.main import todo


# client = TestClient(app=todo)


# def test_hello():
#   name : str = "hi"
#   assert name == "hi"
  
# def test_fastapi_hello():
#     response = client.get("/")
    
#     assert response.json() == {"hello":"mylady"}