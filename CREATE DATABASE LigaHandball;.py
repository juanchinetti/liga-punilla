CREATE DATABASE LigaHandball;
USE LigaHandball;


CREATE TABLE Localidades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE Clubes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    logo BLOB,  -- Se utiliza BLOB para almacenar imágenes del logo
    localidad_id INT,
    tipo ENUM('Masculino', 'Femenino', 'Mixto') NOT NULL,
    FOREIGN KEY (localidad_id) REFERENCES Localidades(id)
);


CREATE TABLE Jugadores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE,
    correo_electronico VARCHAR(100),
    fecha_nacimiento DATE,
    sexo ENUM('Masculino', 'Femenino') NOT NULL,
    localidad_id INT NOT NULL,
    club_id INT,
    ficha_medica BLOB,  -- Se utiliza BLOB para almacenar la ficha médica
    carnet VARCHAR(100),  -- Almacena el número del carnet
    FOREIGN KEY (localidad_id) REFERENCES Localidades(id),
    FOREIGN KEY (club_id) REFERENCES Clubes(id)
);

-- Insertar Localidades (Ejemplo para la región de Punilla, Córdoba)
INSERT INTO Localidades (nombre) VALUES 
('Carlos Paz'), 
('Mina Clavero'), 
('La Falda'), 
('Villa Giardino'), 
('Tanti'), 
('Cosquín'),
('Embalse'), 
('Los Cocos'), 
('Villa del Dique'),
('San Antonio de Arredondo'),
('Villa Carlos Paz');