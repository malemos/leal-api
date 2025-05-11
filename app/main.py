import os
from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, crud
from .database import engine, get_db
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Lê TRUSTED_ORIGINS da variável de ambiente
origins_env = os.getenv("TRUSTED_ORIGINS", "*")
origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if "*" not in origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TRUSTED_ORIGINS = set(origins) if "*" not in origins else set()

@app.post("/cadastro")
async def create_cliente(cliente: schemas.ClienteCreate, request: Request, db: Session = Depends(get_db)):
    origin = request.headers.get("origin")
    if TRUSTED_ORIGINS and origin not in TRUSTED_ORIGINS:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    
    return crud.create_cliente(db=db, cliente=cliente)