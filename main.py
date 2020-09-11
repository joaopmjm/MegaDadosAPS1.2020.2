from fastapi import FastAPI, Query, Body, HTTPException
from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class Tarefa(BaseModel):
    nome : str
    descricao : str
    status : str = "nao concluidos"

tarefas = {
    UUID:Tarefa(
        nome = "Crud",
        descricao = "Fazer esse Crud funcionar"
    ),
    UUID:Tarefa(
        nome = "Kill",
        descricao = "Matar 4 pessoas"
    )
}

app = FastAPI()

@app.get("/tarefas/")
async def listar_tarefas(q: str = "Todos"):
    '''
        Display all tasks

        **Options**
        - Todos // Default, dont need to put as parameter
        - nao concluidos
        - concluidos
    '''
    if q == "Todos":
        return tarefas
    if q == "não concluido" or q == "concluido":
        tarefas_selecionadas = {}
        for i in tarefas:
            if tarefas[i] == q:
                tarefas_selecionadas[i] = tarefas[i]
        return tarefas_selecionadas
    else:
        raise HTTPException(status_code=404, detail="Tarefas Not Found")


@app.patch("/tarefa/{tarefa_id}/descricao", response_model=str)
async def update_descricao(tarefa_id: UUID, nova_descricao: str):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        tarefas[tarefa_id].descricao = nova_descricao
        return nova_descricao

@app.patch("/tarefa/{tarefa_id}/check")
async def update_descricao(tarefa_id: UUID):
    if tarefa_id not in tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        if tarefas[tarefa_id].status == "concluido":
            tarefas[tarefa_id].status = "não concluido"
        else:
            tarefas[tarefa_id].status = "concluido"
    

@app.post("/tarefas/criar")
async def create_item(tarefa: Tarefa):
    '''
    Cria uma tarefa
    Parametros:
    - Descrição

    '''
    return Tarefa

@app.delete("tarefa/deletar/{id_tarefa}")
async def deletar_tarefa(id_tarefa : UUID = Query(...), min_length = 1):
    '''
    Deleta uma tarefa
    Parâmetros:
    - Id da tarefa que deve ser deletada
    '''
    del(tarefas, id_tarefa)
