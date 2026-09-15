import tkinter as tk
from tkinter import ttk, messagebox


class VentanaTransiciones:


    def __init__(
        self,
        ventana_padre,
        automata
    ):

        self.automata = automata


        self.ventana = tk.Toplevel(
            ventana_padre
        )


        self.ventana.title(
            "Editor de Transiciones"
        )


        self.ventana.geometry(
            "700x520"
        )


        self.ventana.minsize(
            600,
            450
        )


        self.crear_interfaz()



    # ---------------------------------
    # Crear interfaz
    # ---------------------------------

    def crear_interfaz(self):

        tk.Label(
            self.ventana,
            text="Editor de Transiciones",
            font=("Arial", 18, "bold")
        ).pack(
            pady=15
        )



        tk.Label(
            self.ventana,
            text=f"Tipo actual: {self.automata.tipo}",
            font=("Arial", 11)
        ).pack()



        marco = ttk.LabelFrame(
            self.ventana,
            text="Nueva transición"
        )


        marco.pack(
            padx=20,
            pady=15
        )



        estados = sorted(
            self.automata.estados
        )



        # ---------------------------------
        # Origen
        # ---------------------------------

        tk.Label(
            marco,
            text="Origen:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=8
        )



        self.origen = ttk.Combobox(
            marco,
            values=estados,
            state="readonly",
            width=20
        )


        self.origen.grid(
            row=0,
            column=1,
            padx=10,
            pady=8
        )



        # ---------------------------------
        # Símbolo
        # ---------------------------------

        tk.Label(
            marco,
            text="Símbolo:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=8
        )



        simbolos = sorted(
            self.automata.alfabeto
        )



        # ε solamente para AFN

        if self.automata.tipo == "AFN":

            simbolos.append(
                "ε"
            )



        self.simbolo = ttk.Combobox(
            marco,
            values=simbolos,
            state="readonly",
            width=20
        )


        self.simbolo.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )



        # ---------------------------------
        # Destino
        # ---------------------------------

        tk.Label(
            marco,
            text="Destino:"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=8
        )



        self.destino = ttk.Combobox(
            marco,
            values=estados,
            state="readonly",
            width=20
        )


        self.destino.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )



        # ---------------------------------
        # Botones
        # ---------------------------------

        marco_botones = ttk.Frame(
            self.ventana
        )


        marco_botones.pack(
            pady=5
        )



        ttk.Button(
            marco_botones,
            text="Agregar",
            command=self.agregar
        ).grid(
            row=0,
            column=0,
            padx=10
        )



        ttk.Button(
            marco_botones,
            text="Eliminar seleccionada",
            command=self.eliminar
        ).grid(
            row=0,
            column=1,
            padx=10
        )



        # ---------------------------------
        # Tabla
        # ---------------------------------

        self.tabla = ttk.Treeview(
            self.ventana,
            columns=(
                "origen",
                "simbolo",
                "destino"
            ),
            show="headings",
            selectmode="browse"
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



        self.tabla.column(
            "origen",
            anchor="center"
        )


        self.tabla.column(
            "simbolo",
            anchor="center"
        )


        self.tabla.column(
            "destino",
            anchor="center"
        )



        self.tabla.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=15
        )



        self.actualizar_tabla()



    # ---------------------------------
    # Agregar
    # ---------------------------------

    def agregar(self):

        origen = self.origen.get()

        simbolo = self.simbolo.get()

        destino = self.destino.get()



        if not origen:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione el estado origen."
            )

            return



        if not simbolo:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un símbolo."
            )

            return



        if not destino:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione el estado destino."
            )

            return



        try:

            self.automata.agregar_transicion(
                origen,
                simbolo,
                destino
            )


            self.actualizar_tabla()



        except ValueError as error:

            messagebox.showerror(
                "Transición inválida",
                str(error)
            )



        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )



    # ---------------------------------
    # Eliminar
    # ---------------------------------

    def eliminar(self):

        seleccion = self.tabla.selection()


        if not seleccion:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione una transición de la tabla."
            )

            return



        datos = self.tabla.item(
            seleccion[0]
        )



        origen, simbolo, destino = datos[
            "values"
        ]



        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar la transición?\n\n"
            f"{origen} --{simbolo}--> {destino}"
        )



        if not respuesta:

            return



        try:

            self.automata.eliminar_transicion(
                origen,
                simbolo,
                destino
            )


            self.actualizar_tabla()



        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )



    # ---------------------------------
    # Actualizar tabla
    # ---------------------------------

    def actualizar_tabla(self):

        for fila in self.tabla.get_children():

            self.tabla.delete(
                fila
            )



        transiciones_ordenadas = sorted(
            self.automata.transiciones.items()
        )



        for (
            origen,
            simbolo
        ), destino in transiciones_ordenadas:


            # ---------------------------------
            # AFN
            # ---------------------------------

            if self.automata.tipo == "AFN":

                for estado_destino in sorted(
                    destino
                ):

                    self.tabla.insert(
                        "",
                        "end",
                        values=(
                            origen,
                            simbolo,
                            estado_destino
                        )
                    )



            # ---------------------------------
            # AFD
            # ---------------------------------

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