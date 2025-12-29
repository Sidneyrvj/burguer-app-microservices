import pytest

def test_preco_valido():
    preco = 25.50
    assert preco > 0
    assert isinstance(preco, float)

def test_nome_produto():
    produto = "Hamburguer Deluxe"
    assert len(produto) > 0
    assert isinstance(produto, str)
    assert "Hamburguer" in produto

def test_estoque():
    estoque = 50
    assert estoque >= 0
    assert isinstance(estoque, int)
