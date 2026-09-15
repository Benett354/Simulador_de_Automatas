import tkinter as tk
from tkinter import ttk, messagebox

from automata import Automata


class FormularioAutomata:


    def __init__(
        self,
        ventana_padre,
        callback
    ):

        self.callback = callback

        self.ventana = tk.Toplevel(
            ventana_padre
        )

        self.ventana.title(
            "Crear Autómata"
        )

        self.ventana.geometry(
            "520x520"
        )

        self.ventana.resizable(
            False,
            False
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

        self.crear_formulario()

        self.ventana.focus_force()


    # ---------------------------------
    # Formulario
    # ---------------------------------

    def crear_formulario(self):

        titulo = tk.Label(
            self.ventana,
            text="Configuración del Autómata",
            font=("Arial", 18, "bold")
        )

        titulo.pack(
            pady=15
        )

        # Tipo
        tk.Label(
            self.ventana,
            text="Tipo de autómata:"
        ).pack()

        self.tipo = ttk.Combobox(
            self.ventana,
            values=[
                "AFD",
                "AFN"
            ],
            state="readonly",
            width=37
        )

        self.tipo.current(
            0
        )

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

        tk.Label(
            self.ventana,
            text="Ejemplo: q0,q1,q2",
            fg="gray"
        ).pack()

        # Alfabeto
        tk.Label(
            self.ventana,
            text="Alfabeto separado por coma:"
        ).pack(
            pady=(10, 0)
        )

        self.alfabeto = tk.Entry(
            self.ventana,
            width=40
        )

        self.alfabeto.pack(
            pady=5
        )

        tk.Label(
            self.ventana,
            text="Ejemplo: 0,1   (No escriba ε aquí)",
            fg="gray"
        ).pack()

        # Inicial
        tk.Label(
            self.ventana,
            text="Estado inicial:"
        ).pack(
            pady=(10, 0)
        )

        self.inicial = tk.Entry(
            self.ventana,
            width=40
        )

        self.inicial.pack(
            pady=5
        )

        # Finales
        tk.Label(
            self.ventana,
            text="Estados finales separados por coma:"
        ).pack(
            pady=(10, 0)
        )

        self.finales = tk.Entry(
            self.ventana,
            width=40
        )

        self.finales.pack(
            pady=5
        )

        marco_botones = ttk.Frame(
            self.ventana
        )

        marco_botones.pack(
            pady=25
        )

        ttk.Button(
            marco_botones,
            text="Crear Autómata",
            command=self.crear
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        ttk.Button(
            marco_botones,
            text="Cancelar",
            command=self.cerrar
        ).grid(
            row=0,
            column=1,
            padx=10
        )


    # ---------------------------------
    # Separar
    # ---------------------------------

    def separar(self, texto):

        return [
            elemento.strip()
            for elemento in texto.split(",")
            if elemento.strip()
        ]


    # ---------------------------------
    # Crear
    # ---------------------------------

    def crear(self):

        try:

            tipo = self.tipo.get().strip()

            lista_estados = self.separar(
                self.estados.get()
            )

            lista_simbolos = self.separar(
                self.alfabeto.get()
            )

            inicial = self.inicial.get().strip()

            lista_finales = self.separar(
                self.finales.get()
            )

            # Estados
            if not lista_estados:

                messagebox.showerror(
                    "Error",
                    "Debe ingresar al menos un estado.",
                    parent=self.ventana
                )

                return

            if len(lista_estados) != len(
                set(lista_estados)
            ):

                messagebox.showerror(
                    "Error",
                    "Existen estados repetidos.",
                    parent=self.ventana
                )

                return

            # Alfabeto
            if not lista_simbolos:

                messagebox.showerror(
                    "Error",
                    "Debe ingresar al menos un símbolo.",
                    parent=self.ventana
                )

                return

            if len(lista_simbolos) != len(
                set(lista_simbolos)
            ):

                messagebox.showerror(
                    "Error",
                    "Existen símbolos repetidos.",
                    parent=self.ventana
                )

                return

            if "ε" in lista_simbolos:

                messagebox.showerror(
                    "Error",
                    (
                        "ε no se escribe dentro del alfabeto.\n\n"
                        "En un AFN aparecerá automáticamente "
                        "en el editor de transiciones."
                    ),
                    parent=self.ventana
                )

                return

            # Inicial
            if not inicial:

                messagebox.showerror(
                    "Error",
                    "Debe indicar el estado inicial.",
                    parent=self.ventana
                )

                return

            if inicial not in lista_estados:

                messagebox.showerror(
                    "Error",
                    f"El estado inicial '{inicial}' "
                    "no pertenece a los estados.",
                    parent=self.ventana
                )

                return

            # Finales
            for estado_final in lista_finales:

                if estado_final not in lista_estados:

                    messagebox.showerror(
                        "Error",
                        f"El estado final '{estado_final}' "
                        "no pertenece a los estados.",
                        parent=self.ventana
                    )

                    return

            # Construcción
            automata = Automata(
                tipo
            )

            for estado in lista_estados:

                automata.agregar_estado(
                    estado
                )

            for simbolo in lista_simbolos:

                automata.agregar_simbolo(
                    simbolo
                )

            automata.establecer_estado_inicial(
                inicial
            )

            for estado_final in lista_finales:

                automata.agregar_estado_final(
                    estado_final
                )

            errores = automata.validar()

            if errores:

                messagebox.showerror(
                    "Error",
                    "\n".join(
                        errores
                    ),
                    parent=self.ventana
                )

                return

            self.callback(
                automata
            )

            messagebox.showinfo(
                "Correcto",
                "Autómata creado correctamente.",
                parent=self.ventana
            )

            self.cerrar()

        except ValueError as error:

            messagebox.showerror(
                "Datos inválidos",
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
    # Cerrar
    # ---------------------------------

    def cerrar(self):

        try:

            self.ventana.grab_release()

        except tk.TclError:

            pass

        self.ventana.destroy()