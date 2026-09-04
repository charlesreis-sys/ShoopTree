from fastapi import FastAPI
from eventos.barramento import barramento
from eventos.consumidores import consumidor_pagamentos, consumidor_notificacoes
from rotas import produtos, pagamentos

app = FastAPI(
    title="PoC Microsserviços ShoopTree",
    description="Demonstração prática da arquitetura evolutiva da ShoopTree em Português"
)

# Registrar Consumidores no Barramento
barramento.inscrever("PedidoCriado", consumidor_pagamentos)
barramento.inscrever("PedidoCriado", consumidor_notificacoes)

# Incluir Rotas dos Serviços
app.include_router(produtos.router)
app.include_router(pagamentos.router)
