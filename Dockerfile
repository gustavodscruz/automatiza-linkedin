FROM python:3.10.12

# Instala dependências
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium

# Instala libs Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Código da app
COPY . /app
WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
