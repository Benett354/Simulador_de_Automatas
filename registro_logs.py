
from pathlib import Path
import logging


class RegistroLogs:

    def __init__(
        self,
        directorio="logs",
        archivo="simulador.txt"
    ):

        # Crear la carpeta de registros si no existe

        self.directorio = Path(directorio)

        self.directorio.mkdir(
            parents=True,
            exist_ok=True
        )

        # Ruta del archivo donde se guardarán los logs

        self.ruta_archivo = self.directorio / archivo

        # Crear el registrador de eventos

        nombre_logger = (
            f"simulador.{self.ruta_archivo.resolve()}"
        )

        self.logger = logging.getLogger(
            nombre_logger
        )

        self.logger.setLevel(logging.INFO)

        # Evitar que los registros se dupliquen
        # en otros registradores de Python

        self.logger.propagate = False

        # Configurar el archivo una sola vez

        if not self.logger.handlers:

            manejador = logging.FileHandler(
                self.ruta_archivo,
                encoding="utf-8"
            )

            formato = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            manejador.setFormatter(formato)

            self.logger.addHandler(manejador)

    # ---------------------------------
    # Registrar información
    # ---------------------------------

    def info(self, mensaje):

        self.logger.info(mensaje)

    # ---------------------------------
    # Registrar advertencias
    # ---------------------------------

    def advertencia(self, mensaje):

        self.logger.warning(mensaje)

    # ---------------------------------
    # Registrar errores
    # ---------------------------------

    def error(self, mensaje):

        self.logger.error(mensaje)

    # ---------------------------------
    # Registrar excepciones
    # ---------------------------------

    def excepcion(self, mensaje):

        self.logger.exception(mensaje)

    # ---------------------------------
    # Obtener la ruta del archivo
    # ---------------------------------

    def obtener_ruta(self):

        return str(self.ruta_archivo)
