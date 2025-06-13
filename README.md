# 🤖 LinkedIn Automation API

![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

## 📋 Sobre o Projeto

Esta API permite automatizar interações com o LinkedIn usando Selenium e FastAPI. Com esta ferramenta, você pode:

- Fazer login automatizado no LinkedIn
- Capturar screenshots da página após o login
- Acessar e coletar certificados do perfil do LinkedIn
- Armazenar os certificados coletados em um banco de dados MySQL

## 🚀 Como Começar

### Pré-requisitos

- Docker e Docker Compose
- Python 3.10+
- MySQL 9.0 (se executar localmente)

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/linkedin-automation-api.git
cd linkedin-automation-api
```

2. Execute com Docker Compose (recomendado):

```bash
docker-compose up -d
```

Isso iniciará tanto a API quanto o banco de dados MySQL.

3. Ou execute localmente:

```bash
# Instale as dependências
pip install -r requirements.txt

# Configure seu próprio banco de dados MySQL e ajuste a variável DATABASE_URL
# em main.py ou como variável de ambiente

# Inicie a aplicação
python main.py
```

A API estará disponível em `http://localhost:5000`

## 🔧 Endpoints da API

### Página Inicial

```
GET /
```

Retorna a documentação interativa da API (Swagger UI).

### Login no LinkedIn

```
POST /linkedin/login
```

Body:
```json
{
  "email": "seu-email@exemplo.com",
  "password": "sua-senha"
}
```

Realiza login no LinkedIn e retorna um screenshot da página inicial após o login bem-sucedido.

### Extrair Certificados do LinkedIn

```
POST /certificado/linkedin/profile
```

Body:
```json
{
  "username": "nome-de-usuario-linkedin",
  "email": "seu-email@exemplo.com",
  "password": "sua-senha"
}
```

Faz login no LinkedIn, navega até a seção de certificados do perfil especificado, extrai todos os certificados encontrados, salva no banco de dados e retorna uma lista com os detalhes dos certificados.

## 📝 Exemplo de Uso

### Login no LinkedIn

```bash
curl -X 'POST' \
  'http://localhost:5000/linkedin/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "usuario@email.com",
  "password": "senha_do_usuario"
}'
```

### Extrair Certificados do LinkedIn

```bash
curl -X 'POST' \
  'http://localhost:5000/certificado/linkedin/profile' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "SEU_USUARIO",
  "email": "usuario@email.com",
  "password": "senha_do_usuario"
}'
```

## ⚠️ Avisos Importantes

- **Segurança**: Nunca compartilhe suas credenciais ou armazene-as em texto simples
- **Termos de Serviço**: Certifique-se de que seu uso está em conformidade com os Termos de Serviço do LinkedIn
- **Rate Limiting**: Evite fazer muitas requisições em curto período para evitar bloqueios

## 🗂️ Estrutura do Projeto

```
.
├── domain/
│   ├── linkedin/
│   │   ├── certificados/
│   │   │   ├── CertificadoController.py  # Endpoints para certificados
│   │   │   ├── CertificadoDto.py        # DTOs de certificados
│   │   │   ├── CertificadoModel.py      # Modelo do banco de dados
│   │   │   └── CertificadoService.py    # Lógica de negócio
│   │   ├── LinkedinController.py        # Endpoints gerais do LinkedIn
│   │   └── LinkedinDto.py               # DTOs para operações do LinkedIn
├── utils/
│   ├── database.py                      # Configuração do banco de dados
│   └── selenium.py                      # Utilitários para o Selenium
├── main.py                              # Ponto de entrada da aplicação
├── Dockerfile                           # Configuração do contêiner
├── docker-compose.yml                   # Configuração de serviços
└── requirements.txt                     # Dependências do projeto
```

## 💾 Modelo de Dados

### Tabela: certificado

| Campo           | Tipo    | Descrição                               |
|-----------------|---------|----------------------------------------|
| id              | Integer | ID único do certificado (chave primária)|
| titulo          | String  | Título do certificado                   |
| empresa         | String  | Empresa emissora do certificado         |
| data_validacao  | String  | Data ou status de validação             |
| link_url        | String  | URL para visualizar a credencial        |

## 🔒 Considerações de Segurança

- A API deve ser executada em ambiente seguro e protegido
- Considere implementar HTTPS para proteger as credenciais durante a transmissão
- Não armazene credenciais em texto simples
- Implemente um sistema de autenticação para a API em ambientes de produção

## 📚 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para construção da API
- **Selenium**: Para automação do navegador e extração de dados
- **Docker & Docker Compose**: Para containerização e orquestração dos serviços
- **MySQL**: Banco de dados para armazenamento dos certificados
- **SQLAlchemy**: ORM para interação com o banco de dados
- **Pydantic**: Para validação de dados e serialização
- **Python 3.10**: Linguagem de programação base

## 📝 TODO

- Criar método que não dependa de banco
- Dividir e organizar melhor o método que puxe os certificados do linkedin
- Separar regras de negócio somente para o service