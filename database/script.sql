-- -----------------------------------------------
-- 1. Crear Tabla de Empresas
-- -----------------------------------------------
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_empresa VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

-- -----------------------------------------------
-- 2. Crear Tabla de Usuarios
-- -----------------------------------------------
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Contraseña encriptada
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
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

-- -----------------------------------------------
-- 10. Insertar Datos de Ejemplo
-- -----------------------------------------------

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

-- Insertar Usuarios
INSERT INTO usuarios (nombre, email, password, estado) VALUES
('Juan Pérez', 'juan.perez@empresa.com', 'password_encriptada_123', TRUE),
('Ana Gómez', 'ana.gomez@empresa.com', 'password_encriptada_456', TRUE),
('Carlos Díaz', 'carlos.diaz@empresa.com', 'password_encriptada_789', TRUE);

-- Insertar Usuario-Empresa-Rol
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
