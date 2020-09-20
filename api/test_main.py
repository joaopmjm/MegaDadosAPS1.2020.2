from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

tarefa_uuid = ""

def test_read_main():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {'detail':'Not Found'}

def test_create_task():
    response = client.post("/criar", json={
        "nome": "teste",
        "descricao": "Descricao teste",
        })
    assert response.status_code == 201
    assert response.json() == { 
        "nome": "teste",
        "descricao": "Descricao teste",
        "status": "nao concluidos"
    }

def test_show_task():
    response = client.get("/listar/")
    assert response.status_code == 200
    global tarefa_uuid
    tarefa_uuid = list(response.json().keys())[0]

def test_check_task():
    response = client.patch(f"/{tarefa_uuid}/check")
    assert response.status_code == 200

def test_update_desc_task():
    response = client.patch(f"/{tarefa_uuid}/descricao?nova_descricao=Nova%20super%20hyper%20megatop%20Descricao")
    assert response.status_code == 200
    assert response.text == '"Nova super hyper megatop Descricao"'

def test_del_task():
    response = client.delete(f"/{tarefa_uuid}/deletar")
    assert response.status_code == 204