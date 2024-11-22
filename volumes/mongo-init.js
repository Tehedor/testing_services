// Archivo para inicializar MongoDB con datos predefinidos.
db = db.getSiblingDB('financedb');

db.createCollection('finances');

db.finances.insertMany([
    { date: "2024-01-01", revenue: 5000, expense: 3000 },
    { date: "2024-02-01", revenue: 6000, expense: 4000 },
    { date: "2024-03-01", revenue: 7000, expense: 4500 },
    { date: "2024-04-01", revenue: 8000, expense: 5000 }
]);

print("Datos iniciales insertados en MongoDB");
