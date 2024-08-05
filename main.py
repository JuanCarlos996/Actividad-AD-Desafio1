import os
import platform
from desafio1 import ProductoElectronico
from desafio1 import ProductoAlimenticio
from desafio1 import Producto
from desafio1 import GestionarProductos

def limpiar_pantalla():
    '''Limpiar la pantalla '''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')



def mostrar_menu():
    print(" -------Menú principal para gestion de Productos-------------")
    print(' 1- Agregar producto Electronico ')
    print(' 2- Agregar producto alimenticio ')
    print(' 3- Buscar producto por Codigo de barra ')
    print(' 4- Ingresar Codigo de barra para actualizar el producto ')
    print(' 5- Ingresar Codigo de barra para eliminar el producto ')
    print(' 6- Mostrato todos los productos ')
    print(' 7- Salir del programa ')
    print(' *************************************************************** ')


def agregar_producto(gestion, tipo_producto):
    try:
        codbarra = int(input('Ingrese Codigo de barra del Producto: '))
        nombre = input('Ingrese nombre de Producto: ')
        precio = float(input('Ingrese Precio del producto: '))
        cant_stock = int(input('Ingrese cantidad en stock del producto: '))
        color = input('Ingrese color de producto: ')
        garantia = int(input('Ingrese si tiene garantia o no el producto: 1=Si/2=No '))

        if tipo_producto == '1':
            consumoKw = int(input('Ingrese consumo en Kw del producto electronico: '))
            producto = ProductoElectronico(codbarra, nombre, precio, cant_stock, color, garantia, consumoKw)
        elif tipo_producto == '2':
            fecha_vencimiento =int(input('Ingrese fecha de vencimiento del producto en formato ddmmaaaa: '))        
            producto = ProductoAlimenticio(codbarra, nombre, precio, cant_stock, color, garantia, fecha_vencimiento)
        else:
            print('Opcion Invalida')
            return
       
        gestion.crear_producto(producto) 
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e} ')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_producto_por_codbarra(gestion):
    codbarra = int(input ('Ingrese codigo de barra a buscar '))
    gestion.leer_producto(codbarra)
    input('Presione enter para continuar...')

def actualizar_precio_producto(gestion):
    codbarra = input('Ingrese el codigo de barra a actualizar  ')
    precio= float(input('Ingrese el nuevo precio del producto  '))
    gestion.actualizar_producto(codbarra, precio)
    input('Presione enter para continuar...')

def eliminar_producto(gestion):
    codbarra = input('Ingrese el codigo de barra a Eliminar  ')
    gestion.eliminar_producto(codbarra)
    input('Presione enter para continuar...')


def mostrar_los_productos(gestion):
    print('--------------Listado de Productos----------------')
    for producto in gestion.leer_datos().values():
        if 'consumoKw' in producto:
            print(f"{producto['nombre']} - Consumo Kw {producto['consumoKw']}")
        else:
            print(f"{producto['nombre']} - Fecha de Vencimiento {producto['fecha_vencimiento']}")
    input('Presione enter para continuar...')








if __name__ == "__main__":
    archivo_producto = 'Productos_base.json'
    gestion = GestionarProductos(archivo_producto)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_producto(gestion, opcion)
        elif opcion == '3':
            buscar_producto_por_codbarra(gestion)
        elif opcion == '4':
            actualizar_precio_producto(gestion)
        elif opcion == '5':
            eliminar_producto(gestion)
        elif opcion == '6':
            mostrar_los_productos(gestion)
        elif opcion == '7': 
            print('Saliendo del Programa!!')
            break
        else: 
            print('Opción invalida')
