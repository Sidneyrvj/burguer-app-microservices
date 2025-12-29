import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from controllers.user_controller import user_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(user_bp, url_prefix='/user')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestUserController:

    @patch('controllers.user_controller.render_template')
    @patch('controllers.user_controller.create_user')
    @patch('controllers.user_controller.redirect')
    def test_create_user_post_success(self, mock_redirect, mock_create_user, mock_render, client):
        mock_create_user.return_value = ({'message': 'Usuário criado com sucesso'}, 201)
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/user/create', data={
            'email': 'teste@email.com',
            'password': 'senha123',
            'name': 'João Silva',
            'address': 'Rua Teste, 123',
            'role': 'cliente'
        })

        mock_create_user.assert_called_once()
        mock_redirect.assert_called_once()

    @patch('controllers.user_controller.render_template')
    @patch('controllers.user_controller.create_user')
    @patch('controllers.user_controller.redirect')
    def test_create_user_post_error(self, mock_redirect, mock_create_user, mock_render, client):
        mock_create_user.return_value = ({'error': 'Usuário já existe'}, 400)
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/user/create', data={
            'email': 'teste@email.com',
            'password': 'senha123',
            'name': 'João Silva',
            'address': 'Rua Teste, 123'
        })

        mock_redirect.assert_called_once()

    @patch('controllers.user_controller.render_template')
    def test_create_user_get(self, mock_render, client):
        mock_render.return_value = 'rendered_template'

        response = client.get('/user/create')

        assert response.status_code == 200
        mock_render.assert_called_once_with('create.html')

    @patch('controllers.user_controller.render_template')
    @patch('controllers.user_controller.get_user_by_email')
    def test_profile_found(self, mock_get_user, mock_render, client):
        mock_get_user.return_value = {
            'email': 'teste@email.com',
            'name': 'João Silva',
            'address': 'Rua Teste, 123',
            'role': 'cliente'
        }
        mock_render.return_value = 'rendered_template'

        response = client.get('/user/profile/teste@email.com')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.user_controller.get_user_by_email')
    def test_profile_not_found(self, mock_get_user, client):
        mock_get_user.return_value = None

        response = client.get('/user/profile/naoexiste@email.com')

        assert response.status_code == 404

    @patch('controllers.user_controller.render_template')
    @patch('controllers.user_controller.redirect')
    @patch('controllers.user_controller.get_user_by_email')
    @patch('controllers.user_controller.update_user')
    def test_edit_user_post(self, mock_update, mock_get_user, mock_redirect, mock_render, client):
        mock_get_user.return_value = {'email': 'teste@email.com', 'name': 'João'}
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/user/edit/teste@email.com', data={
            'name': 'João Silva',
            'address': 'Novo Endereço'
        })

        mock_update.assert_called_once()
        mock_redirect.assert_called_once()

    @patch('controllers.user_controller.render_template')
    @patch('controllers.user_controller.get_user_by_email')
    def test_edit_user_get(self, mock_get_user, mock_render, client):
        mock_get_user.return_value = {'email': 'teste@email.com', 'name': 'João'}
        mock_render.return_value = 'rendered_template'

        response = client.get('/user/edit/teste@email.com')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.user_controller.redirect')
    @patch('controllers.user_controller.delete_user')
    def test_delete_user(self, mock_delete, mock_redirect, client):
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/user/delete/teste@email.com')

        mock_delete.assert_called_once_with('teste@email.com')
        mock_redirect.assert_called_once()
