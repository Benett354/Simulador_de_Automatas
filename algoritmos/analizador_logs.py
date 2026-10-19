
from pathlib import Path
from datetime import datetime


class AnalizadorLogs:

    NIVELES = (
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    )

    def __init__(self, directorio=None):

        # Determinar la carpeta principal del proyecto

        if directorio is None:

            raiz_proyecto = Path(__file__).resolve().parents[1]

            self.directorio = raiz_proyecto / "logs"

        else:

            self.directorio = Path(directorio)

        # Archivo que genera RegistroLogs

        self.archivo_predeterminado = (
            self.directorio / "simulador.txt"
        )

    # ---------------------------------
    # Analizar un archivo TXT
    # ---------------------------------

    def analizar_archivo(self, archivo=None):

        if archivo is None:

            ruta = self.archivo_predeterminado

        else:

            ruta = Path(archivo)

            if not ruta.is_absolute():

                if ruta.exists():

                    ruta = ruta.resolve()

                else:

                    ruta = self.directorio / ruta

        if not ruta.exists():

            raise FileNotFoundError(
                f"No existe el archivo de logs: {ruta}"
            )

        registros = []
        errores = []
        advertencias = []
        lineas_invalidas = []

        niveles = {
            nivel: 0
            for nivel in self.NIVELES
        }

        # Leer el archivo sin modificarlo

        with ruta.open(
            "r",
            encoding="utf-8-sig"
        ) as archivo_txt:

            for numero, linea in enumerate(
                archivo_txt,
                start=1
            ):

                texto = linea.strip()

                # Ignorar líneas vacías

                if not texto:
                    continue

                # Separar fecha, nivel y mensaje

                partes = texto.split("|", 2)

                if len(partes) != 3:

                    lineas_invalidas.append({
                        "linea": numero,
                        "contenido": texto,
                        "motivo": "Formato incorrecto"
                    })

                    continue

                fecha = partes[0].strip()
                nivel = partes[1].strip().upper()
                mensaje = partes[2].strip()

                # Validar la fecha y hora

                try:

                    datetime.strptime(
                        fecha,
                        "%Y-%m-%d %H:%M:%S"
                    )

                except ValueError:

                    lineas_invalidas.append({
                        "linea": numero,
                        "contenido": texto,
                        "motivo": "Fecha u hora incorrecta"
                    })

                    continue

                # Validar el nivel

                if nivel not in self.NIVELES:

                    lineas_invalidas.append({
                        "linea": numero,
                        "contenido": texto,
                        "motivo": "Nivel desconocido"
                    })

                    continue

                # Guardar el registro válido

                registro = {
                    "linea": numero,
                    "fecha": fecha,
                    "nivel": nivel,
                    "mensaje": mensaje,
                    "contenido": texto
                }

                registros.append(registro)

                niveles[nivel] += 1

                if nivel in ("ERROR", "CRITICAL"):

                    errores.append(registro)

                elif nivel == "WARNING":

                    advertencias.append(registro)

        # Entregar un resumen completo

        return {
            "archivo": str(ruta),
            "total_registros": len(registros),
            "niveles": niveles,
            "registros": registros,
            "errores": errores,
            "advertencias": advertencias,
            "lineas_invalidas": lineas_invalidas
        }

    # ---------------------------------
    # Analizar todos los TXT de la carpeta
    # ---------------------------------

    def analizar_directorio(self):

        if not self.directorio.exists():

            raise FileNotFoundError(
                f"No existe la carpeta: {self.directorio}"
            )

        resultados = []

        for ruta in sorted(
            self.directorio.glob("*.txt")
        ):

            resultados.append(
                self.analizar_archivo(ruta)
            )

        return resultados

    # ---------------------------------
    # Filtrar registros por nivel
    # ---------------------------------

    def filtrar_por_nivel(
        self,
        resultado,
        nivel
    ):

        nivel = nivel.strip().upper()

        return [
            registro
            for registro in resultado["registros"]
            if registro["nivel"] == nivel
        ]

    # ---------------------------------
    # Buscar texto en los mensajes
    # ---------------------------------

    def buscar_mensaje(
        self,
        resultado,
        texto
    ):

        texto = texto.casefold()

        return [
            registro
            for registro in resultado["registros"]
            if texto in registro["mensaje"].casefold()
        ]

    # ---------------------------------
    # Mostrar resumen por consola
    # ---------------------------------

    def mostrar_resumen(self, resultado):

        print("\n===== ANALISIS DE LOGS =====")

        print(
            "Archivo:",
            resultado["archivo"]
        )

        print(
            "Total de registros:",
            resultado["total_registros"]
        )

        print("\nRegistros por nivel:")

        for nivel, cantidad in resultado["niveles"].items():

            print(f"{nivel}: {cantidad}")

        print(
            "\nErrores encontrados:",
            len(resultado["errores"])
        )

        print(
            "Advertencias encontradas:",
            len(resultado["advertencias"])
        )

        print(
            "Lineas invalidas:",
            len(resultado["lineas_invalidas"])
        )

        if resultado["errores"]:

            print("\nDetalle de errores:")

            for error in resultado["errores"]:

                print(
                    f"Linea {error['linea']}: "
                    f"{error['fecha']} | "
                    f"{error['mensaje']}"
                )
