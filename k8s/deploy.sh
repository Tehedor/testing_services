#!/bin/bash

# Aplicar ConfigMaps
echo "Aplicando ConfigMaps..."
kubectl apply -f deploys/configmaps.yaml

# Aplicar Persistent Volume Claims
echo "Aplicando Persistent Volume Claims..."
kubectl apply -f deploys/persistent-volume-claims.yaml

# Aplicar despliegue de MongoDB
echo "Aplicando despliegue de MongoDB..."
kubectl apply -f deploys/db/mongo-deployment.yaml

# Aplicar despliegue de MySQL
echo "Aplicando despliegue de MySQL..."
kubectl apply -f deploys/db/mysql-deployment.yaml

# Aplicar despliegue del backend
echo "Aplicando despliegue del backend..."
kubectl apply -f deploys/db/backend-deployment.yaml

# Aplicar despliegue del frontend
echo "Aplicando despliegue del frontend..."
kubectl apply -f deploys/db/frontend-deployment.yaml

echo "Despliegues aplicados correctamente."