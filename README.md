# ShoopTree

Software Architecture & Design Patterns


----------------------------

# Modernização Arquitetural ShoopTree

Este repositório contém a implementação prática da prova de conceito funcional para a modernização arquitetural da plataforma e-commerce **ShoopTree**, demonstrando a migração de um monólito para uma **Arquitetura de Microsserviços Orientada a Eventos (EDA)**.

---

## Visão Geral da Arquitetura

A solução foi projetada para resolver os problemas de escalabilidade e alto acoplamento do sistema legado:
* **Desacoplamento de Domínio:** Os serviços de Produtos e Pagamentos possuem bases isoladas.
* **Comunicação Assíncrona:** Ações como geração de compras disparam eventos (`PedidoCriado`) processados de forma assíncrona por múltiplos consumidores.
* **Resiliência:** Falhas na notificação não interrompem a realização do pedido ou o processamento financeiro.

---

## Design Pattern Utilizado: Strategy Pattern

Para o **Serviço de Pagamentos**, adotou-se o padrão **Strategy**. 
* **Justificativa:** Permite encapsular os algoritmos de pagamento (PIX e Cartão de Crédito) em classes independentes (`CreditCardPayment` e `PixPayment`) que implementam uma interface comum (`PaymentStrategy`).
* **Vantagem:** Facilita a adição de novos gateways ou métodos de pagamento sem modificar o código existente (Respeitando o princípio *Open/Closed* do SOLID).

---

## Como Executar Localmente

### Pré-requisitos
* Python 3.9+ instalado
* Instalação das dependências:
  ```bash
  pip install fastapi uvicorn pydantic


