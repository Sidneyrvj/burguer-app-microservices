import pytest

def test_calcular_total():
    preco = 50
    quantidade = 2
    total = preco * quantidade
    assert total == 100

def test_pedido_valido():
    pedido = {
        "produto": "Pizza",
        "quantidade": 2
    }
    assert "produto" in pedido
    assert pedido["quantidade"] > 0

def test_quantidade_negativa():
    quantidade = -5
    assert quantidade < 0
