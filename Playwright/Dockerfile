# Usa la imagen oficial de Python como base
FROM python:3.9-slim-buster

# Establece el directorio de trabajo
WORKDIR /-SO1-P1F1_201900822

# Copia el script Playwright al contenedor
COPY /Playwright/scraping_script.py /Playwright/scraping_script.py

# Instala Playwright y las dependencias necesarias
RUN pip install playwright
RUN playwright install
RUN apt-get update && \
    apt-get install -y libglib2.0-0 libnss3 libnspr4 libdbus-1-3 \
                       libatk1.0-0 libatk-bridge2.0-0 libcups2 \
                       libdrm2 libxcb1 libxkbcommon0 libatspi2.0-0 \
                       libx11-6 libxcomposite1 libxdamage1 libxext6 \
                       libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 \
                       libcairo2 libasound2

# Comando para ejecutar el script
CMD ["python3", "/Playwright/scraping_script.py"]
