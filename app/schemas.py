from pydantic import BaseModel

class ClienteCreate(BaseModel):
    nome: str
    email: str
    cpfcnpj: str
    servico: str