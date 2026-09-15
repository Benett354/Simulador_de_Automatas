import tkinter as tk
from tkinter import ttk, messagebox


class Interfaz:


    def __init__(self):

        # =================================================
        # COLORES DEL SISTEMA
        # =================================================

        self.COLOR_FONDO = "#F4F6F8"
        self.COLOR_PANEL = "#FFFFFF"

        self.COLOR_PRINCIPAL = "#1F3A5F"
        self.COLOR_SECUNDARIO = "#3C5A7A"

        self.COLOR_TEXTO = "#1E293B"
        self.COLOR_TEXTO_SECUNDARIO = "#64748B"

        self.COLOR_BORDE = "#D6DCE5"

        self.COLOR_EXITO = "#2E7D32"
        self.COLOR_ERROR = "#C62828"

        self.COLOR_PANEL_SUAVE = "#EEF2F7"

        # =================================================
        # VENTANA PRINCIPAL
        # =================================================

        self.ventana = tk.Tk()

        self.ventana.title(
            "Simulador de Autómatas"
        )

        self.ventana.geometry(
            "1200x760"
        )

        self.ventana.minsize(
            1000,
            650
        )

        self.ventana.configure(
            bg=self.COLOR_FONDO
        )

        # Autómata actualmente cargado
        self.automata_actual = None

        # Barra de estado
        self.estado_sistema = tk.StringVar()

        self.estado_sistema.set(
            "Sin autómata cargado"
        )

        # Configurar estilos
        self.configurar_estilos()

        # Crear elementos
        self.crear_menu()
        self.crear_interfaz()


    # =====================================================
    # CONFIGURAR ESTILOS
    # =====================================================

    def configurar_estilos(self):

        self.estilo = ttk.Style()

        self.estilo.theme_use(
            "clam"
        )

        # ---------------------------------
        # Frames
        # ---------------------------------

        self.estilo.configure(
            "Fondo.TFrame",
            background=self.COLOR_FONDO
        )

        self.estilo.configure(
            "Panel.TFrame",
            background=self.COLOR_PANEL
        )

        # ---------------------------------
        # LabelFrames
        # ---------------------------------

        self.estilo.configure(
            "Panel.TLabelframe",
            background=self.COLOR_PANEL,
            bordercolor=self.COLOR_BORDE,
            borderwidth=1,
            relief="solid"
        )

        self.estilo.configure(
            "Panel.TLabelframe.Label",
            background=self.COLOR_PANEL,
            foreground=self.COLOR_PRINCIPAL,
            font=("Arial", 11, "bold")
        )

        # ---------------------------------
        # Etiquetas
        # ---------------------------------

        self.estilo.configure(
            "Normal.TLabel",
            background=self.COLOR_FONDO,
            foreground=self.COLOR_TEXTO,
            font=("Arial", 10)
        )

        self.estilo.configure(
            "Panel.TLabel",
            background=self.COLOR_PANEL,
            foreground=self.COLOR_TEXTO,
            font=("Arial", 10)
        )

        self.estilo.configure(
            "Secundaria.TLabel",
            background=self.COLOR_PANEL,
            foreground=self.COLOR_TEXTO_SECUNDARIO,
            font=("Arial", 9)
        )

        # ---------------------------------
        # Botón principal
        # ---------------------------------

        self.estilo.configure(
            "Primary.TButton",
            background=self.COLOR_PRINCIPAL,
            foreground="white",
            borderwidth=0,
            padding=(12, 9),
            font=("Arial", 10, "bold")
        )

        self.estilo.map(
            "Primary.TButton",
            background=[
                ("active", self.COLOR_SECUNDARIO),
                ("pressed", self.COLOR_PRINCIPAL)
            ],
            foreground=[
                ("active", "white")
            ]
        )

        # ---------------------------------
        # Botón secundario
        # ---------------------------------

        self.estilo.configure(
            "Secondary.TButton",
            background="#E6EBF1",
            foreground=self.COLOR_PRINCIPAL,
            borderwidth=1,
            padding=(12, 9),
            font=("Arial", 10, "bold")
        )

        self.estilo.map(
            "Secondary.TButton",
            background=[
                ("active", "#D6DFE9")
            ],
            foreground=[
                ("active", self.COLOR_PRINCIPAL)
            ]
        )

        # ---------------------------------
        # Botón verde
        # ---------------------------------

        self.estilo.configure(
            "Success.TButton",
            background=self.COLOR_EXITO,
            foreground="white",
            borderwidth=0,
            padding=(12, 9),
            font=("Arial", 10, "bold")
        )

        self.estilo.map(
            "Success.TButton",
            background=[
                ("active", "#256628")
            ],
            foreground=[
                ("active", "white")
            ]
        )

        # ---------------------------------
        # Treeview
        # ---------------------------------

        self.estilo.configure(
            "Treeview",
            background="white",
            foreground=self.COLOR_TEXTO,
            fieldbackground="white",
            rowheight=30,
            font=("Arial", 10)
        )

        self.estilo.configure(
            "Treeview.Heading",
            background=self.COLOR_PRINCIPAL,
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=6
        )

        self.estilo.map(
            "Treeview.Heading",
            background=[
                ("active", self.COLOR_SECUNDARIO)
            ]
        )


    # =====================================================
    # CONTROL DE VENTANAS MODALES
    # =====================================================

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


    # =====================================================
    # MENÚ SUPERIOR
    # =====================================================

    def crear_menu(self):

        barra_menu = tk.Menu(
            self.ventana
        )

        # ---------------------------------
        # Archivo
        # ---------------------------------

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

        # ---------------------------------
        # Herramientas
        # ---------------------------------

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


    # =====================================================
    # INTERFAZ PRINCIPAL
    # =====================================================

    def crear_interfaz(self):

        # =================================================
        # ENCABEZADO
        # =================================================

        encabezado = tk.Frame(
            self.ventana,
            bg=self.COLOR_PRINCIPAL,
            height=100
        )

        encabezado.pack(
            fill="x"
        )

        encabezado.pack_propagate(
            False
        )

        # ---------------------------------
        # Título
        # ---------------------------------

        marco_titulo = tk.Frame(
            encabezado,
            bg=self.COLOR_PRINCIPAL
        )

        marco_titulo.pack(
            side="left",
            padx=30,
            pady=16
        )

        tk.Label(
            marco_titulo,
            text="SIMULADOR DE AUTÓMATAS",
            font=("Arial", 23, "bold"),
            bg=self.COLOR_PRINCIPAL,
            fg="white"
        ).pack(
            anchor="w"
        )

        tk.Label(
            marco_titulo,
            text="AFD  •  AFN  •  ε-transiciones  •  Conversión  •  Minimización",
            font=("Arial", 10),
            bg=self.COLOR_PRINCIPAL,
            fg="#D9E2EC"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # ---------------------------------
        # Indicador derecho
        # ---------------------------------

        tk.Label(
            encabezado,
            text="Autómatas y Lenguajes Formales",
            font=("Arial", 10, "bold"),
            bg=self.COLOR_PRINCIPAL,
            fg="#D9E2EC"
        ).pack(
            side="right",
            padx=30
        )

        # =================================================
        # CONTENEDOR GENERAL
        # =================================================

        contenedor = ttk.Frame(
            self.ventana,
            style="Fondo.TFrame"
        )

        contenedor.pack(
            expand=True,
            fill="both",
            padx=22,
            pady=20
        )

        # =================================================
        # PANEL IZQUIERDO
        # =================================================

        panel_izquierdo = tk.Frame(
            contenedor,
            bg=self.COLOR_PANEL,
            highlightbackground=self.COLOR_BORDE,
            highlightthickness=1,
            width=260
        )

        panel_izquierdo.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        panel_izquierdo.pack_propagate(
            False
        )

        # ---------------------------------
        # Título lateral
        # ---------------------------------

        tk.Label(
            panel_izquierdo,
            text="CONTROL",
            font=("Arial", 11, "bold"),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_PRINCIPAL
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        tk.Label(
            panel_izquierdo,
            text="Administración del autómata",
            font=("Arial", 9),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ---------------------------------
        # Crear
        # ---------------------------------

        ttk.Button(
            panel_izquierdo,
            text="Crear Autómata",
            style="Primary.TButton",
            command=self.abrir_formulario
        ).pack(
            fill="x",
            padx=18,
            pady=5
        )

        # ---------------------------------
        # Transiciones
        # ---------------------------------

        ttk.Button(
            panel_izquierdo,
            text="Administrar Transiciones",
            style="Secondary.TButton",
            command=self.abrir_transiciones
        ).pack(
            fill="x",
            padx=18,
            pady=5
        )

        # ---------------------------------
        # Visualizar
        # ---------------------------------

        ttk.Button(
            panel_izquierdo,
            text="Ver Autómata",
            style="Secondary.TButton",
            command=self.mostrar_automata
        ).pack(
            fill="x",
            padx=18,
            pady=5
        )

        # ---------------------------------
        # Separador
        # ---------------------------------

        ttk.Separator(
            panel_izquierdo,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=18,
            pady=15
        )

        # ---------------------------------
        # Herramientas
        # ---------------------------------

        tk.Label(
            panel_izquierdo,
            text="HERRAMIENTAS",
            font=("Arial", 11, "bold"),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_PRINCIPAL
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        ttk.Button(
            panel_izquierdo,
            text="Convertir AFN → AFD",
            style="Secondary.TButton",
            command=self.convertir_afn_afd
        ).pack(
            fill="x",
            padx=18,
            pady=5
        )

        ttk.Button(
            panel_izquierdo,
            text="Minimizar AFD",
            style="Secondary.TButton",
            command=self.minimizar_afd
        ).pack(
            fill="x",
            padx=18,
            pady=5
        )

        # ---------------------------------
        # Cadena
        # ---------------------------------

        ttk.Separator(
            panel_izquierdo,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=18,
            pady=15
        )

        tk.Label(
            panel_izquierdo,
            text="SIMULACIÓN",
            font=("Arial", 11, "bold"),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_PRINCIPAL
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        tk.Label(
            panel_izquierdo,
            text="Cadena a evaluar",
            font=("Arial", 9),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=20
        )

        self.entrada_cadena = tk.Entry(
            panel_izquierdo,
            font=("Arial", 11),
            bg="white",
            fg=self.COLOR_TEXTO,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDE,
            highlightcolor=self.COLOR_PRINCIPAL
        )

        self.entrada_cadena.pack(
            fill="x",
            padx=18,
            pady=(6, 3),
            ipady=7
        )

        tk.Label(
            panel_izquierdo,
            text="Campo vacío = cadena ε",
            font=("Arial", 8),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 7)
        )

        ttk.Button(
            panel_izquierdo,
            text="Simular Cadena",
            style="Success.TButton",
            command=self.simular_cadena
        ).pack(
            fill="x",
            padx=18,
            pady=5
        )

        # ---------------------------------
        # Limpiar
        # ---------------------------------

        ttk.Button(
            panel_izquierdo,
            text="Limpiar Panel",
            style="Secondary.TButton",
            command=self.limpiar_panel
        ).pack(
            fill="x",
            padx=18,
            pady=(15, 5)
        )

        # =================================================
        # PANEL DERECHO
        # =================================================

        panel_derecho = tk.Frame(
            contenedor,
            bg=self.COLOR_PANEL,
            highlightbackground=self.COLOR_BORDE,
            highlightthickness=1
        )

        panel_derecho.pack(
            side="left",
            expand=True,
            fill="both"
        )

        # ---------------------------------
        # Encabezado del panel
        # ---------------------------------

        encabezado_panel = tk.Frame(
            panel_derecho,
            bg=self.COLOR_PANEL_SUAVE,
            height=55
        )

        encabezado_panel.pack(
            fill="x"
        )

        encabezado_panel.pack_propagate(
            False
        )

        tk.Label(
            encabezado_panel,
            text="INFORMACIÓN DEL PROCESO",
            font=("Arial", 11, "bold"),
            bg=self.COLOR_PANEL_SUAVE,
            fg=self.COLOR_PRINCIPAL
        ).pack(
            side="left",
            padx=18
        )

        tk.Label(
            encabezado_panel,
            text="Resultados, recorridos y procedimientos",
            font=("Arial", 9),
            bg=self.COLOR_PANEL_SUAVE,
            fg=self.COLOR_TEXTO_SECUNDARIO
        ).pack(
            side="right",
            padx=18
        )

        # ---------------------------------
        # Área texto
        # ---------------------------------

        marco_texto = tk.Frame(
            panel_derecho,
            bg=self.COLOR_PANEL
        )

        marco_texto.pack(
            expand=True,
            fill="both",
            padx=12,
            pady=12
        )

        scroll_texto = ttk.Scrollbar(
            marco_texto
        )

        scroll_texto.pack(
            side="right",
            fill="y"
        )

        self.area_texto = tk.Text(
            marco_texto,
            font=("Consolas", 11),
            bg="#FBFCFD",
            fg=self.COLOR_TEXTO,
            insertbackground=self.COLOR_PRINCIPAL,
            relief="flat",
            bd=0,
            wrap="word",
            padx=15,
            pady=15,
            yscrollcommand=scroll_texto.set
        )

        self.area_texto.pack(
            expand=True,
            fill="both"
        )

        scroll_texto.config(
            command=self.area_texto.yview
        )

        # ---------------------------------
        # Etiquetas del Text
        # ---------------------------------

        self.area_texto.tag_configure(
            "titulo",
            foreground=self.COLOR_PRINCIPAL,
            font=("Consolas", 11, "bold")
        )

        self.area_texto.tag_configure(
            "aceptada",
            foreground=self.COLOR_EXITO,
            font=("Consolas", 11, "bold")
        )

        self.area_texto.tag_configure(
            "rechazada",
            foreground=self.COLOR_ERROR,
            font=("Consolas", 11, "bold")
        )

        self.area_texto.tag_configure(
            "secundario",
            foreground=self.COLOR_TEXTO_SECUNDARIO
        )

        self.area_texto.insert(
            "end",
            "Sistema listo.\n",
            "titulo"
        )

        self.area_texto.insert(
            "end",
            "Cree un autómata para comenzar.\n",
            "secundario"
        )

        # =================================================
        # BARRA DE ESTADO
        # =================================================

        barra_estado = tk.Frame(
            self.ventana,
            bg=self.COLOR_PRINCIPAL,
            height=30
        )

        barra_estado.pack(
            side="bottom",
            fill="x"
        )

        barra_estado.pack_propagate(
            False
        )

        tk.Label(
            barra_estado,
            textvariable=self.estado_sistema,
            bg=self.COLOR_PRINCIPAL,
            fg="white",
            font=("Arial", 9),
            anchor="w"
        ).pack(
            fill="both",
            padx=15
        )


    # =====================================================
    # ABRIR FORMULARIO
    # =====================================================

    def abrir_formulario(self):

        if self.hay_ventana_modal():
            return

        if self.automata_actual is not None:

            respuesta = messagebox.askyesno(
                "Nuevo autómata",
                (
                    "Actualmente existe un autómata cargado.\n\n"
                    "¿Desea reemplazarlo?"
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


    # =====================================================
    # RECIBIR AUTÓMATA
    # =====================================================

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
                f"Autómata actual: {automata.tipo}   |   "
                f"Estados: {len(automata.estados)}"
            )
        )

        self.area_texto.insert(
            "end",
            "\n===== AUTÓMATA CREADO =====\n",
            "titulo"
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


    # =====================================================
    # TRANSICIONES
    # =====================================================

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


    # =====================================================
    # SIMULAR CADENA
    # =====================================================

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
            "\n===== SIMULACIÓN =====\n",
            "titulo"
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


    # =====================================================
    # MOSTRAR AUTÓMATA
    # =====================================================

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


    # =====================================================
    # CONVERSIÓN AFN -> AFD
    # =====================================================

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

            self.mostrar_tabla_subconjuntos(
                conversion,
                afd
            )

            self.area_texto.insert(
                "end",
                "\n===== CONVERSIÓN AFN → AFD =====\n",
                "titulo"
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
                    f"Autómata actual: AFD convertido   |   "
                    f"Estados: {len(afd.estados)}"
                )
            )

            self.area_texto.insert(
                "end",
                "\nEl AFD convertido ahora es el autómata actual.\n",
                "secundario"
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


    # =====================================================
    # TABLA DE SUBCONJUNTOS
    # =====================================================

    def mostrar_tabla_subconjuntos(
        self,
        conversion,
        afd
    ):

        ventana_tabla = tk.Toplevel(
            self.ventana
        )

        ventana_tabla.title(
            "Conversión AFN → AFD"
        )

        ventana_tabla.geometry(
            "950x540"
        )

        ventana_tabla.configure(
            bg=self.COLOR_FONDO
        )

        ventana_tabla.transient(
            self.ventana
        )

        ventana_tabla.grab_set()

        # ---------------------------------
        # Encabezado
        # ---------------------------------

        encabezado = tk.Frame(
            ventana_tabla,
            bg=self.COLOR_PRINCIPAL,
            height=80
        )

        encabezado.pack(
            fill="x"
        )

        encabezado.pack_propagate(
            False
        )

        tk.Label(
            encabezado,
            text="CONSTRUCCIÓN DE SUBCONJUNTOS",
            font=("Arial", 17, "bold"),
            bg=self.COLOR_PRINCIPAL,
            fg="white"
        ).pack(
            pady=(15, 2)
        )

        tk.Label(
            encabezado,
            text="Conversión automática de AFN a AFD",
            font=("Arial", 9),
            bg=self.COLOR_PRINCIPAL,
            fg="#D9E2EC"
        ).pack()

        simbolos = sorted(
            afd.alfabeto
        )

        columnas = [
            "estado_afd",
            "subconjunto"
        ] + simbolos

        marco_tabla = tk.Frame(
            ventana_tabla,
            bg=self.COLOR_PANEL
        )

        marco_tabla.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

        tabla = ttk.Treeview(
            marco_tabla,
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
            width=120,
            anchor="center"
        )

        tabla.column(
            "subconjunto",
            width=250,
            anchor="center"
        )

        for simbolo in simbolos:

            tabla.heading(
                simbolo,
                text=f"Símbolo {simbolo}"
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
            fill="both"
        )

        ttk.Button(
            ventana_tabla,
            text="Cerrar",
            style="Primary.TButton",
            command=ventana_tabla.destroy
        ).pack(
            pady=(0, 18)
        )

        ventana_tabla.focus_force()

        ventana_tabla.wait_window()


    # =====================================================
    # MINIMIZACIÓN
    # =====================================================

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
                "\n===== AFD MINIMIZADO =====\n",
                "titulo"
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
                    f"Autómata actual: AFD mínimo   |   "
                    f"Estados: {len(afd_minimo.estados)}"
                )
            )

            self.area_texto.insert(
                "end",
                "\nEl AFD mínimo ahora es el autómata actual.\n",
                "secundario"
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


    # =====================================================
    # MOSTRAR PROCESO DE MINIMIZACIÓN
    # =====================================================

    def mostrar_proceso_minimizacion(
        self,
        minimizador,
        afd_minimo
    ):

        ventana = tk.Toplevel(
            self.ventana
        )

        ventana.title(
            "Minimización del AFD"
        )

        ventana.geometry(
            "900x620"
        )

        ventana.configure(
            bg=self.COLOR_FONDO
        )

        ventana.transient(
            self.ventana
        )

        ventana.grab_set()

        # ---------------------------------
        # Encabezado
        # ---------------------------------

        encabezado = tk.Frame(
            ventana,
            bg=self.COLOR_PRINCIPAL,
            height=80
        )

        encabezado.pack(
            fill="x"
        )

        encabezado.pack_propagate(
            False
        )

        tk.Label(
            encabezado,
            text="MINIMIZACIÓN DEL AFD",
            font=("Arial", 17, "bold"),
            bg=self.COLOR_PRINCIPAL,
            fg="white"
        ).pack(
            pady=(15, 2)
        )

        tk.Label(
            encabezado,
            text="Refinamiento de particiones",
            font=("Arial", 9),
            bg=self.COLOR_PRINCIPAL,
            fg="#D9E2EC"
        ).pack()

        # ---------------------------------
        # Texto
        # ---------------------------------

        marco = tk.Frame(
            ventana,
            bg=self.COLOR_PANEL,
            highlightbackground=self.COLOR_BORDE,
            highlightthickness=1
        )

        marco.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

        texto = tk.Text(
            marco,
            font=("Consolas", 11),
            bg="#FBFCFD",
            fg=self.COLOR_TEXTO,
            relief="flat",
            padx=15,
            pady=15
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
                    "el AFD no tenía todas las transiciones definidas.\n"
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
            style="Primary.TButton",
            command=ventana.destroy
        ).pack(
            pady=(0, 18)
        )

        ventana.focus_force()

        ventana.wait_window()


    # =====================================================
    # LIMPIAR PANEL
    # =====================================================

    def limpiar_panel(self):

        self.area_texto.delete(
            "1.0",
            "end"
        )

        self.area_texto.insert(
            "end",
            "Panel limpiado.\n",
            "titulo"
        )

        if self.automata_actual is not None:

            self.area_texto.insert(
                "end",
                (
                    f"Autómata actual: "
                    f"{self.automata_actual.tipo}\n"
                ),
                "secundario"
            )


    # =====================================================
    # EJECUTAR
    # =====================================================

    def ejecutar(self):

        self.ventana.mainloop()