import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from controllers.auth_controller import auth_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestAuthController:

    @patch('controllers.auth_controller.render_template')
    def test_login_page_get(self, mock_render, client):
        mock_render.return_value = 'rendered_template'

        response = client.get('/auth/login')

        assert response.status_code == 200
        mock_render.assert_called_once_with('login.html')

    @patch('controllers.auth_controller.render_template')
    @patch('controllers.auth_controller.redirect')
    @patch('controllers.auth_controller.login_user')
    def test_login_post_success(self, mock_login, mock_redirect, mock_render, client):
        mock_login.return_value = {
            'email': 'teste@email.com',
            'name': 'João Silva',
            'role': 'cliente',
            'token': 'fake_token'
        }
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/auth/login', data={
            'email': 'teste@email.com',
            'password': 'senha123'
        })

        mock_login.assert_called_once_with('teste@email.com', 'senha123')
        mock_redirect.assert_called()

    @patch('controllers.auth_controller.redirect')
    @patch('controllers.auth_controller.login_user')
    def test_login_post_invalid_credentials(self, mock_login, mock_redirect, client):
        mock_login.return_value = None
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/auth/login', data={
            'email': 'teste@email.com',
            'password': 'senha_errada'
        })

        mock_redirect.assert_called()

    def test_register_page_redirect(self, client):
        response = client.get('/auth/register', follow_redirects=False)

        assert response.status_code == 302
        assert 'localhost:5001/user/create' in response.location

    @patch('controllers.auth_controller.render_template')
    def test_dashboard_with_session(self, mock_render, client):
        mock_render.return_value = 'rendered_template'

        with client.session_transaction() as sess:
            sess['user'] = {
                'email': 'teste@email.com',
                'name': 'João Silva',
                'role': 'cliente'
            }

        response = client.get('/auth/dashboard')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.auth_controller.redirect')
    def test_dashboard_without_session(self, mock_redirect, client):
        mock_redirect.return_value = 'redirect_response'

        response = client.get('/auth/dashboard')

        mock_redirect.assert_called()

    def test_logout(self, client):
        with client.session_transaction() as sess:
            sess['user'] = {'email': 'teste@email.com'}

        response = client.get('/auth/logout', follow_redirects=False)

        assert response.status_code == 302

        with client.session_transaction() as sess:
            assert 'user' not in sess
