# 🧾 Orçamento Imobiliário —

Aplicação em **Python** (arquivo único) que calcula o aluguel conforme regras de negócio e **gera um CSV formatado**, incluindo **Corretor** e **Cliente** no topo do relatório.

---

## 🚀 O que esta versão faz
- Coleta dados: **Corretor**, **Cliente**, **Tipo do imóvel**, **Quartos**, **Vagas**, **Há crianças?**, **Nº de parcelas** (1..5)
- Calcula o **aluguel** com base no tipo e condições
- Calcula a **parcela do contrato** (R$ 2.000 ÷ nº de parcelas)
- Gera **tabela de 12 meses** (aluguel + parcela até quitar o contrato)
- Cria um **CSV formatado** com:
  - Título e bloco de **Resumo** (Aluguel mensal, Parcela, Total)
  - Cabeçalho com cor e **linhas zebradas**
  - Valores em formato **R$**
  - **Corretor** e **Cliente** no topo
  - Cabeçalho fixo (freeze panes) e largura ajustada
- **Abre o Excel automaticamente** ao final (Windows/macOS/Linux)

---

## 📁 Arquivo principal
`orcamento_csv_corretor_cliente.py`

> Não há dependência de outros arquivos. É um script **autônomo**.

---

## ⚙️ Instalação e execução

1) Instale a dependência:
```bash
pip install openpyxl
```

2) Execute o script:
```bash
python orcamento_csv_corretor_cliente.py
```

> No **Spyder**, você pode instalar no Console com `!pip install openpyxl` e rodar com **F5**.

---

## 🧠 Regras de Negócio (resumo)

- **Apartamento (base R$ 700)**  
  + R$ 200 (2 quartos), + R$ 300 (vaga), **–5%** se **sem crianças**  
- **Casa (base R$ 900)**  
  + R$ 250 (2 quartos), + R$ 300 (vaga)  
- **Estúdio (base R$ 1.200)**  
  + R$ 250 (até 2 vagas) + **R$ 60 por vaga extra**  
- **Contrato:** R$ **2.000**, parcelável em até **5x**

---

## 🧮 Pseudocódigo (alto nível)

```text
ler(corretor, cliente, tipo, quartos/vagas, tem_criancas, parcelas)
imovel = Apartamento|Casa|Estudio(...)
aluguel = imovel.calcular_aluguel()
parcela = 2000 / parcelas
para mes em 1..12:
    parcela_mes = parcela se mes ≤ parcelas senão 0
    total_mes = aluguel + parcela_mes
montar_planilha_csv(corretor, cliente, resumo, 12 meses formatados)
abrir_csv()
```

---

## 👥 Integrante
- **André Felipe**
---

## 📝 Observações
- O arquivo CSV é salvo no mesmo diretório do script. O nome padrão sugerido é `parcelas_orcamento.csv`.
- Se o CSV não abrir automaticamente, o arquivo estará salvo e pode ser aberto manualmente.
- Caso use macOS/Linux, é usado o aplicativo padrão de planilhas do sistema.
