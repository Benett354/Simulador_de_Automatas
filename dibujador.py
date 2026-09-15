import tkinter as tk
from tkinter import ttk
import math


class DibujadorAutomata:


    def __init__(
        self,
        ventana_padre,
        automata
    ):

        self.automata = automata

        self.radio_estado = 38
        self.posiciones = {}

        # ---------------------------------
        # PALETA DE COLORES
        # ---------------------------------

        self.color_fondo_ventana = "#F4F6F8"
        self.color_fondo_canvas = "#FAFBFC"
        self.color_principal = "#1F3A5F"
        self.color_secundario = "#3C5A7A"
        self.color_texto = "#1E293B"
        self.color_borde_suave = "#D6DCE5"
        self.color_estado = "#FFFFFF"
        self.color_estado_final = "#2E7D32"
        self.color_etiqueta = "#EEF2F7"
        self.color_inicio = "#C62828"

        # ---------------------------------
        # VENTANA
        # ---------------------------------

        self.ventana = tk.Toplevel(
            ventana_padre
        )

        self.ventana.title(
            "Visualización del Autómata"
        )

        self.ventana.geometry(
            "1050x700"
        )

        self.ventana.minsize(
            800,
            550
        )

        self.ventana.configure(
            bg=self.color_fondo_ventana
        )

        self.ventana.transient(
            ventana_padre
        )

        self.ventana.grab_set()

        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar
        )

        # ---------------------------------
        # ESTILOS ttk
        # ---------------------------------

        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        self.estilo.configure(
            "Custom.TFrame",
            background=self.color_fondo_ventana
        )

        self.estilo.configure(
            "Custom.TLabel",
            background=self.color_fondo_ventana,
            foreground=self.color_texto,
            font=("Arial", 11)
        )

        self.estilo.configure(
            "Titulo.TLabel",
            background=self.color_fondo_ventana,
            foreground=self.color_principal,
            font=("Arial", 16, "bold")
        )

        self.estilo.configure(
            "Custom.TButton",
            font=("Arial", 10, "bold"),
            foreground="white",
            background=self.color_principal,
            borderwidth=0,
            padding=8
        )

        self.estilo.map(
            "Custom.TButton",
            background=[
                ("active", self.color_secundario)
            ]
        )

        # ---------------------------------
        # BARRA SUPERIOR
        # ---------------------------------

        barra = ttk.Frame(
            self.ventana,
            style="Custom.TFrame"
        )

        barra.pack(
            fill="x",
            padx=12,
            pady=12
        )

        ttk.Label(
            barra,
            text="DIAGRAMA DEL AUTÓMATA",
            style="Titulo.TLabel"
        ).pack(
            side="left",
            padx=8
        )

        ttk.Button(
            barra,
            text="Actualizar diagrama",
            style="Custom.TButton",
            command=self.actualizar
        ).pack(
            side="right",
            padx=5
        )

        ttk.Button(
            barra,
            text="Cerrar",
            style="Custom.TButton",
            command=self.cerrar
        ).pack(
            side="right",
            padx=5
        )

        self.etiqueta_info = ttk.Label(
            barra,
            text="",
            style="Custom.TLabel"
        )

        self.etiqueta_info.pack(
            side="right",
            padx=20
        )

        # ---------------------------------
        # MARCO CANVAS
        # ---------------------------------

        marco_canvas = ttk.Frame(
            self.ventana,
            style="Custom.TFrame"
        )

        marco_canvas.pack(
            expand=True,
            fill="both",
            padx=12,
            pady=(0, 12)
        )

        scroll_y = ttk.Scrollbar(
            marco_canvas,
            orient="vertical"
        )
        scroll_y.pack(
            side="right",
            fill="y"
        )

        scroll_x = ttk.Scrollbar(
            marco_canvas,
            orient="horizontal"
        )
        scroll_x.pack(
            side="bottom",
            fill="x"
        )

        self.canvas = tk.Canvas(
            marco_canvas,
            background=self.color_fondo_canvas,
            highlightthickness=1,
            highlightbackground=self.color_borde_suave,
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        self.canvas.pack(
            expand=True,
            fill="both"
        )

        scroll_x.config(
            command=self.canvas.xview
        )
        scroll_y.config(
            command=self.canvas.yview
        )

        self.canvas.bind(
            "<Configure>",
            self.al_redimensionar
        )

        self.ventana.after(
            100,
            self.actualizar
        )

        self.ventana.focus_force()

    # =====================================================
    # REDIMENSIONAR
    # =====================================================

    def al_redimensionar(self, evento):

        if evento.width > 200 and evento.height > 200:

            if hasattr(self, "_evento_redibujar"):

                try:
                    self.ventana.after_cancel(
                        self._evento_redibujar
                    )
                except tk.TclError:
                    pass

            self._evento_redibujar = self.ventana.after(
                120,
                self.actualizar
            )

    # =====================================================
    # ACTUALIZAR
    # =====================================================

    def actualizar(self):

        self.canvas.delete("all")

        self.etiqueta_info.config(
            text=(
                f"Tipo: {self.automata.tipo}   |   "
                f"Estados: {len(self.automata.estados)}"
            )
        )

        if not self.automata.estados:

            ancho = max(
                self.canvas.winfo_width(),
                700
            )
            alto = max(
                self.canvas.winfo_height(),
                450
            )

            self.canvas.create_text(
                ancho / 2,
                alto / 2,
                text="El autómata no contiene estados.",
                font=("Arial", 15, "bold"),
                fill=self.color_texto
            )
            return

        self.posiciones = self.generar_posiciones()
        transiciones = self.agrupar_transiciones()

        for (origen, destino), simbolos in transiciones.items():

            texto_simbolos = ", ".join(
                sorted(simbolos)
            )

            if origen == destino:
                self.dibujar_bucle(
                    origen,
                    texto_simbolos
                )
            else:
                existe_reversa = (
                    destino,
                    origen
                ) in transiciones

                self.dibujar_transicion(
                    origen,
                    destino,
                    texto_simbolos,
                    existe_reversa
                )

        for estado in sorted(
            self.automata.estados
        ):
            self.dibujar_estado(estado)

        self.actualizar_scrollregion()

    # =====================================================
    # POSICIONES
    # =====================================================

    def generar_posiciones(self):

        posiciones = {}
        estados = sorted(self.automata.estados)
        cantidad = len(estados)

        ancho_canvas = max(
            self.canvas.winfo_width(),
            700
        )
        alto_canvas = max(
            self.canvas.winfo_height(),
            450
        )

        centro_x = ancho_canvas / 2
        centro_y = alto_canvas / 2

        if cantidad == 1:
            posiciones[estados[0]] = (
                centro_x,
                centro_y
            )
            return posiciones

        espacio_disponible = min(
            ancho_canvas,
            alto_canvas
        )

        radio_distribucion = espacio_disponible * 0.32
        radio_distribucion = max(130, radio_distribucion)
        radio_necesario = cantidad * 32
        radio_distribucion = max(
            radio_distribucion,
            radio_necesario
        )

        for indice, estado in enumerate(estados):

            angulo = (
                2 * math.pi * indice / cantidad
            )
            angulo -= math.pi / 2

            x = centro_x + radio_distribucion * math.cos(angulo)
            y = centro_y + radio_distribucion * math.sin(angulo)

            posiciones[estado] = (x, y)

        return posiciones

    # =====================================================
    # SCROLL REGION
    # =====================================================

    def actualizar_scrollregion(self):

        self.canvas.update_idletasks()
        bbox = self.canvas.bbox("all")

        if bbox is None:
            return

        x1, y1, x2, y2 = bbox
        margen = 100

        ancho_canvas = max(self.canvas.winfo_width(), 1)
        alto_canvas = max(self.canvas.winfo_height(), 1)

        ancho_dibujo = x2 - x1
        alto_dibujo = y2 - y1

        if ancho_dibujo < ancho_canvas:
            sobrante = (ancho_canvas - ancho_dibujo) / 2
            region_x1 = x1 - sobrante
            region_x2 = x2 + sobrante
        else:
            region_x1 = x1 - margen
            region_x2 = x2 + margen

        if alto_dibujo < alto_canvas:
            sobrante = (alto_canvas - alto_dibujo) / 2
            region_y1 = y1 - sobrante
            region_y2 = y2 + sobrante
        else:
            region_y1 = y1 - margen
            region_y2 = y2 + margen

        self.canvas.config(
            scrollregion=(
                region_x1,
                region_y1,
                region_x2,
                region_y2
            )
        )

        self.centrar_vista()

    # =====================================================
    # CENTRAR VISTA
    # =====================================================

    def centrar_vista(self):

        region = self.canvas.cget("scrollregion")
        if not region:
            return

        valores = list(map(float, region.split()))
        if len(valores) != 4:
            return

        x1, y1, x2, y2 = valores

        ancho_region = x2 - x1
        alto_region = y2 - y1

        ancho_canvas = max(self.canvas.winfo_width(), 1)
        alto_canvas = max(self.canvas.winfo_height(), 1)

        if ancho_region > ancho_canvas:
            fraccion_x = (
                ((ancho_region - ancho_canvas) / 2)
                / ancho_region
            )
            self.canvas.xview_moveto(
                max(0, min(1, fraccion_x))
            )
        else:
            self.canvas.xview_moveto(0)

        if alto_region > alto_canvas:
            fraccion_y = (
                ((alto_region - alto_canvas) / 2)
                / alto_region
            )
            self.canvas.yview_moveto(
                max(0, min(1, fraccion_y))
            )
        else:
            self.canvas.yview_moveto(0)

    # =====================================================
    # AGRUPAR TRANSICIONES
    # =====================================================

    def agrupar_transiciones(self):

        agrupadas = {}

        for (origen, simbolo), destino in self.automata.transiciones.items():

            if self.automata.tipo == "AFN":
                destinos = destino
            else:
                destinos = {destino}

            for estado_destino in destinos:

                clave = (origen, estado_destino)

                if clave not in agrupadas:
                    agrupadas[clave] = set()

                agrupadas[clave].add(simbolo)

        return agrupadas

    # =====================================================
    # DIBUJAR ESTADO
    # =====================================================

    def dibujar_estado(self, estado):

        x, y = self.posiciones[estado]
        radio = self.radio_estado

        # Sombra suave
        self.canvas.create_oval(
            x - radio + 3,
            y - radio + 3,
            x + radio + 3,
            y + radio + 3,
            fill="#E9EEF4",
            outline=""
        )

        # Estado final
        if estado in self.automata.estados_finales:
            self.canvas.create_oval(
                x - radio - 6,
                y - radio - 6,
                x + radio + 6,
                y + radio + 6,
                width=3,
                outline=self.color_estado_final,
                fill=self.color_fondo_canvas
            )

        # Círculo principal
        self.canvas.create_oval(
            x - radio,
            y - radio,
            x + radio,
            y + radio,
            width=2.5,
            outline=self.color_principal,
            fill=self.color_estado
        )

        # Nombre
        self.canvas.create_text(
            x,
            y,
            text=estado,
            font=("Arial", 13, "bold"),
            fill=self.color_texto
        )

        # Estado inicial
        if estado == self.automata.estado_inicial:

            self.canvas.create_line(
                x - radio - 75,
                y,
                x - radio - 5,
                y,
                arrow=tk.LAST,
                width=2.5,
                fill=self.color_inicio
            )

            self.canvas.create_text(
                x - radio - 98,
                y,
                text="Inicio",
                font=("Arial", 10, "bold"),
                fill=self.color_inicio
            )

    # =====================================================
    # DIBUJAR TRANSICIÓN
    # =====================================================

    def dibujar_transicion(
        self,
        origen,
        destino,
        simbolos,
        bidireccional=False
    ):

        x1, y1 = self.posiciones[origen]
        x2, y2 = self.posiciones[destino]

        dx = x2 - x1
        dy = y2 - y1

        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia == 0:
            return

        ux = dx / distancia
        uy = dy / distancia

        radio = self.radio_estado

        inicio_x = x1 + ux * radio
        inicio_y = y1 + uy * radio

        fin_x = x2 - ux * radio
        fin_y = y2 - uy * radio

        perpendicular_x = -uy
        perpendicular_y = ux

        if bidireccional:

            curvatura = 55

            control_x = (
                (x1 + x2) / 2
                + perpendicular_x * curvatura
            )
            control_y = (
                (y1 + y2) / 2
                + perpendicular_y * curvatura
            )

            self.canvas.create_line(
                inicio_x,
                inicio_y,
                control_x,
                control_y,
                fin_x,
                fin_y,
                smooth=True,
                splinesteps=25,
                arrow=tk.LAST,
                width=2.3,
                fill=self.color_secundario
            )

            etiqueta_x = control_x + perpendicular_x * 15
            etiqueta_y = control_y + perpendicular_y * 15

        else:

            self.canvas.create_line(
                inicio_x,
                inicio_y,
                fin_x,
                fin_y,
                arrow=tk.LAST,
                width=2.3,
                fill=self.color_secundario
            )

            etiqueta_x = (inicio_x + fin_x) / 2
            etiqueta_y = (inicio_y + fin_y) / 2

            etiqueta_x += perpendicular_x * 18
            etiqueta_y += perpendicular_y * 18

        self.dibujar_etiqueta(
            etiqueta_x,
            etiqueta_y,
            simbolos
        )

    # =====================================================
    # DIBUJAR BUCLE
    # =====================================================

    def dibujar_bucle(self, estado, simbolos):

        x, y = self.posiciones[estado]
        radio = self.radio_estado

        inicio_x = x - radio * 0.55
        inicio_y = y - radio * 0.8

        fin_x = x + radio * 0.55
        fin_y = y - radio * 0.8

        control1_x = x - radio * 1.8
        control1_y = y - radio * 2.3

        control2_x = x + radio * 1.8
        control2_y = y - radio * 2.3

        self.canvas.create_line(
            inicio_x,
            inicio_y,
            control1_x,
            control1_y,
            control2_x,
            control2_y,
            fin_x,
            fin_y,
            smooth=True,
            splinesteps=30,
            arrow=tk.LAST,
            width=2.3,
            fill=self.color_secundario
        )

        self.dibujar_etiqueta(
            x,
            y - radio * 2.4,
            simbolos
        )

    # =====================================================
    # DIBUJAR ETIQUETA
    # =====================================================

    def dibujar_etiqueta(self, x, y, texto):

        ancho = max(28, len(texto) * 8)
        alto = 22

        self.canvas.create_rectangle(
            x - ancho / 2,
            y - alto / 2,
            x + ancho / 2,
            y + alto / 2,
            fill=self.color_etiqueta,
            outline=self.color_borde_suave,
            width=1
        )

        self.canvas.create_text(
            x,
            y,
            text=texto,
            font=("Arial", 10, "bold"),
            fill=self.color_texto
        )

    # =====================================================
    # CERRAR
    # =====================================================

    def cerrar(self):

        try:
            self.ventana.grab_release()
        except tk.TclError:
            pass

        self.ventana.destroy()