# Image légère Python
FROM python:3.12-slim

# Empêche Python de générer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crée un répertoire pour l’application
WORKDIR /app

# Copie les fichiers dans l’image Docker
COPY . /app

# Installe les dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Port exposé
EXPOSE 8000

# Lancement de l’API
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
