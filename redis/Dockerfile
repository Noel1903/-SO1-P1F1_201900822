# Usa una imagen base con Node.js
FROM node:14

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación
COPY ./redis .

# Instala las dependencias
RUN npm install

# Comando por defecto al ejecutar el contenedor
CMD ["node", "app.js"]
