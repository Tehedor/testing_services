#!/bin/bash

# Variables
BACKEND_IMAGE="finance-backend-image:latest"
FRONTEND_IMAGE="finance-frontend-image:latest"

# Construir la imagen del backend
echo "Construyendo la imagen del backend..."
docker build -t $BACKEND_IMAGE ../Backend

# Construir la imagen del frontend
echo "Construyendo la imagen del frontend..."
docker build -t $FRONTEND_IMAGE ../Frontend

# Listar las imágenes creadas
echo "Imágenes creadas:"
# docker images