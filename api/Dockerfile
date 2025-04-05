# Imagen base de Python
FROM python:3.10-slim

# Setear el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt /app/

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente al contenedor
COPY . /app/

# Exponer el puerto 8000 donde FastAPI corre por defecto
EXPOSE 8200

# Comando para correr la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8200", "--reload"]


