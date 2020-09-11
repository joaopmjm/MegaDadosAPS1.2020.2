from fastapi import FastAPI, Query, Body
from typing import Optional, List
from pydantic import BaseModel, Field

class Tarefa(BaseModel):
    descricao : str = Field(..., exemplo="Fazer café")
    status : str = "não concluido"

tarefas = {}

app = FastAPI()

@app.get("/tarefas/", response_model=Tarefa)
def listar_tarefas():
    return tarefas


@app.put("/tarefas/{id_tarefa}")
async def update_descricao(id_tarefa : int = Query(...), tarefa : Tarefa = Body(...)):
    tarefas[id_tarefa] = tarefa
    

@app.post("/tarefas/criar")
async def create_item(item: Item):
    return item
