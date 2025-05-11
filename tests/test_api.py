import os
import pytest
from fastapi.testclient import TestClient
from app import crud

def test_post_cadastro_success(monkeypatch):
    from app.main import app

    def mock_create_cliente(db, cliente):
        return type("Cliente", (), {
            "id": 1,
            "nome": cliente.nome,
            "email": cliente.email,
            "cpfcnpj": cliente.cpfcnpj,
            "servico": cliente.servico
        })()

    monkeypatch.setattr(crud, "create_cliente", mock_create_cliente)

    client = TestClient(app)

    payload = {
        "nome": "Teste API",
        "email": "api@teste.com",
        "cpfcnpj": "000.000.000-00",
        "servico": "mei"
    }
    headers = {"origin": "http://localhost:5500"}

    response = client.post("/cadastro", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Teste API"
    assert data["email"] == "api@teste.com"

def test_post_cadastro_blocked_origin(monkeypatch):
    os.environ["TRUSTED_ORIGINS"] = "http://localhost:5500"

    from importlib import reload
    import app.main
    reload(app.main)  # força o app a ler nova config

    client = TestClient(app.main.app)

    def mock_create_cliente(*args, **kwargs):
        raise Exception("Não deveria ser chamado")

    monkeypatch.setattr(crud, "create_cliente", mock_create_cliente)

    payload = {
        "nome": "Invasor",
        "email": "hacker@x.com",
        "cpfcnpj": "111.111.111-11",
        "servico": "simples"
    }
    headers = {"origin": "http://site-nao-autorizado.com"}

    response = client.post("/cadastro", json=payload, headers=headers)
    assert response.status_code == 403
    assert "não autorizado" in response.text.lower()