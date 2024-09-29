-- Crear la tabla clientes
CREATE TABLE clientes (
    dni char(8) primary key not null,
    titular VARCHAR(50) NOT NULL
);
-- tabla para las cuentasbancarias
CREATE TABLE cuentaAhorro (
	dni char(8) primary key not null, 
    num_cuenta char(12),
    saldo decimal(10,2) default 0.0,
    tipo_cuenta varchar(10),
    foreign key (dni) references clientes (dni)
);
CREATE TABLE cuentaCorriente (
	dni char(8) primary key not null, 
    num_cuenta char(12),
    saldo decimal(10,2) default 0.0,
    tipo_cuenta varchar(10),
    foreign key (dni) references clientes (dni)
);

-- inserto datos para testear la BD
INSERT INTO clientes (dni,titular)
VALUES ('12345678','Juan Perez');

-- cargo cuentas al mismo cliente
INSERT INTO cuentaAhorro (dni, num_cuenta, saldo, tipo_cuenta)
VALUES ('12345678','1', 1500.00, 'ahorro');

insert into cuentaCorriente (dni, num_cuenta, saldo, tipo_cuenta)
values ('12345678','2', 3000.00, 'corriente');