import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, ttk
from ClaseOrdenes import Ordenes
from ClaseBaseDeDatos import BaseDeDatos
from ClaseProductos import Producto
from ClaseCliente import Cliente
import TkinterVentanaMain

def funcionOrdenes():
    
    global db    
    db = BaseDeDatos("localhost", "root", "hola123", "tpfinal")
    db.conectar()
    orden_db= Ordenes(db)
    producto_db=Producto(db)
    cliente_db=Cliente(db)
    
    if TkinterVentanaMain.ventanaPrincipal is not None and TkinterVentanaMain.ventanaPrincipal.winfo_exists():
        TkinterVentanaMain.ventanaPrincipal.destroy()
        TkinterVentanaMain.ventanaPrincipal = None
   
    global ventanaOrdenes    
    ventanaOrdenes = tk.Tk()
    ventanaOrdenes.title("Gestion de Ordenes")
    ventanaOrdenes.geometry("700x525")
    ventanaOrdenes.config(bg="#9ded91")
    
    estiloboton={
        "font":("Georgia", 16, "bold"),
        "bg": "#38b325",
        "fg": "white",  
        "activebackground": "#1a6110",  
        "activeforeground": "white",  
        "width": 14,
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
    
    def verOrdenes():
        ventana = tk.Toplevel()
        ventana.title("Ver Ordenes")
        ventana.geometry("850x375")
      
        #Se crea y se ingresan todos los datos en un treeview para que el usuario vea las ordenes
        tree=ttk.Treeview(ventana, columns=("ID", "Fecha", "Importe", "Cliente"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Importe", text="Importe")
        tree.heading("Cliente", text="Cliente")
        
        tree.pack(fill="both", expand=True)
    
        for Orden in orden_db.verOrdenes():
            tree.insert("", tk.END, values=(Orden[0], Orden[1], Orden[2], Orden[3]))
           
        def mostrarDetalles():
            #Funcion para mostrar los detalles que faltan ver de la Orden seleccionada (nombre y cantidad de el/los producto/s)
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Seleccionar Ordenes", "Debe seleccionar una orden para ver sus detalles.")
                return

            for item in seleccion:
                valores = tree.item(item, "values")  
                orden_id = valores[0]  
                ventana2 = tk.Toplevel()
                ventana2.title(f"Ver Detalles Orden {orden_id}")
                ventana2.geometry("400x175")
                tree2=ttk.Treeview(ventana2, columns=("Nombre Del Producto", "Cantidad Del Producto"), show="headings")
                tree2.heading("Nombre Del Producto", text="Nombre Del Producto")
                tree2.heading("Cantidad Del Producto", text="Cantidad Del Producto")
                tree2.pack(fill="both", expand=True)                                        

                for orden in orden_db.buscarOrdenPorID(orden_id):
                    tree2.insert("", tk.END, values=(orden[4], orden[5]))

        tk.Button(ventana, text="Cerrar Ventana", command=ventana.destroy).pack(side=tk.RIGHT, pady=5, padx=5)

        tk.Button(ventana, text="Mostrar Detalles", command=mostrarDetalles).pack(side=tk.BOTTOM, pady=5, padx=5)

    def eliminarOrden():
        ventana = tk.Toplevel()
        ventana.title("Eliminar Orden")
        
        #Se crea y se ingresan todos los datos en un treeview para que el usuario vea las ordenes
        tree = ttk.Treeview(ventana, columns=("ID", "Fecha", "Importe", "Dni Del Cliente"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Importe", text="Importe")
        tree.heading("Dni Del Cliente", text="Dni Del Cliente")
            
        tree.pack(fill="both", expand=True)
    
        ordenes = orden_db.verOrdenes()
        for orden in ordenes:
            tree.insert("", tk.END, values=(orden[0], orden[1], orden[2], orden[3]))

        def eliminar_orden():
            #Si se confirma, se elimina la orden seleccionada
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Seleccionar Ordenes", "Debe seleccionar una orden para eliminar.")
                return
                
            confirmar = messagebox.askyesno("Confirmar Eliminacion", "Esta seguro de que desea eliminar la(s) orden(es) seleccionada(s)?")
            if not confirmar:
                return        

            for item in seleccion:
                valores = tree.item(item, "values")  
                orden_db.eliminarOrden(valores[0])                    
                tree.delete(item)
            
            messagebox.showinfo("Exito", "Orden eliminada con exito.")
        
        tk.Button(ventana, text="Confirmar", command=eliminar_orden).pack(pady=5)
        tk.Button(ventana, text="Cerrar Ventana", command=ventana.destroy).pack(side=tk.RIGHT, pady=5, padx=5)
    
    def ingresarOrden():    
        ventana = tk.Toplevel()
        ventana.title("Registrar Orden")

        # Crear un Listbox para mostrar los productos disponibles
        listbox = tk.Listbox(ventana, width=60, selectmode=tk.MULTIPLE)
        listbox.pack()        

        producto_agregar = [] 
        cant = []  
        importe = 0
        
        for producto in producto_db.verProductoOrdenadoPorID():
            listbox.insert(tk.END, f"{producto[0]} - {producto[1]} {producto[2]} {producto[3]}")

        def confirmar_seleccion():
            # Obtener los índices de los productos seleccionados en el Listbox
            seleccionados = listbox.curselection()

            if not seleccionados:
                messagebox.showinfo("Seleccion vacia", "Por favor, selecciona al menos un producto.")
                return

            def pedir_cantidad(index):
                # Llamar recursivamente para pedir cantidades de los productos seleccionados
                if index >= len(seleccionados):
                    messagebox.showinfo("Proceso terminado", "Se han registrado todas las cantidades.")
                    return

                producto = producto_db.verProductoOrdenadoPorID()[seleccionados[index]]  
                producto_agregar.append(producto)  

                # Crear una ventana emergente para ingresar la cantidad del producto seleccionado
                ventana_cantidad = tk.Toplevel(ventana)
                ventana_cantidad.title(f"Cantidad de {producto[1]}")

                label = tk.Label(ventana_cantidad, text=f"Cuantos {producto[1]} deseas comprar?")
                label.pack(padx=20, pady=10)

                cantidad_entry = tk.Entry(ventana_cantidad)
                cantidad_entry.pack(padx=20, pady=5)

                def confirmar_cantidad():
                    # Validar la cantidad ingresada y proceder al siguiente producto
                    cantidad = cantidad_entry.get()
                    if cantidad.isdigit() and int(cantidad) > 0:
                        if int(cantidad) < producto[3]:                            
                            cant.append(int(cantidad))  
                            cantidad_entry.delete(0, tk.END)
                            ventana_cantidad.destroy()
                            messagebox.showinfo("Compra realizada", f"Has comprado {cantidad} {producto[1]}(s).")
                            pedir_cantidad(index + 1)
                        else: 
                            messagebox.showerror("Error", f"Solicito {cantidad} unidades y hay disponibles {producto[3]}.")
                    else:
                        messagebox.showerror("Error", "Por favor, ingresa un numero valido mayor que cero.")
                        
                boton_confirmar = tk.Button(ventana_cantidad, text="Confirmar", command=confirmar_cantidad)
                boton_confirmar.pack(pady=10)

            pedir_cantidad(0)
            
        boton_confirmar_seleccion = tk.Button(ventana, text="Confirmar seleccion", command=confirmar_seleccion)
        boton_confirmar_seleccion.pack(pady=10)

        # Entrada para el DNI del cliente
        tk.Label(ventana, text="DNI:").pack()
        DNI_entry = tk.Entry(ventana)
        DNI_entry.pack()
        DNI = DNI_entry.get()

        def registrarOrden():
            nonlocal importe
            
            DNI = DNI_entry.get()
            
            # Calcular el importe total basado en los productos seleccionados y sus cantidades
            for i in range(len(producto_agregar)):                
                importe += float(producto_db.consultarPrecio(producto_agregar[i][0])[0][0]) * cant[i]            
            
            if not DNI:
                messagebox.showerror("Error", "El DNI es obligatorio.")
                return

            if not producto_agregar or not cant:
                messagebox.showerror("Error", "Debes seleccionar al menos un producto.")
                return
                        
            # Registrar la orden en la base de datos
            orden_db.agregarOrden(producto_agregar, cant, DNI, importe)
            messagebox.showinfo("Exito", "Orden registrada con exito.")
            ventana.destroy()

        tk.Button(ventana, text="Registrar Orden", command=registrarOrden).pack()

            
    frameBotones = tk.Frame(ventanaOrdenes, bg="#9ded91")
    frameBotones.pack(expand=True)
    
    tk.Button(frameBotones, text="Ver Ordenes", command=verOrdenes, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Eliminar Orden", command=eliminarOrden, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Ingresar Orden", command=ingresarOrden, **estiloboton).pack(pady=6)

    tk.Button(ventanaOrdenes, text="Volver al Menu Principal",command=volverAlMenuPrincipal, **estilobotonsalir).place(relx=0.97, rely=0.97, anchor="se")
    
    ventanaOrdenes.mainloop()
    

def volverAlMenuPrincipal():
    ventanaOrdenes.destroy()
    TkinterVentanaMain.VentanaMain()
    db.desconectar()