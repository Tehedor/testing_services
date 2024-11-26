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

docker run -d -p 5000:5000 --restart=always --name registry registry:2
docker tag $BACKEND_IMAGE localhost:5000/$BACKEND_IMAGE
docker tag $FRONTEND_IMAGE localhost:5000/$FRONTEND_IMAGE

docker push localhost:5000/$BACKEND_IMAGE
docker push localhost:5000/$FRONTEND_IMAGE


# Listar las imágenes creadas
echo "Imágenes creadas:"
# docker images