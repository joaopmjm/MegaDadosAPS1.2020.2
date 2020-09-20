from fastapi import FastAPI, HTTPException, Path, APIRouter
from typing import Optional
from uuid import uuid4, UUID
from .database import DBSession
from .models import Tarefa

db = DBSession()
router = APIRouter()
app = FastAPI()
app.include_router(
    router=router,
    prefix="/tarefas",
    tags=["tarefas"],
    responses={404: {"description": "Not found"}},
)

@app.get("/listar/")
async def listar_tarefas(q: str = "Todos"):
    print(f"Listing tarefas, entrou {q}")
    '''
        Display all tasks

        **Options**
        - Todos // Default
        - nao concluidos
        - concluidos
    '''
    if q == "Todos":
        return db.tasks
    if q == "não concluido" or q == "concluido":
        tarefas_selecionadas = {}
        for i in db.tasks:
            if db.tasks[i] == q:
                tarefas_selecionadas[i] = db.tasks[i]
        return tarefas_selecionadas
    else:
        raise HTTPException(status_code=404, detail="Tarefas Not Found")


@app.patch("/{tarefa_id}/descricao", response_model=str)
async def update_descricao(tarefa_id:UUID, nova_descricao: str):
    if tarefa_id not in db.tasks:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        db.tasks[tarefa_id].descricao = nova_descricao
        return nova_descricao

@app.patch("/{tarefa_id}/check")
async def update_descricao(tarefa_id: UUID):
    if tarefa_id not in db.tasks:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        if db.tasks[tarefa_id].status == "concluido":
            db.tasks[tarefa_id].status = "não concluido"
        else:
            db.tasks[tarefa_id].status = "concluido"
    return 201
    

@app.post("/criar", status_code=201)
async def create_item(tarefa: Tarefa):
    '''
    Cria uma tarefa
    Parametros:
    - Descrição

    '''
    db.tasks[uuid4()] = tarefa
    return tarefa

@app.delete("/{id_tarefa}/deletar", status_code=204)
async def deletar_tarefa(id_tarefa : UUID):
    '''
    Deleta uma tarefa
    Parâmetros:
    - Id da tarefa que deve ser deletada
    '''
    if id_tarefa not in db.tasks:
        raise HTTPException(status_code=404, detail="ID não encontrada")
    
    del db.tasks[id_tarefa]
