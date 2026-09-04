from abc import ABC, abstractmethod

class EstrategiaPagamento(ABC):
    @abstractmethod
    def processar_pagamento(self, valor: float) -> dict:
        pass

class PagamentoCartaoCredito(EstrategiaPagamento):
    def processar_pagamento(self, valor: float) -> dict:
        return {"metodo": "Cartão de Crédito", "status": "APROVADO", "valor": valor}

class PagamentoPix(EstrategiaPagamento):
    def processar_pagamento(self, valor: float) -> dict:
        return {"metodo": "PIX", "status": "APROVADO", "valor": valor, "codigo_qr": "00020126360014BR.GOV.BCB.PIX..."}

class ContextoPagamento:
    def __init__(self, estrategia: EstrategiaPagamento):
        self._estrategia = estrategia

    def executar_pagamento(self, valor: float) -> dict:
        return self._estrategia.processar_pagamento(valor)
