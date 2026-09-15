import unittest

from automata import Automata
from simulador import Simulador
from conversion import ConversionAFN_AFD
from minimizacion import MinimizadorAFD


# =========================================================
# PRUEBAS DE LA CLASE AUTOMATA
# =========================================================

class TestAutomata(unittest.TestCase):


    # -----------------------------------------------------
    # 1. Crear AFD válido
    # -----------------------------------------------------

    def test_01_crear_afd_valido(self):

        afd = Automata("AFD")

        afd.agregar_estado("q0")
        afd.agregar_estado("q1")

        afd.agregar_simbolo("0")

        afd.establecer_estado_inicial("q0")
        afd.agregar_estado_final("q1")

        afd.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        self.assertTrue(
            afd.es_valido()
        )



    # -----------------------------------------------------
    # 2. Estado inicial inexistente
    # -----------------------------------------------------

    def test_02_estado_inicial_inexistente(self):

        afd = Automata("AFD")

        afd.agregar_estado("q0")

        with self.assertRaises(ValueError):

            afd.establecer_estado_inicial(
                "q9"
            )



    # -----------------------------------------------------
    # 3. Estado final inexistente
    # -----------------------------------------------------

    def test_03_estado_final_inexistente(self):

        afd = Automata("AFD")

        afd.agregar_estado("q0")

        with self.assertRaises(ValueError):

            afd.agregar_estado_final(
                "q5"
            )



    # -----------------------------------------------------
    # 4. Epsilon no pertenece al alfabeto
    # -----------------------------------------------------

    def test_04_epsilon_no_pertenece_alfabeto(self):

        afn = Automata("AFN")

        with self.assertRaises(ValueError):

            afn.agregar_simbolo(
                "ε"
            )



    # -----------------------------------------------------
    # 5. Símbolos de más de un carácter
    # -----------------------------------------------------

    def test_05_simbolo_multiple_invalido(self):

        afd = Automata("AFD")

        with self.assertRaises(ValueError):

            afd.agregar_simbolo(
                "01"
            )



    # -----------------------------------------------------
    # 6. AFD no acepta dos destinos distintos
    # -----------------------------------------------------

    def test_06_afd_no_permite_dos_destinos(self):

        afd = Automata("AFD")

        for estado in [
            "q0",
            "q1",
            "q2"
        ]:

            afd.agregar_estado(
                estado
            )

        afd.agregar_simbolo("0")

        afd.establecer_estado_inicial(
            "q0"
        )

        afd.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        with self.assertRaises(ValueError):

            afd.agregar_transicion(
                "q0",
                "0",
                "q2"
            )



    # -----------------------------------------------------
    # 7. AFN sí permite múltiples destinos
    # -----------------------------------------------------

    def test_07_afn_permite_dos_destinos(self):

        afn = Automata("AFN")

        for estado in [
            "q0",
            "q1",
            "q2"
        ]:

            afn.agregar_estado(
                estado
            )

        afn.agregar_simbolo("0")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        afn.agregar_transicion(
            "q0",
            "0",
            "q2"
        )

        destinos = afn.obtener_transicion(
            "q0",
            "0"
        )

        self.assertEqual(
            destinos,
            {"q1", "q2"}
        )



    # -----------------------------------------------------
    # 8. AFD no permite epsilon
    # -----------------------------------------------------

    def test_08_afd_no_permite_epsilon(self):

        afd = Automata("AFD")

        afd.agregar_estado("q0")
        afd.agregar_estado("q1")

        afd.agregar_simbolo("0")

        afd.establecer_estado_inicial(
            "q0"
        )

        with self.assertRaises(ValueError):

            afd.agregar_transicion(
                "q0",
                "ε",
                "q1"
            )


# =========================================================
# PRUEBAS DEL SIMULADOR
# =========================================================

class TestSimulador(unittest.TestCase):


    # -----------------------------------------------------
    # Crear AFD de prueba
    # -----------------------------------------------------

    def crear_afd(self):

        afd = Automata("AFD")

        for estado in [
            "q0",
            "q1",
            "q2"
        ]:

            afd.agregar_estado(
                estado
            )

        afd.agregar_simbolo("0")
        afd.agregar_simbolo("1")

        afd.establecer_estado_inicial(
            "q0"
        )

        afd.agregar_estado_final(
            "q2"
        )

        afd.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        afd.agregar_transicion(
            "q1",
            "1",
            "q2"
        )

        return afd



    # -----------------------------------------------------
    # 9. AFD acepta una cadena
    # -----------------------------------------------------

    def test_09_afd_acepta_cadena(self):

        afd = self.crear_afd()

        simulador = Simulador(
            afd
        )

        aceptada, recorrido, mensaje = (
            simulador.simular_afd(
                "01"
            )
        )

        self.assertTrue(
            aceptada
        )

        self.assertEqual(
            mensaje,
            "Cadena aceptada"
        )



    # -----------------------------------------------------
    # 10. AFD rechaza cuando no existe transición
    # -----------------------------------------------------

    def test_10_afd_rechaza_cadena(self):

        afd = self.crear_afd()

        simulador = Simulador(
            afd
        )

        aceptada, recorrido, mensaje = (
            simulador.simular_afd(
                "00"
            )
        )

        self.assertFalse(
            aceptada
        )



    # -----------------------------------------------------
    # 11. Símbolo inválido
    # -----------------------------------------------------

    def test_11_simbolo_invalido(self):

        afd = self.crear_afd()

        simulador = Simulador(
            afd
        )

        aceptada, recorrido, mensaje = (
            simulador.simular_afd(
                "02"
            )
        )

        self.assertFalse(
            aceptada
        )

        self.assertIn(
            "Símbolo inválido",
            mensaje
        )



    # -----------------------------------------------------
    # 12. AFN acepta por uno de varios caminos
    # -----------------------------------------------------

    def test_12_afn_no_determinista(self):

        afn = Automata("AFN")

        for estado in [
            "q0",
            "q1",
            "q2",
            "q3"
        ]:

            afn.agregar_estado(
                estado
            )

        afn.agregar_simbolo("0")
        afn.agregar_simbolo("1")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_estado_final(
            "q3"
        )

        afn.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        afn.agregar_transicion(
            "q0",
            "0",
            "q2"
        )

        afn.agregar_transicion(
            "q1",
            "1",
            "q3"
        )

        simulador = Simulador(
            afn
        )

        aceptada, recorrido, mensaje = (
            simulador.simular_afn(
                "01"
            )
        )

        self.assertTrue(
            aceptada
        )



    # -----------------------------------------------------
    # 13. Epsilon clausura transitiva
    # -----------------------------------------------------

    def test_13_epsilon_clausura(self):

        afn = Automata("AFN")

        for estado in [
            "q0",
            "q1",
            "q2"
        ]:

            afn.agregar_estado(
                estado
            )

        afn.agregar_simbolo("0")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_transicion(
            "q0",
            "ε",
            "q1"
        )

        afn.agregar_transicion(
            "q1",
            "ε",
            "q2"
        )

        simulador = Simulador(
            afn
        )

        clausura = simulador.epsilon_clausura(
            {"q0"}
        )

        self.assertEqual(
            clausura,
            {"q0", "q1", "q2"}
        )



    # -----------------------------------------------------
    # 14. AFN acepta usando epsilon
    # -----------------------------------------------------

    def test_14_afn_con_epsilon(self):

        afn = Automata("AFN")

        for estado in [
            "q0",
            "q1",
            "q2",
            "q3"
        ]:

            afn.agregar_estado(
                estado
            )

        afn.agregar_simbolo("0")
        afn.agregar_simbolo("1")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_estado_final(
            "q3"
        )

        afn.agregar_transicion(
            "q0",
            "ε",
            "q1"
        )

        afn.agregar_transicion(
            "q1",
            "0",
            "q2"
        )

        afn.agregar_transicion(
            "q2",
            "1",
            "q3"
        )

        simulador = Simulador(
            afn
        )

        aceptada, recorrido, mensaje = (
            simulador.simular_afn(
                "01"
            )
        )

        self.assertTrue(
            aceptada
        )



    # -----------------------------------------------------
    # 15. Cadena vacía aceptada mediante epsilon
    # -----------------------------------------------------

    def test_15_cadena_vacia_con_epsilon(self):

        afn = Automata("AFN")

        afn.agregar_estado("q0")
        afn.agregar_estado("q1")

        afn.agregar_simbolo("0")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_estado_final(
            "q1"
        )

        afn.agregar_transicion(
            "q0",
            "ε",
            "q1"
        )

        simulador = Simulador(
            afn
        )

        aceptada, recorrido, mensaje = (
            simulador.simular_afn(
                ""
            )
        )

        self.assertTrue(
            aceptada
        )


# =========================================================
# PRUEBAS DE CONVERSIÓN AFN -> AFD
# =========================================================

class TestConversion(unittest.TestCase):


    # -----------------------------------------------------
    # 16. Conversión básica
    # -----------------------------------------------------

    def test_16_conversion_basica(self):

        afn = Automata("AFN")

        for estado in [
            "q0",
            "q1",
            "q2"
        ]:

            afn.agregar_estado(
                estado
            )

        afn.agregar_simbolo("0")
        afn.agregar_simbolo("1")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_estado_final(
            "q2"
        )

        afn.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        afn.agregar_transicion(
            "q1",
            "1",
            "q2"
        )

        conversion = ConversionAFN_AFD(
            afn
        )

        afd = conversion.convertir()

        self.assertEqual(
            afd.tipo,
            "AFD"
        )

        self.assertTrue(
            afd.es_valido()
        )

        self.assertIsNotNone(
            afd.estado_inicial
        )



    # -----------------------------------------------------
    # 17. AFN y AFD convertido reconocen lo mismo
    # -----------------------------------------------------

    def test_17_conversion_preserva_lenguaje(self):

        afn = Automata("AFN")

        for estado in [
            "q0",
            "q1",
            "q2"
        ]:

            afn.agregar_estado(
                estado
            )

        afn.agregar_simbolo("0")
        afn.agregar_simbolo("1")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_estado_final(
            "q2"
        )

        afn.agregar_transicion(
            "q0",
            "0",
            "q0"
        )

        afn.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        afn.agregar_transicion(
            "q1",
            "1",
            "q2"
        )

        conversion = ConversionAFN_AFD(
            afn
        )

        afd = conversion.convertir()

        sim_afn = Simulador(
            afn
        )

        sim_afd = Simulador(
            afd
        )

        cadenas = [
            "",
            "0",
            "01",
            "001",
            "0001",
            "1",
            "11",
            "010"
        ]


        for cadena in cadenas:

            resultado_afn = sim_afn.simular_afn(
                cadena
            )[0]

            resultado_afd = sim_afd.simular_afd(
                cadena
            )[0]

            self.assertEqual(
                resultado_afn,
                resultado_afd,
                f"Resultados diferentes para la cadena '{cadena}'"
            )



    # -----------------------------------------------------
    # 18. Conversión considera epsilon clausura inicial
    # -----------------------------------------------------

    def test_18_conversion_con_epsilon(self):

        afn = Automata("AFN")

        afn.agregar_estado("q0")
        afn.agregar_estado("q1")

        afn.agregar_simbolo("0")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_estado_final(
            "q1"
        )

        afn.agregar_transicion(
            "q0",
            "ε",
            "q1"
        )

        conversion = ConversionAFN_AFD(
            afn
        )

        afd = conversion.convertir()

        self.assertIn(
            afd.estado_inicial,
            afd.estados_finales
        )



    # -----------------------------------------------------
    # 19. Conversión genera estado vacío / pozo
    # -----------------------------------------------------

    def test_19_conversion_estado_vacio(self):

        afn = Automata("AFN")

        afn.agregar_estado("q0")
        afn.agregar_estado("q1")

        afn.agregar_simbolo("0")
        afn.agregar_simbolo("1")

        afn.establecer_estado_inicial(
            "q0"
        )

        afn.agregar_estado_final(
            "q1"
        )

        afn.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        conversion = ConversionAFN_AFD(
            afn
        )

        afd = conversion.convertir()

        # Cada estado del AFD debe tener transición
        # para cada símbolo del alfabeto.
        for estado in afd.estados:

            for simbolo in afd.alfabeto:

                destino = afd.obtener_transicion(
                    estado,
                    simbolo
                )

                self.assertIsNotNone(
                    destino
                )


# =========================================================
# PRUEBAS DE MINIMIZACIÓN
# =========================================================

class TestMinimizacion(unittest.TestCase):


    # -----------------------------------------------------
    # Crear AFD reducible
    # -----------------------------------------------------

    def crear_afd_reducible(self):

        afd = Automata("AFD")

        for estado in [
            "q0",
            "q1",
            "q2",
            "q3"
        ]:

            afd.agregar_estado(
                estado
            )

        afd.agregar_simbolo("0")
        afd.agregar_simbolo("1")

        afd.establecer_estado_inicial(
            "q0"
        )

        afd.agregar_estado_final(
            "q2"
        )

        afd.agregar_estado_final(
            "q3"
        )


        afd.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        afd.agregar_transicion(
            "q0",
            "1",
            "q2"
        )


        afd.agregar_transicion(
            "q1",
            "0",
            "q0"
        )

        afd.agregar_transicion(
            "q1",
            "1",
            "q3"
        )


        afd.agregar_transicion(
            "q2",
            "0",
            "q2"
        )

        afd.agregar_transicion(
            "q2",
            "1",
            "q2"
        )


        afd.agregar_transicion(
            "q3",
            "0",
            "q3"
        )

        afd.agregar_transicion(
            "q3",
            "1",
            "q3"
        )

        return afd



    # -----------------------------------------------------
    # 20. Reducir cuatro estados a dos
    # -----------------------------------------------------

    def test_20_minimizacion_reduce_estados(self):

        afd = self.crear_afd_reducible()

        minimizador = MinimizadorAFD(
            afd
        )

        minimo = minimizador.minimizar()

        self.assertEqual(
            len(minimo.estados),
            2
        )

        self.assertTrue(
            minimo.es_valido()
        )



    # -----------------------------------------------------
    # 21. Eliminar estados inalcanzables
    # -----------------------------------------------------

    def test_21_elimina_estado_inalcanzable(self):

        afd = Automata("AFD")

        for estado in [
            "q0",
            "q1",
            "q2",
            "qX"
        ]:

            afd.agregar_estado(
                estado
            )

        afd.agregar_simbolo("0")

        afd.establecer_estado_inicial(
            "q0"
        )

        afd.agregar_estado_final(
            "q2"
        )


        afd.agregar_transicion(
            "q0",
            "0",
            "q1"
        )

        afd.agregar_transicion(
            "q1",
            "0",
            "q2"
        )

        afd.agregar_transicion(
            "q2",
            "0",
            "q2"
        )

        # Estado inalcanzable
        afd.agregar_transicion(
            "qX",
            "0",
            "qX"
        )


        minimizador = MinimizadorAFD(
            afd
        )

        minimo = minimizador.minimizar()

        mapeo = minimizador.obtener_mapeo()

        self.assertNotIn(
            "qX",
            mapeo
        )


# =========================================================
# EJECUTAR PRUEBAS
# =========================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )