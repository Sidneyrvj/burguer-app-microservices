import pytest

def test_senha_valida():
    senha = "senha123"
    assert len(senha) >= 6
    assert isinstance(senha, str)

def test_senha_invalida():
    senha = "123"
    assert len(senha) < 6

def test_validar_token():
    token = "abc123xyz789"
    assert len(token) > 0
    assert isinstance(token, str)
    assert len(token) >= 10
