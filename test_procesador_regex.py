import unittest

from procesador_regex import ProcesadorRegex


class TestProcesadorRegex(unittest.TestCase):


    # ---------------------------------
    # Limpieza y estructura básica
    # ---------------------------------

    def test_eliminar_espacios(self):

        procesador = ProcesadorRegex(
            " ( a | b ) * "
        )

        self.assertEqual(
            procesador.obtener_expresion(),
            "(a|b)*"
        )


    def test_obtener_simbolos(self):

        procesador = ProcesadorRegex(
            "(a|b)*abb"
        )

        self.assertEqual(
            procesador.obtener_simbolos(),
            ["a", "b"]
        )


    # ---------------------------------
    # Detección e inserción
    # de concatenaciones
    # ---------------------------------

    def test_concatenacion_dos_simbolos(self):

        procesador = ProcesadorRegex(
            "ab"
        )

        self.assertEqual(
            procesador.obtener_expresion_concatenada(),
            "a·b"
        )


    def test_concatenacion_tres_simbolos(self):

        procesador = ProcesadorRegex(
            "abc"
        )

        self.assertEqual(
            procesador.obtener_expresion_concatenada(),
            "a·b·c"
        )


    def test_simbolo_seguido_de_grupo(self):

        procesador = ProcesadorRegex(
            "a(b|c)"
        )

        self.assertEqual(
            procesador.obtener_expresion_concatenada(),
            "a·(b|c)"
        )


    def test_grupo_seguido_de_simbolo(self):

        procesador = ProcesadorRegex(
            "(a|b)c"
        )

        self.assertEqual(
            procesador.obtener_expresion_concatenada(),
            "(a|b)·c"
        )


    def test_dos_grupos_consecutivos(self):

        procesador = ProcesadorRegex(
            "(a|b)(c|d)"
        )

        self.assertEqual(
            procesador.obtener_expresion_concatenada(),
            "(a|b)·(c|d)"
        )


    def test_concatenacion_despues_de_estrella(self):

        procesador = ProcesadorRegex(
            "a*b"
        )

        self.assertEqual(
            procesador.obtener_expresion_concatenada(),
            "a*·b"
        )


    def test_union_no_genera_concatenacion(self):

        procesador = ProcesadorRegex(
            "a|b"
        )

        self.assertEqual(
            procesador.obtener_expresion_concatenada(),
            "a|b"
        )


    # ---------------------------------
    # Precedencia
    # ---------------------------------

    def test_precedencia_operador_estrella(self):

        procesador = ProcesadorRegex()

        self.assertEqual(
            procesador.obtener_precedencia("*"),
            3
        )


    def test_precedencia_concatenacion(self):

        procesador = ProcesadorRegex()

        self.assertEqual(
            procesador.obtener_precedencia("·"),
            2
        )


    def test_precedencia_union(self):

        procesador = ProcesadorRegex()

        self.assertEqual(
            procesador.obtener_precedencia("|"),
            1
        )


    # ---------------------------------
    # Conversión a postfija
    # ---------------------------------

    def test_postfija_union(self):

        procesador = ProcesadorRegex(
            "a|b"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "ab|"
        )


    def test_postfija_concatenacion(self):

        procesador = ProcesadorRegex(
            "ab"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "ab·"
        )


    def test_postfija_con_parentesis(self):

        procesador = ProcesadorRegex(
            "(a|b)c"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "ab|c·"
        )


    def test_postfija_estrella_kleene(self):

        procesador = ProcesadorRegex(
            "(a|b)*"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "ab|*"
        )


    def test_postfija_expresion_completa(self):

        procesador = ProcesadorRegex(
            "(a|b)*abb"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "ab|*a·b·b·"
        )


    def test_postfija_respeta_precedencia(self):

        procesador = ProcesadorRegex(
            "a|bc"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "abc·|"
        )


    # ---------------------------------
    # Operadores especiales
    # ---------------------------------

    def test_operador_positivo(self):

        procesador = ProcesadorRegex(
            "a+b"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "a+b·"
        )


    def test_operador_opcional(self):

        procesador = ProcesadorRegex(
            "a?b"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "a?b·"
        )


    def test_epsilon_en_postfija(self):

        procesador = ProcesadorRegex(
            "(a|ε)b"
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "aε|b·"
        )


    # ---------------------------------
    # Tokens para Thompson
    # ---------------------------------

    def test_clasificar_epsilon(self):

        procesador = ProcesadorRegex()

        self.assertEqual(
            procesador.clasificar_token("ε"),
            "EPSILON"
        )


    def test_clasificar_operadores(self):

        procesador = ProcesadorRegex()

        self.assertEqual(
            procesador.clasificar_token("|"),
            "UNION"
        )

        self.assertEqual(
            procesador.clasificar_token("·"),
            "CONCATENACION"
        )

        self.assertEqual(
            procesador.clasificar_token("*"),
            "KLEENE"
        )

        self.assertEqual(
            procesador.clasificar_token("+"),
            "POSITIVA"
        )

        self.assertEqual(
            procesador.clasificar_token("?"),
            "OPCIONAL"
        )


    def test_tokens_para_thompson(self):

        procesador = ProcesadorRegex(
            "a|b"
        )

        esperado = [
            ("SIMBOLO", "a"),
            ("SIMBOLO", "b"),
            ("UNION", "|")
        ]

        self.assertEqual(
            procesador.obtener_tokens_para_thompson(),
            esperado
        )


    # ---------------------------------
    # Integración con Wilmer
    # ---------------------------------

    def test_expresion_valida_puede_procesarse(self):

        procesador = ProcesadorRegex(
            "(a|b)*abb"
        )

        self.assertTrue(
            procesador.es_expresion_valida()
        )

        self.assertEqual(
            procesador.obtener_postfija(),
            "ab|*a·b·b·"
        )


    def test_doble_union_es_bloqueada(self):

        procesador = ProcesadorRegex(
            "a||b"
        )

        self.assertFalse(
            procesador.es_expresion_valida()
        )

        with self.assertRaises(
            ValueError
        ):

            procesador.obtener_postfija()


    def test_grupo_vacio_es_bloqueado(self):

        procesador = ProcesadorRegex(
            "()"
        )

        self.assertFalse(
            procesador.es_expresion_valida()
        )

        with self.assertRaises(
            ValueError
        ):

            procesador.obtener_postfija()


    def test_operador_al_inicio_es_bloqueado(self):

        procesador = ProcesadorRegex(
            "*ab"
        )

        self.assertFalse(
            procesador.es_expresion_valida()
        )

        with self.assertRaises(
            ValueError
        ):

            procesador.obtener_postfija()


    def test_parentesis_incompleto_es_bloqueado(self):

        procesador = ProcesadorRegex(
            "(a|b"
        )

        self.assertFalse(
            procesador.es_expresion_valida()
        )

        with self.assertRaises(
            ValueError
        ):

            procesador.obtener_postfija()


if __name__ == "__main__":

    unittest.main()