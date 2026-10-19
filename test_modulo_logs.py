
import io
import logging
import unittest
import uuid

from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from registro_logs import RegistroLogs
from algoritmos.analizador_logs import AnalizadorLogs
from visor_logs import VisorLogs


# =========================================================
# FUNCIONES AUXILIARES PARA LAS PRUEBAS
# =========================================================

def obtener_handlers_archivo(ruta):
    """Obtiene los manejadores que escriben en un archivo."""

    ruta_objetivo = ruta.resolve()
    loggers = [logging.getLogger()]

    for logger in logging.Logger.manager.loggerDict.values():

        if isinstance(logger, logging.Logger):
            loggers.append(logger)

    handlers_encontrados = []

    for logger in loggers:

        for handler in logger.handlers:

            if not isinstance(handler, logging.FileHandler):
                continue

            try:

                ruta_handler = Path(
                    handler.baseFilename
                ).resolve()

                if ruta_handler == ruta_objetivo:

                    handlers_encontrados.append(
                        (logger, handler)
                    )

            except (OSError, ValueError):
                continue

    return handlers_encontrados


def cerrar_handlers_archivo(ruta):

    for logger, handler in obtener_handlers_archivo(ruta):

        logger.removeHandler(handler)
        handler.flush()
        handler.close()


# =========================================================
# PRUEBAS DEL REGISTRO DE EVENTOS
# =========================================================

class TestRegistroLogs(unittest.TestCase):

    def test_registra_eventos_en_archivo(self):

        ruta = Path("logs") / "simulador.txt"

        ruta.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        archivo_existia = ruta.exists()

        contenido_original = (
            ruta.read_bytes()
            if archivo_existia
            else None
        )

        identificador = uuid.uuid4().hex

        try:

            registro = RegistroLogs()

            mensaje_info = f"PRUEBA_{identificador}_INFO"
            mensaje_advertencia = (
                f"PRUEBA_{identificador}_ADVERTENCIA"
            )
            mensaje_warning = (
                f"PRUEBA_{identificador}_WARNING"
            )
            mensaje_error = f"PRUEBA_{identificador}_ERROR"
            mensaje_excepcion = (
                f"PRUEBA_{identificador}_EXCEPCION"
            )

            registro.info(mensaje_info)

            registro.advertencia(
                mensaje_advertencia
            )

            registro.advertencia(
                mensaje_warning
            )

            registro.error(
                mensaje_error
            )

            try:

                raise RuntimeError(
                    "Excepción controlada para prueba"
                )

            except RuntimeError:

                registro.excepcion(
                    mensaje_excepcion
                )

            # Asegurar que los registros estén escritos.

            for _, handler in obtener_handlers_archivo(ruta):
                handler.flush()

            self.assertTrue(
                ruta.exists(),
                "No se creó el archivo de registros."
            )

            contenido = ruta.read_text(
                encoding="utf-8"
            )

            mensajes = [
                mensaje_info,
                mensaje_advertencia,
                mensaje_warning,
                mensaje_error,
                mensaje_excepcion
            ]

            for mensaje in mensajes:

                with self.subTest(mensaje=mensaje):

                    self.assertIn(
                        mensaje,
                        contenido
                    )

        finally:

            cerrar_handlers_archivo(ruta)

            # Restaurar el archivo original para que
            # las pruebas no alteren los logs del usuario.

            if archivo_existia:

                ruta.write_bytes(
                    contenido_original
                )

            elif ruta.exists():

                ruta.unlink()


# =========================================================
# PRUEBAS DEL ANALIZADOR DE LOGS
# =========================================================

class TestAnalizadorLogs(unittest.TestCase):

    def setUp(self):

        self.directorio_temporal = TemporaryDirectory()

        self.directorio = Path(
            self.directorio_temporal.name
        )

        self.archivo = (
            self.directorio / "simulador.txt"
        )

        self.analizador = AnalizadorLogs(
            directorio=self.directorio
        )

    def tearDown(self):

        self.directorio_temporal.cleanup()

    def escribir_registros(self, contenido):

        self.archivo.write_text(
            contenido,
            encoding="utf-8"
        )

    def test_cuenta_correctamente_los_niveles(self):

        contenido = (
            "2026-10-18 10:00:00 | DEBUG | Depuración\n"
            "2026-10-18 10:01:00 | INFO | Inicio\n"
            "2026-10-18 10:02:00 | WARNING | Advertencia\n"
            "2026-10-18 10:03:00 | ERROR | Error de prueba\n"
            "2026-10-18 10:04:00 | CRITICAL | Error crítico\n"
        )

        self.escribir_registros(contenido)

        resultado = self.analizador.analizar_archivo()

        self.assertEqual(
            resultado["total_registros"],
            5
        )

        self.assertEqual(
            resultado["niveles"]["DEBUG"],
            1
        )

        self.assertEqual(
            resultado["niveles"]["INFO"],
            1
        )

        self.assertEqual(
            resultado["niveles"]["WARNING"],
            1
        )

        self.assertEqual(
            resultado["niveles"]["ERROR"],
            1
        )

        self.assertEqual(
            resultado["niveles"]["CRITICAL"],
            1
        )

        self.assertEqual(
            len(resultado["errores"]),
            2
        )

        self.assertEqual(
            len(resultado["advertencias"]),
            1
        )

        self.assertEqual(
            len(resultado["lineas_invalidas"]),
            0
        )

    def test_detecta_lineas_invalidas(self):

        contenido = (
            "2026-10-18 10:00:00 | INFO | Registro válido\n"
            "Esta línea no tiene el formato esperado\n"
            "2026-13-18 10:02:00 | ERROR | Fecha incorrecta\n"
            "2026-10-18 10:03:00 | DESCONOCIDO | Nivel inválido\n"
        )

        self.escribir_registros(contenido)

        resultado = self.analizador.analizar_archivo()

        self.assertEqual(
            resultado["total_registros"],
            1
        )

        self.assertEqual(
            len(resultado["lineas_invalidas"]),
            3
        )

        motivos = [
            linea["motivo"]
            for linea in resultado["lineas_invalidas"]
        ]

        self.assertIn(
            "Formato incorrecto",
            motivos
        )

        self.assertIn(
            "Fecha u hora incorrecta",
            motivos
        )

        self.assertIn(
            "Nivel desconocido",
            motivos
        )

    def test_filtra_registros_por_nivel(self):

        contenido = (
            "2026-10-18 10:00:00 | INFO | Inicio\n"
            "2026-10-18 10:01:00 | ERROR | Error uno\n"
            "2026-10-18 10:02:00 | ERROR | Error dos\n"
            "2026-10-18 10:03:00 | WARNING | Advertencia\n"
        )

        self.escribir_registros(contenido)

        resultado = self.analizador.analizar_archivo()

        errores = self.analizador.filtrar_por_nivel(
            resultado,
            "error"
        )

        self.assertEqual(
            len(errores),
            2
        )

        for error in errores:

            self.assertEqual(
                error["nivel"],
                "ERROR"
            )

    def test_busca_mensajes_sin_distinguir_mayusculas(self):

        contenido = (
            "2026-10-18 10:00:00 | INFO | Inicio del simulador\n"
            "2026-10-18 10:01:00 | ERROR | Error de conexión\n"
            "2026-10-18 10:02:00 | INFO | Proceso terminado\n"
        )

        self.escribir_registros(contenido)

        resultado = self.analizador.analizar_archivo()

        encontrados = self.analizador.buscar_mensaje(
            resultado,
            "ERROR DE CONEXIÓN"
        )

        self.assertEqual(
            len(encontrados),
            1
        )

        self.assertEqual(
            encontrados[0]["nivel"],
            "ERROR"
        )

    def test_analiza_varios_archivos(self):

        self.escribir_registros(
            "2026-10-18 10:00:00 | INFO | Primer archivo\n"
        )

        segundo = self.directorio / "segundo.txt"

        segundo.write_text(
            "2026-10-18 10:01:00 | ERROR | Segundo archivo\n",
            encoding="utf-8"
        )

        resultados = self.analizador.analizar_directorio()

        self.assertEqual(
            len(resultados),
            2
        )

        total = sum(
            resultado["total_registros"]
            for resultado in resultados
        )

        self.assertEqual(
            total,
            2
        )

    def test_archivo_inexistente_lanza_error(self):

        with self.assertRaises(FileNotFoundError):

            self.analizador.analizar_archivo()

    def test_muestra_resumen(self):

        self.escribir_registros(
            "2026-10-18 10:00:00 | INFO | Inicio\n"
            "2026-10-18 10:01:00 | ERROR | Error de prueba\n"
        )

        resultado = self.analizador.analizar_archivo()

        salida = io.StringIO()

        with redirect_stdout(salida):

            self.analizador.mostrar_resumen(
                resultado
            )

        texto = salida.getvalue()

        self.assertIn(
            "ANALISIS DE LOGS",
            texto
        )

        self.assertIn(
            "Total de registros: 2",
            texto
        )

        self.assertIn(
            "Errores encontrados: 1",
            texto
        )


# =========================================================
# PRUEBAS DEL FILTRO Y ORDEN DEL VISOR
# =========================================================

class TestVisorLogs(unittest.TestCase):

    def crear_visor_simulado(self, filtro="TODOS"):

        # No se crea ninguna ventana real de Tkinter.
        # Se prueban los métodos utilizando objetos simulados.

        visor = VisorLogs.__new__(VisorLogs)

        visor.filtro_var = Mock()

        visor.filtro_var.get.return_value = filtro

        visor.registros = [
            {
                "linea": 1,
                "fecha": "2026-10-18 09:00:00",
                "nivel": "INFO",
                "mensaje": "Inicio",
                "contenido": "Inicio"
            },
            {
                "linea": 2,
                "fecha": "2026-10-18 09:00:00",
                "nivel": "ERROR",
                "mensaje": "Error antiguo",
                "contenido": "Error antiguo"
            },
            {
                "linea": 3,
                "fecha": "2026-10-18 08:00:00",
                "nivel": "CRITICAL",
                "mensaje": "Error crítico",
                "contenido": "Error crítico"
            },
            {
                "linea": 4,
                "fecha": "2026-10-18 10:00:00",
                "nivel": "WARNING",
                "mensaje": "Advertencia",
                "contenido": "Advertencia"
            },
            {
                "linea": 5,
                "fecha": "",
                "nivel": "INVALIDO",
                "mensaje": "Línea incorrecta",
                "contenido": "Línea incorrecta"
            },
            {
                "linea": 6,
                "fecha": "2026-10-18 10:00:00",
                "nivel": "ERROR",
                "mensaje": "Error reciente",
                "contenido": "Error reciente"
            },
            {
                "linea": 7,
                "fecha": "2026-10-18 10:00:00",
                "nivel": "DEBUG",
                "mensaje": "Depuración",
                "contenido": "Depuración"
            }
        ]

        visor.registros_visibles = []

        visor.tabla = Mock()

        visor.tabla.get_children.return_value = []

        visor.ventana = Mock()

        return visor

    def test_errores_aparecen_antes_que_info(self):

        visor = self.crear_visor_simulado()

        visor.aplicar_filtro()

        niveles = [
            registro["nivel"]
            for registro in visor.registros_visibles
        ]

        self.assertEqual(
            niveles,
            [
                "CRITICAL",
                "ERROR",
                "ERROR",
                "INVALIDO",
                "WARNING",
                "INFO",
                "DEBUG"
            ]
        )

    def test_errores_mas_recientes_aparecen_primero(self):

        visor = self.crear_visor_simulado()

        visor.aplicar_filtro()

        errores = [
            registro
            for registro in visor.registros_visibles
            if registro["nivel"] == "ERROR"
        ]

        self.assertEqual(
            errores[0]["mensaje"],
            "Error reciente"
        )

        self.assertEqual(
            errores[1]["mensaje"],
            "Error antiguo"
        )

    def test_filtro_error_muestra_solo_errores(self):

        visor = self.crear_visor_simulado(
            filtro="ERROR"
        )

        visor.aplicar_filtro()

        self.assertEqual(
            len(visor.registros_visibles),
            2
        )

        for registro in visor.registros_visibles:

            self.assertEqual(
                registro["nivel"],
                "ERROR"
            )

    def test_filtro_todos_muestra_todos_los_registros(self):

        visor = self.crear_visor_simulado(
            filtro="TODOS"
        )

        visor.aplicar_filtro()

        self.assertEqual(
            len(visor.registros_visibles),
            7
        )

        self.assertEqual(
            visor.tabla.insert.call_count,
            7
        )

    def test_actualiza_la_ventana_despues_de_filtrar(self):

        visor = self.crear_visor_simulado()

        visor.aplicar_filtro()

        visor.ventana.update_idletasks.assert_called_once()


# =========================================================
# EJECUTAR LAS PRUEBAS DIRECTAMENTE
# =========================================================

if __name__ == "__main__":

    unittest.main(verbosity=2)
