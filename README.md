# 🌦️ Weather Pipeline - ETL Project

## 📌 Visão geral

Esse projeto é um pipeline ETL **(Extract, Transform, Load)** desenvolvido em Python para coletar dados de clima de uma API externa, processá-los e armazená-los em um banco de dados PostgreSQL.

O objetivo é simular um fluxo real de engenharia de dados, aplicando boas práticas de organização, documentação, modularização e testes.

---

## ⚙️ Arquitetura do projeto

O pipeline é dividido em três etapas:

- **Extract**: coleta os dados brutos de clima da API OpenWeather
- **Transform**: realiza transformações tratando os dados brutos coletados
- **Load**: armazena os dados processados no PostgreSQL

---

## ⚙️ Orquestração e infraestrutura

O pipeline ETL é orquestrado pelo **Apache Airflow**, enquanto a infraestrutura do ambiente é gerenciada via **Docker e Docker Compose**.

---

## 🧱 Estrutura do projeto

```bash
pipeline_weather/
├── dags/
│   └── weather_dag.py
├── notebooks/
│   └── analysis.ipynb
├── src/
│   └── etl/
│       ├── __init__.py
│       ├── extract/
│       │   ├── __init__.py
│       │   └── extract_data.py
│       ├── transform/
│       │   ├── __init__.py
│       │   └── transform_data.py
│       └── load/
│           ├── __init__.py
│           └── load_data.py
│
├── tests/
│   ├── test_extract.py
│   └── test_transform.py
│
├── docker-compose.yaml
├── main.py
├── pyproject.toml
└── uv.lock

## 🛠️ Tecnologias utilizadas

- **Python** (linguagem principal do projeto)
- **Pandas** (processamento e transformação de dados)
- **Requests** (consumo de API REST - OpenWeatherMap)
- **JSON** (formato de dados da API)
- **Parquet** (armazenamento intermediário dos dados)
- **PostgreSQL** (banco de dados relacional)
- **SQLAlchemy** (conexão com banco de dados)
- **Pytest** (testes unitários)
- **Apache Airflow** (orquestração do pipeline ETL)
- **Docker & Docker Compose** (infraestrutura e ambiente isolado)
- **UV** (gerenciador de dependências Python)

## 💻 Ambiente de desenvolvimento

- **VS Code** (editor de código)
- **WSL2** (Windows Subsystem for Linux)
- **Ubuntu** (ambiente Linux utilizado no desenvolvimento)