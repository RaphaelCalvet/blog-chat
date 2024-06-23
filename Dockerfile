# Imagem base
FROM python:3.10.12

# Setando variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Instalando as dependências
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copiando o projeto
COPY . /code/