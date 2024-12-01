from ClaseBaseDeDatos import BaseDeDatos

class Producto:
    def __init__ (self, db: 'BaseDeDatos'):
        self.db = db
        
    def agregarProducto(self, nombre: str, precio: float, unidadesStock: int):
        query = "INSERT INTO Productos (nombre, precio, unidades_stock) VALUES (%s, %s, %s)"
        valores = (nombre, precio, unidadesStock)
        self.db.ejecutar(query, valores)
        return "Producto agregado con exito."
    
    def eliminarProducto(self, id):
        query = "DELETE FROM Productos WHERE id_producto = %s"
        self.db.ejecutar(query, (id,))
        return "Producto(s) eliminado(s) con exito."
    
    def verProductoOrdenadoPorID(self):
        query = "SELECT * FROM Productos ORDER BY id_producto ASC"
        return self.db.obtener_datos(query)
    
    def verProductoOrdenadoPorStock(self):
        query = "SELECT * FROM Productos ORDER BY unidades_stock DESC"
        return self.db.obtener_datos(query)
    
    def verProductoOrdenadoPorPrecio(self):
        query = "SELECT * FROM Productos ORDER BY precio DESC"
        return self.db.obtener_datos(query)
        
    def modificarProducto(self, id, nombre, precio, unidadesStock):
        query = "UPDATE Productos SET nombre=%s, precio=%s, unidades_stock=%s WHERE id_producto=%s"
        valores = (nombre, precio, unidadesStock, id)
        self.db.ejecutar(query, valores)
        return "Producto actualizado con exito."
    
    def consultarPrecio(self, id_producto):
        query = "SELECT precio FROM Productos WHERE (id_producto LIKE %s)"        
        return self.db.obtener_datos(query, (id_producto,))
    
    def buscarProductoPorNombre(self, nombre):
        query = "SELECT * FROM Productos WHERE (nombre LIKE %s)"
        return self.db.obtener_datos(query, (nombre,))
    
    def buscarProductoPorID(self, id_producto):
        query = "SELECT * FROM Productos WHERE id_producto = %s"
        return self.db.obtener_datos(query, (id_producto,))

    def buscarProductosMasVendidos(self):
        query = "CALL BuscarProductosMasVendidos()"
        return self.db.obtener_datos(query)

    def actualizarConexion(self):
        self.db.desconectar()
        self.db.conectar()