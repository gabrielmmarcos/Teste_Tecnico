# Usa uma imagem oficial do Python
FROM python:3.13-slim

# Impede o Poetry de criar um ambiente virtual isolado dentro do container,
# já que o próprio container já é um ambiente isolado.
ENV POETRY_VIRTUALENVS_CREATE=false

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o código do projeto para o container
COPY . .

# Instala o Poetry
RUN pip install poetry

# Instala as dependências do projeto
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev
RUN chmod +x /app/entrypoint.sh
# Inicia o Container
EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 src.mundo_invest.app:app