import tkinter as tk
import math



class DibujadorAutomata:


    def __init__(self, ventana_padre, automata):


        self.automata = automata


        self.ventana = tk.Toplevel(
            ventana_padre
        )


        self.ventana.title(
            "Visualización del Autómata"
        )


        self.ventana.geometry(
            "900x600"
        )


        self.canvas = tk.Canvas(
            self.ventana,
            bg="white"
        )


        self.canvas.pack(
            expand=True,
            fill="both"
        )


        self.dibujar()



    # ---------------------------------
    # Dibujar autómata completo
    # ---------------------------------

    def dibujar(self):


        posiciones = self.generar_posiciones()



        # Dibujar transiciones primero

        for transicion, destino in self.automata.transiciones.items():


            origen, simbolo = transicion



            if self.automata.tipo == "AFN":

                destinos = destino


            else:

                destinos = [destino]



            for estado_destino in destinos:


                self.dibujar_transicion(
                    posiciones[origen],
                    posiciones[estado_destino],
                    simbolo
                )



        # Dibujar estados

        for estado, posicion in posiciones.items():


            self.dibujar_estado(
                estado,
                posicion
            )



    # ---------------------------------
    # Generar posiciones
    # ---------------------------------

    def generar_posiciones(self):


        posiciones = {}


        estados = list(
            self.automata.estados
        )


        centro_x = 450

        centro_y = 280


        radio = 180



        cantidad = len(estados)



        for i, estado in enumerate(estados):


            angulo = (
                2 *
                math.pi *
                i /
                cantidad
            )


            x = centro_x + radio * math.cos(
                angulo
            )


            y = centro_y + radio * math.sin(
                angulo
            )


            posiciones[estado] = (
                x,
                y
            )



        return posiciones



    # ---------------------------------
    # Dibujar estado
    # ---------------------------------

    def dibujar_estado(self, estado, posicion):


        x,y = posicion


        tamaño = 40



        # Estado final doble círculo

        if estado in self.automata.estados_finales:


            self.canvas.create_oval(
                x-tamaño-5,
                y-tamaño-5,
                x+tamaño+5,
                y+tamaño+5
            )



        self.canvas.create_oval(
            x-tamaño,
            y-tamaño,
            x+tamaño,
            y+tamaño
        )



        self.canvas.create_text(
            x,
            y,
            text=estado,
            font=("Arial",14,"bold")
        )



        # Flecha de estado inicial

        if estado == self.automata.estado_inicial:


            self.canvas.create_line(
                x-100,
                y,
                x-tamaño,
                y,
                arrow=tk.LAST
            )



    # ---------------------------------
    # Dibujar transición
    # ---------------------------------

    def dibujar_transicion(
        self,
        origen,
        destino,
        simbolo
    ):


        x1,y1 = origen

        x2,y2 = destino



        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            arrow=tk.LAST,
            width=2
        )



        medio_x = (
            x1+x2
        ) / 2


        medio_y = (
            y1+y2
        ) / 2



        self.canvas.create_text(
            medio_x,
            medio_y-15,
            text=simbolo,
            font=("Arial",12,"bold")
        )