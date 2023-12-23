# Usa una imagen base de Nginx
FROM nginx

# Instala Nano
RUN apt-get update && \
    apt-get install -y nano && \
    rm -rf /var/lib/apt/lists/*

# Copia la configuración principal de Nginx
COPY nginx/nginx.conf /etc/nginx/sites-available

# Copia la carpeta sites-enabled al contenedor
COPY nginx/sites-available /etc/nginx/sites-available


# Copia el archivo data_post.json al directorio /app dentro del contenedor
COPY data_post.json /app/data_post.json

# Exponer el puerto 80 para que pueda ser accesible desde fuera del contenedor
EXPOSE 80

# Comando para iniciar Nginx en primer plano al arrancar el contenedor
CMD ["nginx", "-g", "daemon off;"]
