import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app import models, schemas, crud
from app.database import Base

# Banco SQLite em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_cliente(db):
    cliente_data = schemas.ClienteCreate(
        nome="João da Silva",
        email="joao@teste.com",
        cpfcnpj="123.456.789-00",
        servico="mei"
    )
    novo_cliente = crud.create_cliente(db, cliente_data)
    assert novo_cliente.id is not None
    assert novo_cliente.nome == "João da Silva"

def test_create_cliente_missing_fields(db):
    with pytest.raises(ValidationError):
        # Campo email ausente
        schemas.ClienteCreate(
            nome="Maria",
            cpfcnpj="999.999.999-99",
            servico="simples"
        )

def test_duplicate_cliente_should_create_twice(db):
    cliente_data = schemas.ClienteCreate(
        nome="Repetido",
        email="rep@teste.com",
        cpfcnpj="123.123.123-00",
        servico="mei"
    )
    c1 = crud.create_cliente(db, cliente_data)
    c2 = crud.create_cliente(db, cliente_data)
    assert c1.id != c2.id