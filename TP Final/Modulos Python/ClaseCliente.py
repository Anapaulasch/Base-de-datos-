from ClaseBaseDeDatos import BaseDeDatos

class Cliente:
    def __init__ (self, db:'BaseDeDatos'):
        self.db = db
        
    def agregarCliente(self, dni:int, nombre:str, domicilio:str):
        query = "INSERT INTO Clientes (dni, nombre, domicilio) VALUES (%s, %s, %s)"
        valores = (dni, nombre, domicilio)
        self.db.ejecutar(query, valores)
        return "Cliente agregado con exito."
    
    def eliminarCliente(self, dni):
        query = "DELETE FROM Clientes WHERE dni = %s"
        self.db.ejecutar(query, (dni,))
        return "Cliente(s) eliminado(s) con exito."
    
    def verClientes(self):
        query = "SELECT * FROM Clientes"
        return self.db.obtener_datos(query)
   
    def buscarClientePorDNI(self, dni):
        query = "SELECT * FROM Clientes WHERE dni = %s"
        return self.db.obtener_datos(query, (dni,))
    
    def modificarCliente(self, dni, nombre, domicilio):
        query = "UPDATE Clientes SET nombre=%s, domicilio=%s WHERE dni=%s"
        valores = (nombre, domicilio, dni)
        self.db.ejecutar(query, valores)
        return "Cliente actualizado con exito."
        
    def buscarClientePorNombre(self, nombre):
        query = "SELECT * FROM Clientes WHERE (nombre LIKE %s)"
        valores = (f"%{nombre}%",)
        return self.db.obtener_datos(query, valores)
    
    def verClientesPorMayorGasto(self):
        query = "CALL ClientesQueMasGastaron()"
        return self.db.obtener_datos(query)
    
    def actualizarConexion(self):
        self.db.desconectar()
        self.db.conectar()