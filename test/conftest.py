import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.base import Base, get_db
from app.main import app


# Set up a test database URL
ADMIN_DATABASE_URL = os.getenv("ADMIN_DATABASE_URL", "postgresql://postgres:root@127.0.0.1/postgres")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:root@127.0.0.1/test_task_manager_db")

os.environ["DATABASE_URL"] = TEST_DATABASE_URL

admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")

def create_test_database():
    """Create the test database if it doesn't exist."""
    with admin_engine.connect() as connection:
        try:
            connection.execute(
                text(f"CREATE DATABASE {TEST_DATABASE_URL.split('/')[-1]}")
            )
        except ProgrammingError as e:
            print("Database already exists, continuing...")
        except Exception as e:
            raise SystemError(f"Error while checking db {type(e)}")

engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    create_test_database()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


