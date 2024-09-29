from lab2_poo import *

def mostrar_menu():
    print("********** Menú de Gestión de Cuentas ***********")
    print('1 - Crear Cuenta Bancaria')
    print('2 - Buscar cuentas por DNI ')
    print('3 - Actualizar Saldo de Cuenta')
    print('4 - Eliminar cuentas Existentes')
    print('5 - Salir de la Aplicación ')


def agregar_cuenta(gestion,tipo_cuenta):
    try:
        dni = input('Ingrese DNI del Titular: ')
        num_cuenta = input('Ingrese numero de Cuenta: ')
        titular =  input('Ingrese Nombre y apellido del titular: ')
        saldo = input('Ingrese monto de la cuenta: ')
        cta_cuenta = input('Ingrese el tipo de Cuenta: 1- AHORRO <===> 2 - CORRIENTE: ')

        if cta_cuenta == '1':
            cta_ahorro = 'AHORRO'
            cuenta = CuentaAhorro(dni, num_cuenta, titular, saldo,cta_ahorro)
            gestionar_cuenta.crear_cuenta(cuenta)

        elif cta_cuenta == '2':
            cta_corriente = 'CORRIENTE'
            cuenta = CuentaCorriente(dni, num_cuenta, titular, saldo,cta_corriente)
            gestionar_cuenta.crear_cuenta(cuenta)

    except ValueError as error:
        print(f'Error {error}')
    except Exception as error:
        print(f'Error inesperado a la crear al cuenta: {error}')

def buscar_cuenta_dni(gestion):
    dni = input('Ingrese DNI del titular: ')
    gestion.leer_cuentas(dni)

def actualizar_cuenta(gestion):
    dni = input('Ingrese DNI del titular: ')
    saldo =  input('Ingrese nuevo saldo: ')
    gestion.actualizar_saldo(dni,saldo)

def eliminar_cuenta(self,dni):
    try:
        connection = self.connect()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM clientes WHERE dni = %s', (dni,))

                if not cursor.fetchone():
                    print('No se encontro el cliente: {dni}')
                    return
                
                cursor.execute('DELETE FROM cuentaahorro WHERE dni = %s', (dni,))
                cursor.execute('DELETE FROM cuentacorriente WHERE dni = %s', (dni,))
                cursor.execute('DELETE FROM clientes WHERE dni = %s', (dni,))
                
                if cursor.rowcount >0 :
                    connection.commit()
                    print(f'Cuentas eliminadas exitosamente ')
                else:
                    print('No se encontraron cuentas con dni : {dni}')

    except Error as e:
        print('No se puede eliminar cuenta: {e}')

if __name__ == '__main__':
    gestionar_cuenta = GestionCuentas()

    while True:
        mostrar_menu()
        opcion = input('Seleccione un opcion: ')

        if opcion == '1':
            agregar_cuenta(gestionar_cuenta, opcion)
        elif opcion == '2':
            buscar_cuenta_dni(gestionar_cuenta)
        elif opcion == '3':
            actualizar_cuenta(gestionar_cuenta)
        elif opcion == '4':
            dni = input('Ingrese el DNI de la cuenta a eliminar: ')
            eliminar_cuenta(gestionar_cuenta,dni)
        elif opcion == '5':
            print(' === FINALIZANDO APLICACION === ')
            break
        else:
            print('opcion no válida')