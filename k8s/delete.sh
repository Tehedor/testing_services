#!/bin/bash

# Eliminar despliegue del frontend
echo "Eliminando despliegue del frontend..."
kubectl delete -f deploys/frontend-deployment.yaml

# Eliminar despliegue del backend
echo "Eliminando despliegue del backend..."
kubectl delete -f deploys/backend-deployment.yaml

# Eliminar despliegue de MySQL
echo "Eliminando despliegue de MySQL..."
kubectl delete -f deploys/db/mysql-deployment.yaml

# Eliminar despliegue de MongoDB
echo "Eliminando despliegue de MongoDB..."
kubectl delete -f deploys/db/mongo-deployment.yaml

# Eliminar Persistent Volume Claims
echo "Eliminando Persistent Volume Claims..."
kubectl delete -f deploys/db/persistent-volume-claims.yaml

# Eliminar ConfigMaps
echo "Eliminando ConfigMaps..."
kubectl delete -f deploys/db/configmaps.yaml

echo "Despliegues eliminados correctamente."