import os
import subprocess
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db



load_dotenv()
test_database_url = os.getenv("SQLALCHEMY_TEST_DATABASE_URL") 

engine = create_engine(test_database_url)
TestingSessionLocal = sessionmaker(bind=engine)

# Apply migrations before the test session
@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    subprocess.run(["alembic", "upgrade", "head"])

# DB session per test, with rollback
@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# FastAPI client with overridden DB
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
