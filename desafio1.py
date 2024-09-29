"""Objetivo: Desarrollar un sistema para manejar productos en un inventario.
Requisitos:
 -Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
 -Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
 -Implementar operaciones CRUD para gestionar productos del inventario.
 -Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
 -Persistir los datos en archivo JSON."""


import mysql.connector 
from mysql.connector import Error 
from decouple import config
import json
class Producto:
    def __init__(self, codbarra, nombre, precio, cant_stock, color, garantia):
        self.__codbarra = self.validar_codigo(codbarra)
        self.__nombre = nombre
        self.__precio = self.validar_precio(precio)
        self.__cant_stock = self.validar_stock(cant_stock)
        self.__color = color
        self.__garantia = garantia
    
    @property
    def codbarra(self):
        return self.__codbarra   
    @property
    def nombre(self):
        return self.__nombre.capitalize() 
    @property
    def precio(self):
        return self.__precio   
    @property
    def cant_stock(self):
        return self.__cant_stock  
    @property
    def color(self):
        return self.__color  
    @property
    def garantia(self):
        return self.__garantia   
    
    @precio.setter 
    def precio(self, precio_nuevo):
        self._precio = self.validar_precio(precio_nuevo)

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError('El precio es menor a 0')
            return precio_num
        except ValueError:
            raise ValueError('El precio no puede ser menor a 0')

    @cant_stock.setter
    def cant_stock(self, stock_nuevo):
        self.__cant_stock = self.validar_stock(stock_nuevo)
    
    def validar_stock(self, cant_stock):
        try:
            stock_nuevo = int(cant_stock)
            if stock_nuevo < 0 :
                raise ValueError('El cantidad en stock no puede ser negativo')
            return stock_nuevo
        except ValueError:
            raise ValueError('El cantidad en stock no valido')
    
    @codbarra.setter
    def codbarra(self, cod_nuevo):
        self.__codbarra = self.validar_codigo(cod_nuevo)
    
    def validar_codigo(self, codbarra):
        try:
            cod_nuevo = int(codbarra)
            if cod_nuevo < 1:
                raise ValueError('El codigo no es valido')
            return codbarra
        except ValueError:
            raise ValueError('El codigo ingresado no es correcto')


    def to_dict(self):
        return {
            "codbarra": self.codbarra,
            "nombre": self.nombre,
            "precio": self.precio,
            "cant_stock": self.cant_stock,
            "color": self.color,
            "garantia": self.garantia
        }

    def __str__(self):
        return f"{self.codbarra} {self.nombre}"
    

class ProductoElectronico(Producto):
    def __init__(self, codbarra, nombre, precio, cant_stock, color, garantia, consumoKw):
        super().__init__(codbarra, nombre, precio, cant_stock, color, garantia)
        self.__consumoKw = self.validar_consumo(consumoKw)

    @property
    def consumoKw(self):
        return self.__consumoKw
    
    @consumoKw.setter
    def consumoKw(self, consumo_nuev):
        self.__consumoKw = self.validar_consumo(consumo_nuev)

    def validar_consumo(self, consumoKw):
        try:
            consumo_nuev = int(consumoKw)
            if consumo_nuev <= 0:
                raise ValueError('El consumo de Kw es menor a 0')
            return consumo_nuev
        except ValueError:
            raise ValueError('El consumo en Kw no puede ser menor a 0 o no es prod. electrico')
        
    def to_dict(self):
        data = super().to_dict()
        data["consumoKw"]  = self.consumoKw
        return data

    def __str__(self):
        return f"{super().__str__()} - consumoKw: {self.consumoKw}"
    
class ProductoAlimenticio(Producto):
    def __init__(self, codbarra, nombre, precio, cant_stock, color, garantia, fecha_vencimiento):
        super().__init__(codbarra, nombre, precio, cant_stock, color, garantia)
        self.__fecha_vencimiento = self.validarFecha(fecha_vencimiento)

    @property
    def fecha_vencimiento(self):
        return self.__fecha_vencimiento
    
    @fecha_vencimiento.setter
    def fecha_vencimiento(self, fecha_nueva):
        self.__fecha_vencimiento = self.validarFecha(fecha_nueva)
    
    def validarFecha(self, fecha_vencimiento):
        try:
            fecha_nueva = int(fecha_vencimiento)
            if len(str(fecha_nueva)) < 8:
                raise ValueError('Fecha incorrecta')
            return fecha_nueva
        except ValueError:
            raise ValueError('Fecha ingresada erronea, error de {error}')
        
    def to_dict(self): 
        data = super().to_dict()
        data['fecha_vencimiento']  = self.fecha_vencimiento
        return data
    
    def __str__(self):
        return f"{super().__str__()} - fecha_vencimiento : {self.fecha_vencimiento}"
    

class GestionarProductos:
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password= config('DB_PASSWORD')
        self.port = config('DB_PORT') 

    def connect(self):
        '''establecer una conexion con la base de datos'''
        try:
            connection = mysql.connector.connect(
                host= self.host,
                database= self.database,
                user= self.user,
                password= self.password,
                port= self.port
            )
            if connection.is_connected():
                return connection
            
        except Error as e:
            print(f'Error al conectar la base de datos: {e}')
            return None
  ####



    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4) 
        except IOError as error:
            print(f'Error al guardar datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error de...: {error}') 
 #####
    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:  #permite aplicar comandos en la base
                    # Verificar si el cod de barra ya existe
                    cursor.execute('SELECT codbarra FROM productos WHERE codbarra = %s', (producto.codbarra,))
                    if cursor.fetchone():
                        print(f'Error: ya existe un Producto con el CODBARRA {producto.codbarra}')
                        return
                                    
                    #Insertar producto dependiendo del tipo
                    if isinstance(producto, ProductoElectronico):
                        query = '''
                        INSERT INTO productos (codbarra, nombre, precio, cant_stock, color, garantia) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codbarra, producto.nombre, producto.precio, producto.cant_stock, producto.color, producto.garantia)) 
                       
                        query = ''' 
                         INSERT INTO productoElectronico (codbarra, consumoKw )
                         VALUES (%s, %s)
                         '''
                        cursor.execute(query, (producto.codbarra, producto.consumoKw ))
                    elif isinstance(producto, ProductoAlimenticio):
                        query = '''
                        INSERT INTO productos (codbarra, nombre, precio, cant_stock, color, garantia) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codbarra, producto.nombre, producto.precio, producto.cant_stock, producto.color, producto.garantia)) 
                       
                        query = ''' 
                         INSERT INTO productoAlimenticio (codbarra, fecha_vencimiento )
                         VALUES (%s, %s)
                         '''
                        cursor.execute(query, (producto.codbarra, producto.fecha_vencimiento ))

                    connection.commit()
                    print(f'Producto {producto.nombre} creado con exito!')

        except Exception as error:
                print(f'Error inesperado al crear Producto: {error}')

    def leer_producto(self, codbarra):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM productos WHERE codbarra = %s', (codbarra,))
                    producto_data = cursor.fetchone()
                  
                    if producto_data:
                        cursor.execute('SELECT consumoKw FROM productoelectronico WHERE codbarra = %s', (codbarra, ))
                        consumoKw = cursor.fetchone()
                        if consumoKw: 
                            producto_data['consumoKw'] = consumoKw['consumoKw']
                            producto = ProductoElectronico(**producto_data)
                        else: 
                            cursor.execute('SELECT fecha_vencimiento FROM productoalimenticio WHERE codbarra = %s', (codbarra,))
                            fecha_vencimiento = cursor.fetchone()
                            if fecha_vencimiento:
                                producto_data['fecha_vencimiento'] = fecha_vencimiento ['fecha_vencimiento']
                                producto = ProductoAlimenticio(**producto_data)
                            else: 
                                producto = Producto(**producto_data)
                        print(f'Producto encontrado: {producto}') 
            else:
                print(f'No se encontró producto con el cod de barra {codbarra}')
       
        except Error as e:
            print('Error al leer producto: {e}')
        finally: 
            if connection.is_connected():
                connection.close()



    def actualizar_producto(self, codbarra, precio_nuevo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM productos WHERE codbarra = %s', (codbarra,))
                    if not cursor.fetchone():
                        print(f'No se encontro el producto con el codBarra ingresado {codbarra}')
                        return
                    
                    cursor.execute('UPDATE productos SET precio = %s WHERE codbarra = %s', (precio_nuevo, codbarra))
                    if cursor.rowcount > 0:   #cuenta las filas
                        connection.commit()
                        print(f'El precio del producto indicado se ah actualizado {codbarra}')
                    else:
                        print(f'El precio del producto indicado no se encontró {codbarra}')
        except Exception as e:
            print(f' Error al actualizar producto: {e}')
        finally: 
            if connection.is_connected():
                connection.close()
    


    def eliminar_producto(self, codbarra):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM productos WHERE codbarra = %s', (codbarra,))
                    if not cursor.fetchone():
                        print(f'No se encontro el producto con el codigo de barra {codbarra}')
                        return
                    
                    cursor.execute('DELETE FROM productoalimenticio WHERE codbarra = %s', (codbarra,))
                    cursor.execute('DELETE FROM productoelectronico WHERE codbarra = %s', (codbarra,))
                    cursor.execute('DELETE FROM productos WHERE codbarra = %s', (codbarra,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'El producto se ELIMINÓ correctamente. Su codigo de barra {codbarra}')
                    else: 
                        print(f'No se encontro el producto {codbarra}')
        except Exception as e:
            print(f' Error al eliminar producto')
        finally: 
            if connection.is_connected():
                connection.close()


    def leer_todos_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM productos')
                    productos_data = cursor.fetchall()

                    productos = []

                    for producto_data in productos_data:
                        codbarra = producto_data['codbarra']

                        cursor.execute('SELECT consumoKw FROM productoelectronico WHERE codbarra = %s', (codbarra,))
                        consumoKw = cursor.fetchone()
                        if consumoKw:
                            producto_data['consumoKw'] = consumoKw['consumoKw'] 
                            producto = ProductoElectronico(**producto_data)
                        else:
                            cursor.execute('SELECT fecha_vencimiento FROM  productoalimenticio WHERE codbarra = %s', (codbarra,))
                            fecha_vencimiento = cursor.fetchone()
                            producto_data['fecha_vencimiento'] = fecha_vencimiento['fecha_vencimiento']
                            producto = ProductoAlimenticio(**producto_data)

                        productos.append(producto)  

        except Exception as e:
            print(f'Error al buscar productos {e}')
        else: return productos
        finally:
              if connection.is_connected():
                connection.close()


