#!/bin/bash

# Aplicar ConfigMaps para MongoDB y MySQL
echo "Aplicando ConfigMaps..."
kubectl apply -f deploys/db-mongo/mongo-seeder.yaml
kubectl apply -f deploys/db-mysql/mysql-seeder.yaml

# Aplicar Persistent Volume Claims para MongoDB y MySQL
echo "Aplicando Persistent Volume Claims..."
kubectl apply -f deploys/db-mongo/mongo-persistent-volume-claims.yaml
kubectl apply -f deploys/db-mysql/mysql-persistent-volume-claims.yaml

# Aplicar Persistent Volumes para MongoDB y MySQL (si es necesario)
echo "Aplicando Persistent Volumes..."
kubectl apply -f deploys/db-mongo/mongo-persistent-volume.yaml
kubectl apply -f deploys/db-mysql/mysql-persistent-volume.yaml

# Aplicar despliegue de MongoDB
echo "Aplicando despliegue de MongoDB..."
kubectl apply -f deploys/db-mongo/mongo-deployment.yaml

# Crear secretos para MySQL
echo "Creando secretos para MySQL..."
bash deploys/db-mysql/create_secrets.sh

# Aplicar despliegue de MySQL
echo "Aplicando despliegue de MySQL..."
kubectl apply -f deploys/db-mysql/mysql-deployment.yaml

# Esperar a que los pods de MongoDB y MySQL estén en estado Running
# echo "Esperando a que los pods de MongoDB y MySQL estén en estado Running..."
# while [[ $(kubectl get pods -l app=mongo -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]] || \
#       [[ $(kubectl get pods -l app=mysql-finances -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]] || \
#       [[ $(kubectl get pods -l app=mysql-users -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do
#   echo "Esperando a que los pods de MongoDB y MySQL estén listos..."
#   sleep 5
# done

# Aplicar despliegue del backend
echo "Aplicando despliegue del backend..."
kubectl apply -f deploys/backend-deployment.yaml

# Aplicar despliegue del frontend
echo "Aplicando despliegue del frontend..."
kubectl apply -f deploys/frontend-deployment.yaml

echo "Despliegues aplicados correctamente."