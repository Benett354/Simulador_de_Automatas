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
            label="Conversión AFN → AFD",
            command=self.convertir_afn_afd
        )


        herramientas.add_command(
            label="Minimización AFD",
            command=self.minimizar_afd
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
            font=("Arial", 24, "bold")
        )


        titulo.pack(
            pady=15
        )



        subtitulo = tk.Label(
            self.ventana,
            text="AFN - AFD - ε-transiciones - Conversión - Minimización",
            font=("Arial", 12)
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



        # ---------------------------------
        # Panel izquierdo
        # ---------------------------------

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
            pady=8,
            padx=15
        )



        ttk.Button(
            panel_control,
            text="Transiciones",
            width=25,
            command=self.abrir_transiciones
        ).pack(
            pady=8,
            padx=15
        )



        ttk.Button(
            panel_control,
            text="Simular Cadena",
            width=25,
            command=self.simular_cadena
        ).pack(
            pady=8,
            padx=15
        )



        ttk.Button(
            panel_control,
            text="Ver Autómata",
            width=25,
            command=self.mostrar_automata
        ).pack(
            pady=8,
            padx=15
        )



        ttk.Button(
            panel_control,
            text="Convertir AFN → AFD",
            width=25,
            command=self.convertir_afn_afd
        ).pack(
            pady=8,
            padx=15
        )



        ttk.Button(
            panel_control,
            text="Minimizar AFD",
            width=25,
            command=self.minimizar_afd
        ).pack(
            pady=8,
            padx=15
        )



        # ---------------------------------
        # Cadena
        # ---------------------------------

        marco_cadena = ttk.LabelFrame(
            panel_control,
            text="Cadena"
        )


        marco_cadena.pack(
            pady=15,
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



        # ---------------------------------
        # Panel de información
        # ---------------------------------

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
            font=("Consolas", 12)
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


        self.area_texto.insert(
            "end",
            "============================\n"
        )


        self.area_texto.see(
            "end"
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

            aceptada, recorrido, resultado = (
                simulador.simular_afd(
                    cadena
                )
            )

        else:

            aceptada, recorrido, resultado = (
                simulador.simular_afn(
                    cadena
                )
            )



        self.area_texto.insert(
            "end",
            "\n===== SIMULACIÓN =====\n"
        )


        self.area_texto.insert(
            "end",
            f"Cadena: {cadena}\n\n"
        )


        self.area_texto.insert(
            "end",
            "Recorrido:\n"
        )



        for paso in recorrido:

            self.area_texto.insert(
                "end",
                str(paso) + "\n"
            )



        self.area_texto.insert(
            "end",
            "\nResultado: "
            + resultado
            + "\n"
        )


        self.area_texto.insert(
            "end",
            "======================\n"
        )


        self.area_texto.see(
            "end"
        )



    # ---------------------------------
    # Mostrar autómata
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
    # Convertir AFN -> AFD
    # ---------------------------------

    def convertir_afn_afd(self):

        if self.automata_actual is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear un AFN"
            )

            return



        if self.automata_actual.tipo != "AFN":

            messagebox.showwarning(
                "Advertencia",
                "El autómata actual debe ser un AFN"
            )

            return



        errores = self.automata_actual.validar()


        if errores:

            messagebox.showerror(
                "Error",
                "\n".join(errores)
            )

            return



        try:

            from conversion import ConversionAFN_AFD


            conversion = ConversionAFN_AFD(
                self.automata_actual
            )


            afd = conversion.convertir()



            self.mostrar_tabla_subconjuntos(
                conversion,
                afd
            )



            self.area_texto.insert(
                "end",
                "\n===== CONVERSIÓN AFN → AFD =====\n"
            )


            self.area_texto.insert(
                "end",
                f"Estados: {afd.estados}\n"
            )


            self.area_texto.insert(
                "end",
                f"Inicial: {afd.estado_inicial}\n"
            )


            self.area_texto.insert(
                "end",
                f"Finales: {afd.estados_finales}\n"
            )


            self.area_texto.insert(
                "end",
                "\nTransiciones:\n"
            )



            for (
                origen,
                simbolo
            ), destino in sorted(
                afd.transiciones.items()
            ):

                self.area_texto.insert(
                    "end",
                    f"{origen} --{simbolo}--> {destino}\n"
                )



            self.automata_actual = afd


            self.area_texto.insert(
                "end",
                "\nEl AFD convertido ahora es el autómata actual.\n"
            )


            self.area_texto.see(
                "end"
            )


            messagebox.showinfo(
                "Conversión completada",
                "El AFN fue convertido correctamente a AFD."
            )



        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )



    # ---------------------------------
    # Tabla de subconjuntos
    # ---------------------------------

    def mostrar_tabla_subconjuntos(
        self,
        conversion,
        afd
    ):

        ventana_tabla = tk.Toplevel(
            self.ventana
        )


        ventana_tabla.title(
            "Tabla de Conversión AFN → AFD"
        )


        ventana_tabla.geometry(
            "900x500"
        )



        tk.Label(
            ventana_tabla,
            text="CONSTRUCCIÓN DE SUBCONJUNTOS",
            font=("Arial", 18, "bold")
        ).pack(
            pady=15
        )



        simbolos = sorted(
            afd.alfabeto
        )


        columnas = [
            "estado_afd",
            "subconjunto"
        ] + simbolos



        tabla = ttk.Treeview(
            ventana_tabla,
            columns=columnas,
            show="headings"
        )



        tabla.heading(
            "estado_afd",
            text="Estado AFD"
        )


        tabla.heading(
            "subconjunto",
            text="Subconjunto AFN"
        )



        tabla.column(
            "estado_afd",
            width=100,
            anchor="center"
        )


        tabla.column(
            "subconjunto",
            width=220,
            anchor="center"
        )



        for simbolo in simbolos:

            tabla.heading(
                simbolo,
                text=simbolo
            )

            tabla.column(
                simbolo,
                width=220,
                anchor="center"
            )



        for fila in conversion.obtener_tabla():

            valores = [
                fila["estado_afd"],
                fila["subconjunto"]
            ]


            for simbolo in simbolos:

                valores.append(
                    fila.get(
                        simbolo,
                        "∅"
                    )
                )


            tabla.insert(
                "",
                "end",
                values=valores
            )



        tabla.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )



    # ---------------------------------
    # Minimizar AFD
    # ---------------------------------

    def minimizar_afd(self):

        if self.automata_actual is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero debe crear un AFD"
            )

            return



        if self.automata_actual.tipo != "AFD":

            messagebox.showwarning(
                "Advertencia",
                "El autómata actual debe ser un AFD"
            )

            return



        try:

            from minimizacion import MinimizadorAFD


            minimizador = MinimizadorAFD(
                self.automata_actual
            )


            afd_minimo = minimizador.minimizar()



            # Mostrar proceso
            self.mostrar_proceso_minimizacion(
                minimizador,
                afd_minimo
            )



            self.area_texto.insert(
                "end",
                "\n===== AFD MINIMIZADO =====\n"
            )


            self.area_texto.insert(
                "end",
                f"Estados: {afd_minimo.estados}\n"
            )


            self.area_texto.insert(
                "end",
                f"Inicial: {afd_minimo.estado_inicial}\n"
            )


            self.area_texto.insert(
                "end",
                f"Finales: {afd_minimo.estados_finales}\n"
            )


            self.area_texto.insert(
                "end",
                "\nTransiciones:\n"
            )



            for (
                origen,
                simbolo
            ), destino in sorted(
                afd_minimo.transiciones.items()
            ):

                self.area_texto.insert(
                    "end",
                    f"{origen} --{simbolo}--> {destino}\n"
                )



            self.automata_actual = afd_minimo


            self.area_texto.insert(
                "end",
                "\nEl AFD mínimo ahora es el autómata actual.\n"
            )


            self.area_texto.see(
                "end"
            )


            messagebox.showinfo(
                "Minimización completada",
                "El AFD fue minimizado correctamente."
            )



        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )



    # ---------------------------------
    # Mostrar proceso de minimización
    # ---------------------------------

    def mostrar_proceso_minimizacion(
        self,
        minimizador,
        afd_minimo
    ):

        ventana = tk.Toplevel(
            self.ventana
        )


        ventana.title(
            "Proceso de Minimización"
        )


        ventana.geometry(
            "900x600"
        )



        tk.Label(
            ventana,
            text="MINIMIZACIÓN DEL AFD",
            font=("Arial", 18, "bold")
        ).pack(
            pady=15
        )



        marco_texto = ttk.Frame(
            ventana
        )


        marco_texto.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=10
        )



        texto = tk.Text(
            marco_texto,
            font=("Consolas", 12)
        )


        texto.pack(
            expand=True,
            fill="both"
        )



        pasos = minimizador.obtener_pasos()



        for numero, particion in enumerate(
            pasos
        ):

            texto.insert(
                "end",
                f"P{numero} = "
            )


            grupos = []


            for bloque in particion:

                grupos.append(
                    "{"
                    + ", ".join(
                        sorted(bloque)
                    )
                    + "}"
                )


            texto.insert(
                "end",
                "{ "
                + ", ".join(grupos)
                + " }\n\n"
            )



        texto.insert(
            "end",
            "===== EQUIVALENCIAS =====\n"
        )



        mapeo = minimizador.obtener_mapeo()



        grupos_minimos = {}



        for estado_original, nuevo in mapeo.items():

            if nuevo not in grupos_minimos:

                grupos_minimos[nuevo] = []


            grupos_minimos[nuevo].append(
                estado_original
            )



        for nuevo, originales in sorted(
            grupos_minimos.items()
        ):

            texto.insert(
                "end",
                f"{nuevo} = "
                + "{"
                + ", ".join(
                    sorted(originales)
                )
                + "}\n"
            )



        if minimizador.estado_pozo is not None:

            texto.insert(
                "end",
                "\nSe agregó un estado POZO porque "
                "el AFD no tenía todas sus transiciones definidas.\n"
            )



        texto.insert(
            "end",
            "\n===== AFD MÍNIMO =====\n"
        )


        texto.insert(
            "end",
            f"Estados: {afd_minimo.estados}\n"
        )


        texto.insert(
            "end",
            f"Inicial: {afd_minimo.estado_inicial}\n"
        )


        texto.insert(
            "end",
            f"Finales: {afd_minimo.estados_finales}\n"
        )



    # ---------------------------------
    # Ejecutar
    # ---------------------------------

    def ejecutar(self):

        self.ventana.mainloop()