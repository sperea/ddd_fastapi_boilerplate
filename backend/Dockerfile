FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Establece la variable de entorno PYTHONPATH para incluir el directorio raíz del proyecto
ENV PYTHONPATH=/app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expone el puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "main.py"]
