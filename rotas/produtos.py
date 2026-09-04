from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from eventos.barramento import barramento

router = APIRouter(prefix="/produtos", tags=["Serviço de Produtos"])

# Banco em memória
db_produtos = [
    {"id": 1, "nome": "Notebook Dell", "preco": 4500.00},
    {"id": 2, "nome": "Mouse Sem Fio", "preco": 120.00}
]

class EsquemaProduto(BaseModel):
    nome: str
    preco: float

class EsquemaCompra(BaseModel):
    id_pedido: int
    id_cliente: int
    id_produto: int
    metodo_pagamento: str

@router.get("")
def listar_produtos():
    return {"status": "sucesso", "dados": db_produtos}

@router.post("")
def criar_produto(produto: EsquemaProduto):
    novo_id = len(db_produtos) + 1
    novo_prod = {"id": novo_id, "nome": produto.nome, "preco": produto.preco}
    db_produtos.append(novo_prod)
    return {"status": "sucesso", "dados": novo_prod}

@router.post("/comprar")
async def realizar_compra(compra: EsquemaCompra):
    produto = next((p for p in db_produtos if p["id"] == compra.id_produto), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    evento_payload = {
        "id_pedido": compra.id_pedido,
        "id_cliente": compra.id_cliente,
        "nome_produto": produto["nome"],
        "valor_total": produto["preco"],
        "metodo_pagamento": compra.metodo_pagamento
    }
    
    await barramento.publicar("PedidoCriado", evento_payload)

    return {
        "status": "sucesso",
        "mensagem": "Compra iniciada! Evento 'PedidoCriado' gerado com sucesso.",
        "id_pedido": compra.id_pedido
    }
