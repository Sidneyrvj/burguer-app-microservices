import pytest
from unittest.mock import patch, MagicMock
from services.auth_service import login_user

@pytest.fixture
def mock_users_col():
    with patch('services.auth_service.users_col') as mock:
        yield mock

class TestAuthService:

    @patch('services.auth_service.check_password_hash')
    @patch('services.auth_service.generate_token')
    def test_login_user_success(self, mock_generate_token, mock_check_password, mock_users_col):
        mock_users_col.find_one.return_value = {
            'email': 'teste@email.com',
            'password': 'hashed_password',
            'name': 'João Silva',
            'address': 'Rua Teste, 123',
            'role': 'cliente'
        }
        mock_check_password.return_value = True
        mock_generate_token.return_value = 'fake_token_123'

        result = login_user('teste@email.com', 'senha123')

        assert result is not None
        assert result['email'] == 'teste@email.com'
        assert result['name'] == 'João Silva'
        assert result['role'] == 'cliente'
        assert result['token'] == 'fake_token_123'

    def test_login_user_not_found(self, mock_users_col):
        mock_users_col.find_one.return_value = None

        result = login_user('naoexiste@email.com', 'senha123')

        assert result is None

    @patch('services.auth_service.check_password_hash')
    def test_login_user_wrong_password(self, mock_check_password, mock_users_col):
        mock_users_col.find_one.return_value = {
            'email': 'teste@email.com',
            'password': 'hashed_password',
            'role': 'cliente'
        }
        mock_check_password.return_value = False

        result = login_user('teste@email.com', 'senha_errada')

        assert result is None
