FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expone el puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "main.py"]
