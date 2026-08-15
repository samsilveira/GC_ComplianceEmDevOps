import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Testa a resposta da rota principal (/)"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Bem-vindo à API do experimento de Compliance em DevOps!"
    assert data["version"] == "1.0.0"

def test_health_route(client):
    """Testa o código de status e o conteúdo da rota /health"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "up"
    assert data["healthy"] is True

def test_not_found_route(client):
    """Cobre um cenário negativo acessando uma rota inexistente"""
    response = client.get("/rota-invalida")
    assert response.status_code == 404
