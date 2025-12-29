import pytest
from unittest.mock import patch, MagicMock
from services.user_service import create_user, get_user_by_email, update_user, delete_user

@pytest.fixture
def mock_db():
    with patch('services.user_service.users_col') as mock_col:
        yield mock_col

class TestUserService:

    def test_create_user_success(self, mock_db):
        mock_db.find_one.return_value = None
        mock_db.insert_one.return_value = MagicMock()

        response, status = create_user(
            email="teste@email.com",
            password="senha123",
            name="João Silva",
            address="Rua Teste, 123",
            role="cliente"
        )

        assert status == 201
        assert response["message"] == "Usuário criado com sucesso"
        mock_db.insert_one.assert_called_once()

    def test_create_user_duplicate_email(self, mock_db):
        mock_db.find_one.return_value = {"email": "teste@email.com"}

        response, status = create_user(
            email="teste@email.com",
            password="senha123",
            name="João Silva",
            address="Rua Teste, 123"
        )

        assert status == 400
        assert "error" in response

    def test_get_user_by_email_found(self, mock_db):
        mock_db.find_one.return_value = {
            "email": "teste@email.com",
            "name": "João Silva",
            "address": "Rua Teste, 123",
            "role": "cliente"
        }

        user = get_user_by_email("teste@email.com")

        assert user is not None
        assert user["email"] == "teste@email.com"

    def test_get_user_by_email_not_found(self, mock_db):
        mock_db.find_one.return_value = None
        user = get_user_by_email("naoexiste@email.com")
        assert user is None

    def test_update_user(self, mock_db):
        mock_db.update_one.return_value = MagicMock()
        update_user("teste@email.com", "Novo Nome", "Novo Endereço")
        mock_db.update_one.assert_called_once()

    def test_delete_user(self, mock_db):
        mock_db.delete_one.return_value = MagicMock()
        delete_user("teste@email.com")
        mock_db.delete_one.assert_called_once()
