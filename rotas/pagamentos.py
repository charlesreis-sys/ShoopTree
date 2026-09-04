from fastapi import APIRouter, HTTPException
from estrategias.estrategia_pagamento import PagamentoCartaoCredito, PagamentoPix, ContextoPagamento

router = APIRouter(prefix="/pagamentos", tags=["Serviço de Pagamentos"])

db_pagamentos = []

@router.get("")
def listar_pagamentos():
    return {"status": "sucesso", "dados": db_pagamentos}

@router.post("")
def processar_pagamento_direto(valor: float, metodo: str):
    mapa_estrategias = {
        "cartao_credito": PagamentoCartaoCredito(),
        "pix": PagamentoPix()
    }
    estrategia = mapa_estrategias.get(metodo)
    if not estrategia:
        raise HTTPException(status_code=400, detail="Método de pagamento inválido")

    contexto = ContextoPagamento(estrategia)
    resultado = contexto.executar_pagamento(valor)
    db_pagamentos.append(resultado)
    return {"status": "sucesso", "dados": resultado}
