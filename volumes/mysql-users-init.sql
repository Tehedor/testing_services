-- Crear base de datos para usuarios si no existe
CREATE DATABASE IF NOT EXISTS userdb;

-- Usar la base de datos de usuarios
USE userdb;

-- Crear tabla 'users'
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos iniciales (usuarios de ejemplo)
INSERT INTO users (username, password, email) VALUES
('admin', 'admin_password_hash', 'admin@example.com'),
('user1', 'user1_password_hash', 'user1@example.com');
