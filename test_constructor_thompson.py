
import unittest

from constructor_thompson import ConstructorThompson


# ---------------------------------
# Simular el AFN mediante sus transiciones
# ---------------------------------

def clausura_epsilon(constructor, estados):

    cierre = set(estados)

    pendientes = list(estados)

    while pendientes:

        estado = pendientes.pop()

        destinos = constructor.obtener_transicion(
            estado,
            "ε"
        )

        for destino in destinos:

            if destino not in cierre:

                cierre.add(destino)

                pendientes.append(destino)

    return cierre


def acepta_cadena(constructor, fragmento, cadena):

    # Paso 1: iniciar desde el estado inicial
    # incluyendo todos los estados alcanzables por epsilon

    actuales = clausura_epsilon(
        constructor,
        {fragmento.estado_inicial}
    )

    # Paso 2: procesar cada símbolo de la cadena

    for simbolo in cadena:

        siguientes = set()

        for estado in actuales:

            destinos = constructor.obtener_transicion(
                estado,
                simbolo
            )

            siguientes.update(destinos)

        # Paso 3: calcular la clausura epsilon
        # después de consumir el símbolo

        actuales = clausura_epsilon(
            constructor,
            siguientes
        )

    # Paso 4: comprobar si el estado final
    # es alcanzable después de consumir la cadena

    return fragmento.estado_final in actuales


# =================================
# PRUEBAS AUTOMÁTICAS
# =================================

class PruebasConstructorThompson(unittest.TestCase):

    def setUp(self):

        self.constructor = ConstructorThompson()

    # ---------------------------------
    # Prueba 1: símbolo
    # ---------------------------------

    def test_fragmento_simbolo(self):

        fragmento = (
            self.constructor.construir_fragmento_simbolo("a")
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "a"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "b"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                ""
            )
        )

    # ---------------------------------
    # Prueba 2: epsilon
    # ---------------------------------

    def test_fragmento_epsilon(self):

        fragmento = (
            self.constructor.construir_fragmento_epsilon()
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                ""
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "a"
            )
        )

    # ---------------------------------
    # Prueba 3: unión
    # ---------------------------------

    def test_union(self):

        self.constructor.construir_fragmento_simbolo("a")

        self.constructor.construir_fragmento_simbolo("b")

        fragmento = self.constructor.construir_union()

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "a"
            )
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "b"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                ""
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "ab"
            )
        )

    # ---------------------------------
    # Prueba 4: concatenación
    # ---------------------------------

    def test_concatenacion(self):

        self.constructor.construir_fragmento_simbolo("a")

        self.constructor.construir_fragmento_simbolo("b")

        fragmento = (
            self.constructor.construir_concatenacion()
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "ab"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "a"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "ba"
            )
        )

    # ---------------------------------
    # Prueba 5: cerradura de Kleene
    # ---------------------------------

    def test_cerradura_kleene(self):

        self.constructor.construir_fragmento_simbolo("a")

        fragmento = (
            self.constructor.construir_cerradura_kleene()
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                ""
            )
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "a"
            )
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "aaa"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "b"
            )
        )

    # ---------------------------------
    # Prueba 6: operador positivo
    # ---------------------------------

    def test_cerradura_positiva(self):

        self.constructor.construir_fragmento_simbolo("a")

        fragmento = (
            self.constructor.construir_cerradura_positiva()
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                ""
            )
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "a"
            )
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "aaa"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "b"
            )
        )

    # ---------------------------------
    # Prueba 7: operador opcional
    # ---------------------------------

    def test_operador_opcional(self):

        self.constructor.construir_fragmento_simbolo("a")

        fragmento = (
            self.constructor.construir_operador_opcional()
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                ""
            )
        )

        self.assertTrue(
            acepta_cadena(
                self.constructor,
                fragmento,
                "a"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "aa"
            )
        )

        self.assertFalse(
            acepta_cadena(
                self.constructor,
                fragmento,
                "b"
            )
        )

    # ---------------------------------
    # Prueba 8: expresión combinada
    # (a|b)*abb
    # ---------------------------------

    def test_expresion_combinada(self):

        # Construir a|b

        self.constructor.construir_fragmento_simbolo("a")

        self.constructor.construir_fragmento_simbolo("b")

        self.constructor.construir_union()

        # Aplicar la cerradura de Kleene

        self.constructor.construir_cerradura_kleene()

        # Concatenar a

        self.constructor.construir_fragmento_simbolo("a")

        self.constructor.construir_concatenacion()

        # Concatenar el primer b

        self.constructor.construir_fragmento_simbolo("b")

        self.constructor.construir_concatenacion()

        # Concatenar el segundo b

        self.constructor.construir_fragmento_simbolo("b")

        fragmento = (
            self.constructor.construir_concatenacion()
        )

        # Cadenas que deben aceptarse

        cadenas_aceptadas = [
            "abb",
            "aabb",
            "babb",
            "abababb"
        ]

        for cadena in cadenas_aceptadas:

            with self.subTest(cadena=cadena):

                self.assertTrue(
                    acepta_cadena(
                        self.constructor,
                        fragmento,
                        cadena
                    )
                )

        # Cadenas que deben rechazarse

        cadenas_rechazadas = [
            "",
            "ab",
            "aba",
            "abba"
        ]

        for cadena in cadenas_rechazadas:

            with self.subTest(cadena=cadena):

                self.assertFalse(
                    acepta_cadena(
                        self.constructor,
                        fragmento,
                        cadena
                    )
                )

    # ---------------------------------
    # Prueba 9: errores de construcción
    # ---------------------------------

    def test_union_sin_fragmentos(self):

        with self.assertRaises(ValueError):

            self.constructor.construir_union()

    def test_concatenacion_sin_fragmentos(self):

        with self.assertRaises(ValueError):

            self.constructor.construir_concatenacion()

    def test_kleene_sin_fragmento(self):

        with self.assertRaises(ValueError):

            self.constructor.construir_cerradura_kleene()

    def test_positivo_sin_fragmento(self):

        with self.assertRaises(ValueError):

            self.constructor.construir_cerradura_positiva()

    def test_opcional_sin_fragmento(self):

        with self.assertRaises(ValueError):

            self.constructor.construir_operador_opcional()

    # ---------------------------------
    # Prueba 10: reiniciar constructor
    # ---------------------------------

    def test_reiniciar(self):

        self.constructor.construir_fragmento_simbolo("a")

        self.constructor.reiniciar()

        self.assertEqual(
            self.constructor.obtener_estados(),
            []
        )

        self.assertEqual(
            self.constructor.obtener_transiciones(),
            {}
        )

        self.assertEqual(
            self.constructor.pila_fragmentos,
            []
        )


if __name__ == "__main__":

    unittest.main(verbosity=2)
