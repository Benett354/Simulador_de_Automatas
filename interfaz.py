import tkinter as tk
from tkinter import ttk



class Interfaz:


    def __init__(self):


        self.ventana = tk.Tk()


        self.ventana.title(
            "Simulador de Autómatas"
        )


        self.ventana.geometry(
            "1100x700"
        )


        self.ventana.minsize(
            900,
            600
        )


        self.crear_menu()


        self.crear_interfaz()



    # ---------------------------------
    # Crear menú superior
    # ---------------------------------

    def crear_menu(self):


        barra_menu = tk.Menu(
            self.ventana
        )


        archivo = tk.Menu(
            barra_menu,
            tearoff=0
        )


        archivo.add_command(
            label="Nuevo autómata"
        )


        archivo.add_separator()


        archivo.add_command(
            label="Salir",
            command=self.ventana.destroy
        )


        barra_menu.add_cascade(
            label="Archivo",
            menu=archivo
        )



        herramientas = tk.Menu(
            barra_menu,
            tearoff=0
        )


        herramientas.add_command(
            label="Conversión AFN → AFD"
        )


        herramientas.add_command(
            label="Minimización AFD"
        )


        barra_menu.add_cascade(
            label="Herramientas",
            menu=herramientas
        )



        self.ventana.config(
            menu=barra_menu
        )



    # ---------------------------------
    # Interfaz principal
    # ---------------------------------

    def crear_interfaz(self):


        titulo = tk.Label(
            self.ventana,
            text="SIMULADOR DE AUTÓMATAS",
            font=("Arial",24,"bold")
        )


        titulo.pack(
            pady=15
        )



        subtitulo = tk.Label(
            self.ventana,
            text="AFN - AFD - ε-transiciones - Conversión - Minimización",
            font=("Arial",12)
        )


        subtitulo.pack()



        contenedor = ttk.Frame(
            self.ventana
        )


        contenedor.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )



        # -----------------------------
        # Panel izquierdo
        # -----------------------------


        panel_control = ttk.LabelFrame(
            contenedor,
            text="Control del Autómata"
        )


        panel_control.pack(
            side="left",
            fill="y",
            padx=10
        )



        botones = [

            "Crear Autómata",
            "Estados",
            "Transiciones",
            "Simular Cadena"

        ]



        for texto in botones:


            boton = ttk.Button(
                panel_control,
                text=texto,
                width=25
            )


            boton.pack(
                pady=10,
                padx=15
            )



        # -----------------------------
        # Panel derecho
        # -----------------------------


        panel_resultado = ttk.LabelFrame(
            contenedor,
            text="Información del proceso"
        )


        panel_resultado.pack(
            expand=True,
            fill="both",
            padx=10
        )



        self.area_texto = tk.Text(
            panel_resultado,
            font=("Consolas",12)
        )


        self.area_texto.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )



        self.area_texto.insert(
            "end",
            "Sistema listo...\n"
        )



    # ---------------------------------
    # Ejecutar aplicación
    # ---------------------------------

    def ejecutar(self):

        self.ventana.mainloop()