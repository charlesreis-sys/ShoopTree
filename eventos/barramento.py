import asyncio
from typing import List, Dict, Callable

class BarramentoEventos:
    """Simula um Broker de Mensageria (ex: RabbitMQ/Kafka) em memória."""
    def __init__(self):
        self._inscritos: Dict[str, List[Callable]] = {}

    def inscrever(self, tipo_evento: str, manipulador: Callable):
        if tipo_evento not in self._inscritos:
            self._inscritos[tipo_evento] = []
        self._inscritos[tipo_evento].append(manipulador)

    async def publicar(self, tipo_evento: str, dados: dict):
        print(f"\n[BARRAMENTO] Evento '{tipo_evento}' publicado: {dados}")
        if tipo_evento in self._inscritos:
            for manipulador in self._inscritos[tipo_evento]:
                asyncio.create_task(manipulador(dados))

# Instância global do barramento
barramento = BarramentoEventos()
