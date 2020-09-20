from pydantic import BaseModel

class Tarefa(BaseModel):
    nome : str
    descricao : str
    status : str = "nao concluidos"