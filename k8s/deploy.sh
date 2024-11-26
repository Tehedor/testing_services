#!/bin/bash

# Aplicar ConfigMaps para MongoDB y MySQL
echo "Aplicando ConfigMaps..."
# kubectl apply -f db-mongo/mongo-seeder.yaml
kubectl apply -f db-mysql/mysql-seeder.yaml

# Aplicar Persistent Volume Claims para MongoDB y MySQL
echo "Aplicando Persistent Volume Claims..."
# kubectl apply -f db-mongo/mongo-persistent-volume-claims.yaml
kubectl apply -f db-mysql/mysql-persistent-volume-claims.yaml

# Aplicar Persistent Volumes para MySQL (si es necesario)
echo "Aplicando Persistent Volumes..."
kubectl apply -f db-mysql/mysql-persistent-volume.yaml

# Aplicar despliegue de MongoDB
echo "Aplicando despliegue de MongoDB..."
# kubectl apply -f db-mongo/mongo-deployment.yaml

# Crear secretos para MySQL
echo "Creando secretos para MySQL..."
bash db-mysql/create_secrets.sh

# Aplicar despliegue de MySQL
echo "Aplicando despliegue de MySQL..."
kubectl apply -f db-mysql/mysql-deployment.yaml

# Aplicar despliegue del backend
echo "Aplicando despliegue del backend..."
kubectl apply -f backend-deployment.yaml

# Aplicar despliegue del frontend
echo "Aplicando despliegue del frontend..."
kubectl apply -f frontend-deployment.yaml

echo "Despliegues aplicados correctamente."