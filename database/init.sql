-- =========================
-- TABLAS GEOGRÁFICAS
-- =========================
CREATE TABLE regiones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    abreviatura VARCHAR(10),
    capital VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE provincias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10),
    id_region INTEGER REFERENCES regiones(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE comunas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10),
    id_provincia INTEGER REFERENCES provincias(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE nacionalidad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    gentilicio_nac VARCHAR(100) NOT NULL,
    iso_nac CHAR(3) NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE estado_civil (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE profesion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE niveles_educacionales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

-- =========================
-- TABLA DE DIRECCIONES
-- =========================
CREATE TABLE direccion (
    id SERIAL PRIMARY KEY,
    calle VARCHAR(150) NOT NULL,
    numero VARCHAR(20),
    complemento VARCHAR(100),
    id_comuna INTEGER REFERENCES comunas(id) ON DELETE SET NULL,
    id_provincia INTEGER REFERENCES provincias(id) ON DELETE SET NULL,
    id_region INTEGER REFERENCES regiones(id) ON DELETE SET NULL,
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
    id_tipo_empresa INTEGER REFERENCES tipos_empresa(id) ON DELETE CASCADE,
    id_direccion INTEGER REFERENCES direccion(id) ON DELETE SET NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dashboard_inicial (
    id SERIAL PRIMARY KEY,
    pagina VARCHAR(100) NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE personas (
    id SERIAL PRIMARY KEY,
    run_rut VARCHAR(20) UNIQUE,
    pasaporte VARCHAR(20),
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    fecha_nacimiento DATE,
    sexo CHAR(1) CHECK (sexo IN ('M', 'F', 'O')),
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20),
    telefono_secundario VARCHAR(20),
    id_direccion INTEGER REFERENCES direccion(id) ON DELETE SET NULL,
    id_estado_civil INTEGER REFERENCES estado_civil(id) ON DELETE SET NULL,
    id_nacionalidad INTEGER REFERENCES nacionalidad(id) ON DELETE SET NULL,
    id_profesion INTEGER REFERENCES profesion(id) ON DELETE SET NULL,
    id_nivel_educacional INTEGER REFERENCES niveles_educacionales(id) ON DELETE SET NULL,
    estado BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    duracion INTEGER DEFAULT 20,
    pagina_inicio VARCHAR(255) NOT NULL,
    id_dashboard INTEGER REFERENCES dashboard_inicial(id) ON DELETE SET NULL,
    id_persona INTEGER REFERENCES personas(id) ON DELETE SET NULL,
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
    id_tipo_menu INTEGER REFERENCES tipos_menu(id) ON DELETE SET NULL,
    id_padre INTEGER REFERENCES menus(id) ON DELETE SET NULL,
    url VARCHAR(255),
    descripcion VARCHAR(255),
    token VARCHAR(255) UNIQUE,
    orden INTEGER,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_rol (
    id_menu INTEGER NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    id_rol INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_menu, id_rol)
);

CREATE TABLE empresa_usuario (
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_empresa, id_usuario)
);

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
CREATE TABLE configuracion_empresa (
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    clave VARCHAR(255) NOT NULL,
    valor TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_empresa, clave)
);

CREATE TABLE auditoria (
    id BIGSERIAL PRIMARY KEY,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    id_empresa INTEGER REFERENCES empresas(id) ON DELETE SET NULL,
    tabla_afectada VARCHAR(255) NOT NULL,
    accion VARCHAR(255) NOT NULL,
    id_registro INTEGER,
    datos_antes TEXT,
    datos_despues TEXT,
    direccion_ip VARCHAR(45)
);

CREATE TABLE acceso (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    id_empresa INTEGER REFERENCES empresas(id) ON DELETE SET NULL,
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
    id_menu INTEGER REFERENCES menus(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE,
    fecha_expiracion TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE menu_tipo_empresa (
    id_menu INTEGER NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    id_tipo_empresa INTEGER NOT NULL REFERENCES tipos_empresa(id) ON DELETE CASCADE,
    PRIMARY KEY (id_menu, id_tipo_empresa)
);

-- =========================
-- PARÁMETROS DEL SISTEMA
-- =========================
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
    id_usuario INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    id_empresa INTEGER REFERENCES empresas(id) ON DELETE SET NULL,
    username VARCHAR(255) NOT NULL,
    exito BOOLEAN NOT NULL,
    mensaje TEXT NOT NULL,
    ip VARCHAR(45),
    user_agent TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- TABLAS MODULOS
-- =========================
CREATE TABLE modulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE empresa_modulo (
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    id_modulo INTEGER NOT NULL REFERENCES modulos(id) ON DELETE CASCADE,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_empresa, id_modulo)
);

CREATE TABLE modulo_menu (
    id_modulo INTEGER NOT NULL REFERENCES modulos(id) ON DELETE CASCADE,
    id_menu INTEGER NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_modulo, id_menu)
);

-- =========================
-- TABLAS VADEMECUM
-- =========================
CREATE TABLE vademecum_laboratorios (
    id_laboratorio SERIAL PRIMARY KEY,
    nombre_laboratorio VARCHAR(100) NOT NULL,
    pais VARCHAR(50),
    direccion VARCHAR(255),
    sitio_web VARCHAR(100),
    contacto VARCHAR(100),
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_categorias_terapeuticas (
    id_categoria SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL,
    descripcion TEXT,
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_medicamentos (
    id_medicamento SERIAL PRIMARY KEY,
    nombre_comercial VARCHAR(100) NOT NULL,
    nombre_generico VARCHAR(100) NOT NULL,
    forma_farmaceutica VARCHAR(50),
    concentracion VARCHAR(50),
    id_laboratorio INTEGER NOT NULL REFERENCES vademecum_laboratorios(id_laboratorio) ON DELETE CASCADE,
    registro_sanitario VARCHAR(50),
    clasificacion VARCHAR(50),
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_indicaciones (
    id_indicacion SERIAL PRIMARY KEY,
    id_medicamento INTEGER NOT NULL REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE CASCADE,
    indicacion TEXT NOT NULL,
    mecanismo_accion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_posologias (
    id_posologia SERIAL PRIMARY KEY,
    id_medicamento INTEGER NOT NULL REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE CASCADE,
    dosis VARCHAR(100),
    via_administracion VARCHAR(50),
    edad_minima INTEGER,
    edad_maxima INTEGER,
    instrucciones_especiales TEXT,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_contraindicaciones (
    id_contraindicacion SERIAL PRIMARY KEY,
    id_medicamento INTEGER NOT NULL REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE CASCADE,
    contraindicacion TEXT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_interacciones (
    id_interaccion SERIAL PRIMARY KEY,
    id_medicamento INTEGER NOT NULL REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE CASCADE,
    id_medicamento_interactua INTEGER REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE SET NULL,
    descripcion_interaccion TEXT NOT NULL,
    tipo_interaccion VARCHAR(50),
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_efectos_secundarios (
    id_efecto SERIAL PRIMARY KEY,
    id_medicamento INTEGER NOT NULL REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE CASCADE,
    efecto_secundario TEXT NOT NULL,
    frecuencia VARCHAR(50),
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_presentaciones (
    id_presentacion SERIAL PRIMARY KEY,
    id_medicamento INTEGER NOT NULL REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE CASCADE,
    formato VARCHAR(100),
    concentracion VARCHAR(50),
    codigo_barras VARCHAR(50),
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_farmacocinetica (
    id_farmacocinetica SERIAL PRIMARY KEY,
    id_medicamento INTEGER NOT NULL REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE CASCADE,
    absorcion TEXT,
    distribucion TEXT,
    metabolismo TEXT,
    eliminacion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_protocolos_clinicos (
    id_protocolo SERIAL PRIMARY KEY,
    id_medicamento INTEGER REFERENCES vademecum_medicamentos(id_medicamento),
    protocolo_clinico TEXT NOT NULL,
    descripcion TEXT,
    fuente VARCHAR(100),
    fecha_actualizacion DATE,
    id_empresa INTEGER NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP
);

CREATE TABLE vademecum_medicamento_categoria (
    id_medicamento INTEGER REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE CASCADE,
    id_categoria INTEGER REFERENCES vademecum_categorias_terapeuticas(id_categoria) ON DELETE CASCADE,
    PRIMARY KEY (id_medicamento, id_categoria)
);

CREATE TABLE imagenes (
    id_imagen SERIAL PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255),
    id_medicamento INTEGER REFERENCES vademecum_medicamentos(id_medicamento) ON DELETE SET NULL,
    id_laboratorio INTEGER REFERENCES vademecum_laboratorios(id_laboratorio) ON DELETE SET NULL,
    id_persona INTEGER REFERENCES personas(id) ON DELETE SET NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_edicion TIMESTAMP,
    CONSTRAINT chk_imagen_ref CHECK (
        (
			id_medicamento IS NOT NULL 
			AND id_laboratorio IS NULL
			AND id_persona IS NULL) OR
        (
			id_medicamento IS NULL AND 
			id_laboratorio IS NOT NULL
			AND id_persona IS NULL) OR
        (
			id_medicamento IS NULL AND 
			id_laboratorio IS NULL
			AND id_persona IS NOT NULL)
    )
);

-- Crear tabla Medicamento-Protocolo (asumiendo que es una tabla de relación si no existe)
CREATE TABLE vademecum_medicamento_protocolo (
    id_medicamento INTEGER REFERENCES vademecum_medicamentos(id_medicamento),
    id_protocolo INTEGER REFERENCES vademecum_protocolos_clinicos(id_protocolo),
    PRIMARY KEY (id_medicamento, id_protocolo),
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating the propiedades table
CREATE TABLE propiedades (
    id SERIAL PRIMARY KEY,
    propiedad VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('texto', 'numero', 'opciones', 'select')),
    posibles_valores TEXT
);

-- Creating the propiedades_empresa table
CREATE TABLE propiedades_empresa (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER NOT NULL,
    propiedad_id INTEGER NOT NULL,
    valor TEXT NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE,
    FOREIGN KEY (propiedad_id) REFERENCES propiedades(id) ON DELETE CASCADE
);

-- =========================
-- CREACION DE INDICES
-- =========================

CREATE INDEX idx_id_tipo_empresa ON empresas(id_tipo_empresa);
CREATE INDEX idx_menu_rol_id_menu ON menu_rol(id_menu);
CREATE INDEX idx_menu_rol_id_rol ON menu_rol(id_rol);
CREATE INDEX idx_acceso_id_usuario ON acceso(id_usuario);
CREATE INDEX idx_auditoria_id_usuario ON auditoria(id_usuario);
CREATE INDEX idx_menus_publicos_token ON menus_publicos(token);
CREATE INDEX idx_menu_tipo_empresa ON menu_tipo_empresa(id_tipo_empresa);
CREATE INDEX idx_menus_estado ON menus(estado);
CREATE INDEX idx_empresas_estado ON empresas(estado);
CREATE INDEX IF NOT EXISTS idx_medicamentos_nombre_comercial 
    ON vademecum_medicamentos(nombre_comercial);
CREATE INDEX IF NOT EXISTS idx_medicamentos_nombre_generico 
    ON vademecum_medicamentos(nombre_generico);
CREATE INDEX IF NOT EXISTS idx_protocolos_medicamento 
    ON vademecum_protocolos_clinicos(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_medicamento_categoria_medicamento 
    ON vademecum_medicamento_categoria(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_medicamento_categoria_categoria 
    ON vademecum_medicamento_categoria(id_categoria);
CREATE INDEX IF NOT EXISTS idx_medicamento_protocolo_medicamento 
    ON vademecum_medicamento_protocolo(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_medicamento_protocolo_protocolo 
    ON vademecum_medicamento_protocolo(id_protocolo);
CREATE INDEX IF NOT EXISTS idx_contraindicaciones_medicamento 
    ON vademecum_contraindicaciones(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_interacciones_medicamento 
    ON vademecum_interacciones(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_interacciones_interactua 
    ON vademecum_interacciones(id_medicamento_interactua);
CREATE INDEX IF NOT EXISTS idx_presentaciones_medicamento 
    ON vademecum_presentaciones(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_efectos_medicamento 
    ON vademecum_efectos_secundarios(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_posologias_medicamento 
    ON vademecum_posologias(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_laboratorios_nombre 
    ON vademecum_laboratorios(nombre_laboratorio);




-- =========================
-- CREACION DE VISTAS
-- =========================

CREATE VIEW vista_menu_rol_empresa AS
SELECT 
    m.id, 
    m.nombre, 
    m.id_tipo_menu, 
    r.nombre AS rol, 
    te.nombre AS tipo_empresa
FROM menus m
JOIN menu_rol mr ON m.id = mr.id_menu
JOIN roles r ON mr.id_rol = r.id
JOIN menu_tipo_empresa mte ON m.id = mte.id_menu
JOIN tipos_empresa te ON mte.id_tipo_empresa = te.id
WHERE m.estado = TRUE AND mr.estado = TRUE AND r.estado = TRUE AND te.estado = TRUE;

CREATE VIEW vista_cumpleanios_mes AS
SELECT
    id,
    run_rut,
    pasaporte,
    nombres,
    apellidos,
    fecha_nacimiento,
    sexo,
    email,
    telefono,
    EXTRACT(DAY FROM fecha_nacimiento) AS dia_cumple,
    EXTRACT(MONTH FROM fecha_nacimiento) AS mes_cumple,
    EXTRACT(YEAR FROM AGE(fecha_nacimiento)) AS edad_actual
FROM personas
WHERE EXTRACT(MONTH FROM fecha_nacimiento) = EXTRACT(MONTH FROM CURRENT_DATE)
AND estado = TRUE;

-- Vista consolidada de Medicamentos
CREATE OR REPLACE VIEW vw_medicamentos_completos AS
SELECT 
    m.id_medicamento,
    m.nombre_comercial,
    m.nombre_generico,
    m.forma_farmaceutica,
    m.concentracion,
    l.nombre_laboratorio,
    c.nombre_categoria,
    m.estado,
    m.fecha_creacion
FROM vademecum_medicamentos m
LEFT JOIN vademecum_laboratorios l 
       ON m.id_laboratorio = l.id_laboratorio
LEFT JOIN vademecum_medicamento_categoria mc 
       ON m.id_medicamento = mc.id_medicamento
LEFT JOIN vademecum_categorias_terapeuticas c 
       ON mc.id_categoria = c.id_categoria;

-- Vista de Medicamentos con Protocolos clínicos
CREATE OR REPLACE VIEW vw_medicamentos_protocolos AS
SELECT 
    m.id_medicamento,
    m.nombre_comercial,
    p.id_protocolo,
    p.protocolo_clinico,
    p.descripcion,
    mp.estado AS estado_relacion,
    p.estado AS estado_protocolo
FROM vademecum_medicamentos m
JOIN vademecum_medicamento_protocolo mp 
     ON m.id_medicamento = mp.id_medicamento
JOIN vademecum_protocolos_clinicos p 
     ON mp.id_protocolo = p.id_protocolo;

-- Vista de Interacciones de Medicamentos
CREATE OR REPLACE VIEW vw_medicamentos_interacciones AS
SELECT 
    m1.nombre_comercial AS medicamento,
    m2.nombre_comercial AS interacciona_con,
    i.descripcion_interaccion,
    i.tipo_interaccion,
    i.estado
FROM vademecum_interacciones i
LEFT JOIN vademecum_medicamentos m1 
       ON i.id_medicamento = m1.id_medicamento
LEFT JOIN vademecum_medicamentos m2 
       ON i.id_medicamento_interactua = m2.id_medicamento;

-- Vista de Medicamentos con efectos secundarios
CREATE OR REPLACE VIEW vw_medicamentos_efectos AS
SELECT 
    m.nombre_comercial,
    e.efecto_secundario,
    e.frecuencia,
    e.estado
FROM vademecum_efectos_secundarios e
JOIN vademecum_medicamentos m 
     ON e.id_medicamento = m.id_medicamento;



-- =========================
-- INSERCIONES DE DATOS
-- =========================

-- Nacionalidades
INSERT INTO nacionalidad (nombre, gentilicio_nac, iso_nac) VALUES
('Afganistán', 'Afgana', 'AFG'),
('Albania', 'Albanesa', 'ALB'),
('Alemania', 'Alemana', 'DEU'),
('Andorra', 'Andorrana', 'AND'),
('Angola', 'Angoleña', 'AGO'),
('Antigua y Barbuda', 'Antiguana', 'ATG'),
('Arabia Saudita', 'Saudí', 'SAU'),
('Argelia', 'Argelina', 'DZA'),
('Argentina', 'Argentina', 'ARG'),
('Armenia', 'Armenia', 'ARM'),
('Aruba', 'Arubeña', 'ABW'),
('Australia', 'Australiana', 'AUS'),
('Austria', 'Austríaca', 'AUT'),
('Azerbaiyán', 'Azerbaiyana', 'AZE'),
('Bahamas', 'Bahameña', 'BHS'),
('Bangladés', 'Bangladesí', 'BGD'),
('Barbados', 'Barbadense', 'BRB'),
('Baréin', 'Bareiní', 'BHR'),
('Bélgica', 'Belga', 'BEL'),
('Belice', 'Beliceña', 'BLZ'),
('Benín', 'Beninesa', 'BEN'),
('Bielorrusia', 'Bielorrusa', 'BLR'),
('Birmania', 'Birmana', 'MMR'),
('Bolivia', 'Boliviana', 'BOL'),
('Bosnia y Herzegovina', 'Bosnia', 'BIH'),
('Botsuana', 'Botsuana', 'BWA'),
('Brasil', 'Brasileña', 'BRA'),
('Brunéi', 'Bruneana', 'BRN'),
('Bulgaria', 'Búlgara', 'BGR'),
('Burkina Faso', 'Burkinés', 'BFA'),
('Burundi', 'Burundesa', 'BDI'),
('Bután', 'Butanesa', 'BTN'),
('Cabo Verde', 'Caboverdiana', 'CPV'),
('Camboya', 'Camboyana', 'KHM'),
('Camerún', 'Camerunesa', 'CMR'),
('Canadá', 'Canadiense', 'CAN'),
('Catar', 'Catarí', 'QAT'),
('Chad', 'Chadiana', 'TCD'),
('Chile', 'Chilena', 'CHL'),
('China', 'China', 'CHN'),
('Chipre', 'Chipriota', 'CYP'),
('Ciudad del Vaticano', 'Vaticana', 'VAT'),
('Colombia', 'Colombiana', 'COL'),
('Comoras', 'Comorense', 'COM'),
('Corea del Norte', 'Norcoreana', 'PRK'),
('Corea del Sur', 'Surcoreana', 'KOR'),
('Costa de Marfil', 'Marfileña', 'CIV'),
('Costa Rica', 'Costarricense', 'CRI'),
('Croacia', 'Croata', 'HRV'),
('Cuba', 'Cubana', 'CUB'),
('Dinamarca', 'Danesa', 'DNK'),
('Dominica', 'Dominiqués', 'DMA'),
('Ecuador', 'Ecuatoriana', 'ECU'),
('Egipto', 'Egipcia', 'EGY'),
('El Salvador', 'Salvadoreña', 'SLV'),
('Emiratos Árabes Unidos', 'Emiratí', 'ARE'),
('Eritrea', 'Eritrea', 'ERI'),
('Eslovaquia', 'Eslovaca', 'SVK'),
('Eslovenia', 'Eslovena', 'SVN'),
('España', 'Española', 'ESP'),
('Estados Unidos', 'Estadounidense', 'USA'),
('Estonia', 'Estona', 'EST'),
('Esuatini', 'Suazi', 'SWZ'),
('Etiopía', 'Etíope', 'ETH'),
('Filipinas', 'Filipina', 'PHL'),
('Finlandia', 'Finlandesa', 'FIN'),
('Fiyi', 'Fiyiana', 'FJI'),
('Francia', 'Francesa', 'FRA'),
('Gabón', 'Gabonesa', 'GAB'),
('Gambia', 'Gambiana', 'GMB'),
('Georgia', 'Georgiana', 'GEO'),
('Ghana', 'Ghanesa', 'GHA'),
('Granada', 'Granadina', 'GRD'),
('Grecia', 'Griega', 'GRC'),
('Guatemala', 'Guatemalteca', 'GTM'),
('Guinea', 'Guineana', 'GIN'),
('Guinea-Bisáu', 'Guineana-Bisauense', 'GNB'),
('Guinea Ecuatorial', 'Ecuatoguineana', 'GNQ'),
('Guyana', 'Guyanesa', 'GUY'),
('Haití', 'Haitiana', 'HTI'),
('Honduras', 'Hondureña', 'HND'),
('Hungría', 'Húngara', 'HUN'),
('India', 'India', 'IND'),
('Indonesia', 'Indonesia', 'IDN'),
('Irak', 'Iraquí', 'IRQ'),
('Irán', 'Iraní', 'IRN'),
('Irlanda', 'Irlandesa', 'IRL'),
('Islandia', 'Islandesa', 'ISL'),
('Islas Marshall', 'Marshalesa', 'MHL'),
('Islas Salomón', 'Salomonense', 'SLB'),
('Israel', 'Israelí', 'ISR'),
('Italia', 'Italiana', 'ITA'),
('Jamaica', 'Jamaiquina', 'JAM'),
('Japón', 'Japonesa', 'JPN'),
('Jordania', 'Jordana', 'JOR'),
('Kazajistán', 'Kazaja', 'KAZ'),
('Kenia', 'Keniana', 'KEN'),
('Kirguistán', 'Kirguisa', 'KGZ'),
('Kiribati', 'Kiribatiana', 'KIR'),
('Kuwait', 'Kuwaití', 'KWT'),
('Laos', 'Laosiana', 'LAO'),
('Lesoto', 'Lesotense', 'LSO'),
('Letonia', 'Letona', 'LVA'),
('Líbano', 'Libanesa', 'LBN'),
('Liberia', 'Liberiana', 'LBR'),
('Libia', 'Libia', 'LBY'),
('Liechtenstein', 'Liechtensteiniana', 'LIE'),
('Lituania', 'Lituana', 'LTU'),
('Luxemburgo', 'Luxemburguesa', 'LUX'),
('Madagascar', 'Malgache', 'MDG'),
('Malasia', 'Malasia', 'MYS'),
('Malaui', 'Malauí', 'MWI'),
('Maldivas', 'Maldiva', 'MDV'),
('Malí', 'Maliense', 'MLI'),
('Malta', 'Maltesa', 'MLT'),
('Marruecos', 'Marroquí', 'MAR'),
('Mauricio', 'Mauriciana', 'MUS'),
('Mauritania', 'Mauritana', 'MRT'),
('México', 'Mexicana', 'MEX'),
('Micronesia', 'Micronesia', 'FSM'),
('Moldavia', 'Moldava', 'MDA'),
('Mónaco', 'Monegasca', 'MCO'),
('Mongolia', 'Mongola', 'MNG'),
('Montenegro', 'Montenegrina', 'MNE'),
('Mozambique', 'Mozambiqueña', 'MOZ'),
('Namibia', 'Namibia', 'NAM'),
('Nauru', 'Nauruana', 'NRU'),
('Nepal', 'Nepalí', 'NPL'),
('Nicaragua', 'Nicaragüense', 'NIC'),
('Níger', 'Nigeriana', 'NER'),
('Nigeria', 'Nigeriana', 'NGA'),
('Noruega', 'Noruega', 'NOR'),
('Nueva Zelanda', 'Neozelandesa', 'NZL'),
('Omán', 'Omaní', 'OMN'),
('Países Bajos', 'Neerlandesa', 'NLD'),
('Pakistán', 'Pakistaní', 'PAK'),
('Palaos', 'Palauense', 'PLW'),
('Palestina', 'Palestina', 'PSE'),
('Panamá', 'Panameña', 'PAN'),
('Papúa Nueva Guinea', 'Papú', 'PNG'),
('Paraguay', 'Paraguaya', 'PRY'),
('Perú', 'Peruana', 'PER'),
('Polonia', 'Polaca', 'POL'),
('Portugal', 'Portuguesa', 'PRT'),
('Reino Unido', 'Británica', 'GBR'),
('República Centroafricana', 'Centroafricana', 'CAF'),
('República Checa', 'Checa', 'CZE'),
('República Democrática del Congo', 'Congolesa', 'COD'),
('República del Congo', 'Congolesa', 'COG'),
('República Dominicana', 'Dominicana', 'DOM'),
('Ruanda', 'Ruandesa', 'RWA'),
('Rumanía', 'Rumana', 'ROU'),
('Rusia', 'Rusa', 'RUS'),
('Samoa', 'Samoana', 'WSM'),
('San Cristóbal y Nieves', 'Sancristobalense', 'KNA'),
('San Marino', 'Sanmarinense', 'SMR'),
('San Vicente y las Granadinas', 'Sanvicentina', 'VCT'),
('Santa Lucía', 'Santalucense', 'LCA'),
('Santo Tomé y Príncipe', 'Santotomense', 'STP'),
('Senegal', 'Senegalesa', 'SEN'),
('Serbia', 'Serbia', 'SRB'),
('Seychelles', 'Seychellense', 'SYC'),
('Sierra Leona', 'Sierraleonesa', 'SLE'),
('Singapur', 'Singapurense', 'SGP'),
('Siria', 'Siria', 'SYR'),
('Somalia', 'Somalí', 'SOM'),
('Sri Lanka', 'Ceilandesa', 'LKA'),
('Sudáfrica', 'Sudafricana', 'ZAF'),
('Sudán', 'Sudanesa', 'SDN'),
('Sudán del Sur', 'Sursudanesa', 'SSD'),
('Suecia', 'Sueca', 'SWE'),
('Suiza', 'Suiza', 'CHE'),
('Surinam', 'Surinamesa', 'SUR'),
('Tailandia', 'Tailandesa', 'THA'),
('Tanzania', 'Tanzana', 'TZA'),
('Tayikistán', 'Tayika', 'TJK'),
('Timor Oriental', 'Timorense', 'TLS'),
('Togo', 'Togolesa', 'TGO'),
('Tonga', 'Tongana', 'TON'),
('Trinidad y Tobago', 'Trinitense', 'TTO'),
('Túnez', 'Tunecina', 'TUN'),
('Turkmenistán', 'Turcomana', 'TKM'),
('Turquía', 'Turca', 'TUR'),
('Tuvalu', 'Tuvaluana', 'TUV'),
('Ucrania', 'Ucraniana', 'UKR'),
('Uganda', 'Ugandesa', 'UGA'),
('Uruguay', 'Uruguaya', 'URY'),
('Uzbekistán', 'Uzbeka', 'UZB'),
('Vanuatu', 'Vanuatuense', 'VUT'),
('Venezuela', 'Venezolana', 'VEN'),
('Vietnam', 'Vietnamita', 'VNM'),
('Yemen', 'Yemení', 'YEM'),
('Yibuti', 'Yibutiana', 'DJI'),
('Zambia', 'Zambiana', 'ZMB'),
('Zimbabue', 'Zimbabuense', 'ZWE');

-- Regiones
INSERT INTO regiones (id, nombre, abreviatura, capital) VALUES
(1, 'Arica y Parinacota', 'AP', 'Arica'),
(2, 'Tarapacá', 'TA', 'Iquique'),
(3, 'Antofagasta', 'AN', 'Antofagasta'),
(4, 'Atacama', 'AT', 'Copiapó'),
(5, 'Coquimbo', 'CO', 'La Serena'),
(6, 'Valparaíso', 'VA', 'Valparaíso'),
(7, 'Metropolitana de Santiago', 'RM', 'Santiago'),
(8, 'Libertador General Bernardo O''Higgins', 'OH', 'Rancagua'),
(9, 'Maule', 'MA', 'Talca'),
(10, 'Ñuble', 'NB', 'Chillán'),
(11, 'Biobío', 'BI', 'Concepción'),
(12, 'La Araucanía', 'AR', 'Temuco'),
(13, 'Los Ríos', 'LR', 'Valdivia'),
(14, 'Los Lagos', 'LL', 'Puerto Montt'),
(15, 'Aysén del General Carlos Ibáñez del Campo', 'AI', 'Coyhaique'),
(16, 'Magallanes y de la Antártida Chilena', 'MG', 'Punta Arenas');

-- Provincias
INSERT INTO provincias (id, nombre, id_region) VALUES
(1, 'Arica', 1),
(2, 'Parinacota', 1),
(3, 'Iquique', 2),
(4, 'El Tamarugal', 2),
(5, 'Tocopilla', 3),
(6, 'El Loa', 3),
(7, 'Antofagasta', 3),
(8, 'Chañaral', 4),
(9, 'Copiapó', 4),
(10, 'Huasco', 4),
(11, 'Elqui', 5),
(12, 'Limarí', 5),
(13, 'Choapa', 5),
(14, 'Petorca', 6),
(15, 'Los Andes', 6),
(16, 'San Felipe de Aconcagua', 6),
(17, 'Quillota', 6),
(18, 'Valparaíso', 6),
(19, 'San Antonio', 6),
(20, 'Isla de Pascua', 6),
(21, 'Marga Marga', 6),
(22, 'Chacabuco', 7),
(23, 'Santiago', 7),
(24, 'Cordillera', 7),
(25, 'Maipo', 7),
(26, 'Melipilla', 7),
(27, 'Talagante', 7),
(28, 'Cachapoal', 8),
(29, 'Colchagua', 8),
(30, 'Cardenal Caro', 8),
(31, 'Curicó', 9),
(32, 'Talca', 9),
(33, 'Linares', 9),
(34, 'Cauquenes', 9),
(35, 'Diguillín', 10),
(36, 'Itata', 10),
(37, 'Punilla', 10),
(38, 'Bio Bío', 11),
(39, 'Concepción', 11),
(40, 'Arauco', 11),
(41, 'Malleco', 12),
(42, 'Cautín', 12),
(43, 'Valdivia', 13),
(44, 'Ranco', 13),
(45, 'Osorno', 14),
(46, 'Llanquihue', 14),
(47, 'Chiloé', 14),
(48, 'Palena', 14),
(49, 'Coyhaique', 15),
(50, 'Aysén', 15),
(51, 'General Carrera', 15),
(52, 'Capitán Prat', 15),
(53, 'Última Esperanza', 16),
(54, 'Magallanes', 16),
(55, 'Tierra del Fuego', 16),
(56, 'Antártida Chilena', 16);

-- Comunas
INSERT INTO comunas (id, nombre, id_provincia) VALUES
(1, 'Arica', 1),
(2, 'Camarones', 1),
(3, 'General Lagos', 2),
(4, 'Putre', 2),
(5, 'Alto Hospicio', 3),
(6, 'Iquique', 3),
(7, 'Camiña', 4),
(8, 'Colchane', 4),
(9, 'Huara', 4),
(10, 'Pica', 4),
(11, 'Pozo Almonte', 4),
(12, 'Tocopilla', 5),
(13, 'María Elena', 5),
(14, 'Calama', 6),
(15, 'Ollagüe', 6),
(16, 'San Pedro de Atacama', 6),
(17, 'Antofagasta', 7),
(18, 'Mejillones', 7),
(19, 'Sierra Gorda', 7),
(20, 'Taltal', 7),
(21, 'Chañaral', 8),
(22, 'Diego de Almagro', 8),
(23, 'Copiapó', 9),
(24, 'Caldera', 9),
(25, 'Tierra Amarilla', 9),
(26, 'Vallenar', 10),
(27, 'Alto del Carmen', 10),
(28, 'Freirina', 10),
(29, 'Huasco', 10),
(30, 'La Serena', 11),
(31, 'Coquimbo', 11),
(32, 'Andacollo', 11),
(33, 'La Higuera', 11),
(34, 'Paiguano', 11),
(35, 'Vicuña', 11),
(36, 'Ovalle', 12),
(37, 'Combarbalá', 12),
(38, 'Monte Patria', 12),
(39, 'Punitaqui', 12),
(40, 'Río Hurtado', 12),
(41, 'Illapel', 13),
(42, 'Canela', 13),
(43, 'Los Vilos', 13),
(44, 'Salamanca', 13),
(45, 'La Ligua', 14),
(46, 'Cabildo', 14),
(47, 'Zapallar', 14),
(48, 'Papudo', 14),
(49, 'Petorca', 14),
(50, 'Los Andes', 15),
(51, 'San Esteban', 15),
(52, 'Calle Larga', 15),
(53, 'Rinconada', 15),
(54, 'San Felipe', 16),
(55, 'Llay-Llay', 16),
(56, 'Putaendo', 16),
(57, 'Santa María', 16),
(58, 'Catemu', 16),
(59, 'Panquehue', 16),
(60, 'Quillota', 17),
(61, 'La Cruz', 17),
(62, 'La Calera', 17),
(63, 'Nogales', 17),
(64, 'Hijuelas', 17),
(65, 'Valparaíso', 18),
(66, 'Viña del Mar', 18),
(67, 'Concón', 18),
(68, 'Quintero', 18),
(69, 'Puchuncaví', 18),
(70, 'Casablanca', 18),
(71, 'Juan Fernández', 18),
(72, 'San Antonio', 19),
(73, 'Cartagena', 19),
(74, 'El Tabo', 19),
(75, 'El Quisco', 19),
(76, 'Algarrobo', 19),
(77, 'Santo Domingo', 19),
(78, 'Isla de Pascua', 20),
(79, 'Quilpué', 21),
(80, 'Limache', 21),
(81, 'Olmué', 21),
(82, 'Villa Alemana', 21),
(83, 'Colina', 22),
(84, 'Lampa', 22),
(85, 'Tiltil', 22),
(86, 'Santiago', 23),
(87, 'Vitacura', 23),
(88, 'San Ramón', 23),
(89, 'San Miguel', 23),
(90, 'San Joaquín', 23),
(91, 'Renca', 23),
(92, 'Recoleta', 23),
(93, 'Quinta Normal', 23),
(94, 'Quilicura', 23),
(95, 'Pudahuel', 23),
(96, 'Providencia', 23),
(97, 'Peñalolén', 23),
(98, 'Pedro Aguirre Cerda', 23),
(99, 'Ñuñoa', 23),
(100, 'Maipú', 23),
(101, 'Macul', 23),
(102, 'Lo Prado', 23),
(103, 'Lo Espejo', 23),
(104, 'Lo Barnechea', 23),
(105, 'Las Condes', 23),
(106, 'La Reina', 23),
(107, 'La Pintana', 23),
(108, 'La Granja', 23),
(109, 'La Florida', 23),
(110, 'La Cisterna', 23),
(111, 'Independencia', 23),
(112, 'Huechuraba', 23),
(113, 'Estación Central', 23),
(114, 'El Bosque', 23),
(115, 'Conchalí', 23),
(116, 'Cerro Navia', 23),
(117, 'Cerrillos', 23),
(118, 'Puente Alto', 24),
(119, 'San José de Maipo', 24),
(120, 'Pirque', 24),
(121, 'San Bernardo', 25),
(122, 'Buin', 25),
(123, 'Paine', 25),
(124, 'Calera de Tango', 25),
(125, 'Melipilla', 26),
(126, 'Alhué', 26),
(127, 'Curacaví', 26),
(128, 'María Pinto', 26),
(129, 'San Pedro', 26),
(130, 'Isla de Maipo', 27),
(131, 'El Monte', 27),
(132, 'Padre Hurtado', 27),
(133, 'Peñaflor', 27),
(134, 'Talagante', 27),
(135, 'Codegua', 28),
(136, 'Coinco', 28),
(137, 'Coltauco', 28),
(138, 'Doñihue', 28),
(139, 'Graneros', 28),
(140, 'Las Cabras', 28),
(141, 'Machalí', 28),
(142, 'Malloa', 28),
(143, 'Mostazal', 28),
(144, 'Olivar', 28),
(145, 'Peumo', 28),
(146, 'Pichidegua', 28),
(147, 'Quinta de Tilcoco', 28),
(148, 'Rancagua', 28),
(149, 'Rengo', 28),
(150, 'Requínoa', 28),
(151, 'San Vicente de Tagua Tagua', 28),
(152, 'Chépica', 29),
(153, 'Chimbarongo', 29),
(154, 'Lolol', 29),
(155, 'Nancagua', 29),
(156, 'Palmilla', 29),
(157, 'Peralillo', 29),
(158, 'Placilla', 29),
(159, 'Pumanque', 29),
(160, 'San Fernando', 29),
(161, 'Santa Cruz', 29),
(162, 'La Estrella', 30),
(163, 'Litueche', 30),
(164, 'Marchigüe', 30),
(165, 'Navidad', 30),
(166, 'Paredones', 30),
(167, 'Pichilemu', 30),
(168, 'Curicó', 31),
(169, 'Hualañé', 31),
(170, 'Licantén', 31),
(171, 'Molina', 31),
(172, 'Rauco', 31),
(173, 'Romeral', 31),
(174, 'Sagrada Familia', 31),
(175, 'Teno', 31),
(176, 'Vichuquén', 31),
(177, 'Talca', 32),
(178, 'San Clemente', 32),
(179, 'Pelarco', 32),
(180, 'Pencahue', 32),
(181, 'Maule', 32),
(182, 'San Rafael', 32),
(183, 'Curepto', 32),
(184, 'Constitución', 32),
(185, 'Empedrado', 32),
(186, 'Río Claro', 32),
(187, 'Linares', 33),
(188, 'San Javier', 33),
(189, 'Parral', 33),
(190, 'Villa Alegre', 33),
(191, 'Longaví', 33),
(192, 'Colbún', 33),
(193, 'Retiro', 33),
(194, 'Yerbas Buenas', 33),
(195, 'Cauquenes', 34),
(196, 'Chanco', 34),
(197, 'Pelluhue', 34),
(198, 'Bulnes', 35),
(199, 'Chillán', 35),
(200, 'Chillán Viejo', 35),
(201, 'El Carmen', 35),
(202, 'Pemuco', 35),
(203, 'Pinto', 35),
(204, 'Quillón', 35),
(205, 'San Ignacio', 35),
(206, 'Yungay', 35),
(207, 'Cobquecura', 36),
(208, 'Coelemu', 36),
(209, 'Ninhue', 36),
(210, 'Portezuelo', 36),
(211, 'Quirihue', 36),
(212, 'Ránquil', 36),
(213, 'Treguaco', 36),
(214, 'San Carlos', 37),
(215, 'Coihueco', 37),
(216, 'San Nicolás', 37),
(217, 'Ñiquén', 37),
(218, 'San Fabián', 37),
(219, 'Alto Biobío', 38),
(220, 'Antuco', 38),
(221, 'Cabrero', 38),
(222, 'Laja', 38),
(223, 'Los Ángeles', 38),
(224, 'Mulchén', 38),
(225, 'Nacimiento', 38),
(226, 'Negrete', 38),
(227, 'Quilaco', 38),
(228, 'Quilleco', 38),
(229, 'San Rosendo', 38),
(230, 'Santa Bárbara', 38),
(231, 'Tucapel', 38),
(232, 'Yumbel', 38),
(233, 'Concepción', 39),
(234, 'Coronel', 39),
(235, 'Chiguayante', 39),
(236, 'Florida', 39),
(237, 'Hualpén', 39),
(238, 'Hualqui', 39),
(239, 'Lota', 39),
(240, 'Penco', 39),
(241, 'San Pedro de la Paz', 39),
(242, 'Santa Juana', 39),
(243, 'Talcahuano', 39),
(244, 'Tomé', 39),
(245, 'Arauco', 40),
(246, 'Cañete', 40),
(247, 'Contulmo', 40),
(248, 'Curanilahue', 40),
(249, 'Lebu', 40),
(250, 'Los Álamos', 40),
(251, 'Tirúa', 40),
(252, 'Angol', 41),
(253, 'Collipulli', 41),
(254, 'Curacautín', 41),
(255, 'Ercilla', 41),
(256, 'Lonquimay', 41),
(257, 'Los Sauces', 41),
(258, 'Lumaco', 41),
(259, 'Purén', 41),
(260, 'Renaico', 41),
(261, 'Traiguén', 41),
(262, 'Victoria', 41),
(263, 'Temuco', 42),
(264, 'Carahue', 42),
(265, 'Cholchol', 42),
(266, 'Cunco', 42),
(267, 'Curarrehue', 42),
(268, 'Freire', 42),
(269, 'Galvarino', 42),
(270, 'Gorbea', 42),
(271, 'Lautaro', 42),
(272, 'Loncoche', 42),
(273, 'Melipeuco', 42),
(274, 'Nueva Imperial', 42),
(275, 'Padre Las Casas', 42),
(276, 'Perquenco', 42),
(277, 'Pitrufquén', 42),
(278, 'Pucón', 42),
(279, 'Saavedra', 42),
(280, 'Teodoro Schmidt', 42),
(281, 'Toltén', 42),
(282, 'Vilcún', 42),
(283, 'Villarrica', 42),
(284, 'Valdivia', 43),
(285, 'Corral', 43),
(286, 'Lanco', 43),
(287, 'Los Lagos', 43),
(288, 'Máfil', 43),
(289, 'Mariquina', 43),
(290, 'Paillaco', 43),
(291, 'Panguipulli', 43),
(292, 'La Unión', 44),
(293, 'Futrono', 44),
(294, 'Lago Ranco', 44),
(295, 'Río Bueno', 44),
(296, 'Osorno', 45),
(297, 'Puerto Octay', 45),
(298, 'Purranque', 45),
(299, 'Puyehue', 45),
(300, 'Río Negro', 45),
(301, 'San Juan de la Costa', 45),
(302, 'San Pablo', 45),
(303, 'Calbuco', 46),
(304, 'Cochamó', 46),
(305, 'Fresia', 46),
(306, 'Frutillar', 46),
(307, 'Llanquihue', 46),
(308, 'Los Muermos', 46),
(309, 'Maullín', 46),
(310, 'Puerto Montt', 46),
(311, 'Puerto Varas', 46),
(312, 'Ancud', 47),
(313, 'Castro', 47),
(314, 'Chonchi', 47),
(315, 'Curaco de Vélez', 47),
(316, 'Dalcahue', 47),
(317, 'Puqueldón', 47),
(318, 'Queilén', 47),
(319, 'Quellón', 47),
(320, 'Quemchi', 47),
(321, 'Quinchao', 47),
(322, 'Chaitén', 48),
(323, 'Futaleufú', 48),
(324, 'Hualaihué', 48),
(325, 'Palena', 48),
(326, 'Lago Verde', 49),
(327, 'Coyhaique', 49),
(328, 'Aysén', 50),
(329, 'Cisnes', 50),
(330, 'Guaitecas', 50),
(331, 'Río Ibáñez', 51),
(332, 'Chile Chico', 51),
(333, 'Cochrane', 52),
(334, 'O''Higgins', 52),
(335, 'Tortel', 52),
(336, 'Natales', 53),
(337, 'Torres del Paine', 53),
(338, 'Laguna Blanca', 54),
(339, 'Punta Arenas', 54),
(340, 'Río Verde', 54),
(341, 'San Gregorio', 54),
(342, 'Porvenir', 55),
(343, 'Primavera', 55),
(344, 'Timaukel', 55),
(345, 'Cabo de Hornos', 56),
(346, 'Antártida', 56);

-- Tipos de empresa
INSERT INTO tipos_empresa (nombre) 
VALUES ('Farmacia'), ('Librería'), ('Bodega'), ('Venta'), ('Iglesia');

-- Empresas
INSERT INTO empresas (nombre, id_tipo_empresa) VALUES 
('FarmaVida', 1),
('SaludPlus', 1),
('MediCare', 1),
('Librería Nacional', 2),
('Tecnología Avanzada', 3);

-- Dashboard inicial
INSERT INTO dashboard_inicial (pagina) VALUES
('dashboard'),
('dashboard-flex');

-- Usuarios
INSERT INTO usuarios (username, email, password, duracion, pagina_inicio, id_dashboard) VALUES
('admin', 'fbirrer@gmail.com', 'cambiar', 30, 'inicio.html', 1),
('test1', 'test1@gmail.com', 'cambiar', 15, 'inicio.html', 2),
('test2', 'test2@gmail.com', 'cambiar', 1000, 'inicio.html', 2);

-- Roles
INSERT INTO roles (nombre) VALUES 
('Soporte'), ('Administrador'), ('Auditor'), ('Usuario');

-- Tipos de menú
INSERT INTO tipos_menu (nombre) VALUES 
('General'), ('Módulos');

-- Menús
INSERT INTO menus (
    id, nombre, icono, id_tipo_menu, id_padre, url, descripcion, "token", orden
)
VALUES
    (1, 'Gestión', 'fa-solid fa-atom', 1, NULL, '/gestion', 'Módulo de gestión', NULL, 2),
    (2, 'Tablas', 'fa-solid fa-table', 1, 1, '/gestion/tablas', 'Tablas base del sistema', NULL, 1),
    (3, 'Tipo de Datos', 'fa-solid fa-database', 1, 1, '/gestion/tipoEmpresa', 'Gestión de Tipo de Empresas', NULL, 2),
    (4, 'Relaciones', 'fa-solid fa-lock', 1, 1, NULL, 'Gestionador de relaciones', NULL, 3),
    (5, 'Geo referencia', 'fa-solid fa-map-location-dot', 1, NULL, NULL, NULL, NULL, 4),
    (6, 'Empresas', 'fa-solid fa-building', 1, 2, '/gestion/empresas', 'Empresas del sistema', NULL, 1),
    (7, 'Usuarios', 'fa-solid fa-users', 1, 2, '/gestion/usuarios', 'Usuarios del sistema', NULL, 2),
    (8, 'Roles', 'fa-solid fa-user-shield', 1, 2, '/gestion/rol', 'Roles del sistema', NULL, 3),
    (9, 'Menús Generales', 'fa-solid fa-bars', 1, 2, '/gestion/menu', 'Menus generales del sistema', NULL, 4),
    (10, 'Menus X Modulo', 'fa-solid fa-sitemap', 1, 2, '/gestion/menusxmodulo', 'Menus por Modulos', NULL, 5),
    (11, 'Modulos', 'fa-solid fa-puzzle-piece', 1, 2, '/gestion/modulo', 'Modulos del sistema', NULL, 6),
    (12, 'Nacionalidad', 'fa-solid fa-flag', 1, 2, '/gestion/nacionalidad', 'Nacionalidades del sistema', NULL, 7),
    (13, 'Rol Menu', 'fa-solid fa-link', 1, 4, '/gestion/rolMenu', NULL, NULL, 1),
    (14, 'Empresa Modulo', 'fa-solid fa-layer-group', 1, 4, NULL, NULL, NULL, 1),
    (15, 'Empresa Usuario', 'fa-solid fa-diagram-project', 1, 4, '/gestion/empresaUsuario', NULL, NULL, 2),
    (16, 'Empresa Otro', 'fa-solid fa-user-tie', 1, 4, NULL, NULL, NULL, 2),
    (17, 'Modulos Menu', 'fa-solid fa-list', 1, 4, NULL, NULL, NULL, 3),
    (18, 'Tipo de Empresas', 'fa-solid fa-industry', 1, 3, '/gestion/tipoEmpresa', NULL, NULL, 1),
    (19, 'Tipo de Menu', 'fa-solid fa-list', 1, 3, '/gestion/tipoMenu', NULL, NULL, 2),
    (20, 'Regiones', 'fa-solid fa-globe', 1, 5, '/modulo-georeferencia/regiones', NULL, NULL, 2),
    (21, 'Provincias', 'fa-solid fa-map', 1, 5, '/modulo-georeferencia/provincias', NULL, NULL, 3),
    (22, 'Comunas', 'fa-solid fa-location-dot', 1, 5, '/modulo-georeferencia/comunas', NULL, NULL, 4),
--vademecum
    (23, 'Vademecum-Lista', 'fa-solid fa-book-medical', 2, NULL, '/modulo-vademecum/lista', NULL, NULL, 1),
    (24, 'Tablas', 'fa-solid fa-table', 2, NULL, '/modulo-inventario', NULL, NULL, 2),
    (25, 'Medicamentos', 'fa-solid fa-capsules', 2, 24, '/modulo-vademecum/medicamento', NULL, NULL, 1),
    (26, 'Laboratorios', 'fa-solid fa-flask', 2, 24, '/modulo-vademecum/laboratorios', NULL, NULL, 2),
    (27, 'Cat. Terapeuticas', 'fa-solid fa-stethoscope', 2, 24, '/modulo-vademecum/catTerapeuticas', NULL, NULL, 3),
    (28, 'Cat. Medicamentos', 'fa-solid fa-prescription', 2, 24, '/modulo-vademecum/cat-medicamentos', NULL, NULL, 4),
    (29, 'Indicaciones', 'fa-solid fa-clipboard-list', 2, 24, '/modulo-vademecum/indicaciones', NULL, NULL, 5),
    (30, 'Posologia', 'fa-solid fa-syringe', 2, 24, '/modulo-vademecum/posologia', NULL, NULL, 6),
    (31, 'ContraIndicaciones', 'fa-solid fa-ban', 2, 24, '/modulo-vademecum/contraIndicaciones', NULL, NULL, 7),
    (32, 'Interacciones', 'fa-solid fa-arrows-to-dot', 2, 24, '/modulo-vademecum/interacciones', NULL, NULL, 8),
    (33, 'Efectos Secundarios', 'fa-solid fa-triangle-exclamation', 2, 24, '/modulo-vademecum/efectosSecundarios', NULL, NULL, 9),
    (34, 'Presentaciones', 'fa-solid fa-box', 2, 24, '/modulo-vademecum/presentaciones', NULL, NULL, 10),
    (35, 'Farmacinetica', 'fa-solid fa-chart-line', 2, 24, '/modulo-vademecum/farmacinetica', NULL, NULL, 11),
    (36, 'Protocolos', 'fa-solid fa-file-prescription', 2, 24, '/modulo-vademecum/protocolos', NULL, NULL, 12),
    (37, 'Logo de Laboratorio', 'fa-solid fa-image', 2, 24, '/modulo-vademecum/logoLaboratorio', NULL, NULL, 13),
    (38, 'Foto de Medicamento', 'fa-solid fa-camera', 2, 24, '/modulo-vademecum/fotoMedicamento', NULL, NULL, 14),
--agenda
    (39, 'Personas', 'fa-solid fa-users', 2, NULL, NULL, NULL, NULL, 1),
    (40, 'Hashtag', 'fa-solid fa-hashtag', 2, NULL, NULL, NULL, NULL, 2),
    (41, 'Informes', 'fa-solid fa-file-lines', 2, NULL, NULL, NULL, NULL, 3),
    (42, 'Correos', 'fa-solid fa-envelope', 2, NULL, NULL, NULL, NULL, 4),
    (43, 'Cumpleaños', 'fa-solid fa-cake-candles', 2, 41, NULL, NULL, NULL, 1),
    (44, 'Busqueda', 'fa-solid fa-magnifying-glass', 2, 41, NULL, NULL, NULL, 2),
    (45, 'Configurados', 'fa-solid fa-gear', 2, 41, NULL, NULL, NULL, 5),
    (46, 'Masivos', 'fa-solid fa-envelopes-bulk', 2, 41, NULL, NULL, NULL, 6),
    (47, 'Templates', 'fa-solid fa-file-code', 2, 46, NULL, NULL, NULL, 1),
    (48, 'Calendarizar', 'fa-solid fa-calendar', 2, 46, NULL, NULL, NULL, 2),
--inventario
    (49, 'Movimientos', 'fa-solid fa-arrow-right-arrow-left', 2, NULL, '/modulo-inventario/movimientos', NULL, NULL, 2),
    (50, 'Clientes', 'fa-solid fa-user-group', 2, 37, '/modulo-inventario/clientes', NULL, NULL, 1),
    (51, 'Proveedores', 'fa-solid fa-truck', 2, 37, '/modulo-inventario/proveedores', NULL, NULL, 2),
    (52, 'Productos', 'fa-solid fa-boxes-stacked', 2, 37, '/modulo-inventario/productos', NULL, NULL, 3),
    (53, 'Sucursales', 'fa-solid fa-store', 2, 37, '/modulo-inventario/sucursales', NULL, NULL, 4),
--propiedades
    (54, 'Configuración', 'fa-solid fa-gear', 1, NULL, NULL, NULL, NULL, 10),
    (55, 'Propiedades', 'fa-solid fa-list-check', 1, 54, '/propiedades/configuracion', NULL, NULL, 1),
    (56, 'Propiedades Empresa', 'fa-solid fa-building-columns', 1, 54, '/propiedades/configuracion-empresa', NULL, NULL, 2),
    (57, 'Carga Masiva', 'fa-solid fa-envelopes-bulk', 1, 54, '/propiedades/carga-masiva', NULL, NULL, 3);

SELECT setval(pg_get_serial_sequence('menus', 'id'), (SELECT MAX(id) FROM menus)+1);


-- Relación menú-rol
INSERT INTO menu_rol (id_menu, id_rol, estado)
VALUES
    (1, 1, true),
    (2, 1, true),
    (3, 1, true),
    (4, 1, true),
    (5, 1, true),
    (6, 1, true),
    (7, 1, true),
    (8, 1, true),
    (9, 1, true),
    (10, 1, true),
    (11, 1, true),
    (12, 1, true),
    (13, 1, true),
    (14, 1, true),
    (23, 2, false),
    (23, 3, false),
    (23, 1, true),
    (23, 4, false),
    (24, 2, false),
    (24, 3, false),
    (24, 1, true),
    (24, 4, false),
    (30, 2, false),
    (30, 3, false),
    (30, 1, true),
    (30, 4, false),
    (31, 2, false),
    (31, 3, false),
    (31, 1, true),
    (31, 4, false),
    (32, 2, false),
    (32, 3, false),
    (32, 1, true),
    (32, 4, false),
    (33, 2, false),
    (33, 3, false),
    (33, 1, true),
    (33, 4, false),
    (34, 2, false),
    (34, 3, false),
    (34, 1, true),
    (34, 4, false),
    (35, 2, false),
    (35, 3, false),
    (35, 1, true),
    (35, 4, false),
    (36, 2, false),
    (36, 3, false),
    (36, 1, true),
    (36, 4, false),
    (37, 2, false),
    (37, 3, false),
    (37, 1, true),
    (37, 4, false),
    (44, 2, false),
    (44, 3, false),
    (44, 1, true),
    (44, 4, false),
    (45, 2, false),
    (45, 3, false),
    (45, 1, true),
    (45, 4, false),
    (48, 2, false),
    (48, 3, false),
    (48, 1, true),
    (48, 4, false),
    (50, 2, false),
    (50, 3, false),
    (50, 1, true),
    (50, 4, false),
    (52, 2, false),
    (52, 3, false),
    (52, 1, true),
    (52, 4, false),
    (53, 2, false),
    (53, 3, false),
    (53, 1, true),
    (53, 4, false),
    (51, 2, false),
    (51, 3, false),
    (51, 1, true),
    (51, 4, false),
    (49, 2, false),
    (49, 3, false),
    (49, 1, true),
    (49, 4, false),
    (46, 2, false),
    (46, 3, false),
    (46, 1, true),
    (46, 4, false),
    (47, 2, false),
    (47, 3, false),
    (47, 1, true),
    (47, 4, false),
    (38, 2, false),
    (38, 3, false),
    (38, 1, true),
    (38, 4, false),
    (39, 2, false),
    (39, 3, false),
    (39, 1, true),
    (39, 4, false),
    (40, 2, false),
    (40, 3, false),
    (40, 1, true),
    (40, 4, false),
    (41, 2, false),
    (41, 3, false),
    (41, 1, true),
    (41, 4, false),
    (42, 2, false),
    (42, 3, false),
    (42, 1, true),
    (42, 4, false),
    (43, 2, false),
    (43, 3, false),
    (43, 1, true),
    (43, 4, false),
    (1, 2, false),
    (1, 3, false),
    (1, 4, false),
    (2, 2, false),
    (2, 3, false),
    (2, 4, false),
    (6, 2, false),
    (6, 3, false),
    (6, 4, false),
    (7, 2, false),
    (7, 3, false),
    (7, 4, false),
    (8, 2, false),
    (8, 3, false),
    (8, 4, false),
    (9, 2, false),
    (9, 3, false),
    (9, 4, false),
    (10, 2, false),
    (10, 3, false),
    (10, 4, false),
    (18, 2, false),
    (18, 1, true),
    (18, 3, false),
    (18, 4, false),
    (19, 2, false),
    (19, 3, false),
    (19, 1, true),
    (19, 4, false),
    (11, 2, false),
    (11, 3, false),
    (11, 4, false),
    (12, 2, false),
    (12, 3, false),
    (12, 4, false),
    (3, 2, false),
    (3, 3, false),
    (3, 4, false),
    (13, 2, false),
    (13, 3, false),
    (13, 4, false),
    (14, 2, false),
    (14, 3, false),
    (14, 4, false),
    (15, 2, false),
    (15, 1, true),
    (15, 4, false),
    (16, 2, false),
    (16, 3, false),
    (16, 1, true),
    (16, 4, false),
    (17, 2, false),
    (17, 3, false),
    (17, 1, true),
    (17, 4, false),
    (4, 2, false),
    (4, 3, false),
    (4, 4, false),
    (5, 2, false),
    (5, 3, false),
    (5, 4, false),
    (20, 2, false),
    (20, 1, true),
    (20, 4, false),
    (21, 2, false),
    (21, 3, false),
    (21, 1, true),
    (21, 4, false),
    (22, 2, false),
    (22, 3, false),
    (22, 1, true),
    (22, 4, false),
    (25, 2, false),
    (25, 1, true),
    (25, 4, false),
    (26, 2, false),
    (26, 3, false),
    (26, 1, true),
    (26, 4, false),
    (29, 2, false),
    (29, 3, false),
    (29, 1, true),
    (29, 4, false),
    (27, 2, false),
    (27, 1, true),
    (27, 4, false),
    (28, 2, false),
    (28, 3, false),
    (28, 1, true),
    (28, 4, false),
    (54, 2, false),
    (54, 3, false),
    (54, 1, true),
    (54, 4, false),
    (55, 2, false),
    (55, 3, false),
    (55, 1, true),
    (55, 4, false),
    (56, 2, false),
    (56, 3, false),
    (56, 1, true),
    (56, 4, false),
    (57, 2, false),
    (57, 3, false),
    (57, 1, true),
    (57, 4, false);
-- Menús específicos para tipos de empresa
INSERT INTO menu_tipo_empresa (id_menu, id_tipo_empresa) VALUES
(1, 1), (2, 1), (3, 1);

-- Relación empresa-usuario
INSERT INTO empresa_usuario (id_empresa, id_usuario) VALUES
(1, 1), (2, 1);

-- Relación empresa-usuario-rol
INSERT INTO empresa_usuario_rol (id_empresa, id_usuario, id_rol) VALUES
(1, 1, 1), (2, 1, 1), (3, 1, 1);

-- Módulos
INSERT INTO modulos (nombre, descripcion) VALUES
('Ventas', 'Módulo para administrar procesos de ventas de productos y servicios'),
('Inventario', 'Módulo para gestionar inventario'),
('Vademécum', 'Módulo para generar y visualizar mantenedor de farmacias/remedios'),
('Agenda', 'Módulo para generar y visualizar manejo de contactos');

-- Parámetros del sistema
INSERT INTO parametro_sistema (clave, valor, descripcion) VALUES
('valida_session', 'true', 'Se valida el tiempo de conexión de los usuarios');

-- Relación módulo-menú
-- 1️⃣ Inserción de registros en modulo_menu (id_modulo_menu es autoincremental)
INSERT INTO public.modulo_menu (id_modulo, id_menu, estado)
VALUES
    -- Módulo 3
    (3, 23, true),
    (3, 24, true),
    (3, 25, true),
    (3, 26, true),
    (3, 27, true),
    (3, 28, true),
    (3, 29, true),
    (3, 30, true),
    (3, 31, true),
    (3, 32, true),
    (3, 33, true),
    (3, 34, true),
    (3, 35, true),
    (3, 37, true),
    (3, 38, true),

    -- Módulo 4
    (4, 39, true),
    (4, 40, true),
    (4, 41, true),
    (4, 42, true),
    (4, 43, true),
    (4, 44, true),
    (4, 45, true),
    (4, 46, true),
    (4, 47, true),
    (4, 48, true),

    -- Módulo 2
    (2, 49, true),
    (2, 50, true),
    (2, 51, true),
    (2, 52, true),
    (2, 53, true),

    -- Módulo 1
    (1, 54, true),
    (1, 55, true),
    (1, 56, true),
    (1, 57, true);

-- Relación empresa-módulo
INSERT INTO empresa_modulo (id_empresa, id_modulo, fecha_inicio, fecha_fin, estado) VALUES
(2, 2, '2000-01-01', NULL, TRUE),
(3, 2, '2000-01-01', NULL, TRUE),
(1, 1, '2000-01-01', NULL, TRUE),
(1, 2, '2000-01-01', NULL, TRUE),
(1, 3, '2000-01-01', NULL, TRUE),
(1, 4, '2000-01-01', NULL, TRUE);

-- Vademécum: Laboratorios
-- Insertar Laboratorios
INSERT INTO vademecum_laboratorios (nombre_laboratorio, pais, direccion, sitio_web, contacto, id_empresa, estado, fecha_creacion) VALUES
('Laboratorio Chile', 'Chile', 'Av. Marathon 1315, Ñuñoa, Santiago', 'https://www.laboratoriochile.cl', 'contacto@laboratoriochile.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Recalcine (Abbott)', 'Chile', 'Av. El Salto 5380, Huechuraba, Santiago', 'https://www.abbott.com', 'info@abbott.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Grünenthal Chilena', 'Chile', 'Av. Apoquindo 4775, Las Condes, Santiago', 'https://www.grunenthal.com', 'info@grunenthal.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Saval', 'Chile', 'Av. Presidente Riesco 5561, Las Condes, Santiago', 'https://www.saval.cl', 'contacto@saval.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Pfizer Chile', 'Chile', 'Av. Andrés Bello 2687, Las Condes, Santiago', 'https://www.pfizer.cl', 'info@pfizer.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Roche Chile', 'Chile', 'Av. Vitacura 2909, Las Condes, Santiago', 'https://www.roche.cl', 'contacto@roche.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Novartis Chile', 'Chile', 'Av. Apoquindo 3600, Las Condes, Santiago', 'https://www.novartis.com', 'contacto@novartis.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Merck Chile', 'Chile', 'Av. Las Condes 11283, Santiago', 'https://www.merckgroup.com', 'info@merck.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Bayer Chile', 'Chile', 'Av. Apoquindo 3100, Las Condes, Santiago', 'https://www.bayer.com', 'contacto@bayer.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Sanofi Chile', 'Chile', 'Av. Providencia 1760, Santiago', 'https://www.sanofi.com', 'info@sanofi.cl', 1, TRUE, CURRENT_TIMESTAMP),
('GlaxoSmithKline Chile', 'Chile', 'Av. Apoquindo 3885, Las Condes, Santiago', 'https://www.gsk.com', 'contacto@gsk.cl', 1, TRUE, CURRENT_TIMESTAMP),
('AstraZeneca Chile', 'Chile', 'Av. Andrés Bello 2457, Santiago', 'https://www.astrazeneca.com', 'info@astrazeneca.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Eli Lilly Chile', 'Chile', 'Av. El Bosque Norte 500, Santiago', 'https://www.lilly.com', 'contacto@lilly.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Boehringer Ingelheim Chile', 'Chile', 'Av. Vitacura 2670, Santiago', 'https://www.boehringer-ingelheim.com', 'info@boehringer.cl', 1, TRUE, CURRENT_TIMESTAMP),
('Janssen Chile', 'Chile', 'Av. Kennedy 5454, Santiago', 'https://www.janssen.com', 'contacto@janssen.cl', 1, TRUE, CURRENT_TIMESTAMP);

-- Insertar Categorías Terapéuticas
INSERT INTO vademecum_categorias_terapeuticas (nombre_categoria, descripcion, id_empresa, estado, fecha_creacion) VALUES
('Analgésicos', 'Medicamentos para el alivio del dolor', 1, TRUE, CURRENT_TIMESTAMP),
('Antibióticos', 'Medicamentos para infecciones bacterianas', 1, TRUE, CURRENT_TIMESTAMP),
('Antiinflamatorios', 'Medicamentos para reducir inflamación', 1, TRUE, CURRENT_TIMESTAMP),
('Antihipertensivos', 'Medicamentos para hipertensión arterial', 1, TRUE, CURRENT_TIMESTAMP),
('Antidiabéticos', 'Medicamentos para diabetes', 1, TRUE, CURRENT_TIMESTAMP),
('Antidepresivos', 'Medicamentos para trastornos depresivos', 1, TRUE, CURRENT_TIMESTAMP),
('Antihistamínicos', 'Medicamentos para alergias', 1, TRUE, CURRENT_TIMESTAMP),
('Broncodilatadores', 'Medicamentos para afecciones respiratorias', 1, TRUE, CURRENT_TIMESTAMP),
('Inhibidores de la bomba de protones', 'Medicamentos para trastornos gástricos', 1, TRUE, CURRENT_TIMESTAMP),
('Estatinas', 'Medicamentos para hiperlipidemia', 1, TRUE, CURRENT_TIMESTAMP),
('Antifúngicos', 'Medicamentos para infecciones fúngicas', 1, TRUE, CURRENT_TIMESTAMP),
('Ansiolíticos', 'Medicamentos para ansiedad', 1, TRUE, CURRENT_TIMESTAMP),
('Anticoagulantes', 'Medicamentos para prevenir trombosis', 1, TRUE, CURRENT_TIMESTAMP),
('Antivirales', 'Medicamentos para infecciones virales', 1, TRUE, CURRENT_TIMESTAMP),
('Inmunosupresores', 'Medicamentos para suprimir el sistema inmune', 1, TRUE, CURRENT_TIMESTAMP);

-- Insertar Medicamentos (50 reales + 950 placeholders)
DO $$
DECLARE
    medicamentos jsonb := '[
        {"nombre_comercial": "Paracetamol FarmaVida", "nombre_generico": "Paracetamol", "forma": "Comprimido", "concentracion": "500 mg", "clasificacion": "Venta libre"},
        {"nombre_comercial": "Ibuprofeno FarmaVida", "nombre_generico": "Ibuprofeno", "forma": "Comprimido", "concentracion": "400 mg", "clasificacion": "Venta libre"},
        {"nombre_comercial": "Amoxicilina FarmaVida", "nombre_generico": "Amoxicilina", "forma": "Cápsula", "concentracion": "500 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Losartán FarmaVida", "nombre_generico": "Losartán", "forma": "Comprimido", "concentracion": "50 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Metformina FarmaVida", "nombre_generico": "Metformina", "forma": "Comprimido", "concentracion": "850 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Sertralina FarmaVida", "nombre_generico": "Sertralina", "forma": "Comprimido", "concentracion": "50 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Omeprazol FarmaVida", "nombre_generico": "Omeprazol", "forma": "Cápsula", "concentracion": "20 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Atorvastatina FarmaVida", "nombre_generico": "Atorvastatina", "forma": "Comprimido", "concentracion": "20 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Ciprofloxacino FarmaVida", "nombre_generico": "Ciprofloxacino", "forma": "Comprimido", "concentracion": "500 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Amlodipino FarmaVida", "nombre_generico": "Amlodipino", "forma": "Comprimido", "concentracion": "5 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Loratadina FarmaVida", "nombre_generico": "Loratadina", "forma": "Comprimido", "concentracion": "10 mg", "clasificacion": "Venta libre"},
        {"nombre_comercial": "Salbutamol FarmaVida", "nombre_generico": "Salbutamol", "forma": "Inhalador", "concentracion": "100 mcg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Levotiroxina FarmaVida", "nombre_generico": "Levotiroxina", "forma": "Comprimido", "concentracion": "100 mcg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Enalapril FarmaVida", "nombre_generico": "Enalapril", "forma": "Comprimido", "concentracion": "10 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Doxiciclina FarmaVida", "nombre_generico": "Doxiciclina", "forma": "Cápsula", "concentracion": "100 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Clonazepam FarmaVida", "nombre_generico": "Clonazepam", "forma": "Comprimido", "concentracion": "2 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Azitromicina FarmaVida", "nombre_generico": "Azitromicina", "forma": "Comprimido", "concentracion": "500 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Simvastatina FarmaVida", "nombre_generico": "Simvastatina", "forma": "Comprimido", "concentracion": "20 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Fluoxetina FarmaVida", "nombre_generico": "Fluoxetina", "forma": "Cápsula", "concentracion": "20 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Diclofenaco FarmaVida", "nombre_generico": "Diclofenaco", "forma": "Comprimido", "concentracion": "50 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Hidroclorotiazida FarmaVida", "nombre_generico": "Hidroclorotiazida", "forma": "Comprimido", "concentracion": "25 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Ranitidina FarmaVida", "nombre_generico": "Ranitidina", "forma": "Comprimido", "concentracion": "150 mg", "clasificacion": "Venta libre"},
        {"nombre_comercial": "Cetirizina FarmaVida", "nombre_generico": "Cetirizina", "forma": "Comprimido", "concentracion": "10 mg", "clasificacion": "Venta libre"},
        {"nombre_comercial": "Metoprolol FarmaVida", "nombre_generico": "Metoprolol", "forma": "Comprimido", "concentracion": "50 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Esomeprazol FarmaVida", "nombre_generico": "Esomeprazol", "forma": "Cápsula", "concentracion": "40 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Tramadol FarmaVida", "nombre_generico": "Tramadol", "forma": "Comprimido", "concentracion": "50 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Citalopram FarmaVida", "nombre_generico": "Citalopram", "forma": "Comprimido", "concentracion": "20 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Clotrimazol FarmaVida", "nombre_generico": "Clotrimazol", "forma": "Crema", "concentracion": "1%", "clasificacion": "Venta libre"},
        {"nombre_comercial": "Insulina Glargina FarmaVida", "nombre_generico": "Insulina Glargina", "forma": "Inyectable", "concentracion": "100 UI/ml", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Montelukast FarmaVida", "nombre_generico": "Montelukast", "forma": "Comprimido", "concentracion": "10 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Aciclovir FarmaVida", "nombre_generico": "Aciclovir", "forma": "Comprimido", "concentracion": "400 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Alprazolam FarmaVida", "nombre_generico": "Alprazolam", "forma": "Comprimido", "concentracion": "0.5 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Aspirina FarmaVida", "nombre_generico": "Ácido acetilsalicílico", "forma": "Comprimido", "concentracion": "100 mg", "clasificacion": "Venta libre"},
        {"nombre_comercial": "Bisoprolol FarmaVida", "nombre_generico": "Bisoprolol", "forma": "Comprimido", "concentracion": "5 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Budesonida FarmaVida", "nombre_generico": "Budesonida", "forma": "Inhalador", "concentracion": "200 mcg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Candesartán FarmaVida", "nombre_generico": "Candesartán", "forma": "Comprimido", "concentracion": "16 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Clindamicina FarmaVida", "nombre_generico": "Clindamicina", "forma": "Cápsula", "concentracion": "300 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Clopidogrel FarmaVida", "nombre_generico": "Clopidogrel", "forma": "Comprimido", "concentracion": "75 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Duloxetina FarmaVida", "nombre_generico": "Duloxetina", "forma": "Cápsula", "concentracion": "60 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Ezetimiba FarmaVida", "nombre_generico": "Ezetimiba", "forma": "Comprimido", "concentracion": "10 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Furosemida FarmaVida", "nombre_generico": "Furosemida", "forma": "Comprimido", "concentracion": "40 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Gabapentina FarmaVida", "nombre_generico": "Gabapentina", "forma": "Cápsula", "concentracion": "300 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Lansoprazol FarmaVida", "nombre_generico": "Lansoprazol", "forma": "Cápsula", "concentracion": "30 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Levofloxacino FarmaVida", "nombre_generico": "Levofloxacino", "forma": "Comprimido", "concentracion": "500 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Lisinopril FarmaVida", "nombre_generico": "Lisinopril", "forma": "Comprimido", "concentracion": "10 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Mirtazapina FarmaVida", "nombre_generico": "Mirtazapina", "forma": "Comprimido", "concentracion": "30 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Naproxeno FarmaVida", "nombre_generico": "Naproxeno", "forma": "Comprimido", "concentracion": "500 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Pantoprazol FarmaVida", "nombre_generico": "Pantoprazol", "forma": "Comprimido", "concentracion": "40 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Prednisona FarmaVida", "nombre_generico": "Prednisona", "forma": "Comprimido", "concentracion": "20 mg", "clasificacion": "Prescripción"},
        {"nombre_comercial": "Rosuvastatina FarmaVida", "nombre_generico": "Rosuvastatina", "forma": "Comprimido", "concentracion": "10 mg", "clasificacion": "Prescripción"}
    ]';
BEGIN
    -- Insertar los 50 medicamentos reales
    INSERT INTO vademecum_medicamentos (
        nombre_comercial, 
        nombre_generico, 
        forma_farmaceutica, 
        concentracion, 
        id_laboratorio, 
        registro_sanitario, 
        clasificacion, 
        id_empresa, 
        estado, 
        fecha_creacion
    )
    SELECT 
        m.nombre_comercial,
        m.nombre_generico,
        m.forma,
        m.concentracion,
        FLOOR(1 + (RANDOM() * 15))::INTEGER,
        CONCAT('REG-', LPAD(ROW_NUMBER() OVER ()::TEXT, 4, '0')),
        m.clasificacion,
        1,
        TRUE,
        CURRENT_TIMESTAMP
    FROM jsonb_to_recordset(medicamentos) AS m (
        nombre_comercial VARCHAR,
        nombre_generico VARCHAR,
        forma VARCHAR,
        concentracion VARCHAR,
        clasificacion VARCHAR
    );

    -- Insertar los 950 medicamentos placeholders
    INSERT INTO vademecum_medicamentos (
        nombre_comercial, 
        nombre_generico, 
        forma_farmaceutica, 
        concentracion, 
        id_laboratorio, 
        registro_sanitario, 
        clasificacion, 
        id_empresa, 
        estado, 
        fecha_creacion
    )
    SELECT 
        CONCAT('Medicamento ', n, ' FarmaVida') AS nombre_comercial,
        CONCAT('Principio Activo ', n) AS nombre_generico,
        CASE 
            WHEN n % 4 = 0 THEN 'Comprimido'
            WHEN n % 4 = 1 THEN 'Cápsula'
            WHEN n % 4 = 2 THEN 'Inyectable'
            ELSE 'Tópico'
        END AS forma_farmaceutica,
        CASE 
            WHEN n % 4 = 0 THEN CONCAT((n % 100 + 10), ' mg')
            WHEN n % 4 = 1 THEN CONCAT((n % 100 + 5), ' mg')
            WHEN n % 4 = 2 THEN CONCAT((n % 10 + 1), ' UI/ml')
            ELSE CONCAT((n % 5 + 1), '%')
        END AS concentracion,
        FLOOR(1 + (RANDOM() * 15))::INTEGER AS id_laboratorio,
        CONCAT('REG-', LPAD((n + 50)::TEXT, 4, '0')) AS registro_sanitario,
        CASE 
            WHEN n % 2 = 0 THEN 'Prescripción'
            ELSE 'Venta libre'
        END AS clasificacion,
        1,
        TRUE,
        CURRENT_TIMESTAMP
    FROM generate_series(1, 950) AS n;
END $$;

-- Insertar Medicamento-Categoría
INSERT INTO vademecum_medicamento_categoria (id_medicamento, id_categoria)
SELECT 
    m.id_medicamento, 
    CASE 
        WHEN m.nombre_generico IN ('Paracetamol', 'Ibuprofeno', 'Diclofenaco', 'Tramadol', 'Ácido acetilsalicílico', 'Naproxeno', 'Prednisona') THEN 1
        WHEN m.nombre_generico IN ('Amoxicilina', 'Ciprofloxacino', 'Doxiciclina', 'Azitromicina', 'Clindamicina', 'Levofloxacino') THEN 2
        WHEN m.nombre_generico IN ('Losartán', 'Amlodipino', 'Enalapril', 'Hidroclorotiazida', 'Metoprolol', 'Candesartán', 'Bisoprolol', 'Lisinopril', 'Furosemida') THEN 4
        WHEN m.nombre_generico IN ('Metformina', 'Insulina Glargina') THEN 5
        WHEN m.nombre_generico IN ('Sertralina', 'Fluoxetina', 'Clonazepam', 'Citalopram', 'Duloxetina', 'Mirtazapina') THEN 6
        WHEN m.nombre_generico IN ('Loratadina', 'Cetirizina') THEN 7
        WHEN m.nombre_generico IN ('Salbutamol', 'Budesonida', 'Montelukast') THEN 8
        WHEN m.nombre_generico IN ('Omeprazol', 'Esomeprazol', 'Lansoprazol', 'Pantoprazol', 'Ranitidina') THEN 9
        WHEN m.nombre_generico IN ('Atorvastatina', 'Simvastatina', 'Rosuvastatina', 'Ezetimiba') THEN 10
        WHEN m.nombre_generico IN ('Clotrimazol', 'Aciclovir') THEN 11
        WHEN m.nombre_generico IN ('Alprazolam', 'Gabapentina') THEN 12
        WHEN m.nombre_generico IN ('Clopidogrel') THEN 13
        ELSE FLOOR(1 + (RANDOM() * 15))::INTEGER
    END AS id_categoria
FROM vademecum_medicamentos m
WHERE m.id_empresa = 1;

-- Insertar Indicaciones
INSERT INTO vademecum_indicaciones (id_medicamento, indicacion, mecanismo_accion, estado, fecha_creacion)
SELECT 
    id_medicamento, 
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Alivio del dolor leve a moderado y fiebre'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Dolor, inflamación y fiebre'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Infecciones bacterianas'
        WHEN nombre_generico = 'Losartán' THEN 'Tratamiento de hipertensión arterial'
        WHEN nombre_generico = 'Metformina' THEN 'Control de glucosa en diabetes tipo 2'
        WHEN nombre_generico = 'Sertralina' THEN 'Tratamiento de depresión y ansiedad'
        WHEN nombre_generico = 'Omeprazol' THEN 'Reflujo gastroesofágico y úlceras'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Reducción de colesterol LDL'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Infecciones bacterianas urinarias y respiratorias'
        WHEN nombre_generico = 'Amlodipino' THEN 'Hipertensión y angina de pecho'
        WHEN nombre_generico = 'Loratadina' THEN 'Alergias estacionales'
        WHEN nombre_generico = 'Salbutamol' THEN 'Asma y broncoespasmo'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Hipotiroidismo'
        WHEN nombre_generico = 'Enalapril' THEN 'Hipertensión e insuficiencia cardíaca'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Infecciones bacterianas y acné'
        WHEN nombre_generico = 'Clonazepam' THEN 'Convulsiones y trastornos de ansiedad'
        WHEN nombre_generico = 'Azitromicina' THEN 'Infecciones respiratorias y de piel'
        WHEN nombre_generico = 'Simvastatina' THEN 'Hiperlipidemia'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Depresión y trastorno obsesivo-compulsivo'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Dolor e inflamación articular'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Hipertensión y edema'
        WHEN nombre_generico = 'Ranitidina' THEN 'Úlceras gástricas y reflujo'
        WHEN nombre_generico = 'Cetirizina' THEN 'Alergias y rinitis alérgica'
        WHEN nombre_generico = 'Metoprolol' THEN 'Hipertensión y arritmias'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Enfermedad por reflujo gastroesofágico'
        WHEN nombre_generico = 'Tramadol' THEN 'Dolor moderado a severo'
        WHEN nombre_generico = 'Citalopram' THEN 'Depresión mayor'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Infecciones fúngicas cutáneas'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Diabetes mellitus tipo 1 y 2'
        WHEN nombre_generico = 'Montelukast' THEN 'Asma y rinitis alérgica'
        WHEN nombre_generico = 'Aciclovir' THEN 'Infecciones por herpes virus'
        WHEN nombre_generico = 'Alprazolam' THEN 'Trastornos de ansiedad y pánico'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Dolor leve, fiebre y prevención cardiovascular'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Hipertensión e insuficiencia cardíaca'
        WHEN nombre_generico = 'Budesonida' THEN 'Asma y enfermedad inflamatoria intestinal'
        WHEN nombre_generico = 'Candesartán' THEN 'Hipertensión e insuficiencia cardíaca'
        WHEN nombre_generico = 'Clindamicina' THEN 'Infecciones bacterianas anaerobias'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Prevención de eventos trombóticos'
        WHEN nombre_generico = 'Duloxetina' THEN 'Depresión y dolor neuropático'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Reducción de colesterol'
        WHEN nombre_generico = 'Furosemida' THEN 'Edema e hipertensión'
        WHEN nombre_generico = 'Gabapentina' THEN 'Dolor neuropático y convulsiones'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Úlceras y reflujo gastroesofágico'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Infecciones bacterianas respiratorias y urinarias'
        WHEN nombre_generico = 'Lisinopril' THEN 'Hipertensión e insuficiencia cardíaca'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Depresión mayor'
        WHEN nombre_generico = 'Naproxeno' THEN 'Dolor e inflamación'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Reflujo gastroesofágico y úlceras'
        WHEN nombre_generico = 'Prednisona' THEN 'Inflamación y enfermedades autoinmunes'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Hiperlipidemia'
        ELSE 'Tratamiento de condiciones específicas'
    END AS indicacion,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Inhibe la síntesis de prostaglandinas en el SNC'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Inhibe la ciclooxigenasa (COX)'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Inhibe la síntesis de la pared celular bacteriana'
        WHEN nombre_generico = 'Losartán' THEN 'Antagonista de receptores de angiotensina II'
        WHEN nombre_generico = 'Metformina' THEN 'Reduce la producción hepática de glucosa'
        WHEN nombre_generico = 'Sertralina' THEN 'Inhibidor selectivo de la recaptación de serotonina'
        WHEN nombre_generico = 'Omeprazol' THEN 'Inhibidor de la bomba de protones'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Inhibe la HMG-CoA reductasa'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Inhibe la ADN girasa bacteriana'
        WHEN nombre_generico = 'Amlodipino' THEN 'Bloqueador de canales de calcio'
        WHEN nombre_generico = 'Loratadina' THEN 'Antagonista de receptores H1'
        WHEN nombre_generico = 'Salbutamol' THEN 'Agonista beta-2 adrenérgico'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Hormona tiroidea sintética'
        WHEN nombre_generico = 'Enalapril' THEN 'Inhibidor de la enzima convertidora de angiotensina'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Inhibe la síntesis de proteínas bacterianas'
        WHEN nombre_generico = 'Clonazepam' THEN 'Potencia la actividad del GABA'
        WHEN nombre_generico = 'Azitromicina' THEN 'Inhibe la síntesis de proteínas bacterianas'
        WHEN nombre_generico = 'Simvastatina' THEN 'Inhibe la HMG-CoA reductasa'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Inhibidor selectivo de la recaptación de serotonina'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Inhibe la ciclooxigenasa (COX)'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Inhibe la reabsorción de sodio en túbulos renales'
        WHEN nombre_generico = 'Ranitidina' THEN 'Antagonista de receptores H2'
        WHEN nombre_generico = 'Cetirizina' THEN 'Antagonista de receptores H1'
        WHEN nombre_generico = 'Metoprolol' THEN 'Bloqueador beta-adrenérgico selectivo'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Inhibidor de la bomba de protones'
        WHEN nombre_generico = 'Tramadol' THEN 'Agonista opioide y inhibidor de recaptación de serotonina/norepinefrina'
        WHEN nombre_generico = 'Citalopram' THEN 'Inhibidor selectivo de la recaptación de serotonina'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Inhibe la síntesis de ergosterol en hongos'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Análogo de insulina de acción prolongada'
        WHEN nombre_generico = 'Montelukast' THEN 'Antagonista de receptores de leucotrienos'
        WHEN nombre_generico = 'Aciclovir' THEN 'Inhibe la replicación del ADN viral'
        WHEN nombre_generico = 'Alprazolam' THEN 'Potencia la actividad del GABA'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Inhibe la ciclooxigenasa (COX)'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Bloqueador beta-adrenérgico selectivo'
        WHEN nombre_generico = 'Budesonida' THEN 'Corticosteroide antiinflamatorio'
        WHEN nombre_generico = 'Candesartán' THEN 'Antagonista de receptores de angiotensina II'
        WHEN nombre_generico = 'Clindamicina' THEN 'Inhibe la síntesis de proteínas bacterianas'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Inhibe la agregación plaquetaria'
        WHEN nombre_generico = 'Duloxetina' THEN 'Inhibidor de la recaptación de serotonina y norepinefrina'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Inhibe la absorción de colesterol'
        WHEN nombre_generico = 'Furosemida' THEN 'Inhibe la reabsorción de sodio y cloro'
        WHEN nombre_generico = 'Gabapentina' THEN 'Modula la actividad de canales de calcio'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Inhibidor de la bomba de protones'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Inhibe la ADN girasa bacteriana'
        WHEN nombre_generico = 'Lisinopril' THEN 'Inhibidor de la enzima convertidora de angiotensina'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Antagonista de receptores alfa-2 y serotoninérgicos'
        WHEN nombre_generico = 'Naproxeno' THEN 'Inhibe la ciclooxigenasa (COX)'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Inhibidor de la bomba de protones'
        WHEN nombre_generico = 'Prednisona' THEN 'Corticosteroide antiinflamatorio'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Inhibe la HMG-CoA reductasa'
        ELSE 'Mecanismo específico según principio activo'
    END AS mecanismo_accion,
    TRUE, 
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos
WHERE id_empresa = 1;

-- Insertar Posologías
INSERT INTO vademecum_posologias (
    id_medicamento, 
    dosis, 
    via_administracion, 
    edad_minima, 
    edad_maxima, 
    instrucciones_especiales, 
    estado, 
    fecha_creacion
)
SELECT 
    id_medicamento,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN '500-1000 mg cada 6-8 horas'
        WHEN nombre_generico = 'Ibuprofeno' THEN '400-800 mg cada 6-8 horas'
        WHEN nombre_generico = 'Amoxicilina' THEN '500 mg cada 8 horas'
        WHEN nombre_generico = 'Losartán' THEN '50-100 mg una vez al día'
        WHEN nombre_generico = 'Metformina' THEN '500-1000 mg dos veces al día'
        WHEN nombre_generico = 'Sertralina' THEN '50-200 mg una vez al día'
        WHEN nombre_generico = 'Omeprazol' THEN '20-40 mg una vez al día'
        WHEN nombre_generico = 'Atorvastatina' THEN '10-40 mg una vez al día'
        WHEN nombre_generico = 'Ciprofloxacino' THEN '500-750 mg cada 12 horas'
        WHEN nombre_generico = 'Amlodipino' THEN '5-10 mg una vez al día'
        WHEN nombre_generico = 'Loratadina' THEN '10 mg una vez al día'
        WHEN nombre_generico = 'Salbutamol' THEN '100-200 mcg cada 4-6 horas según necesidad'
        WHEN nombre_generico = 'Levotiroxina' THEN '25-200 mcg una vez al día'
        WHEN nombre_generico = 'Enalapril' THEN '5-20 mg una o dos veces al día'
        WHEN nombre_generico = 'Doxiciclina' THEN '100 mg cada 12 horas el primer día, luego 100 mg al día'
        WHEN nombre_generico = 'Clonazepam' THEN '0.5-2 mg dos o tres veces al día'
        WHEN nombre_generico = 'Azitromicina' THEN '500 mg el primer día, luego 250 mg al día'
        WHEN nombre_generico = 'Simvastatina' THEN '10-40 mg una vez al día'
        WHEN nombre_generico = 'Fluoxetina' THEN '20-60 mg una vez al día'
        WHEN nombre_generico = 'Diclofenaco' THEN '50-100 mg cada 8-12 horas'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN '12.5-50 mg una vez al día'
        WHEN nombre_generico = 'Ranitidina' THEN '150 mg dos veces al día'
        WHEN nombre_generico = 'Cetirizina' THEN '10 mg una vez al día'
        WHEN nombre_generico = 'Metoprolol' THEN '25-100 mg una o dos veces al día'
        WHEN nombre_generico = 'Esomeprazol' THEN '20-40 mg una vez al día'
        WHEN nombre_generico = 'Tramadol' THEN '50-100 mg cada 4-6 horas'
        WHEN nombre_generico = 'Citalopram' THEN '20-40 mg una vez al día'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Aplicar 2-3 veces al día'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Dosis ajustada según glucosa'
        WHEN nombre_generico = 'Montelukast' THEN '10 mg una vez al día por la noche'
        WHEN nombre_generico = 'Aciclovir' THEN '400 mg cada 8 horas'
        WHEN nombre_generico = 'Alprazolam' THEN '0.25-0.5 mg dos o tres veces al día'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN '100-325 mg al día'
        WHEN nombre_generico = 'Bisoprolol' THEN '5-10 mg una vez al día'
        WHEN nombre_generico = 'Budesonida' THEN '200-400 mcg dos veces al día'
        WHEN nombre_generico = 'Candesartán' THEN '8-32 mg una vez al día'
        WHEN nombre_generico = 'Clindamicina' THEN '300 mg cada 6-8 horas'
        WHEN nombre_generico = 'Clopidogrel' THEN '75 mg una vez al día'
        WHEN nombre_generico = 'Duloxetina' THEN '60 mg una vez al día'
        WHEN nombre_generico = 'Ezetimiba' THEN '10 mg una vez al día'
        WHEN nombre_generico = 'Furosemida' THEN '20-80 mg una o dos veces al día'
        WHEN nombre_generico = 'Gabapentina' THEN '300-600 mg tres veces al día'
        WHEN nombre_generico = 'Lansoprazol' THEN '15-30 mg una vez al día'
        WHEN nombre_generico = 'Levofloxacino' THEN '500-750 mg una vez al día'
        WHEN nombre_generico = 'Lisinopril' THEN '10-40 mg una vez al día'
        WHEN nombre_generico = 'Mirtazapina' THEN '15-45 mg una vez al día'
        WHEN nombre_generico = 'Naproxeno' THEN '250-500 mg dos veces al día'
        WHEN nombre_generico = 'Pantoprazol' THEN '40 mg una o dos veces al día'
        WHEN nombre_generico = 'Prednisona' THEN '5-60 mg al día según condición'
        WHEN nombre_generico = 'Rosuvastatina' THEN '5-40 mg una vez al día'
        ELSE 'Dosis según prescripción médica'
    END AS dosis,
    CASE 
        WHEN nombre_generico IN ('Paracetamol', 'Ibuprofeno', 'Amoxicilina', 'Losartán', 'Metformina', 'Sertralina', 'Omeprazol', 'Atorvastatina', 'Ciprofloxacino', 'Amlodipino', 'Loratadina', 'Levotiroxina', 'Enalapril', 'Doxiciclina', 'Clonazepam', 'Azitromicina', 'Simvastatina', 'Fluoxetina', 'Diclofenaco', 'Hidroclorotiazida', 'Ranitidina', 'Cetirizina', 'Metoprolol', 'Esomeprazol', 'Tramadol', 'Citalopram', 'Aciclovir', 'Alprazolam', 'Ácido acetilsalicílico', 'Bisoprolol', 'Candesartán', 'Clindamicina', 'Clopidogrel', 'Duloxetina', 'Ezetimiba', 'Furosemida', 'Gabapentina', 'Lansoprazol', 'Levofloxacino', 'Lisinopril', 'Mirtazapina', 'Naproxeno', 'Pantoprazol', 'Prednisona', 'Rosuvastatina') THEN 'Oral'
        WHEN nombre_generico = 'Salbutamol' THEN 'Inhalación'
        WHEN nombre_generico = 'Budesonida' THEN 'Inhalación'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Inyectable'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Tópica'
        ELSE 'Oral'
    END AS via_administracion,
    CASE 
        WHEN nombre_generico IN ('Paracetamol', 'Ibuprofeno', 'Loratadina', 'Cetirizina') THEN 12
        WHEN nombre_generico IN ('Amoxicilina', 'Azitromicina', 'Clindamicina', 'Levofloxacino') THEN 6
        ELSE 18
    END AS edad_minima,
    CASE 
        WHEN nombre_generico IN ('Paracetamol', 'Ibuprofeno', 'Loratadina', 'Cetirizina') THEN 65
        ELSE 120
    END AS edad_maxima,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'No exceder 4 g al día. Tomar con alimentos si hay malestar gástrico.'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Tomar con alimentos para evitar irritación gástrica.'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Completar el ciclo de tratamiento.'
        WHEN nombre_generico = 'Losartán' THEN 'Tomar con o sin alimentos, preferiblemente a la misma hora.'
        WHEN nombre_generico = 'Metformina' THEN 'Tomar con las comidas para reducir efectos gastrointestinales.'
        WHEN nombre_generico = 'Sertralina' THEN 'Tomar por la mañana o noche, según indicación médica.'
        WHEN nombre_generico = 'Omeprazol' THEN 'Tomar antes del desayuno.'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Tomar por la noche.'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Evitar lácteos o antiácidos 2 horas antes o después.'
        WHEN nombre_generico = 'Amlodipino' THEN 'Tomar con o sin alimentos.'
        WHEN nombre_generico = 'Loratadina' THEN 'No requiere alimentos.'
        WHEN nombre_generico = 'Salbutamol' THEN 'Usar según necesidad, no exceder 8 inhalaciones al día.'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Tomar en ayunas, 30 minutos antes del desayuno.'
        WHEN nombre_generico = 'Enalapril' THEN 'Tomar con o sin alimentos.'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Tomar con agua abundante, evitar acostarse tras la dosis.'
        WHEN nombre_generico = 'Clonazepam' THEN 'Evitar alcohol y actividades que requieran alerta.'
        WHEN nombre_generico = 'Azitromicina' THEN 'Tomar 1 hora antes o 2 horas después de las comidas.'
        WHEN nombre_generico = 'Simvastatina' THEN 'Tomar por la noche.'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Tomar por la mañana.'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Tomar con alimentos.'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Tomar por la mañana para evitar nocturia.'
        WHEN nombre_generico = 'Ranitidina' THEN 'Tomar con o sin alimentos.'
        WHEN nombre_generico = 'Cetirizina' THEN 'No requiere alimentos.'
        WHEN nombre_generico = 'Metoprolol' THEN 'Tomar con alimentos.'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Tomar antes del desayuno.'
        WHEN nombre_generico = 'Tramadol' THEN 'Tomar con o sin alimentos, evitar alcohol.'
        WHEN nombre_generico = 'Citalopram' THEN 'Tomar una vez al día, con o sin alimentos.'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Aplicar en la zona afectada limpia y seca.'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Inyectar a la misma hora cada día.'
        WHEN nombre_generico = 'Montelukast' THEN 'Tomar por la noche.'
        WHEN nombre_generico = 'Aciclovir' THEN 'Tomar con alimentos para mejorar absorción.'
        WHEN nombre_generico = 'Alprazolam' THEN 'Evitar alcohol y conducir.'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Tomar con alimentos para evitar irritación gástrica.'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Tomar por la mañana.'
        WHEN nombre_generico = 'Budesonida' THEN 'Usar según necesidad, seguir instrucciones del inhalador.'
        WHEN nombre_generico = 'Candesartán' THEN 'Tomar con o sin alimentos.'
        WHEN nombre_generico = 'Clindamicina' THEN 'Tomar con agua abundante.'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Tomar con o sin alimentos.'
        WHEN nombre_generico = 'Duloxetina' THEN 'Tomar con alimentos para reducir náuseas.'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Tomar con o sin alimentos.'
        WHEN nombre_generico = 'Furosemida' THEN 'Tomar por la mañana para evitar nocturia.'
        WHEN nombre_generico = 'Gabapentina' THEN 'Tomar con o sin alimentos.'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Tomar antes del desayuno.'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Evitar lácteos o antiácidos.'
        WHEN nombre_generico = 'Lisinopril' THEN 'Tomar con o sin alimentos.'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Tomar por la noche.'
        WHEN nombre_generico = 'Naproxeno' THEN 'Tomar con alimentos.'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Tomar antes del desayuno.'
        WHEN nombre_generico = 'Prednisona' THEN 'Tomar con alimentos para reducir irritación gástrica.'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Tomar por la noche.'
        ELSE 'Seguir indicaciones del médico.'
    END AS instrucciones_especiales,
    TRUE,
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos
WHERE id_empresa = 1;

-- Insertar Contraindicaciones
INSERT INTO vademecum_contraindicaciones (id_medicamento, contraindicacion, estado, fecha_creacion)
SELECT 
    id_medicamento,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Hipersensibilidad al paracetamol, enfermedad hepática grave'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Úlcera péptica, insuficiencia renal, hipersensibilidad a AINEs'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Hipersensibilidad a penicilinas'
        WHEN nombre_generico = 'Losartán' THEN 'Embarazo, hiperkalemia, insuficiencia renal grave'
        WHEN nombre_generico = 'Metformina' THEN 'Insuficiencia renal, cetoacidosis diabética'
        WHEN nombre_generico = 'Sertralina' THEN 'Uso concomitante con IMAO, hipersensibilidad'
        WHEN nombre_generico = 'Omeprazol' THEN 'Hipersensibilidad, uso concomitante con ciertos medicamentos'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Enfermedad hepática activa, embarazo'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Hipersensibilidad a quinolonas, menores de 18 años'
        WHEN nombre_generico = 'Amlodipino' THEN 'Estenosis aórtica severa, hipersensibilidad'
        WHEN nombre_generico = 'Loratadina' THEN 'Hipersensibilidad a loratadina'
        WHEN nombre_generico = 'Salbutamol' THEN 'Hipersensibilidad, taquicardia severa'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Hipertiroidismo no tratado, infarto reciente'
        WHEN nombre_generico = 'Enalapril' THEN 'Angioedema previo, embarazo'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Hipersensibilidad, embarazo, menores de 8 años'
        WHEN nombre_generico = 'Clonazepam' THEN 'Glaucoma de ángulo estrecho, insuficiencia respiratoria'
        WHEN nombre_generico = 'Azitromicina' THEN 'Hipersensibilidad a macrólidos'
        WHEN nombre_generico = 'Simvastatina' THEN 'Enfermedad hepática activa, embarazo'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Uso concomitante con IMAO, hipersensibilidad'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Úlcera péptica, hipersensibilidad a AINEs'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Anuria, hipersensibilidad a sulfonamidas'
        WHEN nombre_generico = 'Ranitidina' THEN 'Hipersensibilidad, porfiria aguda'
        WHEN nombre_generico = 'Cetirizina' THEN 'Hipersensibilidad, insuficiencia renal severa'
        WHEN nombre_generico = 'Metoprolol' THEN 'Bradicardia severa, bloqueo AV'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Hipersensibilidad, uso concomitante con ciertos medicamentos'
        WHEN nombre_generico = 'Tramadol' THEN 'Hipersensibilidad, intoxicación aguda por alcohol'
        WHEN nombre_generico = 'Citalopram' THEN 'Uso concomitante con IMAO, hipersensibilidad'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Hipersensibilidad al clotrimazol'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Hipersensibilidad, hipoglucemia'
        WHEN nombre_generico = 'Montelukast' THEN 'Hipersensibilidad a montelukast'
        WHEN nombre_generico = 'Aciclovir' THEN 'Hipersensibilidad a aciclovir'
        WHEN nombre_generico = 'Alprazolam' THEN 'Glaucoma de ángulo estrecho, hipersensibilidad'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Úlcera péptica, hemofilia'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Bradicardia severa, asma grave'
        WHEN nombre_generico = 'Budesonida' THEN 'Hipersensibilidad, infecciones fúngicas no tratadas'
        WHEN nombre_generico = 'Candesartán' THEN 'Embarazo, hiperkalemia'
        WHEN nombre_generico = 'Clindamicina' THEN 'Hipersensibilidad, colitis ulcerosa'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Hipersensibilidad, sangrado activo'
        WHEN nombre_generico = 'Duloxetina' THEN 'Uso concomitante con IMAO, insuficiencia hepática'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Hipersensibilidad, enfermedad hepática activa'
        WHEN nombre_generico = 'Furosemida' THEN 'Anuria, hipersensibilidad'
        WHEN nombre_generico = 'Gabapentina' THEN 'Hipersensibilidad, insuficiencia renal severa'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Hipersensibilidad, uso concomitante con ciertos medicamentos'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Hipersensibilidad a quinolonas, menores de 18 años'
        WHEN nombre_generico = 'Lisinopril' THEN 'Angioedema previo, embarazo'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Hipersensibilidad, uso concomitante con IMAO'
        WHEN nombre_generico = 'Naproxeno' THEN 'Úlcera péptica, hipersensibilidad a AINEs'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Hipersensibilidad, uso concomitante con ciertos medicamentos'
        WHEN nombre_generico = 'Prednisona' THEN 'Infecciones fúngicas sistémicas, hipersensibilidad'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Enfermedad hepática activa, embarazo'
        ELSE 'Hipersensibilidad al principio activo'
    END AS contraindicacion,
    TRUE,
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos
WHERE id_empresa = 1;

-- Insertar Interacciones
INSERT INTO vademecum_interacciones (id_medicamento, id_medicamento_interactua, descripcion_interaccion, tipo_interaccion, estado, fecha_creacion)
SELECT 
    m1.id_medicamento,
    m2.id_medicamento,
    CASE 
        WHEN m1.nombre_generico = 'Ibuprofeno' AND m2.nombre_generico = 'Losartán' THEN 'Puede reducir el efecto antihipertensivo de Losartán'
        WHEN m1.nombre_generico = 'Sertralina' AND m2.nombre_generico = 'Tramadol' THEN 'Riesgo de síndrome serotoninérgico'
        WHEN m1.nombre_generico = 'Amoxicilina' AND m2.nombre_generico = 'Metformina' THEN 'Posible aumento de efectos gastrointestinales'
        WHEN m1.nombre_generico = 'Ciprofloxacino' AND m2.nombre_generico = 'Warfarina' THEN 'Aumenta el efecto anticoagulante'
        WHEN m1.nombre_generico = 'Simvastatina' AND m2.nombre_generico = 'Amiodarona' THEN 'Aumenta el riesgo de miopatía'
        WHEN m1.nombre_generico = 'Clopidogrel' AND m2.nombre_generico = 'Omeprazol' THEN 'Reduce la eficacia de clopidogrel'
        WHEN m1.nombre_generico = 'Fluoxetina' AND m2.nombre_generico = 'Tramadol' THEN 'Riesgo de síndrome serotoninérgico'
        ELSE 'Interacción no especificada'
    END AS descripcion_interaccion,
    CASE 
        WHEN m1.nombre_generico IN ('Ibuprofeno', 'Sertralina', 'Amoxicilina', 'Ciprofloxacino', 'Simvastatina', 'Clopidogrel', 'Fluoxetina') THEN 'Moderada'
        ELSE 'Leve'
    END AS tipo_interaccion,
    TRUE,
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos m1
CROSS JOIN vademecum_medicamentos m2
WHERE m1.id_empresa = 1 AND m2.id_empresa = 1
AND m1.id_medicamento < m2.id_medicamento
AND m1.nombre_generico IN ('Ibuprofeno', 'Sertralina', 'Amoxicilina', 'Ciprofloxacino', 'Simvastatina', 'Clopidogrel', 'Fluoxetina')
LIMIT 100;

-- Insertar Efectos Secundarios
INSERT INTO vademecum_efectos_secundarios (id_medicamento, efecto_secundario, frecuencia, estado, fecha_creacion)
SELECT 
    id_medicamento,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Náuseas, erupción cutánea'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Dolor gástrico, náuseas'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Diarrea, erupción cutánea'
        WHEN nombre_generico = 'Losartán' THEN 'Mareos, hiperkalemia'
        WHEN nombre_generico = 'Metformina' THEN 'Náuseas, diarrea'
        WHEN nombre_generico = 'Sertralina' THEN 'Insomnio, náuseas'
        WHEN nombre_generico = 'Omeprazol' THEN 'Dolor de cabeza, diarrea'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Dolor muscular, elevación de enzimas hepáticas'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Náuseas, diarrea, dolor articular'
        WHEN nombre_generico = 'Amlodipino' THEN 'Edema periférico, mareos'
        WHEN nombre_generico = 'Loratadina' THEN 'Somnolencia, dolor de cabeza'
        WHEN nombre_generico = 'Salbutamol' THEN 'Temblores, taquicardia'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Palpitaciones, insomnio'
        WHEN nombre_generico = 'Enalapril' THEN 'Tos seca, hipotensión'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Fotosensibilidad, náuseas'
        WHEN nombre_generico = 'Clonazepam' THEN 'Somnolencia, mareos'
        WHEN nombre_generico = 'Azitromicina' THEN 'Diarrea, dolor abdominal'
        WHEN nombre_generico = 'Simvastatina' THEN 'Dolor muscular, elevación de enzimas hepáticas'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Insomnio, náuseas'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Dolor gástrico, náuseas'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Hipokalemia, mareos'
        WHEN nombre_generico = 'Ranitidina' THEN 'Dolor de cabeza, mareos'
        WHEN nombre_generico = 'Cetirizina' THEN 'Somnolencia, fatiga'
        WHEN nombre_generico = 'Metoprolol' THEN 'Bradicardia, fatiga'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Dolor abdominal, diarrea'
        WHEN nombre_generico = 'Tramadol' THEN 'Náuseas, mareos'
        WHEN nombre_generico = 'Citalopram' THEN 'Náuseas, insomnio'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Irritación local, picazón'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Hipoglucemia, reacción en el sitio de inyección'
        WHEN nombre_generico = 'Montelukast' THEN 'Dolor de cabeza, dolor abdominal'
        WHEN nombre_generico = 'Aciclovir' THEN 'Náuseas, dolor de cabeza'
        WHEN nombre_generico = 'Alprazolam' THEN 'Somnolencia, mareos'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Dolor gástrico, sangrado gastrointestinal'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Bradicardia, fatiga'
        WHEN nombre_generico = 'Budesonida' THEN 'Dolor de garganta, tos'
        WHEN nombre_generico = 'Candesartán' THEN 'Mareos, hiperkalemia'
        WHEN nombre_generico = 'Clindamicina' THEN 'Diarrea, náuseas'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Sangrado, dolor abdominal'
        WHEN nombre_generico = 'Duloxetina' THEN 'Náuseas, boca seca'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Dolor abdominal, diarrea'
        WHEN nombre_generico = 'Furosemida' THEN 'Hipokalemia, deshidratación'
        WHEN nombre_generico = 'Gabapentina' THEN 'Mareos, somnolencia'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Dolor de cabeza, diarrea'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Náuseas, insomnio'
        WHEN nombre_generico = 'Lisinopril' THEN 'Tos seca, mareos'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Somnolencia, aumento de peso'
        WHEN nombre_generico = 'Naproxeno' THEN 'Dolor gástrico, náuseas'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Dolor abdominal, diarrea'
        WHEN nombre_generico = 'Prednisona' THEN 'Insomnio, aumento de peso'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Dolor muscular, elevación de enzimas hepáticas'
        ELSE 'Efectos gastrointestinales leves'
    END AS efecto_secundario,
    CASE 
        WHEN nombre_generico IN ('Paracetamol', 'Ibuprofeno', 'Amoxicilina', 'Loratadina', 'Cetirizina', 'Azitromicina', 'Clindamicina', 'Levofloxacino') THEN 'Frecuente'
        ELSE 'Poco frecuente'
    END AS frecuencia,
    TRUE,
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos
WHERE id_empresa = 1;

-- Insertar datos en Presentaciones
INSERT INTO vademecum_presentaciones (
    id_medicamento, 
    formato, 
    concentracion, 
    codigo_barras, 
    estado, 
    fecha_creacion
)
SELECT 
    id_medicamento,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Caja de 20 comprimidos'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Caja de 10 comprimidos'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Caja de 15 cápsulas'
        WHEN nombre_generico = 'Losartán' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Metformina' THEN 'Caja de 60 comprimidos'
        WHEN nombre_generico = 'Sertralina' THEN 'Caja de 28 comprimidos'
        WHEN nombre_generico = 'Omeprazol' THEN 'Caja de 14 cápsulas'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Caja de 10 comprimidos'
        WHEN nombre_generico = 'Amlodipino' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Loratadina' THEN 'Caja de 10 comprimidos'
        WHEN nombre_generico = 'Salbutamol' THEN 'Inhalador de 200 dosis'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Caja de 50 comprimidos'
        WHEN nombre_generico = 'Enalapril' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Caja de 10 cápsulas'
        WHEN nombre_generico = 'Clonazepam' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Azitromicina' THEN 'Caja de 3 comprimidos'
        WHEN nombre_generico = 'Simvastatina' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Caja de 14 cápsulas'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Caja de 20 comprimidos'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Ranitidina' THEN 'Caja de 20 comprimidos'
        WHEN nombre_generico = 'Cetirizina' THEN 'Caja de 10 comprimidos'
        WHEN nombre_generico = 'Metoprolol' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Caja de 14 cápsulas'
        WHEN nombre_generico = 'Tramadol' THEN 'Caja de 10 comprimidos'
        WHEN nombre_generico = 'Citalopram' THEN 'Caja de 28 comprimidos'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Tubo de 20 g'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Vial de 10 ml'
        WHEN nombre_generico = 'Montelukast' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Aciclovir' THEN 'Caja de 25 comprimidos'
        WHEN nombre_generico = 'Alprazolam' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Caja de 100 comprimidos'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Budesonida' THEN 'Inhalador de 120 dosis'
        WHEN nombre_generico = 'Candesartán' THEN 'Caja de 28 comprimidos'
        WHEN nombre_generico = 'Clindamicina' THEN 'Caja de 16 cápsulas'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Caja de 28 comprimidos'
        WHEN nombre_generico = 'Duloxetina' THEN 'Caja de 28 cápsulas'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Furosemida' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Gabapentina' THEN 'Caja de 30 cápsulas'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Caja de 14 cápsulas'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Caja de 7 comprimidos'
        WHEN nombre_generico = 'Lisinopril' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Caja de 30 comprimidos'
        WHEN nombre_generico = 'Naproxeno' THEN 'Caja de 20 comprimidos'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Caja de 14 comprimidos'
        WHEN nombre_generico = 'Prednisona' THEN 'Caja de 20 comprimidos'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Caja de 30 comprimidos'
        ELSE CONCAT('Caja de ', (10 + (id_medicamento % 20)), ' unidades')
    END AS formato,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN '500 mg'
        WHEN nombre_generico = 'Ibuprofeno' THEN '400 mg'
        WHEN nombre_generico = 'Amoxicilina' THEN '500 mg'
        WHEN nombre_generico = 'Losartán' THEN '50 mg'
        WHEN nombre_generico = 'Metformina' THEN '850 mg'
        WHEN nombre_generico = 'Sertralina' THEN '50 mg'
        WHEN nombre_generico = 'Omeprazol' THEN '20 mg'
        WHEN nombre_generico = 'Atorvastatina' THEN '20 mg'
        WHEN nombre_generico = 'Ciprofloxacino' THEN '500 mg'
        WHEN nombre_generico = 'Amlodipino' THEN '5 mg'
        WHEN nombre_generico = 'Loratadina' THEN '10 mg'
        WHEN nombre_generico = 'Salbutamol' THEN '100 mcg'
        WHEN nombre_generico = 'Levotiroxina' THEN '100 mcg'
        WHEN nombre_generico = 'Enalapril' THEN '10 mg'
        WHEN nombre_generico = 'Doxiciclina' THEN '100 mg'
        WHEN nombre_generico = 'Clonazepam' THEN '2 mg'
        WHEN nombre_generico = 'Azitromicina' THEN '500 mg'
        WHEN nombre_generico = 'Simvastatina' THEN '20 mg'
        WHEN nombre_generico = 'Fluoxetina' THEN '20 mg'
        WHEN nombre_generico = 'Diclofenaco' THEN '50 mg'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN '25 mg'
        WHEN nombre_generico = 'Ranitidina' THEN '150 mg'
        WHEN nombre_generico = 'Cetirizina' THEN '10 mg'
        WHEN nombre_generico = 'Metoprolol' THEN '50 mg'
        WHEN nombre_generico = 'Esomeprazol' THEN '40 mg'
        WHEN nombre_generico = 'Tramadol' THEN '50 mg'
        WHEN nombre_generico = 'Citalopram' THEN '20 mg'
        WHEN nombre_generico = 'Clotrimazol' THEN '1%'
        WHEN nombre_generico = 'Insulina Glargina' THEN '100 UI/ml'
        WHEN nombre_generico = 'Montelukast' THEN '10 mg'
        WHEN nombre_generico = 'Aciclovir' THEN '400 mg'
        WHEN nombre_generico = 'Alprazolam' THEN '0.5 mg'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN '100 mg'
        WHEN nombre_generico = 'Bisoprolol' THEN '5 mg'
        WHEN nombre_generico = 'Budesonida' THEN '200 mcg'
        WHEN nombre_generico = 'Candesartán' THEN '16 mg'
        WHEN nombre_generico = 'Clindamicina' THEN '300 mg'
        WHEN nombre_generico = 'Clopidogrel' THEN '75 mg'
        WHEN nombre_generico = 'Duloxetina' THEN '60 mg'
        WHEN nombre_generico = 'Ezetimiba' THEN '10 mg'
        WHEN nombre_generico = 'Furosemida' THEN '40 mg'
        WHEN nombre_generico = 'Gabapentina' THEN '300 mg'
        WHEN nombre_generico = 'Lansoprazol' THEN '30 mg'
        WHEN nombre_generico = 'Levofloxacino' THEN '500 mg'
        WHEN nombre_generico = 'Lisinopril' THEN '10 mg'
        WHEN nombre_generico = 'Mirtazapina' THEN '30 mg'
        WHEN nombre_generico = 'Naproxeno' THEN '500 mg'
        WHEN nombre_generico = 'Pantoprazol' THEN '40 mg'
        WHEN nombre_generico = 'Prednisona' THEN '20 mg'
        WHEN nombre_generico = 'Rosuvastatina' THEN '10 mg'
        ELSE CONCAT((10 + (id_medicamento % 100)), ' mg')
    END AS concentracion,
    CONCAT('COD-', LPAD(id_medicamento::TEXT, 8, '0')) AS codigo_barras,
    TRUE,
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos
WHERE id_empresa = 1;

-- Insertar en Medicamento-Categoría (completando para todos los medicamentos)
INSERT INTO vademecum_medicamento_categoria (id_medicamento, id_categoria)
SELECT 
    m.id_medicamento, 
    CASE 
        WHEN m.nombre_generico IN ('Paracetamol', 'Ibuprofeno', 'Diclofenaco', 'Tramadol', 'Ácido acetilsalicílico', 'Naproxeno', 'Prednisona') THEN 1
        WHEN m.nombre_generico IN ('Amoxicilina', 'Ciprofloxacino', 'Doxiciclina', 'Azitromicina', 'Clindamicina', 'Levofloxacino') THEN 2
        WHEN m.nombre_generico IN ('Losartán', 'Amlodipino', 'Enalapril', 'Hidroclorotiazida', 'Metoprolol', 'Candesartán', 'Bisoprolol', 'Lisinopril', 'Furosemida') THEN 4
        WHEN m.nombre_generico IN ('Metformina', 'Insulina Glargina') THEN 5
        WHEN m.nombre_generico IN ('Sertralina', 'Fluoxetina', 'Clonazepam', 'Citalopram', 'Duloxetina', 'Mirtazapina') THEN 6
        WHEN m.nombre_generico IN ('Loratadina', 'Cetirizina') THEN 7
        WHEN m.nombre_generico IN ('Salbutamol', 'Budesonida', 'Montelukast') THEN 8
        WHEN m.nombre_generico IN ('Omeprazol', 'Esomeprazol', 'Lansoprazol', 'Pantoprazol', 'Ranitidina') THEN 9
        WHEN m.nombre_generico IN ('Atorvastatina', 'Simvastatina', 'Rosuvastatina', 'Ezetimiba') THEN 10
        WHEN m.nombre_generico IN ('Clotrimazol', 'Aciclovir') THEN 11
        WHEN m.nombre_generico IN ('Alprazolam', 'Gabapentina') THEN 12
        WHEN m.nombre_generico IN ('Clopidogrel') THEN 13
        ELSE FLOOR(1 + (RANDOM() * 15))::INTEGER
    END AS id_categoria
FROM vademecum_medicamentos m
WHERE m.id_empresa = 1
ON CONFLICT (id_medicamento, id_categoria) DO NOTHING;

-- Insertar en Farmacocinética
INSERT INTO vademecum_farmacocinetica (
    id_medicamento, 
    absorcion, 
    distribucion, 
    metabolismo, 
    eliminacion, 
    estado, 
    fecha_creacion
)
SELECT 
    id_medicamento,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Absorción rápida en el tracto gastrointestinal, pico plasmático en 0.5-2 horas.'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Absorción rápida, biodisponibilidad del 80-100%.'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Absorción oral del 70-90%, no afectada por alimentos.'
        WHEN nombre_generico = 'Losartán' THEN 'Absorción oral con biodisponibilidad del 33%.'
        WHEN nombre_generico = 'Metformina' THEN 'Absorción en intestino delgado, biodisponibilidad del 50-60%.'
        WHEN nombre_generico = 'Sertralina' THEN 'Absorción lenta, pico plasmático en 4-8 horas.'
        WHEN nombre_generico = 'Omeprazol' THEN 'Absorción en intestino delgado, biodisponibilidad del 30-40%.'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Absorción rápida, biodisponibilidad del 14%.'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Absorción rápida, biodisponibilidad del 70%.'
        WHEN nombre_generico = 'Amlodipino' THEN 'Absorción lenta y completa, biodisponibilidad del 60-80%.'
        WHEN nombre_generico = 'Loratadina' THEN 'Absorción rápida, pico plasmático en 1-2 horas.'
        WHEN nombre_generico = 'Salbutamol' THEN 'Absorción por vía inhalatoria, inicio de acción en 5-15 minutos.'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Absorción en intestino delgado, biodisponibilidad del 50-80%.'
        WHEN nombre_generico = 'Enalapril' THEN 'Absorción oral del 60%, no afectada por alimentos.'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Absorción oral del 90%, afectada por lácteos.'
        WHEN nombre_generico = 'Clonazepam' THEN 'Absorción oral del 90%, pico plasmático en 1-4 horas.'
        WHEN nombre_generico = 'Azitromicina' THEN 'Absorción oral del 37%, afectada por alimentos.'
        WHEN nombre_generico = 'Simvastatina' THEN 'Absorción oral, biodisponibilidad del 5%.'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Absorción oral completa, pico plasmático en 6-8 horas.'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Absorción rápida, biodisponibilidad del 50%.'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Absorción oral del 70%, pico plasmático en 1-5 horas.'
        WHEN nombre_generico = 'Ranitidina' THEN 'Absorción oral del 50%, pico plasmático en 2-3 horas.'
        WHEN nombre_generico = 'Cetirizina' THEN 'Absorción rápida, biodisponibilidad del 70%.'
        WHEN nombre_generico = 'Metoprolol' THEN 'Absorción oral completa, biodisponibilidad del 50%.'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Absorción en intestino delgado, biodisponibilidad del 64-90%.'
        WHEN nombre_generico = 'Tramadol' THEN 'Absorción oral del 70-75%, pico plasmático en 2 horas.'
        WHEN nombre_generico = 'Citalopram' THEN 'Absorción oral completa, pico plasmático en 4 horas.'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Absorción mínima por vía tópica.'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Absorción lenta y constante tras inyección subcutánea.'
        WHEN nombre_generico = 'Montelukast' THEN 'Absorción oral, biodisponibilidad del 64%.'
        WHEN nombre_generico = 'Aciclovir' THEN 'Absorción oral del 15-30%, pico plasmático en 1.5-2 horas.'
        WHEN nombre_generico = 'Alprazolam' THEN 'Absorción oral del 90%, pico plasmático en 1-2 horas.'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Absorción rápida, biodisponibilidad del 50-70%.'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Absorción oral del 90%, biodisponibilidad del 80%.'
        WHEN nombre_generico = 'Budesonida' THEN 'Absorción por inhalación, biodisponibilidad sistémica baja.'
        WHEN nombre_generico = 'Candesartán' THEN 'Absorción oral, biodisponibilidad del 15%.'
        WHEN nombre_generico = 'Clindamicina' THEN 'Absorción oral del 90%, pico plasmático en 1 hora.'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Absorción oral, biodisponibilidad del 50%.'
        WHEN nombre_generico = 'Duloxetina' THEN 'Absorción oral, biodisponibilidad del 50%.'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Absorción oral, biodisponibilidad variable.'
        WHEN nombre_generico = 'Furosemida' THEN 'Absorción oral del 60%, pico plasmático en 1-2 horas.'
        WHEN nombre_generico = 'Gabapentina' THEN 'Absorción oral, biodisponibilidad del 60%.'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Absorción oral, biodisponibilidad del 80%.'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Absorción oral del 99%, pico plasmático en 1-2 horas.'
        WHEN nombre_generico = 'Lisinopril' THEN 'Absorción oral del 25%, no afectada por alimentos.'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Absorción oral, biodisponibilidad del 50%.'
        WHEN nombre_generico = 'Naproxeno' THEN 'Absorción oral completa, pico plasmático en 2-4 horas.'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Absorción oral, biodisponibilidad del 77%.'
        WHEN nombre_generico = 'Prednisona' THEN 'Absorción oral rápida, biodisponibilidad del 70%.'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Absorción oral, biodisponibilidad del 20%.'
        ELSE 'Absorción oral estándar, pico plasmático en 1-3 horas.'
    END AS absorcion,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Distribución amplia, volumen de distribución 0.9 L/kg.'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Unión a proteínas plasmáticas del 99%.'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Distribución en tejidos y fluidos corporales.'
        WHEN nombre_generico = 'Losartán' THEN 'Volumen de distribución de 34 L.'
        WHEN nombre_generico = 'Metformina' THEN 'Distribución principalmente en eritrocitos.'
        WHEN nombre_generico = 'Sertralina' THEN 'Unión a proteínas plasmáticas del 98%.'
        WHEN nombre_generico = 'Omeprazol' THEN 'Unión a proteínas plasmáticas del 97%.'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Unión a proteínas plasmáticas del 98%.'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Distribución amplia en tejidos.'
        WHEN nombre_generico = 'Amlodipino' THEN 'Volumen de distribución de 21 L/kg.'
        WHEN nombre_generico = 'Loratadina' THEN 'Unión a proteínas plasmáticas del 97%.'
        WHEN nombre_generico = 'Salbutamol' THEN 'Distribución pulmonar tras inhalación.'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Unión a proteínas plasmáticas del 99%.'
        WHEN nombre_generico = 'Enalapril' THEN 'Volumen de distribución de 140 L.'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Distribución amplia, unión a proteínas del 80-90%.'
        WHEN nombre_generico = 'Clonazepam' THEN 'Unión a proteínas plasmáticas del 85%.'
        WHEN nombre_generico = 'Azitromicina' THEN 'Distribución extensa en tejidos.'
        WHEN nombre_generico = 'Simvastatina' THEN 'Unión a proteínas plasmáticas del 95%.'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Unión a proteínas plasmáticas del 94%.'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Unión a proteínas plasmáticas del 99%.'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Unión a proteínas plasmáticas del 68%.'
        WHEN nombre_generico = 'Ranitidina' THEN 'Unión a proteínas plasmáticas del 15%.'
        WHEN nombre_generico = 'Cetirizina' THEN 'Unión a proteínas plasmáticas del 93%.'
        WHEN nombre_generico = 'Metoprolol' THEN 'Unión a proteínas plasmáticas del 12%.'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Unión a proteínas plasmáticas del 97%.'
        WHEN nombre_generico = 'Tramadol' THEN 'Unión a proteínas plasmáticas del 20%.'
        WHEN nombre_generico = 'Citalopram' THEN 'Unión a proteínas plasmáticas del 80%.'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Distribución local en piel.'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Distribución limitada tras inyección.'
        WHEN nombre_generico = 'Montelukast' THEN 'Unión a proteínas plasmáticas del 99%.'
        WHEN nombre_generico = 'Aciclovir' THEN 'Unión a proteínas plasmáticas del 15-30%.'
        WHEN nombre_generico = 'Alprazolam' THEN 'Unión a proteínas plasmáticas del 80%.'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Unión a proteínas plasmáticas del 90%.'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Unión a proteínas plasmáticas del 30%.'
        WHEN nombre_generico = 'Budesonida' THEN 'Distribución pulmonar tras inhalación.'
        WHEN nombre_generico = 'Candesartán' THEN 'Volumen de distribución de 0.13 L/kg.'
        WHEN nombre_generico = 'Clindamicina' THEN 'Distribución amplia, unión a proteínas del 94%.'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Unión a proteínas plasmáticas del 98%.'
        WHEN nombre_generico = 'Duloxetina' THEN 'Unión a proteínas plasmáticas del 90%.'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Unión a proteínas plasmáticas del 99%.'
        WHEN nombre_generico = 'Furosemida' THEN 'Unión a proteínas plasmáticas del 95%.'
        WHEN nombre_generico = 'Gabapentina' THEN 'Unión a proteínas plasmáticas mínima.'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Unión a proteínas plasmáticas del 97%.'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Unión a proteínas plasmáticas del 24-38%.'
        WHEN nombre_generico = 'Lisinopril' THEN 'No se une a proteínas plasmáticas.'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Unión a proteínas plasmáticas del 85%.'
        WHEN nombre_generico = 'Naproxeno' THEN 'Unión a proteínas plasmáticas del 99%.'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Unión a proteínas plasmáticas del 98%.'
        WHEN nombre_generico = 'Prednisona' THEN 'Unión a proteínas plasmáticas del 70%.'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Unión a proteínas plasmáticas del 88%.'
        ELSE 'Distribución estándar en tejidos corporales.'
    END AS distribucion,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Metabolismo hepático por glucuronidación y sulfatación.'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Metabolismo hepático por CYP2C9.'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Mínimo metabolismo, excreción renal.'
        WHEN nombre_generico = 'Losartán' THEN 'Metabolismo hepático por CYP2C9 y CYP3A4.'
        WHEN nombre_generico = 'Metformina' THEN 'No se metaboliza, excreción renal.'
        WHEN nombre_generico = 'Sertralina' THEN 'Metabolismo hepático por CYP2D6 y CYP3A4.'
        WHEN nombre_generico = 'Omeprazol' THEN 'Metabolismo hepático por CYP2C19.'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Metabolismo hepático por CYP3A4.'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Metabolismo hepático parcial.'
        WHEN nombre_generico = 'Amlodipino' THEN 'Metabolismo hepático por CYP3A4.'
        WHEN nombre_generico = 'Loratadina' THEN 'Metabolismo hepático por CYP3A4 y CYP2D6.'
        WHEN nombre_generico = 'Salbutamol' THEN 'Metabolismo hepático parcial.'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Metabolismo hepático y renal.'
        WHEN nombre_generico = 'Enalapril' THEN 'Hidrólisis a enalaprilato en el hígado.'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Mínimo metabolismo, excreción biliar.'
        WHEN nombre_generico = 'Clonazepam' THEN 'Metabolismo hepático por CYP3A4.'
        WHEN nombre_generico = 'Azitromicina' THEN 'Mínimo metabolismo, excreción biliar.'
        WHEN nombre_generico = 'Simvastatina' THEN 'Metabolismo hepático por CYP3A4.'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Metabolismo hepático por CYP2D6.'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Metabolismo hepático por CYP2C9.'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'No se metaboliza, excreción renal.'
        WHEN nombre_generico = 'Ranitidina' THEN 'Metabolismo hepático parcial.'
        WHEN nombre_generico = 'Cetirizina' THEN 'Mínimo metabolismo, excreción renal.'
        WHEN nombre_generico = 'Metoprolol' THEN 'Metabolismo hepático por CYP2D6.'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Metabolismo hepático por CYP2C19.'
        WHEN nombre_generico = 'Tramadol' THEN 'Metabolismo hepático por CYP2D6 y CYP3A4.'
        WHEN nombre_generico = 'Citalopram' THEN 'Metabolismo hepático por CYP2C19 y CYP3A4.'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Metabolismo local mínimo.'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Metabolismo en tejidos periféricos.'
        WHEN nombre_generico = 'Montelukast' THEN 'Metabolismo hepático por CYP3A4 y CYP2C8.'
        WHEN nombre_generico = 'Aciclovir' THEN 'Metabolismo hepático parcial.'
        WHEN nombre_generico = 'Alprazolam' THEN 'Metabolismo hepático por CYP3A4.'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Hidrólisis a ácido salicílico en hígado.'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Metabolismo hepático por CYP3A4.'
        WHEN nombre_generico = 'Budesonida' THEN 'Metabolismo hepático por CYP3A4.'
        WHEN nombre_generico = 'Candesartán' THEN 'Metabolismo hepático por CYP2C9.'
        WHEN nombre_generico = 'Clindamicina' THEN 'Metabolismo hepático parcial.'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Metabolismo hepático por CYP2C19.'
        WHEN nombre_generico = 'Duloxetina' THEN 'Metabolismo hepático por CYP1A2 y CYP2D6.'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Metabolismo hepático e intestinal.'
        WHEN nombre_generico = 'Furosemida' THEN 'Mínimo metabolismo, excreción renal.'
        WHEN nombre_generico = 'Gabapentina' THEN 'No se metaboliza, excreción renal.'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Metabolismo hepático por CYP2C19.'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Mínimo metabolismo, excreción renal.'
        WHEN nombre_generico = 'Lisinopril' THEN 'No se metaboliza, excreción renal.'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Metabolismo hepático por CYP2D6 y CYP3A4.'
        WHEN nombre_generico = 'Naproxeno' THEN 'Metabolismo hepático por CYP2C9.'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Metabolismo hepático por CYP2C19.'
        WHEN nombre_generico = 'Prednisona' THEN 'Metabolismo hepático a prednisolona.'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Metabolismo hepático por CYP2C9.'
        ELSE 'Metabolismo hepático estándar.'
    END AS metabolismo,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Eliminación renal, vida media de 2-3 horas.'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Eliminación renal, vida media de 2-4 horas.'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Eliminación renal, vida media de 1-1.5 horas.'
        WHEN nombre_generico = 'Losartán' THEN 'Eliminación renal y biliar, vida media de 6-9 horas.'
        WHEN nombre_generico = 'Metformina' THEN 'Eliminación renal, vida media de 6 horas.'
        WHEN nombre_generico = 'Sertralina' THEN 'Eliminación renal, vida media de 26 horas.'
        WHEN nombre_generico = 'Omeprazol' THEN 'Eliminación renal, vida media de 0.5-1 hora.'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Eliminación biliar, vida media de 14 horas.'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Eliminación renal, vida media de 4-7 horas.'
        WHEN nombre_generico = 'Amlodipino' THEN 'Eliminación renal, vida media de 30-50 horas.'
        WHEN nombre_generico = 'Loratadina' THEN 'Eliminación renal y fecal, vida media de 8-15 horas.'
        WHEN nombre_generico = 'Salbutamol' THEN 'Eliminación renal, vida media de 3-6 horas.'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Eliminación renal y fecal, vida media de 6-7 días.'
        WHEN nombre_generico = 'Enalapril' THEN 'Eliminación renal, vida media de 11 horas.'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Eliminación biliar y renal, vida media de 16-22 horas.'
        WHEN nombre_generico = 'Clonazepam' THEN 'Eliminación renal, vida media de 20-40 horas.'
        WHEN nombre_generico = 'Azitromicina' THEN 'Eliminación biliar, vida media de 68 horas.'
        WHEN nombre_generico = 'Simvastatina' THEN 'Eliminación biliar, vida media de 3 horas.'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Eliminación renal, vida media de 1-4 días.'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Eliminación renal y biliar, vida media de 1-2 horas.'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Eliminación renal, vida media de 5-15 horas.'
        WHEN nombre_generico = 'Ranitidina' THEN 'Eliminación renal, vida media de 2-3 horas.'
        WHEN nombre_generico = 'Cetirizina' THEN 'Eliminación renal, vida media de 8-9 horas.'
        WHEN nombre_generico = 'Metoprolol' THEN 'Eliminación renal, vida media de 3-7 horas.'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Eliminación renal, vida media de 1-1.5 horas.'
        WHEN nombre_generico = 'Tramadol' THEN 'Eliminación renal, vida media de 6-7 horas.'
        WHEN nombre_generico = 'Citalopram' THEN 'Eliminación renal, vida media de 35 horas.'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Eliminación local, mínima absorción sistémica.'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Eliminación metabólica, duración de 24 horas.'
        WHEN nombre_generico = 'Montelukast' THEN 'Eliminación biliar, vida media de 2.7-5.5 horas.'
        WHEN nombre_generico = 'Aciclovir' THEN 'Eliminación renal, vida media de 2.5-3.3 horas.'
        WHEN nombre_generico = 'Alprazolam' THEN 'Eliminación renal, vida media de 6-27 horas.'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Eliminación renal, vida media de 2-3 horas.'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Eliminación renal y biliar, vida media de 10-12 horas.'
        WHEN nombre_generico = 'Budesonida' THEN 'Eliminación biliar, vida media de 2-3 horas.'
        WHEN nombre_generico = 'Candesartán' THEN 'Eliminación renal y biliar, vida media de 9 horas.'
        WHEN nombre_generico = 'Clindamicina' THEN 'Eliminación biliar y renal, vida media de 2-3 horas.'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Eliminación renal y biliar, vida media de 8 horas.'
        WHEN nombre_generico = 'Duloxetina' THEN 'Eliminación renal, vida media de 12 horas.'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Eliminación biliar, vida media de 22 horas.'
        WHEN nombre_generico = 'Furosemida' THEN 'Eliminación renal, vida media de 1-2 horas.'
        WHEN nombre_generico = 'Gabapentina' THEN 'Eliminación renal, vida media de 5-7 horas.'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Eliminación renal, vida media de 1-2 horas.'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Eliminación renal, vida media de 6-8 horas.'
        WHEN nombre_generico = 'Lisinopril' THEN 'Eliminación renal, vida media de 12 horas.'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Eliminación renal y fecal, vida media de 20-40 horas.'
        WHEN nombre_generico = 'Naproxeno' THEN 'Eliminación renal, vida media de 12-17 horas.'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Eliminación renal, vida media de 1 hora.'
        WHEN nombre_generico = 'Prednisona' THEN 'Eliminación renal, vida media de 3-4 horas.'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Eliminación biliar, vida media de 19 horas.'
        ELSE 'Eliminación renal estándar, vida media de 2-6 horas.'
    END AS eliminacion,
    TRUE,
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos
WHERE id_empresa = 1;

-- Insertar en Protocolos Clínicos
INSERT INTO vademecum_protocolos_clinicos (
    id_medicamento, 
    protocolo_clinico, 
    fecha_creacion,
	id_empresa
)
SELECT 
    id_medicamento,
    CASE 
        WHEN nombre_generico = 'Paracetamol' THEN 'Utilizar como primera línea para dolor leve a moderado y fiebre. Monitorizar función hepática en uso prolongado.'
        WHEN nombre_generico = 'Ibuprofeno' THEN 'Indicado para dolor e inflamación. Evitar en pacientes con úlcera péptica o insuficiencia renal.'
        WHEN nombre_generico = 'Amoxicilina' THEN 'Administrar para infecciones bacterianas sensibles. Completar ciclo completo para evitar resistencia.'
        WHEN nombre_generico = 'Losartán' THEN 'Control de hipertensión. Monitorizar potasio y función renal.'
        WHEN nombre_generico = 'Metformina' THEN 'Primera línea para diabetes tipo 2. Ajustar dosis en insuficiencia renal.'
        WHEN nombre_generico = 'Sertralina' THEN 'Indicado para depresión y ansiedad. Iniciar con dosis baja y ajustar gradualmente.'
        WHEN nombre_generico = 'Omeprazol' THEN 'Tratamiento de reflujo gastroesofágico. Tomar antes del desayuno.'
        WHEN nombre_generico = 'Atorvastatina' THEN 'Reducción de colesterol LDL. Monitorizar enzimas hepáticas.'
        WHEN nombre_generico = 'Ciprofloxacino' THEN 'Infecciones urinarias y respiratorias. Evitar en menores de 18 años.'
        WHEN nombre_generico = 'Amlodipino' THEN 'Hipertensión y angina. Monitorizar edema periférico.'
        WHEN nombre_generico = 'Loratadina' THEN 'Alergias estacionales. No sedante en dosis recomendadas.'
        WHEN nombre_generico = 'Salbutamol' THEN 'Tratamiento agudo de broncoespasmo. Usar según necesidad.'
        WHEN nombre_generico = 'Levotiroxina' THEN 'Hipotiroidismo. Ajustar dosis según TSH.'
        WHEN nombre_generico = 'Enalapril' THEN 'Hipertensión e insuficiencia cardíaca. Monitorizar tos seca.'
        WHEN nombre_generico = 'Doxiciclina' THEN 'Infecciones bacterianas y acné. Evitar exposición solar.'
        WHEN nombre_generico = 'Clonazepam' THEN 'Convulsiones y ansiedad. Uso a corto plazo, evitar retiro abrupto.'
        WHEN nombre_generico = 'Azitromicina' THEN 'Infecciones respiratorias. Administrar en ciclos cortos.'
        WHEN nombre_generico = 'Simvastatina' THEN 'Hiperlipidemia. Tomar por la noche, monitorizar enzimas hepáticas.'
        WHEN nombre_generico = 'Fluoxetina' THEN 'Depresión y TOC. Iniciar con dosis baja.'
        WHEN nombre_generico = 'Diclofenaco' THEN 'Dolor e inflamación articular. Tomar con alimentos.'
        WHEN nombre_generico = 'Hidroclorotiazida' THEN 'Hipertensión y edema. Monitorizar electrolitos.'
        WHEN nombre_generico = 'Ranitidina' THEN 'Úlceras gástricas. Evitar en insuficiencia renal severa.'
        WHEN nombre_generico = 'Cetirizina' THEN 'Rinitis alérgica. Puede causar somnolencia.'
        WHEN nombre_generico = 'Metoprolol' THEN 'Hipertensión y arritmias. Monitorizar frecuencia cardíaca.'
        WHEN nombre_generico = 'Esomeprazol' THEN 'Reflujo gastroesofágico. Uso prolongado requiere monitoreo.'
        WHEN nombre_generico = 'Tramadol' THEN 'Dolor moderado a severo. Evitar en pacientes con riesgo de convulsiones.'
        WHEN nombre_generico = 'Citalopram' THEN 'Depresión mayor. Monitorizar riesgo de suicidio.'
        WHEN nombre_generico = 'Clotrimazol' THEN 'Infecciones fúngicas cutáneas. Aplicar en área limpia.'
        WHEN nombre_generico = 'Insulina Glargina' THEN 'Diabetes tipo 1 y 2. Ajustar según glucosa.'
        WHEN nombre_generico = 'Montelukast' THEN 'Asma y rinitis alérgica. Tomar por la noche.'
        WHEN nombre_generico = 'Aciclovir' THEN 'Infecciones por herpes. Iniciar al primer signo de infección.'
        WHEN nombre_generico = 'Alprazolam' THEN 'Ansiedad y pánico. Uso a corto plazo.'
        WHEN nombre_generico = 'Ácido acetilsalicílico' THEN 'Prevención cardiovascular. Monitorizar sangrado gastrointestinal.'
        WHEN nombre_generico = 'Bisoprolol' THEN 'Hipertensión e insuficiencia cardíaca. Monitorizar bradicardia.'
        WHEN nombre_generico = 'Budesonida' THEN 'Asma y colitis. Usar según protocolo de inhalación.'
        WHEN nombre_generico = 'Candesartán' THEN 'Hipertensión. Monitorizar función renal.'
        WHEN nombre_generico = 'Clindamicina' THEN 'Infecciones anaerobias. Monitorizar diarrea.'
        WHEN nombre_generico = 'Clopidogrel' THEN 'Prevención de trombosis. Monitorizar sangrado.'
        WHEN nombre_generico = 'Duloxetina' THEN 'Depresión y dolor neuropático. Monitorizar función hepática.'
        WHEN nombre_generico = 'Ezetimiba' THEN 'Hiperlipidemia. Combinar con estatinas si necesario.'
        WHEN nombre_generico = 'Furosemida' THEN 'Edema e hipertensión. Monitorizar electrolitos.'
        WHEN nombre_generico = 'Gabapentina' THEN 'Dolor neuropático y convulsiones. Ajustar en insuficiencia renal.'
        WHEN nombre_generico = 'Lansoprazol' THEN 'Úlceras y reflujo. Tomar antes del desayuno.'
        WHEN nombre_generico = 'Levofloxacino' THEN 'Infecciones respiratorias. Evitar en menores de 18 años.'
        WHEN nombre_generico = 'Lisinopril' THEN 'Hipertensión e insuficiencia cardíaca. Monitorizar función renal.'
        WHEN nombre_generico = 'Mirtazapina' THEN 'Depresión mayor. Puede causar aumento de peso.'
        WHEN nombre_generico = 'Naproxeno' THEN 'Dolor e inflamación. Tomar con alimentos.'
        WHEN nombre_generico = 'Pantoprazol' THEN 'Reflujo gastroesofágico. Uso prolongado requiere monitoreo.'
        WHEN nombre_generico = 'Prednisona' THEN 'Enfermedades inflamatorias. Reducir dosis gradualmente.'
        WHEN nombre_generico = 'Rosuvastatina' THEN 'Hiperlipidemia. Monitorizar enzimas hepáticas.'
        ELSE 'Seguir protocolo clínico según indicación médica.'
    END AS protocolo_clinico,
    CURRENT_TIMESTAMP,1
FROM vademecum_medicamentos
WHERE id_empresa = 1;

-- Insertar en Medicamento-Protocolo (relaciona medicamentos con sus protocolos clínicos)
INSERT INTO vademecum_medicamento_protocolo (
    id_medicamento, 
    id_protocolo, 
    estado, 
    fecha_creacion
)
SELECT 
    m.id_medicamento,
    p.id_protocolo,
    TRUE,
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos m
JOIN vademecum_protocolos_clinicos p ON m.id_medicamento = p.id_medicamento
WHERE m.id_empresa = 1;

-- Insertar imágenes de productos para medicamentos conocidos
INSERT INTO imagenes (
    url, 
    descripcion, 
    id_medicamento, 
    estado, 
    fecha_creacion
)
SELECT 
    CASE 
        WHEN m.nombre_generico = 'Paracetamol' THEN 'https://example.com/products/paracetamol_500mg.png'
        WHEN m.nombre_generico = 'Ibuprofeno' THEN 'https://example.com/products/ibuprofeno_400mg.png'
        WHEN m.nombre_generico = 'Amoxicilina' THEN 'https://example.com/products/amoxicilina_500mg.png'
        WHEN m.nombre_generico = 'Losartán' THEN 'https://example.com/products/losartan_50mg.png'
        WHEN m.nombre_generico = 'Metformina' THEN 'https://example.com/products/metformina_850mg.png'
        WHEN m.nombre_generico = 'Sertralina' THEN 'https://example.com/products/sertralina_50mg.png'
        WHEN m.nombre_generico = 'Omeprazol' THEN 'https://example.com/products/omeprazol_20mg.png'
        WHEN m.nombre_generico = 'Atorvastatina' THEN 'https://example.com/products/atorvastatina_20mg.png'
        WHEN m.nombre_generico = 'Ciprofloxacino' THEN 'https://example.com/products/ciprofloxacino_500mg.png'
        WHEN m.nombre_generico = 'Amlodipino' THEN 'https://example.com/products/amlodipino_5mg.png'
        WHEN m.nombre_generico = 'Loratadina' THEN 'https://example.com/products/loratadina_10mg.png'
        WHEN m.nombre_generico = 'Salbutamol' THEN 'https://example.com/products/salbutamol_100mcg.png'
        WHEN m.nombre_generico = 'Levotiroxina' THEN 'https://example.com/products/levotiroxina_100mcg.png'
        WHEN m.nombre_generico = 'Enalapril' THEN 'https://example.com/products/enalapril_10mg.png'
        WHEN m.nombre_generico = 'Doxiciclina' THEN 'https://example.com/products/doxiciclina_100mg.png'
        WHEN m.nombre_generico = 'Clonazepam' THEN 'https://example.com/products/clonazepam_2mg.png'
        WHEN m.nombre_generico = 'Azitromicina' THEN 'https://example.com/products/azitromicina_500mg.png'
        WHEN m.nombre_generico = 'Simvastatina' THEN 'https://example.com/products/simvastatina_20mg.png'
        WHEN m.nombre_generico = 'Fluoxetina' THEN 'https://example.com/products/fluoxetina_20mg.png'
        WHEN m.nombre_generico = 'Diclofenaco' THEN 'https://example.com/products/diclofenaco_50mg.png'
        WHEN m.nombre_generico = 'Hidroclorotiazida' THEN 'https://example.com/products/hidroclorotiazida_25mg.png'
        WHEN m.nombre_generico = 'Ranitidina' THEN 'https://example.com/products/ranitidina_150mg.png'
        WHEN m.nombre_generico = 'Cetirizina' THEN 'https://example.com/products/cetirizina_10mg.png'
        WHEN m.nombre_generico = 'Metoprolol' THEN 'https://example.com/products/metoprolol_50mg.png'
        WHEN m.nombre_generico = 'Esomeprazol' THEN 'https://example.com/products/esomeprazol_40mg.png'
        WHEN m.nombre_generico = 'Tramadol' THEN 'https://example.com/products/tramadol_50mg.png'
        WHEN m.nombre_generico = 'Citalopram' THEN 'https://example.com/products/citalopram_20mg.png'
        WHEN m.nombre_generico = 'Clotrimazol' THEN 'https://example.com/products/clotrimazol_1percent.png'
        WHEN m.nombre_generico = 'Insulina Glargina' THEN 'https://example.com/products/insulina_glargina_100ui.png'
        WHEN m.nombre_generico = 'Montelukast' THEN 'https://example.com/products/montelukast_10mg.png'
        WHEN m.nombre_generico = 'Aciclovir' THEN 'https://example.com/products/aciclovir_400mg.png'
        WHEN m.nombre_generico = 'Alprazolam' THEN 'https://example.com/products/alprazolam_0.5mg.png'
        WHEN m.nombre_generico = 'Ácido acetilsalicílico' THEN 'https://example.com/products/aspirina_100mg.png'
        WHEN m.nombre_generico = 'Bisoprolol' THEN 'https://example.com/products/bisoprolol_5mg.png'
        WHEN m.nombre_generico = 'Budesonida' THEN 'https://example.com/products/budesonida_200mcg.png'
        WHEN m.nombre_generico = 'Candesartán' THEN 'https://example.com/products/candesartan_16mg.png'
        WHEN m.nombre_generico = 'Clindamicina' THEN 'https://example.com/products/clindamicina_300mg.png'
        WHEN m.nombre_generico = 'Clopidogrel' THEN 'https://example.com/products/clopidogrel_75mg.png'
        WHEN m.nombre_generico = 'Duloxetina' THEN 'https://example.com/products/duloxetina_60mg.png'
        WHEN m.nombre_generico = 'Ezetimiba' THEN 'https://example.com/products/ezetimiba_10mg.png'
        WHEN m.nombre_generico = 'Furosemida' THEN 'https://example.com/products/furosemida_40mg.png'
        WHEN m.nombre_generico = 'Gabapentina' THEN 'https://example.com/products/gabapentina_300mg.png'
        WHEN m.nombre_generico = 'Lansoprazol' THEN 'https://example.com/products/lansoprazol_30mg.png'
        WHEN m.nombre_generico = 'Levofloxacino' THEN 'https://example.com/products/levofloxacino_500mg.png'
        WHEN m.nombre_generico = 'Lisinopril' THEN 'https://example.com/products/lisinopril_10mg.png'
        WHEN m.nombre_generico = 'Mirtazapina' THEN 'https://example.com/products/mirtazapina_30mg.png'
        WHEN m.nombre_generico = 'Naproxeno' THEN 'https://example.com/products/naproxeno_500mg.png'
        WHEN m.nombre_generico = 'Pantoprazol' THEN 'https://example.com/products/pantoprazol_40mg.png'
        WHEN m.nombre_generico = 'Prednisona' THEN 'https://example.com/products/prednisona_20mg.png'
        WHEN m.nombre_generico = 'Rosuvastatina' THEN 'https://example.com/products/rosuvastatina_10mg.png'
    END AS url,
    CASE 
        WHEN m.nombre_generico = 'Paracetamol' THEN 'Caja de Paracetamol 500 mg'
        WHEN m.nombre_generico = 'Ibuprofeno' THEN 'Caja de Ibuprofeno 400 mg'
        WHEN m.nombre_generico = 'Amoxicilina' THEN 'Caja de Amoxicilina 500 mg'
        WHEN m.nombre_generico = 'Losartán' THEN 'Caja de Losartán 50 mg'
        WHEN m.nombre_generico = 'Metformina' THEN 'Caja de Metformina 850 mg'
        WHEN m.nombre_generico = 'Sertralina' THEN 'Caja de Sertralina 50 mg'
        WHEN m.nombre_generico = 'Omeprazol' THEN 'Caja de Omeprazol 20 mg'
        WHEN m.nombre_generico = 'Atorvastatina' THEN 'Caja de Atorvastatina 20 mg'
        WHEN m.nombre_generico = 'Ciprofloxacino' THEN 'Caja de Ciprofloxacino 500 mg'
        WHEN m.nombre_generico = 'Amlodipino' THEN 'Caja de Amlodipino 5 mg'
        WHEN m.nombre_generico = 'Loratadina' THEN 'Caja de Loratadina 10 mg'
        WHEN m.nombre_generico = 'Salbutamol' THEN 'Inhalador de Salbutamol 100 mcg'
        WHEN m.nombre_generico = 'Levotiroxina' THEN 'Caja de Levotiroxina 100 mcg'
        WHEN m.nombre_generico = 'Enalapril' THEN 'Caja de Enalapril 10 mg'
        WHEN m.nombre_generico = 'Doxiciclina' THEN 'Caja de Doxiciclina 100 mg'
        WHEN m.nombre_generico = 'Clonazepam' THEN 'Caja de Clonazepam 2 mg'
        WHEN m.nombre_generico = 'Azitromicina' THEN 'Caja de Azitromicina 500 mg'
        WHEN m.nombre_generico = 'Simvastatina' THEN 'Caja de Simvastatina 20 mg'
        WHEN m.nombre_generico = 'Fluoxetina' THEN 'Caja de Fluoxetina 20 mg'
        WHEN m.nombre_generico = 'Diclofenaco' THEN 'Caja de Diclofenaco 50 mg'
        WHEN m.nombre_generico = 'Hidroclorotiazida' THEN 'Caja de Hidroclorotiazida 25 mg'
        WHEN m.nombre_generico = 'Ranitidina' THEN 'Caja de Ranitidina 150 mg'
        WHEN m.nombre_generico = 'Cetirizina' THEN 'Caja de Cetirizina 10 mg'
        WHEN m.nombre_generico = 'Metoprolol' THEN 'Caja de Metoprolol 50 mg'
        WHEN m.nombre_generico = 'Esomeprazol' THEN 'Caja de Esomeprazol 40 mg'
        WHEN m.nombre_generico = 'Tramadol' THEN 'Caja de Tramadol 50 mg'
        WHEN m.nombre_generico = 'Citalopram' THEN 'Caja de Citalopram 20 mg'
        WHEN m.nombre_generico = 'Clotrimazol' THEN 'Tubo de Clotrimazol 1%'
        WHEN m.nombre_generico = 'Insulina Glargina' THEN 'Vial de Insulina Glargina 100 UI/ml'
        WHEN m.nombre_generico = 'Montelukast' THEN 'Caja de Montelukast 10 mg'
        WHEN m.nombre_generico = 'Aciclovir' THEN 'Caja de Aciclovir 400 mg'
        WHEN m.nombre_generico = 'Alprazolam' THEN 'Caja de Alprazolam 0.5 mg'
        WHEN m.nombre_generico = 'Ácido acetilsalicílico' THEN 'Caja de Aspirina 100 mg'
        WHEN m.nombre_generico = 'Bisoprolol' THEN 'Caja de Bisoprolol 5 mg'
        WHEN m.nombre_generico = 'Budesonida' THEN 'Inhalador de Budesonida 200 mcg'
        WHEN m.nombre_generico = 'Candesartán' THEN 'Caja de Candesartán 16 mg'
        WHEN m.nombre_generico = 'Clindamicina' THEN 'Caja de Clindamicina 300 mg'
        WHEN m.nombre_generico = 'Clopidogrel' THEN 'Caja de Clopidogrel 75 mg'
        WHEN m.nombre_generico = 'Duloxetina' THEN 'Caja de Duloxetina 60 mg'
        WHEN m.nombre_generico = 'Ezetimiba' THEN 'Caja de Ezetimiba 10 mg'
        WHEN m.nombre_generico = 'Furosemida' THEN 'Caja de Furosemida 40 mg'
        WHEN m.nombre_generico = 'Gabapentina' THEN 'Caja de Gabapentina 300 mg'
        WHEN m.nombre_generico = 'Lansoprazol' THEN 'Caja de Lansoprazol 30 mg'
        WHEN m.nombre_generico = 'Levofloxacino' THEN 'Caja de Levofloxacino 500 mg'
        WHEN m.nombre_generico = 'Lisinopril' THEN 'Caja de Lisinopril 10 mg'
        WHEN m.nombre_generico = 'Mirtazapina' THEN 'Caja de Mirtazapina 30 mg'
        WHEN m.nombre_generico = 'Naproxeno' THEN 'Caja de Naproxeno 500 mg'
        WHEN m.nombre_generico = 'Pantoprazol' THEN 'Caja de Pantoprazol 40 mg'
        WHEN m.nombre_generico = 'Prednisona' THEN 'Caja de Prednisona 20 mg'
        WHEN m.nombre_generico = 'Rosuvastatina' THEN 'Caja de Rosuvastatina 10 mg'
    END AS descripcion,
    m.id_medicamento,
    TRUE,
    CURRENT_TIMESTAMP
FROM vademecum_medicamentos m
WHERE m.id_empresa = 1
AND m.nombre_generico IN (
    'Paracetamol', 'Ibuprofeno', 'Amoxicilina', 'Losartán', 'Metformina', 
    'Sertralina', 'Omeprazol', 'Atorvastatina', 'Ciprofloxacino', 'Amlodipino', 
    'Loratadina', 'Salbutamol', 'Levotiroxina', 'Enalapril', 'Doxiciclina', 
    'Clonazepam', 'Azitromicina', 'Simvastatina', 'Fluoxetina', 'Diclofenaco', 
    'Hidroclorotiazida', 'Ranitidina', 'Cetirizina', 'Metoprolol', 'Esomeprazol', 
    'Tramadol', 'Citalopram', 'Clotrimazol', 'Insulina Glargina', 'Montelukast', 
    'Aciclovir', 'Alprazolam', 'Ácido acetilsalicílico', 'Bisoprolol', 'Budesonida', 
    'Candesartán', 'Clindamicina', 'Clopidogrel', 'Duloxetina', 'Ezetimiba', 
    'Furosemida', 'Gabapentina', 'Lansoprazol', 'Levofloxacino', 'Lisinopril', 
    'Mirtazapina', 'Naproxeno', 'Pantoprazol', 'Prednisona', 'Rosuvastatina'
);