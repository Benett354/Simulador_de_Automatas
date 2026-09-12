import tkinter as tk
from tkinter import ttk, messagebox



class VentanaTransiciones:


    def __init__(self, ventana_padre, automata):


        self.automata = automata


        self.ventana = tk.Toplevel(
            ventana_padre
        )


        self.ventana.title(
            "Editor de Transiciones"
        )


        self.ventana.geometry(
            "650x500"
        )


        self.crear_interfaz()



    # ---------------------------------
    # Crear interfaz
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


        marco.pack()



        # Origen

        tk.Label(
            marco,
            text="Origen:"
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



        # Símbolo


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



        # Destino


        tk.Label(
            marco,
            text="Destino:"
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



        botones = ttk.Frame(
            self.ventana
        )


        botones.pack(
            pady=15
        )



        ttk.Button(
            botones,
            text="Agregar",
            command=self.agregar
        ).grid(
            row=0,
            column=0,
            padx=10
        )



        ttk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar
        ).grid(
            row=0,
            column=1,
            padx=10
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


        origen = self.origen.get()

        simbolo = self.simbolo.get()

        destino = self.destino.get()



        if not origen or not simbolo or not destino:


            messagebox.showwarning(
                "Advertencia",
                "Complete todos los campos"
            )

            return



        try:


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
    # Eliminar transición
    # ---------------------------------

    def eliminar(self):


        seleccion = self.tabla.selection()



        if not seleccion:


            messagebox.showwarning(
                "Advertencia",
                "Seleccione una transición"
            )

            return



        datos = self.tabla.item(
            seleccion[0]
        )


        origen, simbolo, destino = datos["values"]



        clave = (
            origen,
            simbolo
        )



        if self.automata.tipo == "AFN":


            self.automata.transiciones[clave].remove(
                destino
            )



            if len(
                self.automata.transiciones[clave]
            ) == 0:


                del self.automata.transiciones[clave]



        else:


            del self.automata.transiciones[clave]



        self.actualizar_tabla()



    # ---------------------------------
    # Actualizar tabla
    # ---------------------------------

    def actualizar_tabla(self):


        for fila in self.tabla.get_children():

            self.tabla.delete(
                fila
            )



        for transicion, destino in self.automata.transiciones.items():


            origen, simbolo = transicion



            if self.automata.tipo == "AFN":


                for estado in destino:


                    self.tabla.insert(
                        "",
                        "end",
                        values=(
                            origen,
                            simbolo,
                            estado
                        )
                    )



            else:


                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        origen,
                        simbolo,
                        destino
                    )
                )