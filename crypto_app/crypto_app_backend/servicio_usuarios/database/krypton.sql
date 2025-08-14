DROP DATABASE IF EXISTS krypton;
CREATE DATABASE krypton;
USE krypton;


CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30),
    correo VARCHAR(50),
    fecha_nacimiento DATE,
    contraseña VARCHAR(30),
    notificaciones BOOLEAN,
    ultimo_inicio_sesion DATETIME
);
SELECT * FROM usuarios;


CREATE TABLE criptomonedas (
    id_cripto INT AUTO_INCREMENT PRIMARY KEY,
    simbolo VARCHAR(10) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    id_api VARCHAR(255),
    fecha_creacion DATETIME NOT NULL
);
SELECT * FROM criptomonedas;


CREATE TABLE moneda_fiat (
    id_moneda INT AUTO_INCREMENT PRIMARY KEY,
    COI VARCHAR(3) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL
);
SELECT * FROM moneda_fiat;


CREATE TABLE categoria_noticias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(255) NOT NULL UNIQUE
);
SELECT * FROM categoria_noticias;


CREATE TABLE fuente (
    id_fuentes INT AUTO_INCREMENT PRIMARY KEY,
    fuente VARCHAR(255) NOT NULL
);
SELECT * FROM fuente;


CREATE TABLE noticias (
    id_noticias INT AUTO_INCREMENT PRIMARY KEY,
    id_cripto INT NOT NULL,
    api_id VARCHAR(255),
    titulo VARCHAR(500) NOT NULL,
    url TEXT NOT NULL,
    contenido LONGTEXT,
    fecha_creacion DATETIME NOT NULL,
    id_fuente INT NOT NULL,
    id_categoria INT NOT NULL,
    FOREIGN KEY (id_cripto) REFERENCES criptomonedas(id_cripto) ON DELETE CASCADE,
    FOREIGN KEY (id_fuente) REFERENCES fuente(id_fuentes) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categoria_noticias(id_categoria) ON DELETE CASCADE
);
SELECT * FROM noticias;


CREATE TABLE valor_historico (
    id_valor_historico INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(18, 8) NOT NULL,
    fecha DATE NOT NULL,
    id_cripto INT NOT NULL,
    FOREIGN KEY (id_cripto) REFERENCES criptomonedas(id_cripto) ON DELETE CASCADE
);
SELECT * FROM valor_historico;

CREATE TABLE calculadora_de_divisas (
    id_calculadora INT AUTO_INCREMENT PRIMARY KEY,
    api_valor_fiat DECIMAL(18, 8) NOT NULL,
    id_cripto INT NOT NULL,
    cambio DECIMAL(18, 8) NOT NULL,
    fecha_conversion DATETIME NOT NULL,
    FOREIGN KEY (id_cripto) REFERENCES criptomonedas(id_cripto) ON DELETE CASCADE
);
SELECT * FROM calculadora_de_divisas;

CREATE TABLE consultas_usuario (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_cripto INT,
    id_moneda INT,
    fecha_consulta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_cripto) REFERENCES criptomonedas(id_cripto),
    FOREIGN KEY (id_moneda) REFERENCES moneda_fiat(id_moneda)
);
SELECT * FROM consultas_usuario;

CREATE TABLE valor_fiat (
    id_valor_fiat INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(18, 8) NOT NULL,
    fecha DATE NOT NULL,
    id_moneda INT NOT NULL,
    id_valor_historico INT NOT NULL,
    hora TIME NOT NULL,
    FOREIGN KEY (id_moneda) REFERENCES moneda_fiat(id_moneda) ON DELETE CASCADE,
    FOREIGN KEY (id_valor_historico) REFERENCES valor_historico(id_valor_historico) ON DELETE CASCADE
);
SELECT * FROM valor_fiat;
CREATE TABLE alertas_personalizadas (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_cripto INT NOT NULL,
    precio_objetivo DECIMAL(18, 8),
    porcentaje_cambio_objetivo DECIMAL(5, 2),
    tipo_alerta ENUM('precio', 'porcentaje_cambio') NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultima_activacion DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_cripto) REFERENCES criptomonedas(id_cripto) ON DELETE CASCADE,
    CONSTRAINT chk_alerta_tipo CHECK (
        (tipo_alerta = 'precio' AND precio_objetivo IS NOT NULL AND porcentaje_cambio_objetivo IS NULL) OR
        (tipo_alerta = 'porcentaje_cambio' AND porcentaje_cambio_objetivo IS NOT NULL AND precio_objetivo IS NULL)
    )
);
SELECT * FROM alertas_personalizadas;

-- 1. Resultado adaptado: Hemos encontrado el top 3 de los usuarios con mayor numero de 
-- consultas realizadas en nuestra plataforma con mas de 20 consultas cada uno y que cada uno haya consultado mas de 2 divisas 


SELECT
    u.nombre,
    COUNT(cu.id_consulta),
    COUNT(DISTINCT cu.id_moneda),
    group_concat( c.nombre),
group_concat(mf.COI)
FROM
    consultas_usuario cu
JOIN
    usuarios u ON cu.id_usuario = u.id_usuario
 JOIN
    moneda_fiat mf ON cu.id_moneda = mf.id_moneda
JOIN
    criptomonedas c ON cu.id_cripto = c.id_cripto
WHERE
    cu.id_moneda IS NOT NULL
GROUP BY
    u.nombre
HAVING
    COUNT(cu.id_consulta) > 20
   AND COUNT(DISTINCT cu.id_moneda) > 2
ORDER BY
    COUNT(cu.id_consulta) DESC
LIMIT 10;


-- "Encuentra la criptomoneda más consultada en el último mes y el número total de consultas que tuvo. 
-- Solo considera las criptomonedas que fueron consultadas junto con una moneda fiat."
SELECT
    u.nombre,
    COUNT(cu.id_consulta),
    COUNT(DISTINCT cu.id_moneda),
    group_concat( c.nombre),
group_concat(mf.COI)
FROM
    consultas_usuario cu
JOIN
    usuarios u ON cu.id_usuario = u.id_usuario
 JOIN
    moneda_fiat mf ON cu.id_moneda = mf.id_moneda
JOIN
    criptomonedas c ON cu.id_cripto = c.id_cripto
WHERE
    cu.id_moneda IS NOT NULL
GROUP BY
    u.nombre
HAVING
    COUNT(cu.id_consulta) > 20
   AND COUNT(DISTINCT cu.id_moneda) > 2
ORDER BY
    COUNT(cu.id_consulta) DESC
LIMIT 10;
