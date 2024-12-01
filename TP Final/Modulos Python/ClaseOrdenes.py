from ClaseBaseDeDatos import BaseDeDatos
from datetime import datetime
from ClaseProductos import Producto


class Ordenes:
    def __init__ (self, db:'BaseDeDatos'):
        self.db = db

    def agregarOrden(self, productos:list, cantidad, dni, importe):
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO Ordenes (fecha, importe, dni) VALUES (%s, %s, %s)"
        valores=(fecha, importe, dni)
        self.db.ejecutar(query, valores)
        id_orden = self.db.cursor.lastrowid
        producto=Producto(self.db)
        for i in range(len(productos)):            
            query = "INSERT INTO orden_producto (id_orden, id_producto, cantidad) VALUES (%s, %s, %s)"
            valores = (id_orden, productos[i][0], cantidad[i])
            producto.modificarProducto(productos[i][0],productos[i][1],productos[i][2], productos[i][3]-cantidad[i])
            self.db.ejecutar(query, valores)
        return "Orden agregada con éxito."
    
    def eliminarOrden(self, id_orden):        
        query = "DELETE FROM Ordenes WHERE id_orden = %s"
        self.db.ejecutar(query, (id_orden,))
        return "Orden eliminada con éxito."
    
    def verOrdenes(self):
        query = "SELECT o.id_orden, o.fecha, o.importe, c.nombre FROM Ordenes o INNER JOIN Clientes c ON o.dni = c.dni ORDER BY o.id_orden;"
        return self.db.obtener_datos(query) 
    
    def buscarOrdenPorCliente(self, dni):        
        query = "SELECT dni FROM Ordenes WHERE dni = %s"
        return self.db.obtener_datos(query, (dni,))
    
    def buscarOrdenPorProducto(self, id_producto):        
        query = "SELECT id_producto FROM Orden_producto WHERE id_producto = %s"
        return self.db.obtener_datos(query, (id_producto,))

    def buscarOrdenPorID(self, id_orden):        
        query = "SELECT o.fecha, o.importe, o.dni, op.id_producto, p.nombre, op.cantidad FROM Ordenes o JOIN orden_producto op ON o.id_orden = op.id_orden JOIN Productos p ON op.id_producto = p.id_producto WHERE o.id_orden = %s"
        return self.db.obtener_datos(query, (id_orden,))
    
    def sumarOrdenes(self):
        query = "SELECT dni, SUM(importe) FROM Ordenes GROUP BY dni"
        return self.db.obtener_datos(query)                             