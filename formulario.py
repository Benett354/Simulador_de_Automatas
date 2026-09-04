import tkinter as tk
from tkinter import ttk, messagebox

from automata import Automata



class FormularioAutomata:


    def __init__(self, ventana_padre, callback):


        self.callback = callback


        self.ventana = tk.Toplevel(
            ventana_padre
        )


        self.ventana.title(
            "Crear Autómata"
        )


        self.ventana.geometry(
            "500x500"
        )


        self.crear_formulario()



    def crear_formulario(self):


        titulo = tk.Label(
            self.ventana,
            text="Configuración del Autómata",
            font=("Arial",18,"bold")
        )


        titulo.pack(
            pady=15
        )



        # Tipo

        tk.Label(
            self.ventana,
            text="Tipo:"
        ).pack()



        self.tipo = ttk.Combobox(
            self.ventana,
            values=[
                "AFD",
                "AFN"
            ],
            state="readonly"
        )


        self.tipo.current(0)


        self.tipo.pack(
            pady=5
        )



        # Estados

        tk.Label(
            self.ventana,
            text="Estados separados por coma:"
        ).pack()


        self.estados = tk.Entry(
            self.ventana,
            width=40
        )


        self.estados.pack(
            pady=5
        )



        # Alfabeto

        tk.Label(
            self.ventana,
            text="Alfabeto separado por coma:"
        ).pack()


        self.alfabeto = tk.Entry(
            self.ventana,
            width=40
        )


        self.alfabeto.pack(
            pady=5
        )



        # Estado inicial

        tk.Label(
            self.ventana,
            text="Estado inicial:"
        ).pack()


        self.inicial = tk.Entry(
            self.ventana,
            width=40
        )


        self.inicial.pack(
            pady=5
        )



        # Estados finales

        tk.Label(
            self.ventana,
            text="Estados finales separados por coma:"
        ).pack()


        self.finales = tk.Entry(
            self.ventana,
            width=40
        )


        self.finales.pack(
            pady=5
        )



        boton = ttk.Button(
            self.ventana,
            text="Crear Autómata",
            command=self.crear
        )


        boton.pack(
            pady=25
        )



    def crear(self):


        try:


            automata = Automata(
                self.tipo.get()
            )



            # Estados

            lista_estados = (
                self.estados.get()
                .split(",")
            )


            for estado in lista_estados:


                estado = estado.strip()


                if estado:

                    automata.agregar_estado(
                        estado
                    )



            # Alfabeto

            lista_simbolos = (
                self.alfabeto.get()
                .split(",")
            )


            for simbolo in lista_simbolos:


                simbolo = simbolo.strip()


                if simbolo:

                    automata.agregar_simbolo(
                        simbolo
                    )



            # Inicial

            automata.establecer_estado_inicial(
                self.inicial.get().strip()
            )



            # Finales

            lista_finales = (
                self.finales.get()
                .split(",")
            )


            for estado_final in lista_finales:


                estado_final = estado_final.strip()


                if estado_final:

                    automata.agregar_estado_final(
                        estado_final
                    )



            errores = automata.validar()



            if errores:


                messagebox.showerror(
                    "Error",
                    "\n".join(errores)
                )

                return



            self.callback(
                automata
            )


            messagebox.showinfo(
                "Correcto",
                "Autómata creado correctamente"
            )


            self.ventana.destroy()



        except Exception as error:


            messagebox.showerror(
                "Error",
                str(error)
            )