import tkinter as tk
from ClaseCliente import Cliente
from ClaseOrdenes import Ordenes
from ClaseBaseDeDatos import BaseDeDatos
import TkinterVentanaMain
from tkinter import Listbox, messagebox,simpledialog, ttk

def funcionCliente():
    
    global db
    db = BaseDeDatos(host="localhost", user="root", password="hola123", database="tpfinal")
    db.conectar()
    
    orden_db = Ordenes(db)
    cliente_db = Cliente(db)
    
    global ventanaClientes
    ventanaClientes = tk.Tk()
    ventanaClientes.title("Menu Clientes")
    ventanaClientes.geometry("700x525")
    ventanaClientes.config(bg="#9ded91")
    
    #Este if esta para el caso en que se cierra una subventana de MenuClientes y se vuelve a abrir esta ventana 
    #no intente destruir la ventana main que no existe, y si existe que se destruya al abrir la ventana MenuClientes
    #(se usa tambien en los MenuOrdenes)
    if TkinterVentanaMain.ventanaPrincipal is not None and TkinterVentanaMain.ventanaPrincipal.winfo_exists():
        TkinterVentanaMain.ventanaPrincipal.destroy()
        TkinterVentanaMain.ventanaPrincipal = None

    frameBotones = tk.Frame(ventanaClientes, bg="#9ded91")
    frameBotones.pack(expand=True)

    estiloboton={
        "font":("Georgia", 16, "bold"),
        "bg": "#38b325",
        "fg": "white",  # Color de texto
        "activebackground": "#1a6110",  # Fondo al presionar
        "activeforeground": "white",  # Texto al presionar
        "width": 14,
        "height": 1,
        "relief": "raised",
        "bd": 3
    }
    
    estilobotonsalir={
        "font":("Georgia", 16, "bold"),
        "bg": "#ad1524",
        "fg": "white",  # Color de texto
        "activebackground": "#690812",  # Fondo al presionar
        "activeforeground": "white",  # Texto al presionar
        "width": 20,
        "height": 1,
        "relief": "raised",
        "bd": 3
    }

    def mostrarClientes():
         
        ventana = tk.Tk()
        ventana.title("Clientes")
        ventana.config(bg="#9ded91")
        ventana.geometry("700x400")
        
        #Se cierra la ventana anterior para que se vea unicamente la de esta funcion
        ventanaClientes.destroy()
        
        def verTodos():
            #Si hay un treeview con datos de la funcion verMayoresGastos se borra y se crea otro con los de esta funcion
            if hasattr(ventana, 'tree'):
                ventana.tree.destroy()
            ventana.tree=ttk.Treeview(ventana, columns=("DNI", "Nombre", "Domicilio"), show="headings")
            ventana.tree.heading("DNI", text="DNI")
            ventana.tree.heading("Nombre", text="Nombre")
            ventana.tree.heading("Domicilio", text="Domicilio")
            
            ventana.tree.pack(fill="both", expand=True)
                
            for cliente in cliente_db.verClientes():
                ventana.tree.insert("", tk.END, values=(cliente[0], cliente[1], cliente[2]))

        def verMayoresGastos():
            #Si hay un treeview con datos de la funcion verTodos se borra y se crea otro con los de esta funcion
            if hasattr(ventana, 'tree'):            
                ventana.tree.destroy()
            ventana.tree=ttk.Treeview(ventana, columns=("Cliente", "Total Gastado"), show="headings")
            ventana.tree.heading("Cliente", text="Cliente")
            ventana.tree.heading("Total Gastado", text="Total Gastado")
            
            ventana.tree.pack(fill="both", expand=True)
            
            for cliente in cliente_db.verClientesPorMayorGasto():
                ventana.tree.insert("", tk.END, values=(cliente[0], f"${cliente[1]}"))
            cliente_db.actualizarConexion()
            
        def volver():
            #Se cierra esta ventana y se vuelve a abrir la ventana del menuClientes
            ventana.destroy()
            funcionCliente()

        estiloboton2={
            "font":("Georgia", 16, "bold"),
            "bg": "#38b325",
            "fg": "white",  
            "activebackground": "#1a6110",  
            "activeforeground": "white",  
            "width": 27,
            "height": 1,
            "relief": "raised",
            "bd": 3
        }
        
        tk.Button(ventana, text="Ver Todos los Clientes", command=verTodos, **estiloboton2).pack(pady=6)
        tk.Button(ventana, text="Ver Clientes que mas $ Gastaron", command=verMayoresGastos, **estiloboton2).pack(pady=6)
        tk.Button(ventana, text="Volver al Menu Clientes", command=volver, **estilobotonsalir).pack(side=tk.BOTTOM,pady=6)

    def BuscarCliente():
        ventana = tk.Toplevel(ventanaClientes)
        ventana.title("Buscar Cliente por Nombre o Apellido")
        ventana.geometry("360x235")
        ventana.config(bg="#9ded91")
        frameBuscar = tk.Frame(ventana, bg="#9ded91")
        frameBuscar.pack(expand=True)

        tk.Label(frameBuscar, text="Nombre:").grid(row=0, column=0, pady=10)

        nombre = tk.Entry(frameBuscar)
        nombre.grid(row=0, column=1, pady=10)    

        listbox_resultados = tk.Listbox(frameBuscar, width=60)
        listbox_resultados.grid(row=5, column=0, columnspan=2)

        def buscar():
            resultados = cliente_db.buscarClientePorNombre(nombre.get())
            listbox_resultados.delete(0, tk.END)
            for cliente in resultados:
                listbox_resultados.insert(tk.END, f"{cliente[0]}   {cliente[1]}   {cliente[2]}")

        tk.Button(frameBuscar, text="Buscar", command=buscar).grid(row=4, column=0, columnspan=2)

    def AgregarCliente():
        #Se crea una ventana TopLevel con labels y entrys para que el usuario ingrese los datos
        ventana = tk.Toplevel(ventanaClientes)
        ventana.title("Registrar Cliente")

        tk.Label(ventana, text="DNI:").grid(row=0, column=0)
        tk.Label(ventana, text="Nombre Completo:").grid(row=1, column=0)
        tk.Label(ventana, text="Domicilio:").grid(row=2, column=0)

        dni = tk.Entry(ventana)
        nombreCompleto = tk.Entry(ventana)
        domicilio = tk.Entry(ventana)
        

        dni.grid(row=0, column=1)
        nombreCompleto.grid(row=1, column=1)
        domicilio.grid(row=2, column=1)
        
        #Se registra el nuevo cliente
        def registrar():
            msg = cliente_db.agregarCliente(dni.get(), nombreCompleto.get(), domicilio.get())
            messagebox.showinfo("Informacion", msg)
            ventana.destroy()

        tk.Button(ventana, text="Registrar", command=registrar).grid(row=5, column=0, columnspan=2)

    def EliminarCliente():
        ventana = tk.Toplevel(ventanaClientes)
        ventana.title("Clientes")
        
        #Se crea y se ingresan todos los datos en un treeview para que el usuario elija el/los cliente/s a eliminar
        tree=ttk.Treeview(ventana, columns=("DNI", "Nombre", "Domicilio"), show="headings")
        tree.heading("DNI", text="DNI")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Domicilio", text="Domicilio")
        
        tree.pack(fill="both", expand=True)

        clientes=cliente_db.verClientes()
        for cliente in clientes:
            tree.insert("", tk.END, values=(cliente[0], cliente[1], cliente[2]))

        def eliminar():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Seleccionar Cliente", "Debe seleccionar un cliente para eliminar.")
                return
                
            confirmar = messagebox.askyesno("Confirmar Eliminacion", "Esta seguro de que desea eliminar el(los) cliente(s) seleccionado(s)?")
            if not confirmar:
                return
            
            seleccion_lista = list(seleccion)
            
            #Se eliminan los clientes seleccionados
            for item in seleccion_lista:
                valores = tree.item(item, "values")
                if orden_db.buscarOrdenPorCliente(valores[0]) == []:
                    msg = cliente_db.eliminarCliente(valores[0])                    
                    tree.delete(item)
                    messagebox.showinfo("Exito", msg)
                else:
                    messagebox.showwarning("Cliente Invalido", f"El cliente '{valores[1]}' tiene ordenes. No se puede eliminar.")
                
            ventana.destroy()
        
        tk.Button(ventana, text="Confirmar", command=eliminar).pack()
    
    def modificarCliente():
        ventana = tk.Toplevel(ventanaClientes)
        ventana.title("Clientes")
        
        #Se crea y se ingresan todos los datos en un treeview para que el usuario elija el cliente a modificar
        tree=ttk.Treeview(ventana, columns=("DNI", "Nombre", "Domicilio"), show="headings", selectmode="browse")
        tree.heading("DNI", text="DNI")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Domicilio", text="Domicilio")
        
        tree.pack(fill="both", expand=True)

        clientes=cliente_db.verClientes()
        for cliente in clientes:
            tree.insert("", tk.END, values=(cliente[0], cliente[1], cliente[2]))
        
        def actualizar():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Seleccionar Cliente", "Debe seleccionar un cliente para Modificar.")
                return            

            #Se crea una subventana con labels y entrys para que el usuario modifique los datos del cliente
            for item in seleccion:
                valores = tree.item(item, "values")
                
                ventana2 = tk.Toplevel(ventana)
                ventana2.title("Actualizar Cliente")
    
                tk.Label(ventana2, text="Nombre:").grid(row=0, column=0)        
                tk.Label(ventana2, text="Domicilio:").grid(row=1, column=0)
                
                nombre = tk.Entry(ventana2)
                domicilio = tk.Entry(ventana2)
    
                nombre.grid(row=0, column=1)
                domicilio.grid(row=1, column=1)
    
                nombre.insert(0, valores[1])
                domicilio.insert(0, valores[2])

                #Funcion para confirmar y realizar la modificacion
                def confirmar():                    
                    cliente_db.modificarCliente(valores[0], nombre.get(), domicilio.get())                    
                    
                    #Aca se actualizan los datos del treeview para que se vea efectivamente la modificacion realizada.                    
                    tree.delete(*tree.get_children())
                    clientes=cliente_db.verClientes()
                    for cliente in clientes:
                        tree.insert("", tk.END, values=(cliente[0], cliente[1], cliente[2]))
        
                    confirmar = messagebox.askyesno("Confirmar Modificacion", "Esta seguro de que desea modificar el cliente seleccionado?")
                    if not confirmar:
                        return                
                    
                    messagebox.showinfo("Exito", "Cliente modificado con exito.")
                
                tk.Button(ventana2, text="Confirmar", command=confirmar).grid(row=3, column=0, columnspan=2)
               
        tk.Button(ventana, text="Cerrar Ventana", command=ventana.destroy).pack(side=tk.RIGHT, pady=5, padx=5)
        tk.Button(ventana, text="Actualizar", command=actualizar).pack(pady=5)

    tk.Button(frameBotones, text="Ver Clientes", command=mostrarClientes, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Agregar Cliente", command=AgregarCliente, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Buscar Cliente", command=BuscarCliente, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Eliminar Cliente", command=EliminarCliente, **estiloboton).pack(pady=6)
    tk.Button(frameBotones, text="Modificar Cliente", command=modificarCliente, **estiloboton).pack(pady=6)

    tk.Button(ventanaClientes, text="Volver al Menu Principal",command=volverAlMenuPrincipal, **estilobotonsalir).place(relx=0.97, rely=0.97, anchor="se")

    ventanaClientes.mainloop()

def volverAlMenuPrincipal():
    ventanaClientes.destroy()
    TkinterVentanaMain.VentanaMain()
    db.desconectar()