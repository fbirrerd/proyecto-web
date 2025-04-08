

CREATE ROLE postgres WITH LOGIN PASSWORD 'PasswordPostgres';
ALTER ROLE postgres CREATEDB;

-- Tabla: empresa
CREATE TABLE empresa (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado SMALLINT NOT NULL DEFAULT 0 -- 0: Habilitado, 1: Deshabilitado
);

-- Tabla: rol
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado SMALLINT NOT NULL DEFAULT 0 -- 0: Habilitado, 1: Deshabilitado
);

-- Tabla: usuario
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL, -- Considera usar hashing para contraseñas
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado SMALLINT NOT NULL DEFAULT 0, -- 0: Habilitado, 1: Deshabilitado
    duracion INT DEFAULT 20 -- Duración con valor por defecto de 20
);


CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    empresa_id INT NULL,
    nombre VARCHAR(255) NOT NULL,
    tipo VARCHAR(10) NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    icono VARCHAR(50) NULL, 
    orden INT,
    padre_id INT NULL, -- Para la estructura multinivel
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado SMALLINT NOT NULL DEFAULT 0, -- 0: Habilitado, 1: Deshabilitado
    FOREIGN KEY (empresa_id) REFERENCES empresa(id),
    FOREIGN KEY (padre_id) REFERENCES menu(id) ON DELETE SET NULL
);

-- Tabla de relación: usuario_empresa
CREATE TABLE usuario_empresa (
    usuario_id INT NOT NULL,
    empresa_id INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (usuario_id, empresa_id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (empresa_id) REFERENCES empresa(id)
);

-- Tabla de relación: usuario_rol
CREATE TABLE usuario_rol (
    usuario_id INT NOT NULL,
    rol_id INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (usuario_id, rol_id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (rol_id) REFERENCES rol(id)
);

-- Tabla: modulo
CREATE TABLE modulo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado SMALLINT NOT NULL DEFAULT 0
);

-- Tabla de relación: rol_modulo
CREATE TABLE rol_modulo (
    rol_id INT NOT NULL,
    modulo_id INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rol_id, modulo_id),
    FOREIGN KEY (rol_id) REFERENCES rol(id),
    FOREIGN KEY (modulo_id) REFERENCES modulo(id)
);

-- Tabla: permiso
CREATE TABLE permiso (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado SMALLINT NOT NULL DEFAULT 0
);

-- Tabla de relación: rol_permiso_menu
CREATE TABLE rol_permiso_menu (
    rol_id INT NOT NULL,
    permiso_id INT NOT NULL,
    menu_id INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rol_id, permiso_id, menu_id),
    FOREIGN KEY (rol_id) REFERENCES rol(id),
    FOREIGN KEY (permiso_id) REFERENCES permiso(id),
    FOREIGN KEY (menu_id) REFERENCES menu(id)
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
    FOREIGN KEY (empresa_id) REFERENCES empresa(id)
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
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (empresa_id) REFERENCES empresa(id)
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
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (empresa_id) REFERENCES empresa(id)
);

-- Asegurar que el token sea único, si es necesario
CREATE UNIQUE INDEX idx_token ON acceso(token);


-- Insertar un usuario
INSERT INTO usuario (nombre_usuario, email, contrasena)
VALUES 
('admin', 'fbirrer@gmail.com', 'cambiar'),
('rbirrer', 'rbirrerd@gmail.com', 'cambiar'),
('fbirrer', 'panchobirrerd@gmail.com', 'cambiar');


INSERT INTO public.menu
(id, empresa_id, nombre, tipo, url, icono, orden, padre_id)
VALUES
('Dashboard', 'url', 'dashboard_content.html', 'home', 1, NULL),
('Gestión', 'padre', '#', 'folder', 2, NULL),
('Informes', 'padre', '#', 'chart-line', 3, NULL),
('Farmacia', 'padre', '#', 'chart-line', 4, NULL),
('Links de Interés', 'padre', '#', 'link', 5, NULL)
('Ayuda', 'padre', '#', 'help', 6, NULL),
('Tablas', 'padre', '#', 'fas fa-chart-line', 1, 2),
('Usuarios', 'url', 'usuarios.html', 'users', 1, 7),
('Empresas', 'url', 'empresas.html', 'building', 2, 7),
('Menú', 'url', 'menu.html', 'bars', 3, 7),
('Accesos', 'url', 'accesos.html', 'lock', 1, 8),
('Consulta de remedios', 'padre', '#', 'chart-line', 1, 4),
('Consulta de precios', 'padre', '#', 'chart-line', 2, 4),
('Vademecum', 'padre', '#', 'chart-line', 3, 4),
('Emol', 'url', 'http://www.emol.com', 'users', 1, 5),
('Lun', 'url', 'http://www.lun.cl', 'building', 2, 5),
('La Tercera', 'url', 'http://www.latercera.cl', 'building', 3, 5);


INSERT INTO empresa (nombre) 
VALUES 
('Bookstore'),
('Soprole'),
('Banco de Chile'),
('Farmacia de la calle');

INSERT INTO usuario_empresa (usuario_id, empresa_id, fecha_inicio)
VALUES 
(2, 1, CURRENT_DATE),
(3, 2, CURRENT_DATE),
(3, 3, CURRENT_DATE);

INSERT INTO rol (nombre, descripcion) VALUES 
('soberano', 'Rol con todos los privilegios del sistema'),
('administrador', 'Administrador del sistema con permisos avanzados'),
('informes', 'Acceso solo a generación y visualización de informes'),
('bookstore', 'Rol específico para usuarios de la empresa de Bookstore'),
('farmacia', 'Rol específico para usuarios de farmacia');

INSERT INTO usuario_rol (usuario_id, rol_id) VALUES
(2, 2),  -- Usuario 1 => Rol soberano
(2, 4),  -- Usuario 2 => Rol administrador
(1, 1);   -- Usuario 3 => Rol informes

