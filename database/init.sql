
-- =========================
-- TABLAS GEOGRÁFICAS
-- =========================
-- Crear tabla de regiones
CREATE TABLE regiones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    abreviatura VARCHAR(10),
    capital VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE
);

-- Crear tabla de provincias
CREATE TABLE provincias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10),
    id_region INTEGER REFERENCES regiones(id),
    estado BOOLEAN DEFAULT TRUE
);

-- Crear tabla de comunas
CREATE TABLE comunas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10),
    id_provincia INTEGER REFERENCES provincias(id),
    estado BOOLEAN DEFAULT TRUE
);

-- Script para crear la tabla nacionalidad en PostgreSQL
CREATE TABLE nacionalidad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    gentilicio_nac VARCHAR(100) NOT NULL,
    iso_nac CHAR(3) NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);
-- Script para crear la tabla nacionalidad en PostgreSQL
CREATE TABLE estado_civil (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

-- 🟡 Tabla: profesiones
CREATE TABLE profesion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    estado BOOLEAN DEFAULT TRUE
);

-- 🟡 Tabla: niveles_educacionales
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
    id_direccion INT REFERENCES direccion(id) ON DELETE SET NULL,
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

-- 🧑 Tabla: personas
CREATE TABLE personas (
    id SERIAL PRIMARY KEY,
    run_rut VARCHAR(12) UNIQUE,
    pasaporte VARCHAR(20),
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    fecha_nacimiento DATE,
    sexo CHAR(1) CHECK (sexo IN ('M', 'F', 'O')),
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20),
    telefono_secundario VARCHAR(20),
    id_direccion INTEGER REFERENCES direccion(id),
    id_estado_civil INTEGER REFERENCES estado_civil(id),
    id_nacionalidad INTEGER REFERENCES nacionalidad(id),
    id_profesion INTEGER REFERENCES profesion(id),
    id_nivel_educacional INTEGER REFERENCES niveles_educacionales(id),
    estado BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- 🖼️ Tabla: fotos_personas
CREATE TABLE fotos_personas (
    id SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES personas(id) ON DELETE CASCADE,
    url_foto VARCHAR(250) NOT NULL,
    es_principal BOOLEAN DEFAULT FALSE,
    estado BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    nombre_mostrar VARCHAR(200) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    duracion INT DEFAULT 20, -- Minutos de sesión u otro uso
    pagina_inicio VARCHAR(255) NOT NULL,
    id_dashboard INT REFERENCES dashboard_inicial(id) ON DELETE SET NULL,
    id_persona INT REFERENCES personas(id) ON DELETE SET NULL,
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


CREATE OR REPLACE VIEW vista_cumpleanios_mes AS
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
FROM
    personas
WHERE
    EXTRACT(MONTH FROM fecha_nacimiento) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND estado = TRUE;

-- =========================
-- =========================
-- (INSERTS)
-- =========================
-- =========================


-- Insert masivo de nacionalidades
INSERT INTO nacionalidad (nombre, gentilicio_nac, iso_nac) VALUES
('Afganistán', 'AFGANA', 'AFG'),
('Albania', 'ALBANESA', 'ALB'),
('Alemania', 'ALEMANA', 'DEU'),
('Andorra', 'ANDORRANA', 'AND'),
('Angola', 'ANGOLEÑA', 'AGO'),
('Antigua y Barbuda', 'ANTIGUANA', 'ATG'),
('Arabia Saudita', 'SAUDÍ', 'SAU'),
('Argelia', 'ARGELINA', 'DZA'),
('Argentina', 'ARGENTINA', 'ARG'),
('Armenia', 'ARMENIA', 'ARM'),
('Aruba', 'ARUBEÑA', 'ABW'),
('Australia', 'AUSTRALIANA', 'AUS'),
('Austria', 'AUSTRIACA', 'AUT'),
('Azerbaiyán', 'AZERBAIYANA', 'AZE'),
('Bahamas', 'BAHAMEÑA', 'BHS'),
('Bangladés', 'BANGLADESÍ', 'BGD'),
('Barbados', 'BARBADENSE', 'BRB'),
('Baréin', 'BAREINÍ', 'BHR'),
('Bélgica', 'BELGA', 'BEL'),
('Belice', 'BELICEÑA', 'BLZ'),
('Benín', 'BENINÉSA', 'BEN'),
('Bielorrusia', 'BIELORRUSA', 'BLR'),
('Birmania', 'BIRMANA', 'MMR'),
('Bolivia', 'BOLIVIANA', 'BOL'),
('Bosnia y Herzegovina', 'BOSNIA', 'BIH'),
('Botsuana', 'BOTSUANA', 'BWA'),
('Brasil', 'BRASILEÑA', 'BRA'),
('Brunéi', 'BRUNEANA', 'BRN'),
('Bulgaria', 'BÚLGARA', 'BGR'),
('Burkina Faso', 'BURKINÉS', 'BFA'),
('Burundi', 'BURUNDÉSA', 'BDI'),
('Bután', 'BUTANÉSA', 'BTN'),
('Cabo Verde', 'CABOVERDIANA', 'CPV'),
('Camboya', 'CAMBOYANA', 'KHM'),
('Camerún', 'CAMERUNESA', 'CMR'),
('Canadá', 'CANADIENSE', 'CAN'),
('Catar', 'CATARÍ', 'QAT'),
('Chad', 'CHADIANA', 'TCD'),
('Chile', 'CHILENA', 'CHL'),
('China', 'CHINA', 'CHN'),
('Chipre', 'CHIPRIOTA', 'CYP'),
('Ciudad del Vaticano', 'VATICANA', 'VAT'),
('Colombia', 'COLOMBIANA', 'COL'),
('Comoras', 'COMORENSE', 'COM'),
('Corea del Norte', 'NORCOREANA', 'PRK'),
('Corea del Sur', 'SURCOREANA', 'KOR'),
('Costa de Marfil', 'MARFILEÑA', 'CIV'),
('Costa Rica', 'COSTARRICENSE', 'CRI'),
('Croacia', 'CROATA', 'HRV'),
('Cuba', 'CUBANA', 'CUB'),
('Dinamarca', 'DANÉSA', 'DNK'),
('Dominica', 'DOMINIQUÉS', 'DMA'),
('Ecuador', 'ECUATORIANA', 'ECU'),
('Egipto', 'EGIPCIA', 'EGY'),
('El Salvador', 'SALVADOREÑA', 'SLV'),
('Emiratos Árabes Unidos', 'EMIRATÍ', 'ARE'),
('Eritrea', 'ERITREA', 'ERI'),
('Eslovaquia', 'ESLOVACA', 'SVK'),
('Eslovenia', 'ESLOVENA', 'SVN'),
('España', 'ESPAÑOLA', 'ESP'),
('Estados Unidos', 'ESTADOUNIDENSE', 'USA'),
('Estonia', 'ESTONA', 'EST'),
('Esuatini', 'SUAZI', 'SWZ'),
('Etiopía', 'ETÍOPE', 'ETH'),
('Filipinas', 'FILIPINA', 'PHL'),
('Finlandia', 'FINLANDÉSA', 'FIN'),
('Fiyi', 'FIYIANA', 'FJI'),
('Francia', 'FRANCÉSA', 'FRA'),
('Gabón', 'GABONÉSA', 'GAB'),
('Gambia', 'GAMBIANA', 'GMB'),
('Georgia', 'GEORGIANA', 'GEO'),
('Ghana', 'GHANÉSA', 'GHA'),
('Granada', 'GRANADINA', 'GRD'),
('Grecia', 'GRIEGA', 'GRC'),
('Guatemala', 'GUATEMALTECA', 'GTM'),
('Guinea', 'GUINEANA', 'GIN'),
('Guinea-Bisáu', 'GUINEANA-BISAUENSE', 'GNB'),
('Guinea Ecuatorial', 'ECUATOGUINEANA', 'GNQ'),
('Guyana', 'GUYANESA', 'GUY'),
('Haití', 'HAITIANA', 'HTI'),
('Honduras', 'HONDUREÑA', 'HND'),
('Hungría', 'HÚNGARA', 'HUN'),
('India', 'INDIA', 'IND'),
('Indonesia', 'INDONESIA', 'IDN'),
('Irak', 'IRAQUÍ', 'IRQ'),
('Irán', 'IRANÍ', 'IRN'),
('Irlanda', 'IRLANDÉSA', 'IRL'),
('Islandia', 'ISLANDÉSA', 'ISL'),
('Islas Marshall', 'MARSHALÉSA', 'MHL'),
('Islas Salomón', 'SALOMONENSE', 'SLB'),
('Israel', 'ISRAELÍ', 'ISR'),
('Italia', 'ITALIANA', 'ITA'),
('Jamaica', 'JAMAIQUINA', 'JAM'),
('Japón', 'JAPONÉSA', 'JPN'),
('Jordania', 'JORDANA', 'JOR'),
('Kazajistán', 'KAZAJA', 'KAZ'),
('Kenia', 'KENIANA', 'KEN'),
('Kirguistán', 'KIRGUISA', 'KGZ'),
('Kiribati', 'KIRIBATIANA', 'KIR'),
('Kuwait', 'KUWAITÍ', 'KWT'),
('Laos', 'LAOSIANA', 'LAO'),
('Lesoto', 'LESOTENSE', 'LSO'),
('Letonia', 'LETÓNA', 'LVA'),
('Líbano', 'LIBANÉSA', 'LBN'),
('Liberia', 'LIBERIANA', 'LBR'),
('Libia', 'LIBIA', 'LBY'),
('Liechtenstein', 'LIECHTENSTEINIANA', 'LIE'),
('Lituania', 'LITUANA', 'LTU'),
('Luxemburgo', 'LUXEMBURGUÉSA', 'LUX'),
('Madagascar', 'MALGACHE', 'MDG'),
('Malasia', 'MALASIA', 'MYS'),
('Malaui', 'MALAUÍ', 'MWI'),
('Maldivas', 'MALDIVA', 'MDV'),
('Malí', 'MALIENSE', 'MLI'),
('Malta', 'MALTÉSA', 'MLT'),
('Marruecos', 'MARROQUÍ', 'MAR'),
('Mauricio', 'MAURICIANA', 'MUS'),
('Mauritania', 'MAURITANA', 'MRT'),
('México', 'MEXICANA', 'MEX'),
('Micronesia', 'MICRONESIA', 'FSM'),
('Moldavia', 'MOLDAVA', 'MDA'),
('Mónaco', 'MONEGASCA', 'MCO'),
('Mongolia', 'MONGOLA', 'MNG'),
('Montenegro', 'MONTENEGRINA', 'MNE'),
('Mozambique', 'MOZAMBIQUEÑA', 'MOZ'),
('Namibia', 'NAMIBIA', 'NAM'),
('Nauru', 'NAURUANA', 'NRU'),
('Nepal', 'NEPALÍ', 'NPL'),
('Nicaragua', 'NICARAGÜENSE', 'NIC'),
('Níger', 'NIGERIANA', 'NER'),
('Nigeria', 'NIGERIANA', 'NGA'),
('Noruega', 'NORUEGA', 'NOR'),
('Nueva Zelanda', 'NEOZELANDÉSA', 'NZL'),
('Omán', 'OMANÍ', 'OMN'),
('Países Bajos', 'NEERLANDÉSA', 'NLD'),
('Pakistán', 'PAKISTANÍ', 'PAK'),
('Palaos', 'PALAUESA', 'PLW'),
('Palestina', 'PALESTINA', 'PSE'),
('Panamá', 'PANAMEÑA', 'PAN'),
('Papúa Nueva Guinea', 'PAPÚ', 'PNG'),
('Paraguay', 'PARAGUAYA', 'PRY'),
('Perú', 'PERUANA', 'PER'),
('Polonia', 'POLACA', 'POL'),
('Portugal', 'PORTUGUÉSA', 'PRT'),
('Reino Unido', 'BRITÁNICA', 'GBR'),
('República Centroafricana', 'CENTROAFRICANA', 'CAF'),
('República Checa', 'CHECA', 'CZE'),
('República Democrática del Congo', 'CONGOLESA', 'COD'),
('República del Congo', 'CONGOLESA', 'COG'),
('República Dominicana', 'DOMINICANA', 'DOM'),
('Ruanda', 'RUANDÉSA', 'RWA'),
('Rumanía', 'RUMANA', 'ROU'),
('Rusia', 'RUSA', 'RUS'),
('Samoa', 'SAMOANA', 'WSM'),
('San Cristóbal y Nieves', 'SANCRISTOBALENSE', 'KNA'),
('San Marino', 'SANMARINENSE', 'SMR'),
('San Vicente y las Granadinas', 'SANVICENTINA', 'VCT'),
('Santa Lucía', 'SANTALUCENSE', 'LCA'),
('Santo Tomé y Príncipe', 'SANTOTOMENSE', 'STP'),
('Senegal', 'SENEGALÉSA', 'SEN'),
('Serbia', 'SERBIA', 'SRB'),
('Seychelles', 'SEYCHELLENSE', 'SYC'),
('Sierra Leona', 'SIERRALEONÉSA', 'SLE'),
('Singapur', 'SINGAPURENSE', 'SGP'),
('Siria', 'SIRIA', 'SYR'),
('Somalia', 'SOMALÍ', 'SOM'),
('Sri Lanka', 'CEILANDÉSA', 'LKA'),
('Sudáfrica', 'SUDAFRICANA', 'ZAF'),
('Sudán', 'SUDANÉSA', 'SDN'),
('Sudán del Sur', 'SURSUDANÉSA', 'SSD'),
('Suecia', 'SUECA', 'SWE'),
('Suiza', 'SUIZA', 'CHE'),
('Surinam', 'SURINAMESA', 'SUR'),
('Tailandia', 'TAILANDÉSA', 'THA'),
('Tanzania', 'TANZANA', 'TZA'),
('Tayikistán', 'TAYIKA', 'TJK'),
('Timor Oriental', 'TIMORENSE', 'TLS'),
('Togo', 'TOGOLÉSA', 'TGO'),
('Tonga', 'TONGANA', 'TON'),
('Trinidad y Tobago', 'TRINITENSE', 'TTO'),
('Túnez', 'TUNECINA', 'TUN'),
('Turkmenistán', 'TURCOMANA', 'TKM'),
('Turquía', 'TURCA', 'TUR'),
('Tuvalu', 'TUVALUANA', 'TUV'),
('Ucrania', 'UCRANIANA', 'UKR'),
('Uganda', 'UGANDÉSA', 'UGA'),
('Uruguay', 'URUGUAYA', 'URY'),
('Uzbekistán', 'UZBEKA', 'UZB'),
('Vanuatu', 'VANUATUENSE', 'VUT'),
('Venezuela', 'VENEZOLANA', 'VEN'),
('Vietnam', 'VIETNAMITA', 'VNM'),
('Yemen', 'YEMENÍ', 'YEM'),
('Yibuti', 'YIBUTIANA', 'DJI'),
('Zambia', 'ZAMBIANA', 'ZMB'),
('Zimbabue', 'ZIMBABUENSE', 'ZWE');


-- Script comunas, regiones, provincias Junio 2022
INSERT INTO regiones (id,nombre,abreviatura,capital)
VALUES
	(1,'Arica y Parinacota','AP','Arica'),
	(2,'Tarapacá','TA','Iquique'),
	(3,'Antofagasta','AN','Antofagasta'),
	(4,'Atacama','AT','Copiapó'),
	(5,'Coquimbo','CO','La Serena'),
	(6,'Valparaiso','VA','valparaíso'),
	(7,'Metropolitana de Santiago','RM','Santiago'),
	(8,'Libertador General Bernardo O''Higgins','OH','Rancagua'),
	(9,'Maule','MA','Talca'),
	(10,'Ñuble','NB','Chillán'),
	(11,'Biobío','BI','Concepción'),
	(12,'La Araucanía','IAR','Temuco'),
	(13,'Los Ríos','LR','Valdivia'),
	(14,'Los Lagos','LL','Puerto Montt'),
	(15,'Aysén del General Carlos Ibáñez del Campo','AI','Coyhaique'),
	(16,'Magallanes y de la Antártica Chilena','MG','Punta Arenas');

INSERT INTO provincias (id,nombre,id_region)
VALUES
	(1,'Arica',1),
	(2,'Parinacota',1),
	(3,'Iquique',2),
	(4,'El Tamarugal',2),
	(5,'Tocopilla',3),
	(6,'El Loa',3),
	(7,'Antofagasta',3),
	(8,'Chañaral',4),
	(9,'Copiapó',4),
	(10,'Huasco',4),
	(11,'Elqui',5),
	(12,'Limarí',5),
	(13,'Choapa',5),
 	(14,'Petorca',6),
	(15,'Los Andes',6),
 	(16,'San Felipe de Aconcagua',6),
 	(17,'Quillota',6),
	(18,'Valparaiso',6),
	(19,'San Antonio',6),
	(20,'Isla de Pascua',6),
	(21,'Marga Marga',6),
	(22,'Chacabuco',7),
	(23,'Santiago',7),
	(24,'Cordillera',7),
	(25,'Maipo',7),
	(26,'Melipilla',7),
	(27,'Talagante',7),
	(28,'Cachapoal',8),
	(29,'Colchagua',8),
	(30,'Cardenal Caro',8),
	(31,'Curicó',9),
	(32,'Talca',9),
 	(33,'Linares',9),
	(34,'Cauquenes',9),
	(35,'Diguillín',10),
	(36,'Itata',10),
	(37,'Punilla',10),
	(38,'Bio Bío',11),
	(39,'Concepción',11),
	(40,'Arauco',11),
	(41,'Malleco',12),
	(42,'Cautín',12),
	(43,'Valdivia',13),
	(44,'Ranco',13),
	(45,'Osorno',14),
	(46,'Llanquihue',14),
	(47,'Chiloé',14),
	(48,'Palena',14),
	(49,'Coyhaique',15),
	(50,'Aysén',15),
	(51,'General Carrera',15),
	(52,'Capitán Prat',15),
	(53,'Última Esperanza',16),
	(54,'Magallanes',16),
	(55,'Tierra del Fuego',16),
	(56,'Antártica Chilena',16);



INSERT INTO comunas (id,nombre,id_provincia)
VALUES
	(1,'Arica',1),
	(2,'Camarones',1),
	(3,'General Lagos',2),
	(4,'Putre',2),
	(5,'Alto Hospicio',3),
	(6,'Iquique',3),
	(7,'Camiña',4),
	(8,'Colchane',4),
	(9,'Huara',4),
	(10,'Pica',4),
	(11,'Pozo Almonte',4),
  	(12,'Tocopilla',5),
  	(13,'María Elena',5),
	(14,'Calama',6),
	(15,'Ollague',6),
	(16,'San Pedro de Atacama',6),
  	(17,'Antofagasta',7),
	(18,'Mejillones',7),
	(19,'Sierra Gorda',7),
	(20,'Taltal',7),
	(21,'Chañaral',8),
	(22,'Diego de Almagro',8),
  	(23,'Copiapó',9),
	(24,'Caldera',9),
	(25,'Tierra Amarilla',9),
  	(26,'Vallenar',10),
	(27,'Alto del Carmen',10),
	(28,'Freirina',10),
	(29,'Huasco',10),
	(30,'La Serena',11),
  	(31,'Coquimbo',11),
  	(32,'Andacollo',11),
  	(33,'La Higuera',11),
  	(34,'Paihuano',11),
	(35,'Vicuña',11),
	(36,'Ovalle',12),
  	(37,'Combarbalá',12),
  	(38,'Monte Patria',12),
  	(39,'Punitaqui',12),
	(40,'Río Hurtado',12),
	(41,'Illapel',13),
	(42,'Canela',13),
	(43,'Los Vilos',13),
	(44,'Salamanca',13),
	(45,'La Ligua',14),
  	(46,'Cabildo',14),
	(47,'Zapallar',14),
  	(48,'Papudo',14),
	(49,'Petorca',14),
	(50,'Los Andes',15),
	(51,'San Esteban',15),
  	(52,'Calle Larga',15),
  	(53,'Rinconada',15),
	(54,'San Felipe',16),
  	(55,'Llaillay',16),
  	(56,'Putaendo',16),
	(57,'Santa María',16),
	(58,'Catemu',16),
	(59,'Panquehue',16),
  	(60,'Quillota',17),
  	(61,'La Cruz',17),
	(62,'La Calera',17),
	(63,'Nogales',17),
  	(64,'Hijuelas',17),
	(65,'Valparaíso',18),	
  	(66,'Viña del Mar',18),
	(67,'Concón',18),
 	(68,'Quintero',18),
  	(69,'Puchuncaví',18),
	(70,'Casablanca',18),
	(71,'Juan Fernández',18),
	(72,'San Antonio',19),
  	(73,'Cartagena',19),
	(74,'El Tabo',19),
	(75,'El Quisco',19),
	(76,'Algarrobo',19),
	(77,'Santo Domingo',19),
	(78,'Isla de Pascua',20),
	(79,'Quilpué',21),
	(80,'Limache',21),
	(81,'Olmué',21),
	(82,'Villa Alemana',21),
	(83,'Colina',22),
	(84,'Lampa',22),
	(85,'Tiltil',22),
	(86,'Santiago',23),
	(87,'Vitacura',23),
  	(88,'San Ramón',23),
	(89,'San Miguel',23),
	(90,'San Joaquín',23),
  	(91,'Renca',23),
	(92,'Recoleta',23),
  	(93,'Quinta Normal',23),
	(94,'Quilicura',23),
  	(95,'Pudahuel',23),
  	(96,'Providencia',23),
	(97,'Peñalolén',23),
  	(98,'Pedro Aguirre Cerda',23),
	(99,'Ñuñoa',23),
	(100,'Maipú',23),
	(101,'Macul',23),
	(102,'Lo Prado',23),
	(103,'Lo Espejo',23),
	(104,'Lo Barnechea',23),
	(105,'Las Condes',23),
	(106,'La Reina',23),
	(107,'La Pintana',23),
	(108,'La Granja',23),
	(109,'La Florida',23),
  	(110,'La Cisterna',23),
  	(111,'Independencia',23),
  	(112,'Huechuraba',23),
	(113,'Estación Central',23),
  	(114,'El Bosque',23),
  	(115,'Conchalí',23),
  	(116,'Cerro Navia',23),
  	(117,'Cerrillos',23),
	(118,'Puente Alto',24),
	(119,'San José de Maipo',24),
  	(120,'Pirque',24),
	(121,'San Bernardo',25),
	(122,'Buin',25),
  	(123,'Paine',25),
	(124,'Calera de Tango',25),
	(125,'Melipilla',26),
	(126,'Alhué',26),
	(127,'Curacaví',26),
	(128,'María Pinto',26),
	(129,'San Pedro',26),
	(130,'Isla de Maipo',27),
  	(131,'El Monte',27),
	(132,'Padre Hurtado',27),
	(133,'Peñaflor',27),
	(134,'Talagante',27),
	(135,'Codegua',28),
	(136,'Coínco',28),
	(137,'Coltauco',28),
	(138,'Doñihue',28),
	(139,'Graneros',28),
	(140,'Las Cabras',28),
	(141,'Machalí',28),
	(142,'Malloa',28),
	(143,'Mostazal',28),
	(144,'Olivar',28),
	(145,'Peumo',28),
	(146,'Pichidegua',28),
	(147,'Quinta de Tilcoco',28),
	(148,'Rancagua',28),
	(149,'Rengo',28),
	(150,'Requínoa',28),
	(151,'San Vicente de Tagua Tagua',28),
	(152,'Chépica',29),
	(153,'Chimbarongo',29),
	(154,'Lolol',29),
  	(155,'Nancagua',29),
  	(156,'Palmilla',29),
  	(157,'Peralillo',29),
	(158,'Placilla',29),
 	(159,'Pumanque',29),
	(160,'San Fernando',29),
	(161,'Santa Cruz',29),
	(162,'La Estrella',30),
	(163,'Litueche',30),
	(164,'Marchigüe',30),
	(165,'Navidad',30),
	(166,'Paredones',30),
	(167,'Pichilemu',30),
	(168,'Curicó',31),
	(169,'Hualañé',31),
	(170,'Licantén',31),
 	(171,'Molina',31),
	(172,'Rauco',31),
	(173,'Romeral',31),
	(174,'Sagrada Familia',31),
	(175,'Teno',31),
	(176,'Vichuquén',31),
	(177,'Talca',32),
	(178,'San Clemente',32),
	(179,'Pelarco',32),
	(180,'Pencahue',32),
	(181,'Maule',32),
	(182,'San Rafael',32),
	(183,'Curepto',33),
	(184,'Constitución',32),
	(185,'Empedrado',32),
	(186,'Río Claro',32),
  	(187,'Linares',33),
	(188,'San Javier',33),
	(189,'Parral',33),
	(190,'Villa Alegre',33),
	(191,'Longaví',33),
	(192,'Colbún',33),
	(193,'Retiro',33),
	(194,'Yerbas Buenas',33),
  	(195,'Cauquenes',34),
	(196,'Chanco',34),
	(197,'Pelluhue',34),
	(198,'Bulnes',35),
	(199,'Chillán',35),
	(200,'Chillán Viejo',35),
	(201,'El Carmen',35),
	(202,'Pemuco',35),
	(203,'Pinto',35),
	(204,'Quillón',35),
	(205,'San Ignacio',35),
	(206,'Yungay',35),
	(207,'Cobquecura',36),
	(208,'Coelemu',36),
	(209,'Ninhue',36),
	(210,'Portezuelo',36),
	(211,'Quirihue',36),
	(212,'Ránquil',36),
	(213,'Treguaco',36),
	(214,'San Carlos',37),
	(215,'Coihueco',37),
	(216,'San Nicolás',37),
	(217,'Ñiquén',37),
	(218,'San Fabián',37),
	(219,'Alto Biobío',38),
	(220,'Antuco',38),
	(221,'Cabrero',38),
	(222,'Laja',38),
	(223,'Los Ángeles',38),
	(224,'Mulchén',38),
	(225,'Nacimiento',38),
	(226,'Negrete',38),
	(227,'Quilaco',38),
	(228,'Quilleco',38),
	(229,'San Rosendo',38),
	(230,'Santa Bárbara',38),
	(231,'Tucapel',38),
	(232,'Yumbel',38),
	(233,'Concepción',39),
	(234,'Coronel',39),
	(235,'Chiguayante',39),
	(236,'Florida',39),
	(237,'Hualpén',39),
	(238,'Hualqui',39),
	(239,'Lota',39),
	(240,'Penco',39),
	(241,'San Pedro de La Paz',39),
	(242,'Santa Juana',39),
	(243,'Talcahuano',39),
	(244,'Tomé',39),
	(245,'Arauco',40),
	(246,'Cañete',40),
	(247,'Contulmo',40),
	(248,'Curanilahue',40),
	(249,'Lebu',40),
	(250,'Los Álamos',40),
	(251,'Tirúa',40),
	(252,'Angol',41),
	(253,'Collipulli',41),
	(254,'Curacautín',41),
	(255,'Ercilla',41),
	(256,'Lonquimay',41),
	(257,'Los Sauces',41),
	(258,'Lumaco',41),
	(259,'Purén',41),
	(260,'Renaico',41),
	(261,'Traiguén',41),
	(262,'Victoria',41),
	(263,'Temuco',42),
	(264,'Carahue',42),
	(265,'Cholchol',42),
	(266,'Cunco',42),
	(267,'Curarrehue',42),
	(268,'Freire',42),
	(269,'Galvarino',42),
	(270,'Gorbea',42),
	(271,'Lautaro',42),
	(272,'Loncoche',42),
	(273,'Melipeuco',42),
	(274,'Nueva Imperial',42),
	(275,'Padre Las Casas',42),
	(276,'Perquenco',42),
	(277,'Pitrufquén',42),
	(278,'Pucón',42),
	(279,'Saavedra',42),
	(280,'Teodoro Schmidt',42),
	(281,'Toltén',42),
	(282,'Vilcún',42),
	(283,'Villarrica',42),
	(284,'Valdivia',43),
	(285,'Corral',43),
	(286,'Lanco',43),
	(287,'Los Lagos',43),
	(288,'Máfil',43),
	(289,'Mariquina',43),
	(290,'Paillaco',43),
	(291,'Panguipulli',43),
	(292,'La Unión',44),
	(293,'Futrono',44),
	(294,'Lago Ranco',44),
	(295,'Río Bueno',44),
	(296,'Osorno',45),
	(297,'Puerto Octay',45),
	(298,'Purranque',45),
	(299,'Puyehue',45),
	(300,'Río Negro',45),
	(301,'San Juan de la Costa',45),
	(302,'San Pablo',45),
	(303,'Calbuco',46),
	(304,'Cochamó',46),
	(305,'Fresia',46),
	(306,'Frutillar',46),
	(307,'Llanquihue',46),
	(308,'Los Muermos',46),
	(309,'Maullín',46),
	(310,'Puerto Montt',46),
	(311,'Puerto Varas',46),
	(312,'Ancud',47),
	(313,'Castro',47),
	(314,'Chonchi',47),
	(315,'Curaco de Vélez',47),
	(316,'Dalcahue',47),
	(317,'Puqueldón',47),
	(318,'Queilén',47),
	(319,'Quellón',47),
	(320,'Quemchi',47),
	(321,'Quinchao',47),
	(322,'Chaitén',48),
	(323,'Futaleufú',48),
	(324,'Hualaihué',48),
	(325,'Palena',48),
	(326,'Lago Verde',49),
	(327,'Coihaique',49),
	(328,'Aysén',50),
	(329,'Cisnes',50),
	(330,'Guaitecas',50),
	(331,'Río Ibáñez',51),
	(332,'Chile Chico',51),
	(333,'Cochrane',52),
	(334,'O''Higgins',52),
	(335,'Tortel',52),
	(336,'Natales',53),
	(337,'Torres del Paine',53),
	(338,'Laguna Blanca',54),
	(339,'Punta Arenas',54),
	(340,'Río Verde',54),
	(341,'San Gregorio',54),
	(342,'Porvenir',55),
	(343,'Primavera',55),
	(344,'Timaukel',55),
	(345,'Cabo de Hornos',56),
	(346,'Antártica',56);




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
    nombre_mostrar,
    email,
    "password",
    duracion,
	pagina_inicio
) VALUES (
    'admin',
    'Administrador Principal',
    'fbirrer@gmail.com',
    'cambiar',  -- ¡Reemplazar por una contraseña hasheada en producción!
    30,
	'inicio.html'
);

-- Roles
INSERT INTO roles (nombre) VALUES 
('Soporte'), ('Administrador'), ('Auditor'), ('Usuario');



INSERT INTO tipos_menu (nombre) VALUES ('General'), ('Modulos');

-- Menús
INSERT INTO menus (nombre, icono, id_tipo_menu, id_padre, url, descripcion, "token", orden, estado) VALUES
('Dashboard', 'fa-solid fa-dashboard', 1, NULL, '/dashboard', 'Vista principal', 'token_dashboard', 1, true),
('Gestión', 'fa-solid fa-atom', 1, NULL, '/gestion', 'Módulo de gestión', 'token_gestion', 2, true),
('Tablas', 'fa-solid fa-table', 1, 2, '/gestion/tablas', 'Tablas base del sistema', 'token_tablas', 1, true),
('Permisos', 'fa-solid fa-lock', 1, 2, NULL, 'Gestionador de relaciones', NULL, 3, true),
('Usuarios', 'fa-solid fa-users', 1, 3, '/gestion/usuarios', 'Usuarios del sistema', NULL, 2, true),
('Menús Generales', 'fa-solid fa-bars', 1, 3, '/gestion/menu', 'Menus generales del sistema', NULL, 4, true),
('Roles', 'fa-solid fa-user-shield', 1, 3, '/gestion/rol', 'Roles del sistema', NULL, 3, true),
('Empresas', 'fa-solid fa-building', 1, 3, '/gestion/empresas', 'Empresas del sistema', NULL, 1, true),
('Rol Menu', 'fa-solid fa-link', 1, 4, '/gestion/rolMenu', NULL, NULL, 1, true),
('Empresa Usuario', 'fa-solid fa-diagram-project', NULL, 4, '/gestion/empresaUsuario', NULL, NULL, 2, true),
('Tipo de Datos', 'fa-solid fa-database', 1, 2, '/gestion/tipoEmpresa', 'Gestión de Tipo de Empresas', NULL, 2, true),
('Tipo de Empresas', 'fa-solid fa-industry', 1, 11, '/gestion/tipoEmpresa', NULL, NULL, 1, true),
('Tipo de Menu', 'fa-solid fa-list', 1, 11, '/gestion/tipoMenu', NULL, NULL, 2, true),
('Modulos', 'fa-solid fa-puzzle-piece', 1, 3, '/gestion/modulo', 'Modulos del sistema', NULL, 6, true),
('Empresa Modulo', 'fa-solid fa-layer-group', 1, 4, NULL, NULL, NULL, 1, true),
('Empresa Usuario', 'fa-solid fa-user-tie', 1, 4, NULL, NULL, NULL, 2, true),
('Modulos Menu', 'fa-solid fa-list', 1, 4, NULL, NULL, NULL, 3, true),
('Geo referencia', 'fa-solid fa-map-location-dot', 1, 2, NULL, NULL, NULL, 4, true),
('Laboratorios', 'fa-solid fa-check-to-slot fa-fw', 2, NULL, '/vademecum/laboratorios', 'Gestión de Tipo de Empresas', NULL, 1, true),
('Farmacias', 'fa-solid fa-landmark-flag fa-fw', 2, NULL, '/vademecum/farmacias', NULL, NULL, 1, true),
('Remedios', 'fa-solid fa-user-tag fa-fw', 2, NULL, '/vademecum/remdios', NULL, NULL, 3, true),
('Vademecum', 'fa-solid fa-book-medical', 2, NULL, '/vademecum/remdios', NULL, NULL, 4, true),
('Regiones', 'fa-solid fa-globe', 1, 18, '/modulo-georeferencia/regiones', NULL, NULL, 2, true),
('Provincias', 'fa-solid fa-map', 1, 18, '/modulo-georeferencia/provincias', NULL, NULL, 3, true),
('Comunas', 'fa-solid fa-location-dot', 1, 18, '/modulo-georeferencia/comunas', NULL, NULL, 4, true),
('Menus X Modulo', 'fa-solid fa-sitemap', 1, 3, '/gestion/menusxmodulo', 'Menus por Modulos', NULL, 5, true),
('Nacionaliad', 'fa-solid fa-flag', 1, 3, '/gestion/nacionalidad', 'Nacionalidades del sistema', NULL, 7, true),
('test3', 'fa-solid fa-user-tag fa-fw', 2, NULL, '/vademecum/remdios', NULL, NULL, 3, true),
('test4', 'fa-solid fa-check-to-slot fa-fw', 2, NULL, '/vademecum/laboratorios', 'Gestión de Tipo de Empresas', NULL, 1, true),
('test5', 'fa-solid fa-landmark-flag fa-fw', 2, NULL, '/vademecum/farmacias', NULL, NULL, 1, true),
('test6', 'fa-solid fa-user-tag fa-fw', 2, NULL, '/vademecum/remdios', NULL, NULL, 3, true),
('test7', 'fa-solid fa-check-to-slot fa-fw', 2, NULL, '/vademecum/laboratorios', 'Gestión de Tipo de Empresas', NULL, 1, true),
('test8', 'fa-solid fa-landmark-flag fa-fw', 2, NULL, '/vademecum/farmacias', NULL, NULL, 1, true),
('test9', 'fa-solid fa-user-tag fa-fw', 2, NULL, '/vademecum/remdios', NULL, NULL, 3, true);

-- Relación menú-rol
INSERT INTO menu_rol (id_menu, id_rol) 
VALUES 
(1, 1),(2, 1),(3, 1),(4, 1),(5, 1),(6, 1),(7, 1),(8, 1),(9, 1);

-- Menús específicos para tipos de empresa
INSERT INTO menu_tipo_empresa (id_menu, id_tipo_empresa) VALUES (1, 1);

INSERT INTO empresa_usuario (id_empresa, id_usuario)
VALUES
(1, 1),
(2, 1);

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

INSERT INTO modulo_menu (id_modulo, id_menu)
VALUES
(3, 27),
(3, 28),
(3, 29),
(3, 30),
(3, 31),
(3, 32),
(3, 33),
(3, 34),
(2, 14),
(2, 15),
(2, 16),
(2, 17);

INSERT INTO empresa_modulo (id_empresa, id_modulo, fecha_inicio, fecha_fin, estado) 
VALUES
(1, 2, '2000-01-01', NULL, true),
(2, 2, '2000-01-01', NULL, true),
(1, 3, '2000-01-01', NULL, true);

-- =========================
-- FIN DEL SCRIPT
-- =========================
