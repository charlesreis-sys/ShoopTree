from fastapi import APIRouter
from pydantic import BaseModel
from eventos.barramento import barramento

router = APIRouter(prefix="/produtos", tags=["Serviço de Produtos"])

db_produtos = [
    {"id": 1, "nome": "Notebook Dell", "preco": 4500.00},
    {"id": 2, "nome": "Mouse Sem Fio", "preco": 120.00}
]

class EsquemaProduto(BaseModel):
    nome: str
    preco: float
    metodo_pagamento: str = "pix"  # Opções: 'pix' ou 'cartao_credito'

@router.get("")
def listar_produtos():
    """GET /produtos - Lista os produtos cadastrados"""
    return {"status": "sucesso", "dados": db_produtos}

@router.post("")
async def criar_produto_e_gerar_compra(produto: EsquemaProduto):
    """POST /produtos - Cadastra produto e dispara o evento de compra no barramento"""
    novo_id = len(db_produtos) + 1
    novo_item = {
        "id": novo_id, 
        "nome": produto.nome, 
        "preco": produto.preco
    }
    db_produtos.append(novo_item)

    # Payload do Evento
    evento_compra = {
        "id_produto": novo_id,
        "nome": produto.nome,
        "valor": produto.preco,
        "metodo_pagamento": produto.metodo_pagamento
    }

    # PRODUCER: Publica o evento 'CompraRealizada' no barramento assíncrono
    await barramento.publicar("CompraRealizada", evento_compra)

    return {
        "status": "sucesso",
        "mensagem": "Produto registrado e evento de compra gerado com sucesso!",
        "dados": novo_item
    }
