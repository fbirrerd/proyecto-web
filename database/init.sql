
-- =========================
-- CREACIÓN DE USUARIO Y ROL
-- =========================
CREATE USER superuser WITH PASSWORD 'claveapp';
ALTER USER superuser WITH SUPERUSER;
CREATE ROLE postgres WITH LOGIN PASSWORD 'PasswordPostgres';
ALTER ROLE postgres CREATEDB;

-- =========================
-- TABLAS GEOGRÁFICAS
-- =========================
CREATE TABLE regiones (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(5) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    geom_wkt TEXT,  -- Ejemplo: 'MULTIPOLYGON(((...)))'
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
    id_region INTEGER REFERENCES regiones(id),
    geom_wkt TEXT,  -- Ejemplo: 'MULTIPOLYGON(((...)))'
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
    id_provincia INTEGER REFERENCES provincias(id),
    id_region INTEGER REFERENCES regiones(id),
    geom_wkt TEXT,  -- Ejemplo: 'MULTIPOLYGON(((...)))'
    area_km2 DOUBLE PRECISION,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- =========================
-- TABLA DE DIRECCIONES
-- =========================
CREATE TABLE direcciones (
    id SERIAL PRIMARY KEY,
    calle VARCHAR(150) NOT NULL,
    numero VARCHAR(20),
    complemento VARCHAR(100), -- depto, block, oficina, etc.
    id_comuna INTEGER REFERENCES comunas(id),
    id_provincia INTEGER REFERENCES provincias(id),
    id_region INTEGER REFERENCES regiones(id),
    codigo_postal VARCHAR(10),
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- =========================
-- TABLAS DE EMPRESAS Y USUARIOS
-- =========================
CREATE TABLE tipos_empresa (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_tipo_empresa INT REFERENCES tipos_empresa(id) ON DELETE CASCADE,
    id_direccion INT REFERENCES direcciones(id) ON DELETE SET NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    id_direccion INT REFERENCES direcciones(id) ON DELETE SET NULL,
    duracion INT DEFAULT 20, -- Minutos de sesión u otro uso
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- ROLES Y MENÚS
-- =========================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tipos_menu (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tipos_menu (nombre) VALUES ('general'), ('especifico');

CREATE TABLE menus (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    icono VARCHAR(50),
	ruta VARCHAR(255),
    id_tipo_menu INT REFERENCES tipos_menu(id),
    id_padre INT REFERENCES menus(id) ON DELETE SET NULL,
    url VARCHAR(255),
    descripcion VARCHAR(255),
    token VARCHAR(255) UNIQUE,
	orden int,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_rol (
    id_menu INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    id_rol INT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_menu, id_rol)
);


-- Relación entre empresas y usuarios
CREATE TABLE empresa_usuario (
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_empresa, id_usuario)
);

    -- Relación entre empresa, usuario y rol
CREATE TABLE empresa_usuario_rol (
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    id_rol INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_empresa, id_usuario, id_rol)
);


-- =========================
-- ACCESO, AUDITORÍA Y TOKENS
-- =========================
-- Tabla: configuracion_empresa
CREATE TABLE configuracion_empresa (
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    clave VARCHAR(255) NOT NULL,
    valor TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_empresa, clave)
);

-- Tabla: auditoria
CREATE TABLE auditoria (
    id BIGSERIAL PRIMARY KEY,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuarios(id),
    id_empresa INTEGER REFERENCES empresas(id),
    tabla_afectada VARCHAR(255) NOT NULL,
    accion VARCHAR(255) NOT NULL,
    id_registro INTEGER,
    datos_antes TEXT,
    datos_despues TEXT,
    direccion_ip VARCHAR(45)
);

-- Tabla: acceso
CREATE TABLE acceso (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
    id_empresa INTEGER REFERENCES empresas(id),
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento TIMESTAMP NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- MENÚS ESPECÍFICOS Y RELACIONES
-- =========================
CREATE TABLE menus_publicos (
    id SERIAL PRIMARY KEY,
    id_menu INT REFERENCES menus(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE,
    fecha_expiracion TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE menu_tipo_empresa (
    id_menu INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    id_tipo_empresa INT NOT NULL REFERENCES tipos_empresa(id) ON DELETE CASCADE,
    PRIMARY KEY (id_menu, id_tipo_empresa)
);


-- =========================
-- PARÁMETROS DEL SISTEMA
-- =========================
-- Tabla: parametro_sistema
CREATE TABLE parametro_sistema (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(255) UNIQUE NOT NULL,
    valor TEXT,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE logs_acceso (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id),
    id_empresa INTEGER REFERENCES empresas(id),
    username VARCHAR NOT NULL,
    exito BOOLEAN NOT NULL,
    mensaje TEXT NOT NULL,
    ip VARCHAR,
    user_agent TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- ÍNDICES
-- =========================
CREATE INDEX idx_id_tipo_empresa ON empresas(id_tipo_empresa);
CREATE INDEX idx_menu_id_rol_menu ON menu_rol(id_menu);
CREATE INDEX idx_menu_id_rol_rol ON menu_rol(id_rol);
CREATE INDEX idx_acceso_id_usuario ON acceso(id_usuario);
CREATE INDEX idx_auditoria_id_usuario ON auditoria(id_usuario);
CREATE INDEX idx_menus_publicos_token ON menus_publicos(token);
CREATE INDEX idx_menu_tipo_empresa ON menu_tipo_empresa(id_tipo_empresa);
CREATE INDEX idx_menus_estado ON menus(estado);
CREATE INDEX idx_empresas_estado ON empresas(estado);

-- =========================
-- VISTAS
-- =========================
CREATE VIEW vista_menu_rol_empresa AS
SELECT m.id, m.nombre, m.id_tipo_menu, r.nombre AS rol, te.nombre AS tipo_empresa
FROM menus m
JOIN menu_rol mr ON m.id = mr.id_menu
JOIN roles r ON mr.id_rol = r.id
JOIN menu_tipo_empresa mte ON m.id = mte.id_menu
JOIN tipos_empresa te ON mte.id_tipo_empresa = te.id;


-- =========================
-- DATOS DE EJEMPLO (INSERTS)
-- =========================

-- Tipos de empresa
INSERT INTO tipos_empresa (nombre) 
VALUES ('Farmacia'), ('Librería'), ('Tecnologia'), ('Bodega');

-- Empresas
INSERT INTO empresas (nombre, id_tipo_empresa) VALUES 
('Test', 1),
('Farmacia', 1),
('Libreria', 2),
('Tecnologia', 3);

-- Usuarios
INSERT INTO usuarios (
    username,
    nombres,
    apellidos,
    email,
    "password",
    duracion
) VALUES (
    'admin',
    'Administrador',
    'Principal',
    'fbirrer@gmail.com',
    'cambiar',  -- ¡Reemplazar por una contraseña hasheada en producción!
    30
);

-- Roles
INSERT INTO roles (nombre) VALUES 
('Soporte'), ('Administrador'), ('Auditor'), ('Usuario');

-- Menús
INSERT INTO menus (nombre, icono, id_tipo_menu, id_padre, url, descripcion, token, orden)
VALUES 
('Dashboard', 'home', 1, NULL, '/dashboard', 'Vista principal', 'token_dashboard', 1),
('Gestión', 'folder', 1, NULL, '/gestion', 'Módulo de gestión', 'token_gestion', 2),
('Tablas', 'table', 1, 2, '/gestion/tablas', 'Tablas base del sistema', 'token_tablas', 1),
('Usuarios', 'user', 1, 3, '/gestion/tablas/usuarios', 'Gestión de usuarios', 'token_usuarios', 1),
('Menús', 'list', 1, 3, '/gestion/tablas/menus', 'Gestión de menús', 'token_menus', 2),
('Roles', 'shield', 1, 3, '/gestion/tablas/roles', 'Gestión de roles', 'token_roles', 3);
-- Relación menú-rol
INSERT INTO menu_rol (id_menu, id_rol) 
VALUES 
(1, 1),(2, 1),(3, 1),(4, 1),(5, 1),(6, 1);

-- Menús específicos para tipos de empresa
INSERT INTO menu_tipo_empresa (id_menu, id_tipo_empresa) VALUES (1, 1);

INSERT INTO empresa_usuario (id_empresa, id_usuario)
VALUES
(1, 1);

INSERT INTO empresa_usuario_rol
(id_empresa, id_usuario, id_rol)
VALUES(1, 1, 1);



INSERT INTO parametro_sistema
(clave, valor, descripcion)
VALUES('valida_session', 'true', 'Se valida el tiempo de conexion de los usuarios');

-- =========================
-- FIN DEL SCRIPT
-- =========================
