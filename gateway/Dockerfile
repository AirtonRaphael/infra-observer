# Usa imagem oficial Python slim para reduzir tamanho
FROM python:3.11-slim

# Define diretório de trabalho no container
WORKDIR /app

# Copia arquivos de requirements (se tiver) para instalar dependências
COPY requirements.txt .

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte do gateway
COPY src/ .

# Expõe a porta do serviço (padrão 8000 para uvicorn)
EXPOSE 8081

# Comando de inicialização do FastAPI via uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]

