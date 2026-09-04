import tkinter as tk
from tkinter import ttk, messagebox



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


        self.automata_actual = None


        self.crear_menu()


        self.crear_interfaz()



    # ---------------------------------
    # Menú superior
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
            label="Nuevo autómata",
            command=self.abrir_formulario
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



        panel_control = ttk.LabelFrame(
            contenedor,
            text="Control del Autómata"
        )


        panel_control.pack(
            side="left",
            fill="y",
            padx=10
        )



        ttk.Button(
            panel_control,
            text="Crear Autómata",
            width=25,
            command=self.abrir_formulario
        ).pack(
            pady=10,
            padx=15
        )



        ttk.Button(
            panel_control,
            text="Transiciones",
            width=25,
            command=self.abrir_transiciones
        ).pack(
            pady=10,
            padx=15
        )



        ttk.Button(
            panel_control,
            text="Simular Cadena",
            width=25,
            command=self.simular_cadena
        ).pack(
            pady=10,
            padx=15
        )



        ttk.Button(
            panel_control,
            text="Ver Autómata",
            width=25,
            command=self.mostrar_automata
        ).pack(
            pady=10,
            padx=15
        )



        marco_cadena = ttk.LabelFrame(
            panel_control,
            text="Cadena"
        )


        marco_cadena.pack(
            pady=20,
            padx=10
        )



        self.entrada_cadena = tk.Entry(
            marco_cadena,
            width=25
        )


        self.entrada_cadena.pack(
            padx=10,
            pady=10
        )



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
    # Abrir formulario
    # ---------------------------------

    def abrir_formulario(self):


        from formulario import FormularioAutomata


        FormularioAutomata(
            self.ventana,
            self.recibir_automata
        )



    # ---------------------------------
    # Recibir autómata
    # ---------------------------------

    def recibir_automata(self, automata):


        self.automata_actual = automata


        self.area_texto.insert(
            "end",
            "\n===== AUTÓMATA CREADO =====\n"
        )


        self.area_texto.insert(
            "end",
            f"Tipo: {automata.tipo}\n"
        )


        self.area_texto.insert(
            "end",
            f"Estados: {automata.estados}\n"
        )


        self.area_texto.insert(
            "end",
            f"Alfabeto: {automata.alfabeto}\n"
        )


        self.area_texto.insert(
            "end",
            f"Inicial: {automata.estado_inicial}\n"
        )


        self.area_texto.insert(
            "end",
            f"Finales: {automata.estados_finales}\n"
        )



    # ---------------------------------
    # Abrir transiciones
    # ---------------------------------

    def abrir_transiciones(self):


        if self.automata_actual is None:


            messagebox.showwarning(
                "Advertencia",
                "Primero cree un autómata"
            )


            return



        from transiciones import VentanaTransiciones


        VentanaTransiciones(
            self.ventana,
            self.automata_actual
        )



    # ---------------------------------
    # Simular cadena
    # ---------------------------------

    def simular_cadena(self):


        if self.automata_actual is None:


            messagebox.showwarning(
                "Advertencia",
                "Primero cree un autómata"
            )


            return



        cadena = self.entrada_cadena.get()



        from simulador import Simulador



        simulador = Simulador(
            self.automata_actual
        )



        if self.automata_actual.tipo == "AFD":


            aceptada, recorrido, resultado = simulador.simular_afd(
                cadena
            )

        else:


            aceptada, recorrido, resultado = simulador.simular_afn(
                cadena
            )



        self.area_texto.insert(
            "end",
            "\n===== SIMULACIÓN =====\n"
        )


        for paso in recorrido:


            self.area_texto.insert(
                "end",
                str(paso)+"\n"
            )


        self.area_texto.insert(
            "end",
            "\nResultado: "
            + resultado
            + "\n"
        )



    # ---------------------------------
    # Mostrar dibujo del autómata
    # ---------------------------------

    def mostrar_automata(self):


        if self.automata_actual is None:


            messagebox.showwarning(
                "Advertencia",
                "Primero cree un autómata"
            )


            return



        from dibujador import DibujadorAutomata



        DibujadorAutomata(
            self.ventana,
            self.automata_actual
        )



    # ---------------------------------
    # Ejecutar
    # ---------------------------------

    def ejecutar(self):

        self.ventana.mainloop()