FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 fonts-liberation \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    chromium chromium-driver

# Cria diretório
WORKDIR /app

# Copia arquivos
COPY . /app

# Instala libs Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Permite execução do script
RUN chmod +x start.sh

# Executa o bot
CMD ["./start.sh"]
