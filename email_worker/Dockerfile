# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY . .

# Establecer las variables de entorno necesarias para Redis
ENV REDIS_URL=redis://redis_db:6379

# Exponer el puerto (si es necesario para monitoreo o administración)
EXPOSE 8000

# Comando para ejecutar el worker de Celery
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
