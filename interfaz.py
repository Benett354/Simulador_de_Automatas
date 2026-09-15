import tkinter as tk
from tkinter import ttk, messagebox


class Interfaz:


    def __init__(self):

        self.ventana = tk.Tk()

        self.ventana.title(
            "Simulador de Autómatas"
        )

        self.ventana.geometry(
            "1150x720"
        )

        self.ventana.minsize(
            950,
            620
        )

        self.automata_actual = None

        # Texto de estado inferior
        self.estado_sistema = tk.StringVar()

        self.estado_sistema.set(
            "Sin autómata cargado"
        )

        self.crear_menu()

        self.crear_interfaz()


    # ---------------------------------
    # ¿Hay ventana modal?
    # ---------------------------------

    def hay_ventana_modal(self):

        actual = self.ventana.grab_current()

        if (
            actual is not None
            and actual != self.ventana
        ):

            try:

                actual.lift()
                actual.focus_force()

            except tk.TclError:

                pass

            return True

        return False


    # ---------------------------------
    # Menú
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
    # Interfaz
    # ---------------------------------

    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="SIMULADOR DE AUTÓMATAS",
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            pady=(15, 5)
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
            pady=15
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
            padx=(0, 10)
        )

        ttk.Button(
            panel_control,
            text="Crear Autómata",
            width=25,
            command=self.abrir_formulario
        ).pack(
            pady=7,
            padx=15
        )

        ttk.Button(
            panel_control,
            text="Transiciones",
            width=25,
            command=self.abrir_transiciones
        ).pack(
            pady=7,
            padx=15
        )

        ttk.Button(
            panel_control,
            text="Simular Cadena",
            width=25,
            command=self.simular_cadena
        ).pack(
            pady=7,
            padx=15
        )

        ttk.Button(
            panel_control,
            text="Ver Autómata",
            width=25,
            command=self.mostrar_automata
        ).pack(
            pady=7,
            padx=15
        )

        ttk.Separator(
            panel_control,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=15,
            pady=8
        )

        ttk.Button(
            panel_control,
            text="Convertir AFN → AFD",
            width=25,
            command=self.convertir_afn_afd
        ).pack(
            pady=7,
            padx=15
        )

        ttk.Button(
            panel_control,
            text="Minimizar AFD",
            width=25,
            command=self.minimizar_afd
        ).pack(
            pady=7,
            padx=15
        )

        # Cadena
        marco_cadena = ttk.LabelFrame(
            panel_control,
            text="Cadena a evaluar"
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
            pady=(10, 3)
        )

        ttk.Label(
            marco_cadena,
            text="Vacío = cadena ε"
        ).pack(
            pady=(0, 8)
        )

        ttk.Button(
            panel_control,
            text="Limpiar panel",
            width=25,
            command=self.limpiar_panel
        ).pack(
            pady=7,
            padx=15
        )

        # ---------------------------------
        # Panel derecho
        # ---------------------------------

        panel_resultado = ttk.LabelFrame(
            contenedor,
            text="Información del proceso"
        )

        panel_resultado.pack(
            expand=True,
            fill="both"
        )

        scroll_texto = ttk.Scrollbar(
            panel_resultado
        )

        scroll_texto.pack(
            side="right",
            fill="y"
        )

        self.area_texto = tk.Text(
            panel_resultado,
            font=("Consolas", 11),
            yscrollcommand=scroll_texto.set
        )

        self.area_texto.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        scroll_texto.config(
            command=self.area_texto.yview
        )

        self.area_texto.tag_configure(
            "aceptada",
            foreground="green"
        )

        self.area_texto.tag_configure(
            "rechazada",
            foreground="red"
        )

        self.area_texto.insert(
            "end",
            "Sistema listo...\n"
        )

        # ---------------------------------
        # Barra de estado
        # ---------------------------------

        barra_estado = ttk.Label(
            self.ventana,
            textvariable=self.estado_sistema,
            relief="sunken",
            anchor="w"
        )

        barra_estado.pack(
            side="bottom",
            fill="x"
        )


    # ---------------------------------
    # Crear/Nuevo autómata
    # ---------------------------------

    def abrir_formulario(self):

        if self.hay_ventana_modal():

            return

        if self.automata_actual is not None:

            respuesta = messagebox.askyesno(
                "Nuevo autómata",
                (
                    "Ya existe un autómata cargado.\n\n"
                    "¿Desea reemplazarlo por uno nuevo?"
                ),
                parent=self.ventana
            )

            if not respuesta:

                return

        from formulario import FormularioAutomata

        FormularioAutomata(
            self.ventana,
            self.recibir_automata
        )


    # ---------------------------------
    # Recibir autómata
    # ---------------------------------

    def recibir_automata(
        self,
        automata
    ):

        self.automata_actual = automata

        self.entrada_cadena.delete(
            0,
            "end"
        )

        self.estado_sistema.set(
            (
                f"Autómata actual: {automata.tipo} | "
                f"{len(automata.estados)} estados"
            )
        )

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
            f"Estados: {sorted(automata.estados)}\n"
        )

        self.area_texto.insert(
            "end",
            f"Alfabeto: {sorted(automata.alfabeto)}\n"
        )

        self.area_texto.insert(
            "end",
            f"Inicial: {automata.estado_inicial}\n"
        )

        self.area_texto.insert(
            "end",
            f"Finales: {sorted(automata.estados_finales)}\n"
        )

        self.area_texto.insert(
            "end",
            "============================\n"
        )

        self.area_texto.see(
            "end"
        )


    # ---------------------------------
    # Transiciones
    # ---------------------------------

    def abrir_transiciones(self):

        if self.hay_ventana_modal():

            return

        if self.automata_actual is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero cree un autómata.",
                parent=self.ventana
            )

            return

        from transiciones import VentanaTransiciones

        VentanaTransiciones(
            self.ventana,
            self.automata_actual
        )


    # ---------------------------------
    # Simular
    # ---------------------------------

    def simular_cadena(self):

        if self.hay_ventana_modal():

            return

        if self.automata_actual is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero cree un autómata.",
                parent=self.ventana
            )

            return

        # IMPORTANTE:
        # "" es una cadena válida.
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

        if cadena == "":

            self.area_texto.insert(
                "end",
                "Cadena: ε (cadena vacía)\n\n"
            )

        else:

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
        )

        if aceptada:

            self.area_texto.insert(
                "end",
                resultado + "\n",
                "aceptada"
            )

        else:

            self.area_texto.insert(
                "end",
                resultado + "\n",
                "rechazada"
            )

        self.area_texto.insert(
            "end",
            "======================\n"
        )

        self.area_texto.see(
            "end"
        )


    # ---------------------------------
    # Ver autómata
    # ---------------------------------

    def mostrar_automata(self):

        if self.hay_ventana_modal():

            return

        if self.automata_actual is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero cree un autómata.",
                parent=self.ventana
            )

            return

        from dibujador import DibujadorAutomata

        DibujadorAutomata(
            self.ventana,
            self.automata_actual
        )


    # ---------------------------------
    # Conversión
    # ---------------------------------

    def convertir_afn_afd(self):

        if self.hay_ventana_modal():

            return

        if self.automata_actual is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero cree un AFN.",
                parent=self.ventana
            )

            return

        if self.automata_actual.tipo != "AFN":

            messagebox.showwarning(
                "Advertencia",
                "El autómata actual debe ser un AFN.",
                parent=self.ventana
            )

            return

        errores = self.automata_actual.validar()

        if errores:

            messagebox.showerror(
                "Error",
                "\n".join(
                    errores
                ),
                parent=self.ventana
            )

            return

        try:

            from conversion import ConversionAFN_AFD

            conversion = ConversionAFN_AFD(
                self.automata_actual
            )

            afd = conversion.convertir()

            # Mostrar tabla de conversión.
            # Esperamos a que se cierre.
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
                f"Estados: {sorted(afd.estados)}\n"
            )

            self.area_texto.insert(
                "end",
                f"Inicial: {afd.estado_inicial}\n"
            )

            self.area_texto.insert(
                "end",
                f"Finales: {sorted(afd.estados_finales)}\n"
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

            self.estado_sistema.set(
                (
                    f"Autómata actual: AFD convertido | "
                    f"{len(afd.estados)} estados"
                )
            )

            self.area_texto.insert(
                "end",
                "\nEl AFD convertido ahora es el autómata actual.\n"
            )

            self.area_texto.see(
                "end"
            )

            messagebox.showinfo(
                "Conversión completada",
                "El AFN fue convertido correctamente a AFD.",
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
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

        ventana_tabla.transient(
            self.ventana
        )

        ventana_tabla.grab_set()

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
            pady=15
        )

        ttk.Button(
            ventana_tabla,
            text="Cerrar",
            command=ventana_tabla.destroy
        ).pack(
            pady=10
        )

        ventana_tabla.focus_force()

        # Bloquea la conversión hasta cerrar
        ventana_tabla.wait_window()


    # ---------------------------------
    # Minimización
    # ---------------------------------

    def minimizar_afd(self):

        if self.hay_ventana_modal():

            return

        if self.automata_actual is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero cree un AFD.",
                parent=self.ventana
            )

            return

        if self.automata_actual.tipo != "AFD":

            messagebox.showwarning(
                "Advertencia",
                "El autómata actual debe ser un AFD.",
                parent=self.ventana
            )

            return

        try:

            from minimizacion import MinimizadorAFD

            minimizador = MinimizadorAFD(
                self.automata_actual
            )

            afd_minimo = minimizador.minimizar()

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
                f"Estados: {sorted(afd_minimo.estados)}\n"
            )

            self.area_texto.insert(
                "end",
                f"Inicial: {afd_minimo.estado_inicial}\n"
            )

            self.area_texto.insert(
                "end",
                f"Finales: {sorted(afd_minimo.estados_finales)}\n"
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

            self.estado_sistema.set(
                (
                    f"Autómata actual: AFD mínimo | "
                    f"{len(afd_minimo.estados)} estados"
                )
            )

            self.area_texto.insert(
                "end",
                "\nEl AFD mínimo ahora es el autómata actual.\n"
            )

            self.area_texto.see(
                "end"
            )

            messagebox.showinfo(
                "Minimización completada",
                "El AFD fue minimizado correctamente.",
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )


    # ---------------------------------
    # Proceso de minimización
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

        ventana.transient(
            self.ventana
        )

        ventana.grab_set()

        tk.Label(
            ventana,
            text="MINIMIZACIÓN DEL AFD",
            font=("Arial", 18, "bold")
        ).pack(
            pady=15
        )

        texto = tk.Text(
            ventana,
            font=("Consolas", 12)
        )

        texto.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=10
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

                grupos_minimos[
                    nuevo
                ] = []

            grupos_minimos[
                nuevo
            ].append(
                estado_original
            )

        for nuevo, originales in sorted(
            grupos_minimos.items()
        ):

            texto.insert(
                "end",
                (
                    f"{nuevo} = "
                    + "{"
                    + ", ".join(
                        sorted(originales)
                    )
                    + "}\n"
                )
            )

        if minimizador.estado_pozo is not None:

            texto.insert(
                "end",
                (
                    "\nSe agregó un estado POZO porque "
                    "el AFD no tenía todas sus transiciones.\n"
                )
            )

        texto.insert(
            "end",
            "\n===== AFD MÍNIMO =====\n"
        )

        texto.insert(
            "end",
            f"Estados: {sorted(afd_minimo.estados)}\n"
        )

        texto.insert(
            "end",
            f"Inicial: {afd_minimo.estado_inicial}\n"
        )

        texto.insert(
            "end",
            f"Finales: {sorted(afd_minimo.estados_finales)}\n"
        )

        ttk.Button(
            ventana,
            text="Cerrar",
            command=ventana.destroy
        ).pack(
            pady=10
        )

        ventana.focus_force()

        ventana.wait_window()


    # ---------------------------------
    # Limpiar panel
    # ---------------------------------

    def limpiar_panel(self):

        self.area_texto.delete(
            "1.0",
            "end"
        )

        self.area_texto.insert(
            "end",
            "Panel limpiado.\n"
        )


    # ---------------------------------
    # Ejecutar
    # ---------------------------------

    def ejecutar(self):

        self.ventana.mainloop()