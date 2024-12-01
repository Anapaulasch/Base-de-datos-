import tkinter as tk
from ClaseProductos import Producto
from ClaseOrdenes import Ordenes
from ClaseBaseDeDatos import BaseDeDatos
import TkinterVentanaMain
from tkinter import messagebox,simpledialog, ttk

def funcionProductos():
    
    global db
    db = BaseDeDatos(host="localhost", user="root", password="hola123", database="tpfinal")
    db.conectar()

    orden_db=Ordenes(db)
    producto_db= Producto(db)
    
    global ventanaProductos
    ventanaProductos = tk.Tk()
    ventanaProductos.title("Menu Productos")
    ventanaProductos.geometry("700x525")
    ventanaProductos.config(bg="#9ded91")
    
    #Aca no se usa el if usado en los otros dos menus porque no se abre ninguna subventana que requiera cerrar esta
    TkinterVentanaMain.ventanaPrincipal.destroy()

    #Frame para contener los botones
    frameBotones = tk.Frame(ventanaProductos, bg="#9ded91")
    frameBotones.pack(expand=True)
    
    #Estilos de los dos tipos de botones que se usan en las ventanas principales
    estiloboton={
        "font":("Georgia", 16, "bold"),
        "bg": "#38b325",
        "fg": "white",  
        "activebackground": "#1a6110",  
        "activeforeground": "white",  
        "width": 24,
        "height": 1,
        "relief": "raised",
        "bd": 3
    }
    
    estilobotonsalir={
        "font":("Georgia", 16, "bold"),
        "bg": "#ad1524",
        "fg": "white",  
        "activebackground": "#690812",  
        "activeforeground": "white",  
        "width": 20,
        "height": 1,
        "relief": "raised",
        "bd": 3
    }

    def AgregarProducto():
        #Se abre una subventana que le pide al usuario entrys de los datos del producto nuevo
        ventana = tk.Toplevel(ventanaProductos)
        ventana.title("Registrar Producto")

        tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
        tk.Label(ventana, text="Precio:").grid(row=1, column=0)
        tk.Label(ventana, text="Unidades en Stock:").grid(row=2, column=0)

        nombre = tk.Entry(ventana)
        precio= tk.Entry(ventana)
        unidadesStock= tk.Entry(ventana)
        
        nombre.grid(row=0, column=1)
        precio.grid(row=1, column=1)
        unidadesStock.grid(row=2, column=1)

        def registrar():
            #Se registran los datos ingresados y se le avisa al usuario
            msg = producto_db.agregarProducto(nombre.get(), precio.get(), unidadesStock.get())
            messagebox.showinfo("Informacion", msg)
            ventana.destroy()

        tk.Button(ventana, text="Registrar", command=registrar).grid(row=5, column=0, columnspan=2)

    def EliminarProducto():
        ventana = tk.Toplevel(ventanaProductos)
        ventana.title("Productos")

        #Se crea y se ingresan todos los datos en un treeview para que el usuario elija el/los producto/s a eliminar
        tree=ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Unidades en Stock"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Precio", text="Precio")
        tree.heading("Unidades en Stock", text="Unidades en Stock")
        
        tree.pack(fill="both", expand=True)

        productos=producto_db.verProductoOrdenadoPorID()
        for producto in productos:
            tree.insert("", tk.END, values=(producto[0], producto[1], producto[2], producto[3]))

        def eliminar():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Seleccionar Producto", "Debe seleccionar un producto para eliminar.")
                return
                
            confirmar = messagebox.askyesno("Confirmar Eliminacion", "Esta seguro de que desea eliminar el(los) producto(s) seleccionado(s)?")
            if not confirmar:
                return
            
            seleccion_lista=list(seleccion)    
            
            #Se eliminan los productos seleccionados
            for item in seleccion_lista:
                valores = tree.item(item, "values")
                if orden_db.buscarOrdenPorProducto(valores[0]) == []:                    
                    msg = producto_db.eliminarProducto(valores[0])                    
                    tree.delete(item)                        
                    messagebox.showinfo("Exito", msg)
                else:
                    messagebox.showwarning("Producto Invalido", f"El Producto '{valores[1]}' esta presente en ordenes. No se puede eliminar.")
                    
            ventana.destroy()
        
        tk.Button(ventana, text="Confirmar", command=eliminar).pack()

    def modificarProducto():
        ventana = tk.Toplevel(ventanaProductos)
        ventana.title("Productos")

        #Se crea y se ingresan todos los datos en un treeview para que el usuario elija el producto a modificar        
        tree=ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Unidades en Stock"), show="headings", selectmode="browse")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Precio", text="Precio")
        tree.heading("Unidades en Stock", text="Unidades en Stock")
        
        tree.pack(fill="both", expand=True)

        productos=producto_db.verProductoOrdenadoPorID()
        for producto in productos:
            tree.insert("", tk.END, values=(producto[0], producto[1], producto[2], producto[3]))
        
        def actualizar():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Seleccionar Producto", "Debe seleccionar un producto para Modificar.")
                return            

            #Se crea una subventana con labels y entrys para que el usuario modifique los datos del cliente            
            for item in seleccion:
                valores = tree.item(item, "values")
                
                ventana2 = tk.Toplevel(ventana)
                ventana2.title("Actualizar Producto")
    
                tk.Label(ventana2, text="Nombre:").grid(row=0, column=0)        
                tk.Label(ventana2, text="Precio:").grid(row=1, column=0)
                tk.Label(ventana2, text="Unidades En Stock:").grid(row=2, column=0)
                
                nombre = tk.Entry(ventana2)
                precio= tk.Entry(ventana2)
                unidadesStock= tk.Entry(ventana2)
    
                nombre.grid(row=0, column=1)
                precio.grid(row=1, column=1)
                unidadesStock.grid(row=2, column=1)
    
                nombre.insert(0, valores[1])
                precio.insert(0, valores[2])
                unidadesStock.insert(0, valores[3])        

                #Funcion para confirmar y realizar la modificacion
                def confirmar():
    
                    producto_db.modificarProducto(valores[0], nombre.get(), precio.get(), unidadesStock.get())                    

                    #Aca se actualizan los datos del treeview para que se vea efectivamente la modificacion realizada.                    
                    tree.delete(*tree.get_children())
                    productos=producto_db.verProductoOrdenadoPorID()
                    for producto in productos:
                        tree.insert("", tk.END, values=(producto[0], producto[1], producto[2], producto[3]))
    
                    confirmar = messagebox.askyesno("Confirmar Modificacion", "Esta seguro de que desea modificar el producto seleccionado?")
                    if not confirmar:
                        return                
                    
                    messagebox.showinfo("Exito", "Producto modificado con exito.")
                
                tk.Button(ventana2, text="Confirmar", command=confirmar).grid(row=3, column=0, columnspan=2)
               
        tk.Button(ventana, text="Cerrar Ventana", command=ventana.destroy).pack(side=tk.RIGHT, pady=5, padx=5)
        tk.Button(ventana, text="Actualizar", command=actualizar).pack(pady=5)
        
    def mostrarProductos():
        ventana = tk.Toplevel(ventanaProductos)
        ventana.title("Productos")
        ventana.geometry("800x400")
        
        #Se crea un treeview para que ingresar los datos
        tree=ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Unidades en Stock"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Precio", text="Precio")
        tree.heading("Unidades en Stock", text="Unidades en Stock")
        
        tree.pack(fill="both", expand=True)        

        def ordenPorID():
            #Se borran los datos del treeview y se vuelven a ingresar ordenados por id.
            tree.delete(*tree.get_children())
            for producto in producto_db.verProductoOrdenadoPorID():
                tree.insert("", tk.END, values=(producto[0], producto[1], producto[2], producto[3]))
        
        def ordenPorPrecio():
            #Se borran los datos del treeview y se vuelven a ingresar ordenados por precio.
            tree.delete(*tree.get_children())
            for producto in producto_db.verProductoOrdenadoPorPrecio():
                tree.insert("", tk.END, values=(producto[0], producto[1], producto[2], producto[3]))
        
        def ordenPorStock():
            #Se borran los datos del treeview y se vuelven a ingresar ordenados por stock disponible.
            tree.delete(*tree.get_children())
            for producto in producto_db.verProductoOrdenadoPorStock():
                tree.insert("", tk.END, values=(producto[0], producto[1], producto[2], producto[3]))

        #Por defecto los datos se ingresan ordenados por id
        ordenPorID()

        frame_botones = tk.Frame(ventana)
        frame_botones.pack(side=tk.BOTTOM, pady=10)
        label = tk.Label(ventana, text="Ordenar por:")
        label.pack(side=tk.BOTTOM, padx= 15)
        tk.Button(frame_botones, text="ID", command=ordenPorID).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Precio", command=ordenPorPrecio).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Stock Disponible", command=ordenPorStock).pack(side=tk.LEFT, padx=5)

    def mostrarProductosMasVendidos():
        
        ventana = tk.Toplevel(ventanaProductos)
        ventana.title("Productos Mas Vendidos")
        ventana.geometry("600x300")
        
        #Se crea un treeview para ingresar los datos
        tree=ttk.Treeview(ventana, columns=("ID", "Nombre", "Cantidad Vendida"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Cantidad Vendida", text="Cantidad Vendida")
        
        tree.pack(fill="both", expand=True)
        
        #Se ingresan los 5 productos mas vendidos, ordenados de manera descendente
        for producto in producto_db.buscarProductosMasVendidos():
            tree.insert("", tk.END, values=(producto[0], producto[1], producto[2]))
        
        producto_db.actualizarConexion()
        
        tk.Button(ventana, text="Cerrar Ventana", command=ventana.destroy).pack(side=tk.RIGHT, pady=5, padx=5)

    tk.Button(frameBotones, text="Agregar Producto", command=AgregarProducto, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Ver Productos", command=mostrarProductos, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Ver Productos mas Vendidos", command=mostrarProductosMasVendidos, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Eliminar Producto", command=EliminarProducto, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Modificar Producto", command=modificarProducto, **estiloboton).pack(pady=6)

    tk.Button(ventanaProductos, text="Volver al Menu Principal",command=volverAlMenuPrincipal, **estilobotonsalir).place(relx=0.97, rely=0.97, anchor="se")
    
def volverAlMenuPrincipal():
    ventanaProductos.destroy()
    TkinterVentanaMain.VentanaMain()
    db.desconectar()