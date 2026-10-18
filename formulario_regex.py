import tkinter as tk
from tkinter import ttk, messagebox


class FormularioRegex:
    """Interfaz para validar expresiones regulares y construir un AFN-ε."""

    COLOR_PRINCIPAL = "#1F3A5F"
    COLOR_FONDO = "#F4F6F8"
    COLOR_PANEL = "#FFFFFF"
    COLOR_TEXTO = "#1E293B"
    COLOR_SECUNDARIO = "#64748B"
    COLOR_BORDE = "#D6DCE5"
    COLOR_EXITO = "#2E7D32"
    COLOR_ERROR = "#C62828"

    def __init__(self, padre, al_crear_automata, al_mostrar_grafica):
        self.padre = padre
        self.al_crear_automata = al_crear_automata
        self.al_mostrar_grafica = al_mostrar_grafica
        self.automata_generado = None

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Expresión regular → AFN-ε")
        self.ventana.geometry("880x700")
        self.ventana.minsize(760, 600)
        self.ventana.configure(bg=self.COLOR_FONDO)
        self.ventana.transient(padre)
        self.ventana.grab_set()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.crear_interfaz()

    def crear_interfaz(self):
        encabezado = tk.Frame(
            self.ventana,
            bg=self.COLOR_PRINCIPAL,
            height=86
        )
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="CONSTRUCTOR DE THOMPSON",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_PRINCIPAL,
            fg="white"
        ).pack(anchor="w", padx=22, pady=(14, 2))

        tk.Label(
            encabezado,
            text="Validación de expresiones regulares y generación de un AFN con transiciones ε",
            font=("Arial", 10),
            bg=self.COLOR_PRINCIPAL,
            fg="#D9E2EC"
        ).pack(anchor="w", padx=22)

        cuerpo = tk.Frame(self.ventana, bg=self.COLOR_FONDO)
        cuerpo.pack(expand=True, fill="both", padx=20, pady=16)

        tk.Label(
            cuerpo,
            text="Expresión regular",
            font=("Arial", 11, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_PRINCIPAL
        ).pack(anchor="w")

        tk.Label(
            cuerpo,
            text="Operadores: |  *  +  ?  ( ). La concatenación se detecta automáticamente.",
            font=("Arial", 9),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_SECUNDARIO
        ).pack(anchor="w", pady=(3, 8))

        marco_entrada = tk.Frame(
            cuerpo,
            bg=self.COLOR_PANEL,
            highlightbackground=self.COLOR_BORDE,
            highlightthickness=1
        )
        marco_entrada.pack(fill="x")

        self.entrada_expresion = tk.Entry(
            marco_entrada,
            font=("Consolas", 14),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXTO,
            insertbackground=self.COLOR_PRINCIPAL,
            relief="flat"
        )
        self.entrada_expresion.pack(fill="x", padx=10, pady=10)
        self.entrada_expresion.insert(0, "(a|b)*abb")
        self.entrada_expresion.bind(
            "<Return>",
            lambda evento: self.construir_automata()
        )

        tk.Label(
            cuerpo,
            text="Ejemplo: (a|b)*abb    |    ε representa la cadena vacía",
            font=("Arial", 9),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_SECUNDARIO
        ).pack(anchor="w", pady=(5, 0))

        fila_botones = tk.Frame(cuerpo, bg=self.COLOR_FONDO)
        fila_botones.pack(fill="x", pady=10)

        ttk.Button(
            fila_botones,
            text="Validar y procesar",
            style="Secondary.TButton",
            command=self.validar_expresion
        ).pack(side="left", padx=(0, 7))

        ttk.Button(
            fila_botones,
            text="Generar AFN-ε",
            style="Primary.TButton",
            command=self.construir_automata
        ).pack(side="left", padx=7)

        ttk.Button(
            fila_botones,
            text="Limpiar",
            style="Secondary.TButton",
            command=self.limpiar
        ).pack(side="left", padx=7)

        tk.Label(
            cuerpo,
            text="Procedimiento y resultado",
            font=("Arial", 11, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_PRINCIPAL
        ).pack(anchor="w", pady=(5, 7))

        marco_salida = tk.Frame(
            cuerpo,
            bg=self.COLOR_PANEL,
            highlightbackground=self.COLOR_BORDE,
            highlightthickness=1
        )
        marco_salida.pack(expand=True, fill="both")

        scroll = ttk.Scrollbar(marco_salida, orient="vertical")
        scroll.pack(side="right", fill="y")

        self.salida = tk.Text(
            marco_salida,
            font=("Consolas", 10),
            bg=self.COLOR_PANEL,
            fg=self.COLOR_TEXTO,
            wrap="word",
            relief="flat",
            padx=12,
            pady=10,
            yscrollcommand=scroll.set
        )
        self.salida.pack(expand=True, fill="both")
        scroll.configure(command=self.salida.yview)

        self.salida.tag_configure(
            "titulo",
            foreground=self.COLOR_PRINCIPAL,
            font=("Consolas", 10, "bold")
        )
        self.salida.tag_configure(
            "error",
            foreground=self.COLOR_ERROR,
            font=("Consolas", 10, "bold")
        )
        self.salida.tag_configure(
            "exito",
            foreground=self.COLOR_EXITO,
            font=("Consolas", 10, "bold")
        )

        fila_final = tk.Frame(cuerpo, bg=self.COLOR_FONDO)
        fila_final.pack(fill="x", pady=(12, 0))

        self.boton_grafica = ttk.Button(
            fila_final,
            text="Mostrar gráfica del autómata",
            style="Success.TButton",
            command=self.mostrar_grafica,
            state="disabled"
        )
        self.boton_grafica.pack(side="left")

        ttk.Button(
            fila_final,
            text="Cerrar",
            style="Secondary.TButton",
            command=self.cerrar
        ).pack(side="right")

        self.salida.insert(
            "end",
            "Ejemplo cargado: (a|b)*abb\n",
            "titulo"
        )
        self.salida.insert(
            "end",
            "Pulsa 'Validar y procesar' para revisar los pasos o 'Generar AFN-ε' para construir el autómata.\n"
        )
        self.entrada_expresion.focus_set()
        self.entrada_expresion.selection_range(0, "end")

    def _escribir_encabezado(self, texto):
        self.salida.insert("end", "\n" + texto + "\n", "titulo")

    @staticmethod
    def _orden_estado(estado):
        if isinstance(estado, str) and estado.startswith("q"):
            try:
                return int(estado[1:])
            except ValueError:
                pass
        return estado

    def validar_expresion(self):
        expresion = self.entrada_expresion.get().strip()
        self.salida.delete("1.0", "end")

        try:
            from procesador_regex import ProcesadorRegex

            procesador = ProcesadorRegex(expresion)
            errores = procesador.obtener_errores_validacion()

            self._escribir_encabezado("1. VALIDACIÓN")
            self.salida.insert(
                "end",
                f"Expresión ingresada: {expresion or '(vacía)'}\n"
            )

            if errores:
                self.salida.insert(
                    "end",
                    "La expresión contiene errores:\n",
                    "error"
                )
                for error in errores:
                    self.salida.insert("end", f"  • {error}\n", "error")
                self.salida.see("end")
                return False

            self.salida.insert(
                "end",
                "Resultado: expresión válida.\n",
                "exito"
            )

            self._escribir_encabezado("2. CONCATENACIÓN EXPLÍCITA")
            self.salida.insert(
                "end",
                procesador.obtener_expresion_concatenada() + "\n"
            )

            self._escribir_encabezado("3. CONVERSIÓN A POSTFIJA")
            self.salida.insert("end", procesador.obtener_postfija() + "\n")

            self._escribir_encabezado("4. TOKENS PARA THOMPSON")
            for tipo, token in procesador.obtener_tokens_para_thompson():
                self.salida.insert("end", f"{tipo:<18} {token}\n")

            self.salida.see("end")
            return True

        except Exception as error:
            self.salida.insert("end", f"ERROR: {error}\n", "error")
            self.salida.see("end")
            messagebox.showerror(
                "Error al procesar expresión",
                str(error),
                parent=self.ventana
            )
            return False

    def construir_automata(self):
        expresion = self.entrada_expresion.get().strip()

        if not self.validar_expresion():
            return

        try:
            from constructor_thompson import ConstructorThompson

            constructor = ConstructorThompson()
            automata = constructor.construir_automata(expresion)
            errores = automata.validar()

            if errores:
                raise ValueError(
                    "El AFN generado no es válido:\n" + "\n".join(errores)
                )

            self.automata_generado = automata
            self.al_crear_automata(automata)
            self.boton_grafica.configure(state="normal")

            self._escribir_encabezado("5. AFN-ε GENERADO CON THOMPSON")
            self.salida.insert("end", f"Tipo: {automata.tipo}\n")
            self.salida.insert(
                "end",
                "Estados: " + ", ".join(
                    sorted(automata.estados, key=self._orden_estado)
                ) + "\n"
            )
            self.salida.insert(
                "end",
                "Alfabeto: " + ", ".join(sorted(automata.alfabeto)) + "\n"
            )
            self.salida.insert("end", f"Estado inicial: {automata.estado_inicial}\n")
            self.salida.insert(
                "end",
                "Estados finales: " + ", ".join(
                    sorted(automata.estados_finales, key=self._orden_estado)
                ) + "\n"
            )

            self._escribir_encabezado("6. TRANSICIONES")
            transiciones = sorted(
                automata.transiciones.items(),
                key=lambda elemento: (
                    self._orden_estado(elemento[0][0]),
                    elemento[0][1]
                )
            )

            for (origen, simbolo), destinos in transiciones:
                destinos_lista = (
                    sorted(destinos, key=self._orden_estado)
                    if isinstance(destinos, set)
                    else [destinos]
                )
                for destino in destinos_lista:
                    self.salida.insert(
                        "end",
                        f"{origen} --{simbolo}--> {destino}\n"
                    )

            self.salida.insert(
                "end",
                "\nAFN generado correctamente. El autómata ya está cargado en la ventana principal.\n",
                "exito"
            )
            self.salida.insert(
                "end",
                "Al cerrar esta ventana podrás simular cadenas y utilizar las herramientas de conversión y minimización.\n"
            )
            self.salida.see("end")

        except Exception as error:
            self.salida.insert(
                "end",
                f"\nERROR AL GENERAR EL AFN: {error}\n",
                "error"
            )
            self.salida.see("end")
            messagebox.showerror(
                "Error de Thompson",
                str(error),
                parent=self.ventana
            )

    def mostrar_grafica(self):
        if self.automata_generado is None:
            return

        self.cerrar()
        self.al_mostrar_grafica()

    def limpiar(self):
        self.entrada_expresion.delete(0, "end")
        self.salida.delete("1.0", "end")
        self.automata_generado = None
        self.boton_grafica.configure(state="disabled")
        self.entrada_expresion.focus_set()

    def cerrar(self):
        try:
            self.ventana.grab_release()
        except tk.TclError:
            pass

        if self.ventana.winfo_exists():
            self.ventana.destroy()
