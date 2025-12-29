import pytest
from unittest.mock import patch
import jwt
import datetime
from utils.jwt_handler import generate_token, decode_token

class TestJWTHandler:

    @patch('utils.jwt_handler.SECRET', 'test-secret')
    def test_generate_token(self):
        token = generate_token('teste@email.com', 'cliente')

        assert token is not None
        assert isinstance(token, str)

    @patch('utils.jwt_handler.SECRET', 'test-secret')
    def test_decode_token_valid(self):
        token = generate_token('teste@email.com', 'admin')
        decoded = decode_token(token)

        assert decoded is not None
        assert decoded['email'] == 'teste@email.com'
        assert decoded['role'] == 'admin'

    @patch('utils.jwt_handler.SECRET', 'test-secret')
    def test_decode_token_expired(self):
        # Create an expired token
        payload = {
            'email': 'teste@email.com',
            'role': 'cliente',
            'exp': datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        }
        expired_token = jwt.encode(payload, 'test-secret', algorithm='HS256')

        decoded = decode_token(expired_token)

        assert decoded is None
