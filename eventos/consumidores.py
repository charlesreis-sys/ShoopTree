import asyncio
from estrategias.estrategia_pagamento import PagamentoCartaoCredito, PagamentoPix, ContextoPagamento

async def consumidor_pagamentos(dados_evento: dict):
    """Consumer 1: Serviço de Pagamento consumindo o evento 'CompraRealizada'"""
    print(f"[CONSUMER: Pagamentos] Evento recebido! Processando pagamento da compra do produto #{dados_evento['id_produto']}...")
    
    metodo = dados_evento.get("metodo_pagamento", "pix")
    valor = dados_evento.get("valor", 0.0)

    mapa_estrategias = {
        "cartao_credito": PagamentoCartaoCredito(),
        "pix": PagamentoPix()
    }
    
    estrategia = mapa_estrategias.get(metodo, PagamentoPix())
    contexto = ContextoPagamento(estrategia)
    resultado = contexto.executar_pagamento(valor)
    
    print(f"[CONSUMER: Pagamentos] Cobrança concluída com sucesso: {resultado}")

async def consumidor_notificacoes(dados_evento: dict):
    """Consumer 2: Serviço de Notificação consumindo o evento 'CompraRealizada'"""
    print(f"[CONSUMER: Notificações] Evento recebido! Preparando e-mail de confirmação...")
    await asyncio.sleep(0.5)
    print(f"[CONSUMER: Notificações] E-mail de confirmação enviado para o cliente sobre a compra de '{dados_evento['nome']}'!")
