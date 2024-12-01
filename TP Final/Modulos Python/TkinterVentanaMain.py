import tkinter as tk
from TkinterCliente import funcionCliente
from TkinterProductos import funcionProductos
from TkinterOrdenes import funcionOrdenes

def VentanaMain():
    global ventanaPrincipal
    ventanaPrincipal = tk.Tk()
    ventanaPrincipal.title("Sistema de Gestion de Ventas en Linea")
    ventanaPrincipal.geometry("700x525")
    ventanaPrincipal.config(bg="#9ded91")
    frameBotones = tk.Frame(ventanaPrincipal, bg="#9ded91")
    frameBotones.pack(expand=True)

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
        "width": 16,
        "height": 1,
        "relief": "raised",
        "bd": 3
    }

    botonCliente=tk.Button(frameBotones, text="Menu Clientes", command=funcionCliente, **estiloboton)
    botonCliente.pack(pady=10)
    botonProductos=tk.Button(frameBotones, text="Menu Productos", command=funcionProductos, **estiloboton)
    botonProductos.pack(pady=10)
    botonOrdenes=tk.Button(frameBotones, text="Menu Ordenes",command=funcionOrdenes, **estiloboton)
    botonOrdenes.pack(pady=10)
    botonSalir=tk.Button(ventanaPrincipal, text="Cerrar Programa",command=ventanaPrincipal.destroy, **estilobotonsalir)
    botonSalir.place(relx=0.97, rely=0.97, anchor="se")

    ventanaPrincipal.mainloop()

