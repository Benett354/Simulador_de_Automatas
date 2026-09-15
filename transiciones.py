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
            "700x540"
        )

        self.ventana.minsize(
            600,
            450
        )

        # ---------------------------------
        # Hacer ventana modal
        # ---------------------------------

        self.ventana.transient(
            ventana_padre
        )

        self.ventana.grab_set()

        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar
        )

        self.crear_interfaz()

        self.ventana.focus_force()


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

        # Origen
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

        # Símbolo
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

        # Destino
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

        # Botones
        marco_botones = ttk.Frame(
            self.ventana
        )

        marco_botones.pack(
            pady=5
        )

        ttk.Button(
            marco_botones,
            text="Agregar transición",
            command=self.agregar
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        ttk.Button(
            marco_botones,
            text="Eliminar seleccionada",
            command=self.eliminar
        ).grid(
            row=0,
            column=1,
            padx=8
        )

        ttk.Button(
            marco_botones,
            text="Cerrar",
            command=self.cerrar
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        # Tabla
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
                "Seleccione el estado origen.",
                parent=self.ventana
            )

            return

        if not simbolo:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione un símbolo.",
                parent=self.ventana
            )

            return

        if not destino:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione el estado destino.",
                parent=self.ventana
            )

            return

        try:

            cantidad_antes = len(
                self.automata.transiciones
            )

            self.automata.agregar_transicion(
                origen,
                simbolo,
                destino
            )

            self.actualizar_tabla()

            # Dejar listo para otra transición
            self.origen.set("")
            self.simbolo.set("")
            self.destino.set("")

        except ValueError as error:

            messagebox.showerror(
                "Transición inválida",
                str(error),
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )


    # ---------------------------------
    # Eliminar
    # ---------------------------------

    def eliminar(self):

        seleccion = self.tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Advertencia",
                "Seleccione una transición de la tabla.",
                parent=self.ventana
            )

            return

        datos = self.tabla.item(
            seleccion[0]
        )

        valores = datos[
            "values"
        ]

        if len(valores) != 3:

            messagebox.showerror(
                "Error",
                "No se pudieron obtener los datos de la transición.",
                parent=self.ventana
            )

            return

        # IMPORTANTE:
        # Treeview puede convertir "0" o "1"
        # automáticamente a números.
        origen = str(
            valores[0]
        )

        simbolo = str(
            valores[1]
        )

        destino = str(
            valores[2]
        )

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            (
                "¿Desea eliminar esta transición?\n\n"
                f"{origen} --{simbolo}--> {destino}"
            ),
            parent=self.ventana
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

            messagebox.showinfo(
                "Eliminada",
                "La transición fue eliminada correctamente.",
                parent=self.ventana
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error inesperado",
                str(error),
                parent=self.ventana
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

            # AFN
            if self.automata.tipo == "AFN":

                for estado_destino in sorted(
                    destino
                ):

                    # Convertimos explícitamente
                    # todos los valores en cadenas.
                    self.tabla.insert(
                        "",
                        "end",
                        values=(
                            str(origen),
                            str(simbolo),
                            str(estado_destino)
                        )
                    )

            # AFD
            else:

                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        str(origen),
                        str(simbolo),
                        str(destino)
                    )
                )


    # ---------------------------------
    # Cerrar ventana
    # ---------------------------------

    def cerrar(self):

        try:

            self.ventana.grab_release()

        except tk.TclError:

            pass

        self.ventana.destroy()