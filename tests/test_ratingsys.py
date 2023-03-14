import pytest
from app import app


def test_landing():
    with app.app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

def test_home():
    with app.app.test_client() as test_client:
        response = test_client.get('/home')
        assert response.status_code == 200

def test_login():
    with app.app.test_client() as test_client:
        response = test_client.get('/login')
        assert response.status_code == 200

def test_logout():
    with app.app.test_client() as test_client:
        response = test_client.get('/logout')
        assert response.status_code == 200

def test_register():
    with app.app.test_client() as test_client:
        response = test_client.get('/register')
        assert response.status_code == 200


def test_create_rating():
     with app.app.test_client() as test_client:
        response = test_client.get('/go_to_create_rating')
        assert response.status_code == 200

def test_rating_given():
    with app.app.test_client() as test_client:
        response = test_client.get('/go_to_view_ratings_given')
        assert response.status_code == 200









