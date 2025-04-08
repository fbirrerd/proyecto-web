

CREATE ROLE postgres WITH LOGIN PASSWORD 'PasswordPostgres';
ALTER ROLE postgres CREATEDB;



-- -----------------------------------------------
-- 1. Crear Tablas GIS
-- -----------------------------------------------

-- Tabla de regiones
-- Activar extensión
CREATE EXTENSION IF NOT EXISTS postgis;

-- Crear tabla
CREATE TABLE regiones (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(5) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    geom GEOMETRY(MULTIPOLYGON, 4326),
    area_km2 DOUBLE PRECISION,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- Tabla de provincias
CREATE TABLE provincias (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(5) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    region_id INTEGER REFERENCES regiones(id),
    geom GEOMETRY(MULTIPOLYGON, 4326),
    area_km2 DOUBLE PRECISION,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- Tabla de comunas
CREATE TABLE comunas (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    provincia_id INTEGER REFERENCES provincias(id),
    region_id INTEGER REFERENCES regiones(id),
    geom GEOMETRY(MULTIPOLYGON, 4326),
    area_km2 DOUBLE PRECISION,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE direcciones (
    id SERIAL PRIMARY KEY,
    calle VARCHAR(150) NOT NULL,
    numero VARCHAR(20),
    complemento VARCHAR(100), -- depto, block, oficina, etc.
    comuna_id INTEGER REFERENCES comunas(id),
    provincia_id INTEGER REFERENCES provincias(id),
    region_id INTEGER REFERENCES regiones(id),
    codigo_postal VARCHAR(10),
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- -----------------------------------------------
-- 1. Crear Tabla de Empresas
-- -----------------------------------------------
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_empresa VARCHAR(50) NOT NULL,
    direccion_id INTEGER REFERENCES direcciones(id), -- Nullable por defecto
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- -----------------------------------------------
-- 2. Crear Tabla de Usuarios
-- -----------------------------------------------CREATE TABLE usuarios (
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL, -- Recomendado: almacenar hash
    direccion_id INTEGER REFERENCES direcciones(id), -- Nullable por defecto
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado SMALLINT NOT NULL DEFAULT 0, -- 0: Habilitado, 1: Deshabilitado
    duracion INT DEFAULT 20 -- Minutos de sesión u otro uso
);

-- -----------------------------------------------
-- 3. Crear Tabla de Roles
-- -----------------------------------------------
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- -----------------------------------------------
-- 4. Crear Tabla Relacionada entre Usuarios, Empresas y Roles
-- -----------------------------------------------
CREATE TABLE usuario_empresa_rol (
    id SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id),
    id_empresa INT REFERENCES empresas(id),
    id_rol INT REFERENCES roles(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    UNIQUE (id_usuario, id_empresa, id_rol)
);

-- -----------------------------------------------
-- 5. Crear Tabla de Menús Generales
-- -----------------------------------------------
CREATE TABLE menus_generales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    icono VARCHAR(50),
    ruta VARCHAR(255),
    id_padre INT REFERENCES menus_generales(id) ON DELETE SET NULL,
    es_publico BOOLEAN DEFAULT FALSE,  -- Indica si el menú es público
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- -----------------------------------------------
-- 6. Crear Tabla de Relación entre Menús Generales y Roles
-- -----------------------------------------------
CREATE TABLE menu_general_rol (
    id_menu INT REFERENCES menus_generales(id),
    id_rol INT REFERENCES roles(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_menu, id_rol)
);

-- -----------------------------------------------
-- 7. Crear Tabla de Menús Específicos
-- -----------------------------------------------
CREATE TABLE menus_especificos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    icono VARCHAR(50),
    ruta VARCHAR(255),
    id_padre INT REFERENCES menus_especificos(id) ON DELETE SET NULL,
    es_publico BOOLEAN DEFAULT FALSE,  -- Indica si el menú específico es público
    tipo_ventana VARCHAR(50),  -- 'popup', 'iframe', 'pagina'
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- -----------------------------------------------
-- 8. Crear Tabla de Relación entre Menús Específicos y Tipos de Empresa
-- -----------------------------------------------
CREATE TABLE menu_especifico_tipo_empresa (
    id_menu INT REFERENCES menus_especificos(id),
    tipo_empresa VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_menu, tipo_empresa)
);

-- -----------------------------------------------
-- 9. Crear Tabla de Menús Públicos
-- -----------------------------------------------
CREATE TABLE menus_publicos (
    id SERIAL PRIMARY KEY,
    id_menu INT REFERENCES menus_generales(id),  -- Relacionado con un menú general
    url_publica VARCHAR(255) NOT NULL,           -- URL pública que se puede acceder sin autenticación
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);


-- Tabla: configuracion_empresa
CREATE TABLE configuracion_empresa (
    id SERIAL PRIMARY KEY,
    empresa_id INT NULL,
    clave VARCHAR(255) NOT NULL,
    valor TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (empresa_id, clave),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

-- Tabla: auditoria
CREATE TABLE auditoria (
    id BIGSERIAL PRIMARY KEY,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT NULL,
    empresa_id INT NULL,
    tabla_afectada VARCHAR(255) NOT NULL,
    accion VARCHAR(255) NOT NULL,
    registro_id INT NULL,
    datos_antes TEXT NULL,
    datos_despues TEXT NULL,
    direccion_ip VARCHAR(45) NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

-- Tabla: parametro_sistema
CREATE TABLE parametro_sistema (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL UNIQUE,
    valor TEXT,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado SMALLINT NOT NULL DEFAULT 0
);

-- Tabla: acceso
CREATE TABLE acceso (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    empresa_id INT NULL,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento TIMESTAMP NOT NULL,
    token VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

-- Asegurar que el token sea único, si es necesario
CREATE UNIQUE INDEX idx_token ON acceso(token);


-- Insertar un usuario
INSERT INTO usuarios (username, nombres, apellidos, email, "password")
VALUES
('admin', 'Francisco', 'Birrer Donoso', 'fbirrer@gmail.com', 'cambiar'),
('mfernandez', 'María', 'Fernández Soto', 'mfernandez@example.com', 'cambiar'),
('clagos', 'Carlos', 'Lagos Torres', 'clagos@example.com', 'cambiar'),
('anamunoz', 'Ana', 'Muñoz Díaz', 'anamunoz@example.com', 'cambiar'),
('pedrosilva', 'Pedro', 'Silva Reyes', 'pedrosilva@example.com', 'cambiar');

-- Insertar Empresas
INSERT INTO empresas (nombre, tipo_empresa, estado) VALUES
('Farmacia ABC', 'Farmacia', TRUE),
('Librería XYZ', 'Librería', TRUE),
('Negocios Internacionales', 'Negocios', TRUE),
('Inventarios Global', 'Inventario', TRUE);

-- Insertar Roles
INSERT INTO roles (nombre, estado) VALUES
('Administrador', TRUE),
('Usuario', TRUE),
('Auditor', TRUE),
('Informe', TRUE);

-- INSERT INTO menu
-- (id, empresa_id, nombre, tipo, url, icono, orden, padre_id)
-- VALUES
-- ('Dashboard', 'url', 'dashboard_content.html', 'home', 1, NULL),
-- ('Gestión', 'padre', '#', 'folder', 2, NULL),
-- ('Informes', 'padre', '#', 'chart-line', 3, NULL),
-- ('Farmacia', 'padre', '#', 'chart-line', 4, NULL),
-- ('Links de Interés', 'padre', '#', 'link', 5, NULL)
-- ('Ayuda', 'padre', '#', 'help', 6, NULL),
-- ('Tablas', 'padre', '#', 'fas fa-chart-line', 1, 2),
-- ('Usuarios', 'url', 'usuarios.html', 'users', 1, 7),
-- ('Empresas', 'url', 'empresas.html', 'building', 2, 7),
-- ('Menú', 'url', 'menu.html', 'bars', 3, 7),
-- ('Accesos', 'url', 'accesos.html', 'lock', 1, 8),
-- ('Consulta de remedios', 'padre', '#', 'chart-line', 1, 4),
-- ('Consulta de precios', 'padre', '#', 'chart-line', 2, 4),
-- ('Vademecum', 'padre', '#', 'chart-line', 3, 4),
-- ('Emol', 'url', 'http://www.emol.com', 'users', 1, 5),
-- ('Lun', 'url', 'http://www.lun.cl', 'building', 2, 5),
-- ('La Tercera', 'url', 'http://www.latercera.cl', 'building', 3, 5);




INSERT INTO usuario_empresa_rol (id_usuario, id_empresa, id_rol, estado) VALUES
(1, 1, 1, TRUE),  -- Juan Pérez es Administrador de la Farmacia ABC
(2, 2, 2, TRUE),  -- Ana Gómez es Usuario en la Librería XYZ
(3, 3, 3, TRUE);  -- Carlos Díaz es Auditor en Negocios Internacionales

-- Insertar Menús Generales
INSERT INTO menus_generales (nombre, icono, ruta, es_publico, estado) VALUES
('Dashboard', 'icon-dashboard', '/dashboard', FALSE, TRUE),
('Informes', 'icon-reports', '/informes', FALSE, TRUE),
('Ayuda', 'icon-help', '/ayuda', TRUE, TRUE);  -- Menú Público

-- Insertar Menú General-Rol
INSERT INTO menu_general_rol (id_menu, id_rol, estado) VALUES
(1, 1, TRUE),  -- Dashboard solo visible para Administrador
(2, 3, TRUE),  -- Informes solo visible para Auditor
(3, 1, TRUE);  -- Ayuda visible para todos los roles (público)

-- Insertar Menús Específicos
INSERT INTO menus_especificos (nombre, icono, ruta, es_publico, tipo_ventana, estado) VALUES
('Inventario Farmacia', 'icon-inventory', '/inventario/farmacia', FALSE, 'iframe', TRUE),
('Inventario Librería', 'icon-inventory', '/inventario/libreria', FALSE, 'popup', TRUE),
('Formulario Pedido', 'icon-order', '/pedido/formulario', TRUE, 'pagina', TRUE);  -- Menú Público

-- Insertar Menú Específico-Tipo Empresa
INSERT INTO menu_especifico_tipo_empresa (id_menu, tipo_empresa, estado) VALUES
(1, 'Farmacia', TRUE),  -- Inventario Farmacia solo visible para empresas del tipo Farmacia
(2, 'Librería', TRUE),  -- Inventario Librería solo visible para empresas del tipo Librería
(3, 'Negocios', TRUE);  -- Formulario Pedido visible para todas las empresas

-- Insertar Menús Públicos
INSERT INTO menus_publicos (id_menu, url_publica, estado) VALUES
(3, '/pedido/formulario', TRUE);  -- URL pública de "Formulario Pedido"
