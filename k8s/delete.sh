#!/bin/bash

# Eliminar despliegue del frontend
echo "Eliminando despliegue del frontend..."
kubectl delete -f frontend-deployment.yaml

# Eliminar despliegue del backend
echo "Eliminando despliegue del backend..."
kubectl delete -f backend-deployment.yaml

# Eliminar despliegue de MySQL
echo "Eliminando despliegue de MySQL..."
kubectl delete -f db-mysql/mysql-deployment.yaml

# Eliminar despliegue de MongoDB
echo "Eliminando despliegue de MongoDB..."
kubectl delete -f db-mongo/mongo-deployment.yaml

# Eliminar Persistent Volumes para MySQL (si es necesario)
echo "Eliminando Persistent Volumes..."
kubectl delete -f db-mysql/mysql-persistent-volume.yaml

# Eliminar Persistent Volume Claims para MongoDB y MySQL
echo "Eliminando Persistent Volume Claims..."
kubectl delete -f db-mongo/mongo-persistent-volume-claims.yaml
kubectl delete -f db-mysql/mysql-persistent-volume-claims.yaml

# Eliminar ConfigMaps para MongoDB y MySQL
echo "Eliminando ConfigMaps..."
kubectl delete -f db-mongo/mongo-seeder.yaml
kubectl delete -f db-mysql/mysql-seeder.yaml

echo "Despliegues eliminados correctamente."