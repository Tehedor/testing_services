-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS financedb;

-- Usar la base de datos creada
USE financedb;

-- Crear tabla 'finances'
CREATE TABLE IF NOT EXISTS finances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    revenue DECIMAL(10, 2) NOT NULL,
    expense DECIMAL(10, 2) NOT NULL
);

-- Insertar datos iniciales
INSERT INTO finances (date, revenue, expense) VALUES 
('2024-01-01', 5000.00, 3000.00),
('2024-02-01', 6000.00, 4000.00),
('2024-03-01', 7000.00, 4500.00),
('2024-04-01', 8000.00, 5000.00);
