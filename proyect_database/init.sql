
-- =========================
-- CREACIÓN DE USUARIO Y ROL
-- =========================
CREATE USER superuser WITH PASSWORD 'correoapp';
ALTER USER superuser WITH SUPERUSER;


CREATE DATABASE "CORREO_DB" OWNER superuser;

-- =========================
-- CONECTARSE A CORREO_DB
-- =========================
\connect "CORREO_DB"

-- Crear tablas en CORREO_DB
CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    de VARCHAR(255) NOT NULL,
    para VARCHAR(255) NOT NULL,
    concopia VARCHAR(255),
    concopiaoculta VARCHAR(255),
    asunto VARCHAR(255),
    parametros TEXT NOT NULL,
    cuerpoHtml TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS templates (
    id SERIAL PRIMARY KEY,
    code VARCHAR(255) NOT NULL,
    template_html TEXT NOT NULL,
    parameters TEXT[] NOT NULL
);
-- =========================
-- CREACIÓN DE USUARIO Y ROL
-- =========================


    INSERT INTO templates
    (code, template_html, parameters)
    VALUES('iglesia-bienvenida-1', '<!DOCTYPE html>
    <html>
    <head>
        <title>¡Feliz Cumpleaños!</title>
    </head>
    <body>
        <h1>¡Feliz cumpleaños, !#cumpleañero#!!</h1>
        <p>!#saludo#!</p>
        <br>
        <p>Con cariño,</p>
        <p>!#firma#!</p>
    </body>
    </html>
    ', '{}');



\connect "API_DB"


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


CREATE TABLE menus (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    icono VARCHAR(50),
    id_tipo_menu INT REFERENCES tipos_menu(id),
    id_padre INT REFERENCES menus(id) ON DELETE SET NULL,
    "url" VARCHAR(255),
    descripcion VARCHAR(255),
    "token" VARCHAR(255) UNIQUE,
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

-- Tabla principal de módulos
CREATE TABLE modulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relación N a N entre empresas y módulos
CREATE TABLE empresa_modulo (
    id_empresa INT NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    id_modulo INT NOT NULL REFERENCES modulos(id) ON DELETE CASCADE,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_empresa, id_modulo)
);

-- Relación N a N entre módulos y menús
CREATE TABLE modulo_menu (
    id_modulo INT NOT NULL REFERENCES modulos(id) ON DELETE CASCADE,
    id_menu INT NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    
    PRIMARY KEY (id_modulo, id_menu)
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
VALUES ('Farmacia'), ('Librería'), ('Tecnologia'), ('Bodega'), ('Venta'), ('Iglesia');

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



INSERT INTO tipos_menu (nombre) VALUES ('General'), ('Modulos');
-- Menús
INSERT INTO menus
(nombre, icono, id_tipo_menu, id_padre, url, descripcion, "token", orden, estado)
VALUES
('Dashboard', 'fa-solid fa-power-off fa-fw', 1, NULL, '/dashboard', 'Vista principal', 'token_dashboard', 1, true),
('Gestión', 'fa-solid fa-compass fa-fw', 1, NULL, '/gestion', 'Módulo de gestión', 'token_gestion', 2, true),
('Tablas', 'fa-solid fa-table fa-fw', 1, 2, '/gestion/tablas', 'Tablas base del sistema', 'token_tablas', 1, true),
('Permisos', 'fa-solid fa-key fa-fw', 1, 2, NULL, 'Gestionador de relaciones', NULL, 3, true),
('Usuarios', 'fa-solid fa-users fa-fw', 1, 3, '/gestion/usuarios', 'Gestión de usuarios', 'token_usuarios', 2, true),
('Menús', 'fa-solid fa-sitemap fa-fw', 1, 3, '/gestion/menu', 'Gestión de menús', 'token_menus', 3, true),
('Roles', 'fa-solid fa-users-line fa-fw', 1, 3, '/gestion/rol', 'Gestión de roles', 'token_roles', 4, true),
('Empresas', 'fa-solid fa-hotel fa-fw', 1, 3, '/gestion/empresas', 'Mantener las empresas del sistem', NULL, 1, true),
('Rol Menu', 'fa-solid fa-diagram-project fa-fw', 1, 4, '/gestion/rolMenu', NULL, NULL, NULL, true),
('Empresa Usuario', 'fa-solid fa-building-user fa-fw', NULL, 4, '/gestion/empresaUsuario', NULL, NULL, NULL, true),
('Tipo de Datos', 'fa-solid fa-check-to-slot fa-fw', 1, 2, '/gestion/tipoEmpresa', 'Gestión de Tipo de Empresas', NULL, 2, true),
('Tipo de Empresas', 'fa-solid fa-landmark-flag fa-fw', 1, 11, '/gestion/tipoEmpresa', NULL, NULL, 1, true),
('Tipo de Menu', 'fa-solid fa-user-tag fa-fw', 1, 11, '/gestion/tipoMenu', NULL, NULL, 2, true);

INSERT INTO menus
(nombre, icono, id_tipo_menu, id_padre, url, descripcion, "token", orden, estado)
VALUES
('Laboratorios', 'fa-solid fa-check-to-slot fa-fw', 2, null, '/vademecum/laboratorios', 'Gestión de Tipo de Empresas', NULL, 1, true),
('Farmacias', 'fa-solid fa-landmark-flag fa-fw', 2, null, '/vademecum/farmacias', NULL, NULL, 1, true),
('Remedios', 'fa-solid fa-user-tag fa-fw', 2, null, '/vademecum/remdios', NULL, NULL, 3, true),
('Vademecum', 'fa-solid fa-user-tag fa-fw', 2, null, '/vademecum/remdios', NULL, NULL, 4, true);





-- Relación menú-rol
INSERT INTO menu_rol (id_menu, id_rol) 
VALUES 
(1, 1),(2, 1),(3, 1),(4, 1),(5, 1),(6, 1),(7, 1),(8, 1),(9, 1);

-- Menús específicos para tipos de empresa
INSERT INTO menu_tipo_empresa (id_menu, id_tipo_empresa) VALUES (1, 1);

INSERT INTO empresa_usuario (id_empresa, id_usuario)
VALUES
(1, 1);

INSERT INTO empresa_usuario_rol
(id_empresa, id_usuario, id_rol)
VALUES(1, 1, 1);

INSERT INTO modulos (nombre, descripcion)
VALUES 
('Ventas', 'Módulo para administrar procesos de ventas de productos y servicios'),
('Vademecum', 'Módulo para generar y visualizar mantenedor de farmacias/remedios'), 
('Agenda', 'Módulo para generar y visualizar manejo de contactos');

INSERT INTO parametro_sistema
(clave, valor, descripcion)
VALUES('valida_session', 'true', 'Se valida el tiempo de conexion de los usuarios');

-- =========================
-- FIN DEL SCRIPT
-- =========================
