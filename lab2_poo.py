import mysql.connector
from mysql.connector import Error
import json
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
            print('Error al conectar con la Base de Datos: {e}')
            return None

    def crear_cuenta(self,cuenta): #! Funcionando: revisar esta funcion para cuentas multiples para un mismo DNI
            try:
                connection = self.connect()
                if connection:
                    with connection.cursor() as cursor:
                    #? verifico si la existe alguna cuenta con ese DNI
                        cursor.execute('SELECT dni FROM clientes WHERE dni = %s', (cuenta.dni,))
                        if cursor.fetchone():
                            print(f'Este cliente {cuenta.dni} ya posee una cuenta')
                            return

                        if isinstance(cuenta, CuentaAhorro):
                            query='''
                            INSERT INTO clientes (dni,titular)
                            VALUES (%s, %s)
                            '''
                            cursor.execute(query,(cuenta.dni,cuenta.titular))
                            query='''
                            INSERT INTO cuentaahorro (dni, num_cuenta, saldo, tipo_cuenta)
                            VALUES (%s,%s,%s,%s)
                            '''
                            cursor.execute(query,(cuenta.dni,cuenta.num_cuenta,cuenta.saldo,cuenta.cta_ahorro))
                        
                        elif isinstance (cuenta, CuentaCorriente):
                            query='''
                            INSERT INTO clientes (dni,titular)
                            VALUES (%s, %s)
                            '''
                            cursor.execute(query,(cuenta.dni,cuenta.titular))
                            query='''
                            INSERT INTO cuentacorriente (dni, num_cuenta, saldo, tipo_cuenta)
                            VALUES (%s,%s,%s,%s)
                            '''
                            cursor.execute(query,(cuenta.dni,cuenta.num_cuenta,cuenta.saldo,cuenta.cta_corriente))
                        
                        connection.commit()
                        print('**** Cuenta Creada Existosamente! ****')
                        
            except Exception as error:
                print(f'Error al intentar crear la cuenta: {error}')

    def leer_cuentas(self,dni): #! Lanza un error cuando el cliente posee solo una cuenta
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM clientes WHERE dni = %s', (dni,))
                    cuenta_existente = cursor.fetchone()

                    if cuenta_existente:
                        cursor.execute('SELECT * FROM cuentaahorro WHERE dni = %s', (dni,))
                        cuentas_ahorros = cursor.fetchone()

                        cursor.execute('SELECT * FROM cuentacorriente WHERE dni = %s', (dni,))
                        cuentas_corrientes = cursor.fetchone()
                                                                                                                # agrego cta_cte y se cae
                        print(cuenta_existente['dni'],cuenta_existente['titular'], cuentas_ahorros['tipo_cuenta'])#,cuentas_corrientes['tipo_cuenta'])

        except Error as e:
            print(f'Error al buscar los datos en la base de datos {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def actualizar_saldo(self,dni,saldo): #! <--- aca estoy, no hay error, pero no actualiza la base de datos
        try:
            connection=self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM clientes WHERE dni = %s',(dni,))
                    seleccion = input('Que tipo de Cuenta desea Actualizar:  1 - Cta. Ahorro <==> 2 - Cta. Corriente: ')

                    if not cursor.fetchone():
                        print(f'No existe cuenta para actualizar: {dni}')
                        return

                    if seleccion == 1:
                        cursor.execute('UPDATE cuentaahorro SET saldo = %s WHERE dni = %s', (saldo,dni))
                    elif seleccion == 2:
                        cursor.execute('UPDATE cuentacorriente SET saldo = %s WHERE dni = %s', (saldo,dni))

                    if cursor.rowcount >0:
                        connection.commit()
                        print('El saldo se ha actualizado correctamente')
                    else:
                        print('No se puede actualizar la cuenta')

        except Error as e:
            print('Error al actualizar datos: {e}')
        finally:
            if connection.is_connected():
                connection.close()

