import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_variants_missing_gene(client):
    response = client.get("/variants")
    assert response.status_code == 400


def test_variants_with_gene(client):
    response = client.get("/variants?gene=TP53")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    for row in data:
        assert "gene" in row
        assert "variant" in row