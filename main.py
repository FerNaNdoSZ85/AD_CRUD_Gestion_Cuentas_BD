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
    gestion.actualizar_saldo()

def eliminar_cuenta(self):
    try:
        connection = self.connect()
        if connection:
            with connection.cursor() as cursor:
                # Paso 1: Ingresar el DNI del cliente
                dni = input("Ingrese el DNI del cliente: ")

                # Paso 2: Consultar las cuentas asociadas al DNI
                query = '''
                SELECT ca.id_cuenta, ca.num_cuenta, ca.saldo 
                FROM cuentas_ahorro ca
                JOIN clientes c ON ca.id_cliente = c.id_cliente
                WHERE c.dni = %s
                UNION ALL
                SELECT cc.id_cuenta, cc.num_cuenta, cc.saldo 
                FROM cuentas_corriente cc
                JOIN clientes c ON cc.id_cliente = c.id_cliente
                WHERE c.dni = %s;
                '''
                cursor.execute(query, (dni, dni))
                cuentas = cursor.fetchall()

                # Paso 3: Mostrar las cuentas encontradas
                if cuentas:
                    print(f'Cuentas para el cliente con DNI {dni}:\n')
                    for cuenta in cuentas:
                        print(f'ID Cuenta: {cuenta[0]}, Número de cuenta: {cuenta[1]}, Saldo: {cuenta[2]}')

                    # Paso 4: Seleccionar la cuenta a eliminar
                    id_cuenta_seleccionada = input("Ingrese el ID de la cuenta que desea eliminar: ")

                    # Paso 5: Confirmar eliminación
                    confirmar = input(f"¿Está seguro de que desea eliminar la cuenta con ID {id_cuenta_seleccionada}? (S/N): ").upper()
                    
                    if confirmar == 'S':
                        # Paso 6: Intentar eliminar de la tabla cuentas_ahorro
                        query = '''
                        DELETE FROM cuentas_ahorro
                        WHERE id_cuenta = %s;
                        '''
                        cursor.execute(query, (id_cuenta_seleccionada,))

                        if cursor.rowcount == 0:  # Si no se eliminó, intentar en cuentas_corrientes
                            query = '''
                            DELETE FROM cuentas_corriente
                            WHERE id_cuenta = %s;
                            '''
                            cursor.execute(query, (id_cuenta_seleccionada,))

                        connection.commit()
                        print('**** Cuenta eliminada exitosamente! ****')
                    else:
                        print('Cancelación de la eliminación de la cuenta.')
                else:
                    print(f'No se encontraron cuentas para el cliente con DNI {dni}.')

    except Exception as error:
        print(f'Error al intentar eliminar la cuenta: {error}')


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
            eliminar_cuenta(gestionar_cuenta)
        elif opcion == '5':
            print(' === FINALIZANDO APLICACION === ')
            break
        else:
            print('opcion no válida')