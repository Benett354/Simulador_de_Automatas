
import tkinter as tk
from tkinter import ttk, messagebox

from algoritmos.analizador_logs import AnalizadorLogs


class VisorLogs:

    def __init__(self, padre):

        self.padre = padre
        self.ventana = tk.Toplevel(padre)
        self.ventana.transient(padre)
        self.ventana.grab_set()

        self.ventana.title("Visor de registros del simulador")
        self.ventana.geometry("1050x650")
        self.ventana.minsize(780, 480)

        self.analizador = AnalizadorLogs()

        self.resultado = None
        self.registros = []
        self.registros_visibles = []

        self.filtro_var = tk.StringVar(value="TODOS")

        self.crear_interfaz()
        self.cargar_logs()

    # =================================
    # CREAR INTERFAZ
    # =================================

    def crear_interfaz(self):

        contenedor = ttk.Frame(
            self.ventana,
            padding=15
        )

        contenedor.pack(
            expand=True,
            fill="both"
        )

        # Encabezado

        ttk.Label(
            contenedor,
            text="VISOR DE REGISTROS",
            font=("Arial", 20, "bold")
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

        ttk.Label(
            contenedor,
            text="Consulta y análisis de eventos del simulador"
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # Panel de controles

        controles = ttk.LabelFrame(
            contenedor,
            text="Filtros y acciones",
            padding=10
        )

        controles.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            controles,
            text="Nivel:"
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.combo_filtro = ttk.Combobox(
            controles,
            textvariable=self.filtro_var,
            values=[
                "TODOS",
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
                "INVALIDO"
            ],
            state="readonly",
            width=14
        )

        self.combo_filtro.pack(
            side="left",
            padx=(0, 12)
        )

        self.combo_filtro.bind(
            "<<ComboboxSelected>>",
            lambda evento: self.aplicar_filtro()
        )

        ttk.Button(
            controles,
            text="Actualizar",
            command=self.cargar_logs
        ).pack(
            side="left",
            padx=4
        )

        ttk.Button(
            controles,
            text="Mostrar todos",
            command=self.mostrar_todos
        ).pack(
            side="left",
            padx=4
        )

        ttk.Button(
            controles,
            text="Cerrar",
            command=self.ventana.destroy
        ).pack(
            side="right",
            padx=4
        )

        # Resumen

        self.etiqueta_resumen = ttk.Label(
            contenedor,
            text="Esperando registros...",
            font=("Arial", 10, "bold")
        )

        self.etiqueta_resumen.pack(
            anchor="w",
            pady=(0, 10)
        )

        # Tabla de registros

        panel_tabla = ttk.LabelFrame(
            contenedor,
            text="Registros encontrados",
            padding=8
        )

        panel_tabla.pack(
            expand=True,
            fill="both"
        )

        columnas = (
            "linea",
            "fecha",
            "nivel",
            "mensaje"
        )

        self.tabla = ttk.Treeview(
            panel_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        self.tabla.heading(
            "linea",
            text="Línea"
        )

        self.tabla.heading(
            "fecha",
            text="Fecha y hora"
        )

        self.tabla.heading(
            "nivel",
            text="Nivel"
        )

        self.tabla.heading(
            "mensaje",
            text="Mensaje"
        )

        self.tabla.column(
            "linea",
            width=60,
            anchor="center",
            stretch=False
        )

        self.tabla.column(
            "fecha",
            width=155,
            anchor="center",
            stretch=False
        )

        self.tabla.column(
            "nivel",
            width=95,
            anchor="center",
            stretch=False
        )

        self.tabla.column(
            "mensaje",
            width=500,
            anchor="w"
        )

        # Diferenciar visualmente los niveles

        self.tabla.tag_configure(
            "ERROR",
            foreground="#C62828"
        )

        self.tabla.tag_configure(
            "CRITICAL",
            foreground="#8E0000"
        )

        self.tabla.tag_configure(
            "WARNING",
            foreground="#B26A00"
        )

        self.tabla.tag_configure(
            "INVALIDO",
            foreground="#666666"
        )

        barra_vertical = ttk.Scrollbar(
            panel_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        barra_horizontal = ttk.Scrollbar(
            panel_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        self.tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        panel_tabla.rowconfigure(
            0,
            weight=1
        )

        panel_tabla.columnconfigure(
            0,
            weight=1
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.mostrar_detalle
        )

        # Detalle del registro seleccionado

        panel_detalle = ttk.LabelFrame(
            contenedor,
            text="Detalle del registro seleccionado",
            padding=8
        )

        panel_detalle.pack(
            fill="x",
            pady=(10, 0)
        )

        self.detalle = tk.Text(
            panel_detalle,
            height=4,
            wrap="word",
            font=("Consolas", 10),
            state="disabled"
        )

        self.detalle.pack(
            fill="x"
        )

    # =================================
    # CARGAR ARCHIVO DE LOGS
    # =================================

    def cargar_logs(self):

        try:

            resultado = self.analizador.analizar_archivo()

        except FileNotFoundError:

            self.resultado = None
            self.registros = []

            self.aplicar_filtro()

            self.etiqueta_resumen.configure(
                text="No existe el archivo de registros."
            )

            self.actualizar_detalle(
                "No se encontró logs/simulador.txt. "
                "Genera algún evento en el simulador "
                "y vuelve a pulsar Actualizar."
            )

            return

        except (OSError, UnicodeError, ValueError) as error:

            messagebox.showerror(
                "Error al leer registros",
                str(error),
                parent=self.ventana
            )

            return

        self.resultado = resultado

        # Copiar registros válidos

        self.registros = list(
            resultado["registros"]
        )

        # Añadir líneas inválidas para poder consultarlas

        for linea in resultado["lineas_invalidas"]:

            self.registros.append({
                "linea": linea["linea"],
                "fecha": "",
                "nivel": "INVALIDO",
                "mensaje": (
                    linea["motivo"]
                    + ": "
                    + linea["contenido"]
                ),
                "contenido": linea["contenido"]
            })

        niveles = resultado["niveles"]

        resumen = (
            f"Registros: {resultado['total_registros']}  |  "
            f"Errores: {len(resultado['errores'])}  |  "
            f"Advertencias: {len(resultado['advertencias'])}  |  "
            f"Líneas inválidas: "
            f"{len(resultado['lineas_invalidas'])}"
        )

        self.etiqueta_resumen.configure(
            text=resumen
        )

        self.aplicar_filtro()

    # =================================
    # APLICAR FILTRO
    # =================================

    def aplicar_filtro(self):

        filtro = self.filtro_var.get()

        if filtro == "TODOS":

            self.registros_visibles = list(
                self.registros
            )

        else:

            self.registros_visibles = [
                registro
                for registro in self.registros
                if registro["nivel"] == filtro
            ]

        # Limpiar tabla anterior

        elementos = self.tabla.get_children()

        if elementos:

            self.tabla.delete(*elementos)

        # Insertar los registros filtrados

        for indice, registro in enumerate(
            self.registros_visibles
        ):

            nivel = registro["nivel"]

            self.tabla.insert(
                "",
                "end",
                iid=str(indice),
                values=(
                    registro["linea"],
                    registro["fecha"],
                    nivel,
                    registro["mensaje"]
                ),
                tags=(nivel,)
            )

        # Actualizar la cantidad visible

        self.ventana.update_idletasks()

    # =================================
    # MOSTRAR TODOS LOS REGISTROS
    # =================================

    def mostrar_todos(self):

        self.filtro_var.set("TODOS")

        self.aplicar_filtro()

    # =================================
    # MOSTRAR DETALLE
    # =================================

    def mostrar_detalle(self, evento=None):

        seleccion = self.tabla.selection()

        if not seleccion:

            return

        indice = int(seleccion[0])

        registro = self.registros_visibles[indice]

        texto = (
            f"Línea: {registro['linea']}\n"
            f"Fecha: {registro['fecha'] or 'No disponible'}\n"
            f"Nivel: {registro['nivel']}\n"
            f"Mensaje: {registro['mensaje']}"
        )

        self.actualizar_detalle(texto)

    # =================================
    # ACTUALIZAR DETALLE
    # =================================

    def actualizar_detalle(self, texto):

        self.detalle.configure(
            state="normal"
        )

        self.detalle.delete(
            "1.0",
            "end"
        )

        self.detalle.insert(
            "1.0",
            texto
        )

        self.detalle.configure(
            state="disabled"
        )


# =================================
# EJECUCIÓN INDEPENDIENTE
# =================================

if __name__ == "__main__":

    raiz = tk.Tk()

    raiz.withdraw()

    visor = VisorLogs(raiz)

    raiz.mainloop()
