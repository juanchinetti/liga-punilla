-- Borrar la base de datos actual si existe
DROP DATABASE IF EXISTS LigaHandball;

-- Crear la base de datos
CREATE DATABASE LigaHandball;
USE LigaHandball;

-- Crear la tabla de Localidades
CREATE TABLE Localidades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Crear la tabla de Géneros
CREATE TABLE Generos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(50) NOT NULL UNIQUE
);

-- Crear la tabla de Clubes con el atributo 'grupo' y 'logo' como LONGBLOB
CREATE TABLE Clubes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    genero_id INT NOT NULL,
    localidad_id INT NOT NULL,
    grupo CHAR(1) NOT NULL, -- Grupo A o B
    logo LONGBLOB, -- Imagen del logo en formato binario
    activo BOOLEAN DEFAULT TRUE, -- Indicador de si el club está activo o no
    FOREIGN KEY (genero_id) REFERENCES Generos(id),
    FOREIGN KEY (localidad_id) REFERENCES Localidades(id),
    UNIQUE (nombre, genero_id, localidad_id)
);

-- Crear la tabla de Jugadores
CREATE TABLE Jugadores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(10) NOT NULL UNIQUE,
    correo_electronico VARCHAR(100) UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    genero_id INT NOT NULL,
    localidad_id INT NOT NULL,
    club_id INT,
    ficha_medica_activa BOOLEAN NOT NULL DEFAULT 0,
    carnet VARCHAR(255),
    FOREIGN KEY (genero_id) REFERENCES Generos(id),
    FOREIGN KEY (localidad_id) REFERENCES Localidades(id),
    FOREIGN KEY (club_id) REFERENCES Clubes(id)
);

-- Crear la tabla de Usuarios
CREATE TABLE Usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Crear la tabla de Puestos para autoridades
CREATE TABLE Puestos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- Crear la tabla de Autoridades con relación a Puestos
CREATE TABLE Autoridades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    puesto_id INT NOT NULL,
    FOREIGN KEY (puesto_id) REFERENCES Puestos(id)
);

-- Crear la tabla de Encuentros
CREATE TABLE IF NOT EXISTS Encuentros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jornada INT NOT NULL,
    grupo CHAR(1) NOT NULL,
    club1 VARCHAR(100) NOT NULL,
    club2 VARCHAR(100) NOT NULL,
    resultado VARCHAR(10) NOT NULL -- Almacena el resultado del encuentro
);

-- Insertar datos en la tabla Localidades
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
('Córdoba Capital'),
('Villa Saldán');

-- Insertar datos en la tabla Generos
INSERT INTO Generos (descripcion) VALUES 
('Masculino'),
('Femenino');

-- Insertar datos en la tabla Puestos
INSERT INTO Puestos (nombre) VALUES 
('Presidenta'), 
('Tesorero'), 
('Secretaria'), 
('Vocal Titular'), 
('Revisor de Cuenta');

-- Insertar autoridades
INSERT INTO Autoridades (nombre, apellido, puesto_id) VALUES 
('Ana', 'Gómez', (SELECT id FROM Puestos WHERE nombre = 'Presidenta')),
('Carlos', 'Martínez', (SELECT id FROM Puestos WHERE nombre = 'Tesorero')),
('Laura', 'Pérez', (SELECT id FROM Puestos WHERE nombre = 'Secretaria')),
('Jorge', 'López', (SELECT id FROM Puestos WHERE nombre = 'Vocal Titular')),
('María', 'Rodríguez', (SELECT id FROM Puestos WHERE nombre = 'Revisor de Cuenta'));

-- Insertar datos en la tabla Clubes con el campo 'activo' como TRUE
INSERT INTO Clubes (nombre, genero_id, localidad_id, grupo, activo) VALUES
('Municipalidad Malagueño', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Malagueño'), 'B', TRUE),
('Club Sarmiento', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Villa Carlos Paz'), 'B', TRUE),
('Zona Sur', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Córdoba Capital'), 'B', TRUE),
('Universitario Cosquín', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Cosquín (cabecera)'), 'B', TRUE),
('Club Huerta Grande', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Huerta Grande'), 'B', TRUE),
('Club Capilla del Monte', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Capilla del Monte'), 'B', TRUE),
('Municipalidad Malagueño', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Malagueño'), 'A', TRUE),
('Club Sarmiento', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Villa Carlos Paz'), 'A', TRUE),
('Zona Sur', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Córdoba Capital'), 'A', TRUE),
('Universitario Cosquín', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Cosquín (cabecera)'), 'A', TRUE),
('Club Huerta Grande', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Huerta Grande'), 'A', TRUE),
('Club Capilla del Monte', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Capilla del Monte'), 'A', TRUE);

-- Insertar algunos jugadores de ejemplo
INSERT INTO Jugadores (nombre, apellido, dni, correo_electronico, fecha_nacimiento, genero_id, localidad_id, club_id) VALUES
('Juan', 'Pérez', '12345678', 'juan.perez@example.com', '1995-05-15', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Bialet Massé'), 1),
('Maria', 'González', '87654321', 'maria.gonzalez@example.com', '1998-08-22', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Villa Carlos Paz'), 2),
('Luis', 'Martínez', '11223344', 'luis.martinez@example.com', '2002-03-30', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Cosquín (cabecera)'), 3),
('Ana', 'Lopez', '44332211', 'ana.lopez@example.com', '1999-11-11', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Malagueño'), 4);

-- Insertar el usuario "Karina" con la contraseña "Punilla2018"
INSERT INTO Usuarios (username, password) VALUES ('Karina', 'Punilla2018');
