import mysql.connector
from mysql.connector import Error
from decouple import config


class CuentaBancaria:
    def __init__(self, dni,num_cuenta,titular,saldo):
        self.__dni = self.validar_dni(dni)  
        self.__num_cuenta= self.validar_cuenta(num_cuenta)
        self.__titular = titular
        self.__saldo = saldo
        
    @property
    def dni(self):
        return self.__dni
    
    @property
    def num_cuenta(self):
        return self.__num_cuenta
    
    @property
    def titular(self):
        return self.__titular.upper()
    
    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self,nuevo_saldo):
        self.__saldo = nuevo_saldo

    def validar_dni(self, dni):
        try:
            dni_num = int(dni)
            if len(str(dni)) not in [7, 8]:
                raise ValueError("El DNI debe tener 7 u 8 dígitos.")
            if dni_num <= 0:
                raise ValueError("El DNI debe ser numérico positivo.")
            return dni_num
        except ValueError:
            raise ValueError("El DNI debe ser numérico y estar compuesto por 7 u 8 dígitos.")

    def validar_cuenta(self, num_cuenta):
        try:
            cuenta_num = float(num_cuenta)
            if cuenta_num <0:
                raise ValueError('El saldo debe se numero Positivo')
            return cuenta_num
        except ValueError:
            raise ValueError ('El saldo debe ser numero valido')
    
    def to_dict(self):
        return{
            'DNI': self.__dni,
            'N_Cuenta':self.__num_cuenta,
            'Titular':self.__titular,
            'Saldo': self.__saldo
        }

class CuentaAhorro(CuentaBancaria):
    def __init__(self, dni, num_cuenta, titular, saldo,cta_ahorro):
        super().__init__(dni, num_cuenta, titular, saldo)
        self.cta_ahorro =cta_ahorro

    def to_dict(self):
        data = super().to_dict()
        data['Tipo_cuenta'] = self.cta_ahorro
        return data

class CuentaCorriente(CuentaBancaria):
    def __init__(self, dni, num_cuenta, titular, saldo,cta_corriente):
        super().__init__(dni, num_cuenta, titular, saldo)
        self.cta_corriente = cta_corriente

    def to_dict(self):
        data = super().to_dict()
        data['Tipo_cuenta'] = self.cta_corriente
        return data

class GestionCuentas:
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user= config('DB_USER')
        self.password=config('DB_PASSWORD')
        self.port = config('DB_PORT')

    def connect(self):
        'Establezco mi conexion con la DB'
        try:
            connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password,
                port = self.port
            )

            if connection.is_connected():
                return connection
        except Error as e:
            print(f'Error al conectar con la Base de Datos: {e}')
            return None

    def crear_cuenta(self, cuenta):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verifico si existe algún cliente con ese DNI
                    cursor.execute('SELECT id_cliente FROM clientes WHERE dni = %s', (cuenta.dni,))
                    cliente = cursor.fetchone()

                    if cliente:
                        id_cliente = cliente[0]  # Obtener el id_cliente
                        print(f'Este cliente {cuenta.dni} ya posee una cuenta.')
                        agregar_cta = input('Desea agregar cuenta al mismo cliente? 1 - SI   <===> 2 - NO: ')

                        if agregar_cta == '1':
                            cuenta_ac = input('Seleccione tipo de cuenta: 1 - Cta. Ahorro <===> 2 - Cta. Corriente: ').upper()

                            if cuenta_ac == '1':
                                if isinstance(cuenta, CuentaAhorro):
                                    query = '''
                                    INSERT INTO cuentas_ahorro (id_cliente, num_cuenta, saldo, tipo_cuenta)
                                    VALUES (%s, %s, %s, %s)
                                    '''
                                    cursor.execute(query, (id_cliente, cuenta.num_cuenta, cuenta.saldo, cuenta.cta_ahorro))
                                    print(f'Cuenta de AHORRO agregada para el cliente {cuenta.titular}.')

                            elif cuenta_ac == '2':
                                if isinstance(cuenta, CuentaCorriente):
                                    query = '''
                                    INSERT INTO cuentas_corriente (id_cliente, num_cuenta, saldo, tipo_cuenta)
                                    VALUES (%s, %s, %s, %s)
                                    '''
                                    cursor.execute(query, (id_cliente, cuenta.num_cuenta, cuenta.saldo, cuenta.cta_corriente))
                                    print(f'Cuenta CORRIENTE agregada para el cliente {cuenta.titular}.')
                        
                        elif agregar_cta == '2':
                            print('OPCION FINALIZADA - SALIDA DEL COMANDO \n')
                            return

                    else:
                        # cuando el cliente no existe lo agrego
                        query = '''
                        INSERT INTO clientes (dni, titular)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (cuenta.dni, cuenta.titular))
                        id_cliente = cursor.lastrowid  # Recupero el id_cliente del cliente

                        if isinstance(cuenta, CuentaAhorro):
                            query = '''
                            INSERT INTO cuentas_ahorro (id_cliente, num_cuenta, saldo, tipo_cuenta)
                            VALUES (%s, %s, %s, %s)
                            '''
                            cursor.execute(query, (id_cliente, cuenta.num_cuenta, cuenta.saldo, cuenta.cta_ahorro))
                            print(f'Cuenta de ahorro creada para el nuevo cliente {cuenta.dni}.')

                        elif isinstance(cuenta, CuentaCorriente):
                            query = '''
                            INSERT INTO cuentas_corriente (id_cliente, num_cuenta, saldo, tipo_cuenta)
                            VALUES (%s, %s, %s, %s)
                            '''
                            cursor.execute(query, (id_cliente, cuenta.num_cuenta, cuenta.saldo, cuenta.cta_corriente))
                            print(f'Cuenta corriente creada para el nuevo cliente {cuenta.dni}.')

                connection.commit()
                print(f'**** La cuenta de {cuenta.titular} creada exitosamente! ****')

        except Exception as error:
            print(f'Error al intentar crear la cuenta: {error}')

    def leer_cuentas(self, dni):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Consulta combinada para cuentas de ahorro y corrientes incluyendo el titular
                    query = '''
                    SELECT 'Ahorro' AS tipo_cuenta, c.titular, ca.num_cuenta, ca.saldo 
                    FROM cuentas_ahorro ca
                    JOIN clientes c ON ca.id_cliente = c.id_cliente
                    WHERE c.dni = %s

                    UNION ALL

                    SELECT 'Corriente' AS tipo_cuenta, c.titular, cc.num_cuenta, cc.saldo 
                    FROM cuentas_corriente cc
                    JOIN clientes c ON cc.id_cliente = c.id_cliente
                    WHERE c.dni = %s;
                    '''
                    
                    cursor.execute(query, (dni, dni))
                    cuentas = cursor.fetchall()

                    # Mostrar resultados
                    if cuentas:
                        print(f'Cuentas para el cliente con DNI {dni}:\n')
                        for cuenta in cuentas:
                            print(f'Tipo de cuenta: {cuenta[0]}, Titular: {cuenta[1]}, Número de cuenta: {cuenta[2]}, Saldo: {cuenta[3]}')
                    else:
                        print(f'No se encontraron cuentas para el cliente con DNI {dni}.')

        except Exception as error:
            print(f'Error al intentar listar las cuentas: {error}')

    def actualizar_saldo(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Ingresar el DNI del cliente
                    dni = input("Ingrese el DNI del cliente: ")

                    # Consultar las cuentas asociadas al DNI
                    query = '''
                    SELECT ca.id_cuenta, ca.num_cuenta, ca.saldo, ca.tipo_cuenta
                    FROM cuentas_ahorro ca
                    JOIN clientes c ON ca.id_cliente = c.id_cliente
                    WHERE c.dni = %s
                    UNION ALL
                    SELECT cc.id_cuenta, cc.num_cuenta, cc.saldo , cc.tipo_cuenta
                    FROM cuentas_corriente cc
                    JOIN clientes c ON cc.id_cliente = c.id_cliente
                    WHERE c.dni = %s;
                    '''
                    cursor.execute(query, (dni, dni))
                    cuentas = cursor.fetchall()

                    if cuentas:
                        print(f'Cuentas para el cliente con DNI {dni}:\n')
                        for cuenta in cuentas:
                            print(f'ID Cuenta: {cuenta[0]}, Número de cuenta: {cuenta[1]}, Saldo: {cuenta[2]}, Cuenta tipo: {cuenta[3]}')

                        # Seleccionar la cuenta a modificar
                        id_cuenta_seleccionada = input("Ingrese el ID de la cuenta que desea modificar: ")

                        # Ingresar el nuevo saldo
                        nuevo_saldo = float(input("Ingrese el nuevo saldo: "))

                        # Actualizar el saldo en la tabla correspondiente
                        # Verificar en qué tabla se encuentra la cuenta seleccionada
                        query = '''
                        UPDATE cuentas_ahorro
                        SET saldo = %s
                        WHERE id_cuenta = %s;
                        '''
                        cursor.execute(query, (nuevo_saldo, id_cuenta_seleccionada))

                        if cursor.rowcount == 0:
                            query = '''
                            UPDATE cuentas_corriente
                            SET saldo = %s
                            WHERE id_cuenta = %s;
                            '''
                            cursor.execute(query, (nuevo_saldo, id_cuenta_seleccionada))

                        connection.commit()
                        print('**** Saldo actualizado exitosamente! ****')
                    else:
                        print(f'No se encontraron cuentas para el cliente con DNI {dni}. \n')

        except Exception as error:
            print(f'Error al intentar actualizar el saldo: {error}')

    def listar_todas_las_cuentas(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Consulta para traer todas las cuentas (ahorro y corriente) de todos los clientes
                    query = '''
                    SELECT c.dni, c.titular, ca.num_cuenta, ca.saldo, ca.tipo_cuenta
                    FROM cuentas_ahorro ca
                    JOIN clientes c ON ca.id_cliente = c.id_cliente
                    UNION ALL
                    SELECT c.dni, c.titular, cc.num_cuenta, cc.saldo, cc.tipo_cuenta
                    FROM cuentas_corriente cc
                    JOIN clientes c ON cc.id_cliente = c.id_cliente;
                    '''
                    cursor.execute(query)
                    cuentas = cursor.fetchall()

                    # Verificar si hay cuentas
                    if cursor.rowcount() > 0 :
                        print(f'Listado de todas las cuentas existentes:\n')
                        for cuenta in cuentas:
                            print(f'DNI: {cuenta[0]}, Titular: {cuenta[1]}, Número de cuenta: {cuenta[2]}, Saldo: {cuenta[3]}, Tipo de cuenta: {cuenta[4]}')
                    else:
                        print('No se encontraron cuentas en el sistema.')
        except Exception as error:
            print(f'Error al intentar listar las cuentas: {error}')
