# Vendas CLI

Uma ferramenta de linha de comando em Python para processar arquivos CSV de vendas e gerar relatórios.

## Funcionalidades

- Leitura de CSV de vendas.
- Cálculo de total de vendas por produto.
- Cálculo do valor total de todas as vendas.
- Identificação do produto mais vendido.
- Filtragem de vendas por intervalo de datas.
- Saída em formato de texto formatado (tabela) ou JSON.

## Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/rodrigoFerreir/sales_report && cd sales_report
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Linux/macOS
    # .venv\Scripts\activate   # No Windows
    ```

3.  **Instale o pacote**

    ```bash
    pip install .
    ```

## Uso

O comando principal é `vendas-cli`. Ele aceita o caminho para um arquivo CSV de vendas como argumento obrigatório.

### Exemplo de Arquivo CSV (`data/vendas.csv`)

```csv
produto,preco_unitario,quantidade,data
Laptop,3500.50,2,2025-10-20
Mouse,150.00,5,2025-10-21
Teclado,300.25,3,2025-10-21
Monitor,800.00,1,2025-10-22
Laptop,3400.00,1,2025-10-22
Fone de ouvido,200.00,4,2025-10-23
Mouse,160.00,2,2025-10-23
```

### Executando o Relatório

-   **Relatório completo em texto:**

    ```bash
    vendas-cli data/vendas.csv
    ```

-   **Relatório completo em JSON:**

    ```bash
    vendas-cli data/vendas.csv --format json
    ```

-   **Relatório filtrado por intervalo de datas (ex: entre 2025-10-21 e 2025-10-22):**

    ```bash
    vendas-cli data/vendas.csv --start-date 2025-10-21 --end-date 2025-10-22
    ```

## Executando os Testes

Para executar os testes unitários, certifique-se de estar no diretório raiz do projeto e com o ambiente virtual ativado:

```bash
pytest
```
