from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from estrategias.estrategia_pagamento import PagamentoCartaoCredito, PagamentoPix, ContextoPagamento

router = APIRouter(prefix="/pagamentos", tags=["Serviço de Pagamentos"])

db_pagamentos = []

class EsquemaPagamentoDireto(BaseModel):
    valor: float
    metodo: str  # 'pix' ou 'cartao_credito'

@router.get("")
def listar_pagamentos():
    """GET /pagamentos - Lista o histórico de pagamentos"""
    return {"status": "sucesso", "dados": db_pagamentos}

@router.post("")
def processar_pagamento_direto(pagamento: EsquemaPagamentoDireto):
    """POST /pagamentos - Processa um pagamento direto via API síncrona"""
    mapa_estrategias = {
        "cartao_credito": PagamentoCartaoCredito(),
        "pix": PagamentoPix()
    }
    
    estrategia = mapa_estrategias.get(pagamento.metodo)
    if not estrategia:
        raise HTTPException(status_code=400, detail="Método de pagamento inválido. Use 'pix' ou 'cartao_credito'.")

    contexto = ContextoPagamento(estrategia)
    resultado = contexto.executar_pagamento(pagamento.valor)
    db_pagamentos.append(resultado)
    
    return {"status": "sucesso", "dados": resultado}
