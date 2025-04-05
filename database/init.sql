CREATE DATABASE ${POSTGRES_DB};
use ${POSTGRES_DB};

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


-- Tabla: menu
CREATE TYPE tipo_menu AS ENUM ('formulario', 'url', 'iframe');

CREATE TABLE menu (
    id SERIAL PRIMARY KEY,
    empresa_id INT NULL,
    nombre VARCHAR(255) NOT NULL,
    tipo tipo_menu NOT NULL,
    valor VARCHAR(255) NOT NULL, -- Almacena la URL, nombre del formulario, etc.
    icono VARCHAR(255) NULL, 
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
    empresa_id INT NOT NULL,
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
INSERT INTO usuario (nombre_usuario, email, contrasena, estado)
VALUES ('admin', 'fbirrer@gmail.com', 'cambiar', 0);


-- Nivel 1: Mi cuenta, Gestión, Informes
-- Insertamos los elementos de nivel 1
INSERT INTO menu (empresa_id, nombre, tipo, valor, icono, orden, estado)
VALUES (NULL, 'Mi Cuenta', 'url', '#', 'fas fa-user', 1, 0);

INSERT INTO menu (empresa_id, nombre, tipo, valor, icono, orden, estado)
VALUES (NULL, 'Gestión', 'url', '#', 'fas fa-cogs', 2, 0);

INSERT INTO menu (empresa_id, nombre, tipo, valor, icono, orden, estado)
VALUES (NULL, 'Informes', 'url', '#', 'fas fa-chart-line', 3, 0);

-- Nivel 2: Bajo 'Gestión'
-- Insertamos los elementos de nivel 2 bajo 'Gestión'
INSERT INTO menu (empresa_id, nombre, tipo, valor, icono, orden, padre_id, estado)
VALUES (NULL, 'Usuarios', 'url', '#', 'fas fa-users', 1, 2, 0);  -- 'padre_id' es 2, que corresponde a 'Gestión'

INSERT INTO menu (empresa_id, nombre, tipo, valor, icono, orden, padre_id, estado)
VALUES (NULL, 'Empresas', 'url', '#', 'fas fa-building', 2, 2, 0);

INSERT INTO menu (empresa_id, nombre, tipo, valor, icono, orden, padre_id, estado)
VALUES (NULL, 'Accesos', 'url', '#', 'fas fa-lock', 3, 2, 0);

INSERT INTO menu (empresa_id, nombre, tipo, valor, icono, orden, padre_id, estado)
VALUES (NULL, 'Menú', 'url', '#', 'fas fa-bars', 4, 2, 0);
