import logging
import os

import pytest
from app import create_app, User
from app.db import db

@pytest.fixture()
def application():
    """This makes the app"""
    #you need this one if you want to see whats in the database
    #os.environ['FLASK_ENV'] = 'development'
    #you need to run it in testing to pass on github
    os.environ['FLASK_ENV'] = 'testing'

    application = create_app()

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        # db.drop_all()
"""
@pytest.fixture()
def add_user(application):
    with application.app_context():
        user = User('test@email.com', 'tester')
        db.session.add(user)
        db.session.commit()
"""
class AuthActions:
    def __init__(self, client):
        self._client = client

    def register(self, email="test@email.com", password="Tester1@"):
        return self._client.post(
            "/register", data={"email": email, "password": password, "confirm": password}
        )
    def login(self, email="test@email.com", password="Tester1@"):
        return self._client.post(
            "/login", data={"email": email, "password": password}
        )
    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()