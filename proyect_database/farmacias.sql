-- =======================
-- SCRIPT COMPLETO: VADEMÉCUM MULTIFARMACIA
-- =======================

-- 1. LABORATORIOS
CREATE TABLE laboratorios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais_origen VARCHAR(50),
    contacto VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- 2. MEDICAMENTOS
CREATE TABLE medicamentos (
    id SERIAL PRIMARY KEY,
    nombre_comercial VARCHAR(100) NOT NULL,
    principio_activo VARCHAR(100),
    descripcion TEXT,
    laboratorio_id INT REFERENCES laboratorios(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- 3. PRESENTACIONES
CREATE TABLE presentaciones (
    id SERIAL PRIMARY KEY,
    medicamento_id INT REFERENCES medicamentos(id),
    forma_farmaceutica VARCHAR(50),
    concentracion VARCHAR(50),
    contenido VARCHAR(100),
    unidad_venta VARCHAR(20),
    precio_referencial DECIMAL(10, 2),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- 4. CONTRAINDICACIONES
CREATE TABLE contraindicaciones (
    id SERIAL PRIMARY KEY,
    medicamento_id INT REFERENCES medicamentos(id),
    descripcion TEXT,
    tipo VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- 5. CATEGORÍAS
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE medicamento_categoria (
    id SERIAL PRIMARY KEY,
    medicamento_id INT REFERENCES medicamentos(id),
    categoria_id INT REFERENCES categorias(id)
);

-- 6. EMPRESAS (FARMACIAS)
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    tipo VARCHAR(50), -- farmacia, librería, etc.
    direccion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- 7. FARMACIA - MEDICAMENTO
CREATE TABLE farmacia_medicamento (
    id SERIAL PRIMARY KEY,
    farmacia_id INT REFERENCES empresas(id),
    presentacion_id INT REFERENCES presentaciones(id),
    precio DECIMAL(10, 2),
    stock INT,
    visible BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- =======================
-- DATOS DE PRUEBA
-- =======================

-- Laboratorios
INSERT INTO laboratorios (nombre, pais_origen, contacto) VALUES
('Lab Chile', 'Chile', 'contacto@labchile.cl'),
('Bayer', 'Alemania', 'info@bayer.com');

-- Medicamentos
INSERT INTO medicamentos (nombre_comercial, principio_activo, descripcion, laboratorio_id) VALUES
('Paracetamol Forte', 'Paracetamol', 'Analgésico y antipirético', 1),
('Aspirina', 'Ácido Acetilsalicílico', 'Analgésico, antipirético y antiinflamatorio', 2);

-- Presentaciones
INSERT INTO presentaciones (medicamento_id, forma_farmaceutica, concentracion, contenido, unidad_venta, precio_referencial) VALUES
(1, 'Comprimido', '500 mg', 'Caja x 10', 'Caja', 1800),
(2, 'Comprimido', '100 mg', 'Caja x 20', 'Caja', 2500);

-- Contraindicaciones
INSERT INTO contraindicaciones (medicamento_id, descripcion, tipo) VALUES
(1, 'No usar en caso de insuficiencia hepática severa.', 'Hepática'),
(2, 'No usar en caso de úlcera gástrica activa.', 'Gástrica');

-- Categorías
INSERT INTO categorias (nombre, descripcion) VALUES
('Analgésico', 'Medicamentos para el dolor'),
('Antiinflamatorio', 'Reduce inflamaciones');

-- Relación Medicamento-Categoría
INSERT INTO medicamento_categoria (medicamento_id, categoria_id) VALUES
(1, 1),
(2, 1),
(2, 2);

-- Farmacias
INSERT INTO empresas (nombre, tipo, direccion) VALUES
('Farmacia Central', 'farmacia', 'Av. Providencia 123'),
('Farmacia del Pueblo', 'farmacia', 'Av. Matta 456');

-- Farmacia-Medicamento
INSERT INTO farmacia_medicamento (farmacia_id, presentacion_id, precio, stock) VALUES
(1, 1, 1900, 100),
(2, 2, 2600, 50);
