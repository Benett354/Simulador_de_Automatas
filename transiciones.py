import tkinter as tk
from tkinter import ttk, messagebox



class VentanaTransiciones:


    def __init__(self, ventana_padre, automata):


        self.automata = automata



        self.ventana = tk.Toplevel(
            ventana_padre
        )


        self.ventana.title(
            "Agregar Transiciones"
        )


        self.ventana.geometry(
            "600x500"
        )


        self.crear_interfaz()



    # ---------------------------------
    # Crear ventana
    # ---------------------------------

    def crear_interfaz(self):


        titulo = tk.Label(
            self.ventana,
            text="Editor de Transiciones",
            font=("Arial",18,"bold")
        )


        titulo.pack(
            pady=15
        )



        marco = ttk.Frame(
            self.ventana
        )


        marco.pack(
            pady=10
        )



        # -----------------------------
        # Estado origen
        # -----------------------------


        tk.Label(
            marco,
            text="Estado origen:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )


        self.origen = ttk.Combobox(
            marco,
            values=list(self.automata.estados),
            state="readonly"
        )


        self.origen.grid(
            row=0,
            column=1
        )



        # -----------------------------
        # Símbolo
        # -----------------------------


        tk.Label(
            marco,
            text="Símbolo:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )


        simbolos = list(
            self.automata.alfabeto
        )


        if self.automata.tipo == "AFN":

            simbolos.append("ε")



        self.simbolo = ttk.Combobox(
            marco,
            values=simbolos,
            state="readonly"
        )


        self.simbolo.grid(
            row=1,
            column=1
        )



        # -----------------------------
        # Estado destino
        # -----------------------------


        tk.Label(
            marco,
            text="Estado destino:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5
        )



        self.destino = ttk.Combobox(
            marco,
            values=list(self.automata.estados),
            state="readonly"
        )


        self.destino.grid(
            row=2,
            column=1
        )



        # Botón agregar

        boton = ttk.Button(
            self.ventana,
            text="Agregar transición",
            command=self.agregar
        )


        boton.pack(
            pady=15
        )



        # Tabla

        self.tabla = ttk.Treeview(
            self.ventana,
            columns=(
                "origen",
                "simbolo",
                "destino"
            ),
            show="headings"
        )


        self.tabla.heading(
            "origen",
            text="Origen"
        )


        self.tabla.heading(
            "simbolo",
            text="Símbolo"
        )


        self.tabla.heading(
            "destino",
            text="Destino"
        )


        self.tabla.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=10
        )


        self.actualizar_tabla()



    # ---------------------------------
    # Agregar transición
    # ---------------------------------

    def agregar(self):


        try:


            origen = self.origen.get()

            simbolo = self.simbolo.get()

            destino = self.destino.get()



            if not origen or not simbolo or not destino:


                messagebox.showwarning(
                    "Advertencia",
                    "Complete todos los campos"
                )

                return



            self.automata.agregar_transicion(
                origen,
                simbolo,
                destino
            )



            self.actualizar_tabla()



        except Exception as error:


            messagebox.showerror(
                "Error",
                str(error)
            )



    # ---------------------------------
    # Actualizar tabla
    # ---------------------------------

    def actualizar_tabla(self):


        for fila in self.tabla.get_children():

            self.tabla.delete(fila)



        for transicion, destino in self.automata.transiciones.items():


            origen, simbolo = transicion



            self.tabla.insert(
                "",
                "end",
                values=(
                    origen,
                    simbolo,
                    destino
                )
            )