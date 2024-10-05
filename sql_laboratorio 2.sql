CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) UNIQUE,  -- Para no repetir
    titular VARCHAR(50)
);

CREATE TABLE cuentas_ahorro (
    id_cuenta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,  -- Clave foránea a la tabla clientes
    num_cuenta VARCHAR(20),
    saldo DECIMAL(10, 2),
    tipo_cuenta VARCHAR(20) default ('AHORRO'),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE cuentas_corriente (
    id_cuenta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,  -- Clave foránea a la tabla a clientes
    num_cuenta VARCHAR(20),
    saldo DECIMAL(10, 2),
    tipo_cuenta VARCHAR(20) default ('CORRIENTE'),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);


-- Insertar un cliente
INSERT INTO clientes (dni, titular)
VALUES ('12345678', 'Juan Perez');

-- Insertar cuentas de ahorro asociadas a un cliente
INSERT INTO cuentas_ahorro (num_cuenta, saldo,tipo_cuenta)
VALUES ('1', 5000.00, 'ahorro'),
       ('2', 2500.00, 'ahorro');

-- Insertar cuentas corrientes asociadas a un cliente
INSERT INTO cuentas_corriente (num_cuenta, saldo,tipo_cuenta)
VALUES ('3', 1000.00,'corriente');

INSERT INTO cuentas_ahorro (num_cuenta, saldo,tipo_cuenta)
VALUES ('5', 6500.00, 'ahorro')
