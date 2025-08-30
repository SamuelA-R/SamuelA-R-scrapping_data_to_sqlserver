# Imagem base (a partir de uma já existente no Docker Hub, por exemplo)
FROM python:3.12-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /mnt/c/projetos-paralelos-samuel/projeto-webscraping-sqlserver

# Copiar arquivos do projeto para dentro do container
COPY . .

# Instalar dependências (exemplo: requirements.txt para Python)
RUN pip install --no-cache-dir -r /mnt/c/projetos-paralelos-samuel/projeto-webscraping-sqlserver/requirements.txt

# Expor a porta que a aplicação vai rodar
EXPOSE 5000

# Comando padrão que será executado quando o container iniciar
CMD ["python", "main.py"]