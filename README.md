# 🤖 LinkedIn Automation API

![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 📋 Sobre o Projeto

Esta API permite automatizar interações com o LinkedIn usando Selenium e FastAPI. Com esta ferramenta, você pode:

- Fazer login automatizado no LinkedIn
- Capturar screenshots de qualquer página web
- Acessar diferentes funcionalidades do LinkedIn via API

## 🚀 Como Começar

### Pré-requisitos

- Docker e Docker Compose
- Python 3.10+

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/linkedin-automation-api.git
cd linkedin-automation-api
```

2. Execute com Docker:

```bash
docker build -t linkedin-automation .
docker run -p 8000:8000 linkedin-automation
```

3. Ou execute localmente:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🔧 Endpoints da API

### Página Inicial

```
GET /
```

Retorna uma mensagem de boas-vindas.

### Capturar Screenshot

```
GET /screenshot?url={url}
```

Captura um screenshot de qualquer URL especificada.

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

### Dizer Olá

```
GET /hello/{name}
```

Retorna uma mensagem personalizada de saudação.

## 📝 Exemplo de Uso

### Login no LinkedIn

```python
import requests

url = "http://localhost:8000/linkedin/login"
data = {
    "email": "seu-email@exemplo.com",
    "password": "sua-senha"
}

response = requests.post(url, json=data)
print(response.json())
```

## ⚠️ Avisos Importantes

- **Segurança**: Nunca compartilhe suas credenciais ou armazene-as em texto simples
- **Termos de Serviço**: Certifique-se de que seu uso está em conformidade com os Termos de Serviço do LinkedIn
- **Rate Limiting**: Evite fazer muitas requisições em curto período para evitar bloqueios

## 🔒 Considerações de Segurança

- A API deve ser executada em ambiente seguro e protegido
- Considere implementar HTTPS para proteger as credenciais durante a transmissão
- Não armazene credenciais em texto simples

## 📚 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **Selenium**: Para automação do navegador
- **Docker**: Para containerização e fácil implantação
- **Python 3.10**: Linguagem de programação base
