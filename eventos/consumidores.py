import asyncio
from estrategias.estrategia_pagamento import PagamentoCartaoCredito, PagamentoPix, ContextoPagamento

async def consumidor_pagamentos(dados_evento: dict):
    """Consumidor: Serviço de Pagamento escuta 'PedidoCriado'"""
    print(f"[CONSUMIDOR: Pagamentos] Processando pagamento para o pedido #{dados_evento['id_pedido']}...")
    
    metodo = dados_evento.get("metodo_pagamento", "pix")
    valor = dados_evento.get("valor_total", 0.0)

    mapa_estrategias = {
        "cartao_credito": PagamentoCartaoCredito(),
        "pix": PagamentoPix()
    }
    
    estrategia = mapa_estrategias.get(metodo, PagamentoPix())
    contexto = ContextoPagamento(estrategia)
    resultado = contexto.executar_pagamento(valor)
    
    print(f"[CONSUMIDOR: Pagamentos] Sucesso! Resultado: {resultado}")

async def consumidor_notificacoes(dados_evento: dict):
    """Consumidor: Serviço de Notificação escuta 'PedidoCriado'"""
    print(f"[CONSUMIDOR: Notificações] Enviando e-mail de confirmação do pedido #{dados_evento['id_pedido']}...")
    await asyncio.sleep(0.5)
    print(f"[CONSUMIDOR: Notificações] E-mail enviado com sucesso para o Cliente #{dados_evento['id_cliente']}!")
