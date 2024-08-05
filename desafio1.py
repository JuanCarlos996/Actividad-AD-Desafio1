"""Objetivo: Desarrollar un sistema para manejar productos en un inventario.
Requisitos:
 -Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
 -Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
 -Implementar operaciones CRUD para gestionar productos del inventario.
 -Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
 -Persistir los datos en archivo JSON."""

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
            return cant_stock
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
            "Codigo de barra": self.codbarra,
            "Nombre ": self.nombre,
            "Precio ": self.precio,
            "Cantidad en Stock ": self.cant_stock,
            "Color ": self.color,
            "Garantia ": self.garantia
        }

    def __srt__(self):
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
        data["consumo en Kw"]  = self.consumoKw
        return data
    
    def __str__(self):
        return f"{super().__str__()} - Consumo Kw: {self.consumoKw}"
    
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
        data['Fecha de Vencimiento']  = self.fecha_vencimiento
        return data
    
    def __str__(self):
        return f"{super().__str__()} - Fecha de Vencimiento : {self.fecha_vencimiento}"
    

class GestionarProductos:
    def __init__(self, archivo):
        self.archivo = archivo
    
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

    def crear_producto(self, producto):
        try:
            datos = self.leer_datos() 
            codbarra = producto.codbarra
            if not str(codbarra) in datos.keys():
                datos[codbarra] = producto.to_dict()
                self.guardar_datos(datos)
                print(f"Se guardaron los datos del nuevo producto {codbarra} de nombre {self.nombre }")
            else: 
                print(f'Producto {self.producto} ya existe')
        except Exception as error:
                print(f'Error inesperado al crear Producto: {error}')

    def leer_producto(self, codbarra):
        try:
            datos = self.leer_datos()
            if (codbarra) in datos:
                producto_dato = datos[codbarra]
                if 'consumoKm' in producto_dato:
                    producto = ProductoElectronico(**producto_dato) 
                else:
                    producto = ProductoAlimenticio(**producto_dato)
                print(f'Producto con Cod. de barra {codbarra} econtrado')
            else: print(f'No se encontro producto con el codigo de barra {codbarra}')
        except Exception as e:
            print(f'Error al leer producto: {e}')



    def actualizar_producto(self, codbarra, precio_nuevo):
        try:
            datos = self.leer_datos()
            if str(codbarra) in datos.keys():
                datos[codbarra]['precio']  = precio_nuevo 
                self.guardar_datos(datos) 
                print(f' Precio del Producto Actualizado correctamente ')
            else: print(f' No se encontro producto con el cod Barra {codbarra} ')
        except Exception as e:
            print(f' Error al actualizar producto')


    def eliminar_producto(self, codbarra):
        try:
            datos = self.leer_datos()
            if str(codbarra) in datos.keys():
                del datos[codbarra]
                self.guardar_datos(datos)
                print(f' Producto eliminado correctamente ')
            else: print(f' No se encontro producto con el cod Barra {codbarra} ')
        except Exception as e:
            print(f' Error al eliminar producto')


