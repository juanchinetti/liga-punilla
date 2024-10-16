-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS LigaHandball;
USE LigaHandball;

-- Tabla de Localidades
CREATE TABLE Localidades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de Géneros
CREATE TABLE Generos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de Clubes
CREATE TABLE Clubes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    logo VARCHAR(255),  -- Almacena la ruta del archivo del logo
    localidad_id INT,
    tipo ENUM('Masculino', 'Femenino', 'Mixto') NOT NULL,
    fecha_fundacion DATE,
    FOREIGN KEY (localidad_id) REFERENCES Localidades(id)
);

-- Tabla de Jugadores
CREATE TABLE Jugadores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(10) NOT NULL UNIQUE,  -- Limitar a 10 caracteres para evitar datos inconsistentes
    correo_electronico VARCHAR(100) UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    genero_id INT NOT NULL,
    localidad_id INT NOT NULL,
    club_id INT,
    ficha_medica_activa BOOLEAN NOT NULL DEFAULT 0,  -- Indicador de ficha médica activa
    carnet VARCHAR(255),  -- Almacena la ruta del archivo del carnet
    FOREIGN KEY (genero_id) REFERENCES Generos(id),
    FOREIGN KEY (localidad_id) REFERENCES Localidades(id),
    FOREIGN KEY (club_id) REFERENCES Clubes(id)
);

-- Insertar Localidades (Ejemplo para la región de Punilla, Córdoba)
-- Insertar Localidades
INSERT INTO Localidades (nombre) VALUES 
('Bialet Massé'), 
('Capilla del Monte'), 
('Cosquín (cabecera)'), 
('Huerta Grande'), 
('La Cumbre'), 
('La Falda'), 
('Los Cocos'), 
('San Antonio de Arredondo'), 
('San Esteban'), 
('Santa María'), 
('Tanti'), 
('Valle Hermoso'), 
('Villa Carlos Paz'), 
('Villa Giardino'), 
('Villa Icho Cruz'), 
('Villa Santa Cruz del Lago'), 
('Cabalango'), 
('Casa Grande'), 
('Charbonier'), 
('Cuesta Blanca'), 
('Estancia Vieja'), 
('Mayu Sumaj'), 
('San Roque'), 
('Tala Huasi'), 
('Villa Parque Siquiman'), 
('Malagueño'), 
('Córdoba Capital');

-- Insertar Géneros
INSERT INTO Generos (descripcion) VALUES 
('Masculino'),
('Femenino'),
('No binario');
