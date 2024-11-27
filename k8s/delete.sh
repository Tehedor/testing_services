#!/bin/bash

# Eliminar despliegue del frontend
echo "Eliminando despliegue del frontend..."
kubectl delete -f deploys/frontend-deployment.yaml

# Eliminar despliegue del backend
echo "Eliminando despliegue del backend..."
kubectl delete -f deploys/backend-deployment.yaml

# Eliminar despliegue de MySQL
echo "Eliminando despliegue de MySQL..."
kubectl delete -f deploys/db-mysql/mysql-deployment.yaml

# Eliminar despliegue de MongoDB
echo "Eliminando despliegue de MongoDB..."
kubectl delete -f deploys/db-mongo/mongo-deployment.yaml

# Eliminar Persistent Volumes para MongoDB y MySQL (si es necesario)
# echo "Eliminando Persistent Volumes..."
# kubectl delete -f deploys/db-mongo/mongo-persistent-volume.yaml
# kubectl delete -f deploys/db-mysql/mysql-persistent-volume.yaml

# Eliminar Persistent Volume Claims para MongoDB y MySQL
echo "Eliminando Persistent Volume Claims..."
kubectl delete -f deploys/db-mongo/mongo-persistent-volume-claims.yaml
kubectl delete -f deploys/db-mysql/mysql-persistent-volume-claims.yaml
### Eliminar referencias a los PVCs en los PVs manualmente, sino luego no se podria asociar un nuevo PVC a los PVs 
kubectl patch pv mongo-pv-volume -p '{"spec":{"claimRef": null}}'
kubectl patch pv mysql-finance-pv-volume -p '{"spec":{"claimRef": null}}'
kubectl patch pv mysql-users-pv-volume -p '{"spec":{"claimRef": null}}'


# Eliminar ConfigMaps para MongoDB y MySQL
echo "Eliminando ConfigMaps..."
kubectl delete -f deploys/db-mongo/mongo-seeder.yaml
kubectl delete -f deploys/db-mysql/mysql-seeder.yaml

# Eliminar secretos para MySQL
echo "Eliminando secretos para MySQL..."
kubectl delete secret mysql-secret

echo "Despliegues eliminados correctamente."