import unittest

from expresion_regular import ExpresionRegular


class TestExpresionRegular(unittest.TestCase):


    # ---------------------------------
    # Pruebas de estructura básica
    # ---------------------------------

    def test_eliminar_espacios(self):

        expresion = ExpresionRegular(
            "  a | b  "
        )

        self.assertEqual(
            expresion.obtener_expresion(),
            "a|b"
        )


    def test_longitud_expresion(self):

        expresion = ExpresionRegular(
            "a|b"
        )

        self.assertEqual(
            expresion.longitud(),
            3
        )


    def test_obtener_simbolos(self):

        expresion = ExpresionRegular(
            "(a|b)*abb"
        )

        self.assertEqual(
            expresion.obtener_simbolos(),
            {"a", "b"}
        )


    def test_obtener_operadores(self):

        expresion = ExpresionRegular(
            "(a|b)*"
        )

        self.assertEqual(
            expresion.obtener_operadores(),
            ["(", "|", ")", "*"]
        )


    # ---------------------------------
    # Expresiones válidas
    # ---------------------------------

    def test_expresion_simple_valida(self):

        expresion = ExpresionRegular(
            "a"
        )

        self.assertTrue(
            expresion.es_valida()
        )


    def test_union_valida(self):

        expresion = ExpresionRegular(
            "a|b"
        )

        self.assertTrue(
            expresion.es_valida()
        )


    def test_parentesis_validos(self):

        expresion = ExpresionRegular(
            "(a|b)"
        )

        self.assertTrue(
            expresion.es_valida()
        )


    def test_estrella_kleene_valida(self):

        expresion = ExpresionRegular(
            "(a|b)*"
        )

        self.assertTrue(
            expresion.es_valida()
        )


    def test_expresion_compleja_valida(self):

        expresion = ExpresionRegular(
            "(a|b)*abb"
        )

        self.assertTrue(
            expresion.es_valida()
        )


    def test_epsilon_valido(self):

        expresion = ExpresionRegular(
            "(a|ε)b"
        )

        self.assertTrue(
            expresion.es_valida()
        )


    def test_operador_mas_valido(self):

        expresion = ExpresionRegular(
            "(a|b)+"
        )

        self.assertTrue(
            expresion.es_valida()
        )


    def test_operador_opcional_valido(self):

        expresion = ExpresionRegular(
            "a?b"
        )

        self.assertTrue(
            expresion.es_valida()
        )


    # ---------------------------------
    # Expresiones inválidas
    # ---------------------------------

    def test_expresion_vacia_invalida(self):

        expresion = ExpresionRegular(
            ""
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_caracter_invalido(self):

        expresion = ExpresionRegular(
            "a@b"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_parentesis_sin_cierre(self):

        expresion = ExpresionRegular(
            "(a|b"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_parentesis_sin_apertura(self):

        expresion = ExpresionRegular(
            "a|b)"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_union_al_inicio(self):

        expresion = ExpresionRegular(
            "|ab"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_union_al_final(self):

        expresion = ExpresionRegular(
            "ab|"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_doble_union(self):

        expresion = ExpresionRegular(
            "a||b"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_operador_unario_al_inicio(self):

        expresion = ExpresionRegular(
            "*ab"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_operadores_unarios_consecutivos(self):

        expresion = ExpresionRegular(
            "a**"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_grupo_vacio(self):

        expresion = ExpresionRegular(
            "()"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_union_antes_de_cierre(self):

        expresion = ExpresionRegular(
            "(a|)"
        )

        self.assertFalse(
            expresion.es_valida()
        )


    def test_union_despues_de_apertura(self):

        expresion = ExpresionRegular(
            "(|a)"
        )

        self.assertFalse(
            expresion.es_valida()
        )


if __name__ == "__main__":

    unittest.main()