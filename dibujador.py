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

        # Modal
        self.ventana.transient(
            ventana_padre
        )

        self.ventana.grab_set()

        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar
        )

        # Barra superior
        barra = ttk.Frame(
            self.ventana
        )

        barra.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            barra,
            text="DIAGRAMA DEL AUTÓMATA",
            font=("Arial", 16, "bold")
        ).pack(
            side="left",
            padx=10
        )

        ttk.Button(
            barra,
            text="Actualizar diagrama",
            command=self.actualizar
        ).pack(
            side="right",
            padx=5
        )

        ttk.Button(
            barra,
            text="Cerrar",
            command=self.cerrar
        ).pack(
            side="right",
            padx=5
        )

        self.etiqueta_info = ttk.Label(
            barra,
            text=""
        )

        self.etiqueta_info.pack(
            side="right",
            padx=20
        )

        marco_canvas = ttk.Frame(
            self.ventana
        )

        marco_canvas.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=(0, 10)
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
            background="white",
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            scrollregion=(
                0,
                0,
                1600,
                1000
            )
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

        self.actualizar()

        self.ventana.focus_force()


    # ---------------------------------
    # Actualizar
    # ---------------------------------

    def actualizar(self):

        self.canvas.delete(
            "all"
        )

        self.etiqueta_info.config(
            text=(
                f"Tipo: {self.automata.tipo}   |   "
                f"Estados: {len(self.automata.estados)}"
            )
        )

        if not self.automata.estados:

            self.canvas.create_text(
                500,
                300,
                text="El autómata no contiene estados.",
                font=("Arial", 15)
            )

            return

        self.posiciones = (
            self.generar_posiciones()
        )

        transiciones = (
            self.agrupar_transiciones()
        )

        for (
            origen,
            destino
        ), simbolos in transiciones.items():

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

            self.dibujar_estado(
                estado
            )


    # ---------------------------------
    # Posiciones
    # ---------------------------------

    def generar_posiciones(self):

        posiciones = {}

        estados = sorted(
            self.automata.estados
        )

        cantidad = len(
            estados
        )

        centro_x = 750
        centro_y = 450

        if cantidad == 1:

            posiciones[
                estados[0]
            ] = (
                centro_x,
                centro_y
            )

            return posiciones

        radio_distribucion = max(
            190,
            cantidad * 35
        )

        for indice, estado in enumerate(
            estados
        ):

            angulo = (
                2
                * math.pi
                * indice
                / cantidad
            )

            angulo -= (
                math.pi / 2
            )

            x = (
                centro_x
                + radio_distribucion
                * math.cos(angulo)
            )

            y = (
                centro_y
                + radio_distribucion
                * math.sin(angulo)
            )

            posiciones[
                estado
            ] = (
                x,
                y
            )

        return posiciones


    # ---------------------------------
    # Agrupar transiciones
    # ---------------------------------

    def agrupar_transiciones(self):

        agrupadas = {}

        for (
            origen,
            simbolo
        ), destino in self.automata.transiciones.items():

            if self.automata.tipo == "AFN":

                destinos = destino

            else:

                destinos = {
                    destino
                }

            for estado_destino in destinos:

                clave = (
                    origen,
                    estado_destino
                )

                if clave not in agrupadas:

                    agrupadas[
                        clave
                    ] = set()

                agrupadas[
                    clave
                ].add(
                    simbolo
                )

        return agrupadas


    # ---------------------------------
    # Estado
    # ---------------------------------

    def dibujar_estado(
        self,
        estado
    ):

        x, y = self.posiciones[
            estado
        ]

        radio = self.radio_estado

        if estado in self.automata.estados_finales:

            self.canvas.create_oval(
                x - radio - 6,
                y - radio - 6,
                x + radio + 6,
                y + radio + 6,
                width=2
            )

        self.canvas.create_oval(
            x - radio,
            y - radio,
            x + radio,
            y + radio,
            width=2
        )

        self.canvas.create_text(
            x,
            y,
            text=estado,
            font=(
                "Arial",
                13,
                "bold"
            )
        )

        if (
            estado
            ==
            self.automata.estado_inicial
        ):

            self.canvas.create_line(
                x - radio - 75,
                y,
                x - radio - 5,
                y,
                arrow=tk.LAST,
                width=2
            )

            self.canvas.create_text(
                x - radio - 95,
                y,
                text="Inicio",
                font=("Arial", 10)
            )


    # ---------------------------------
    # Transición
    # ---------------------------------

    def dibujar_transicion(
        self,
        origen,
        destino,
        simbolos,
        bidireccional=False
    ):

        x1, y1 = self.posiciones[
            origen
        ]

        x2, y2 = self.posiciones[
            destino
        ]

        dx = x2 - x1
        dy = y2 - y1

        distancia = math.sqrt(
            dx ** 2
            + dy ** 2
        )

        if distancia == 0:

            return

        ux = dx / distancia
        uy = dy / distancia

        radio = self.radio_estado

        inicio_x = (
            x1
            + ux * radio
        )

        inicio_y = (
            y1
            + uy * radio
        )

        fin_x = (
            x2
            - ux * radio
        )

        fin_y = (
            y2
            - uy * radio
        )

        perpendicular_x = -uy
        perpendicular_y = ux

        if bidireccional:

            curvatura = 55

            control_x = (
                (x1 + x2) / 2
                + perpendicular_x
                * curvatura
            )

            control_y = (
                (y1 + y2) / 2
                + perpendicular_y
                * curvatura
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
                width=2
            )

            etiqueta_x = (
                control_x
                + perpendicular_x * 15
            )

            etiqueta_y = (
                control_y
                + perpendicular_y * 15
            )

        else:

            self.canvas.create_line(
                inicio_x,
                inicio_y,
                fin_x,
                fin_y,
                arrow=tk.LAST,
                width=2
            )

            etiqueta_x = (
                inicio_x + fin_x
            ) / 2

            etiqueta_y = (
                inicio_y + fin_y
            ) / 2

            etiqueta_x += (
                perpendicular_x * 18
            )

            etiqueta_y += (
                perpendicular_y * 18
            )

        self.dibujar_etiqueta(
            etiqueta_x,
            etiqueta_y,
            simbolos
        )


    # ---------------------------------
    # Bucle
    # ---------------------------------

    def dibujar_bucle(
        self,
        estado,
        simbolos
    ):

        x, y = self.posiciones[
            estado
        ]

        radio = self.radio_estado

        inicio_x = (
            x - radio * 0.55
        )

        inicio_y = (
            y - radio * 0.8
        )

        fin_x = (
            x + radio * 0.55
        )

        fin_y = (
            y - radio * 0.8
        )

        control1_x = (
            x - radio * 1.8
        )

        control1_y = (
            y - radio * 2.3
        )

        control2_x = (
            x + radio * 1.8
        )

        control2_y = (
            y - radio * 2.3
        )

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
            width=2
        )

        self.dibujar_etiqueta(
            x,
            y - radio * 2.4,
            simbolos
        )


    # ---------------------------------
    # Etiqueta
    # ---------------------------------

    def dibujar_etiqueta(
        self,
        x,
        y,
        texto
    ):

        ancho = max(
            24,
            len(texto) * 8
        )

        alto = 20

        self.canvas.create_rectangle(
            x - ancho / 2,
            y - alto / 2,
            x + ancho / 2,
            y + alto / 2,
            fill="white",
            outline=""
        )

        self.canvas.create_text(
            x,
            y,
            text=texto,
            font=(
                "Arial",
                11,
                "bold"
            )
        )


    # ---------------------------------
    # Cerrar
    # ---------------------------------

    def cerrar(self):

        try:

            self.ventana.grab_release()

        except tk.TclError:

            pass

        self.ventana.destroy()