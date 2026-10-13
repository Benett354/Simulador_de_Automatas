class ProcesadorRegex:


    # ---------------------------------
    # Operadores escritos por el usuario
    # ---------------------------------

    OPERADORES = {
        "|",
        "*",
        "+",
        "?",
        "(",
        ")"
    }


    # ---------------------------------
    # Operadores unarios
    # ---------------------------------

    OPERADORES_UNARIOS = {
        "*",
        "+",
        "?"
    }


    # ---------------------------------
    # Operador interno de concatenación
    # ---------------------------------

    OPERADOR_CONCATENACION = "·"


    # ---------------------------------
    # Precedencia de operadores
    # ---------------------------------

    PRECEDENCIA = {
        "|": 1,
        "·": 2,
        "*": 3,
        "+": 3,
        "?": 3
    }


    # ---------------------------------
    # Constructor
    # ---------------------------------

    def __init__(
        self,
        expresion=""
    ):

        self.expresion_original = ""

        self.expresion = ""

        self.establecer_expresion(
            expresion
        )


    # ---------------------------------
    # Establecer expresión
    # ---------------------------------

    def establecer_expresion(
        self,
        expresion
    ):

        expresion = str(
            expresion
        )

        self.expresion_original = expresion

        self.expresion = expresion.replace(
            " ",
            ""
        )


    # ---------------------------------
    # Obtener expresión original
    # ---------------------------------

    def obtener_expresion_original(self):

        return self.expresion_original


    # ---------------------------------
    # Obtener expresión limpia
    # ---------------------------------

    def obtener_expresion(self):

        return self.expresion


    # ---------------------------------
    # Verificar expresión vacía
    # ---------------------------------

    def esta_vacia(self):

        return self.expresion == ""


    # ---------------------------------
    # Obtener longitud
    # ---------------------------------

    def longitud(self):

        return len(
            self.expresion
        )


    # ---------------------------------
    # Verificar si es operador
    # escrito por el usuario
    # ---------------------------------

    def es_operador(
        self,
        caracter
    ):

        return caracter in self.OPERADORES


    # ---------------------------------
    # Verificar operador unario
    # ---------------------------------

    def es_operador_unario(
        self,
        caracter
    ):

        return caracter in self.OPERADORES_UNARIOS


    # ---------------------------------
    # Verificar operador interno
    # de procesamiento
    # ---------------------------------

    def es_operador_procesamiento(
        self,
        caracter
    ):

        return caracter in self.PRECEDENCIA


    # ---------------------------------
    # Obtener precedencia
    # ---------------------------------

    def obtener_precedencia(
        self,
        operador
    ):

        if operador in self.PRECEDENCIA:

            return self.PRECEDENCIA[
                operador
            ]


        return 0


    # ---------------------------------
    # Comparar precedencia
    # ---------------------------------

    def tiene_mayor_o_igual_precedencia(
        self,
        operador_1,
        operador_2
    ):

        precedencia_1 = (
            self.obtener_precedencia(
                operador_1
            )
        )

        precedencia_2 = (
            self.obtener_precedencia(
                operador_2
            )
        )


        return (
            precedencia_1
            >= precedencia_2
        )


    # ---------------------------------
    # Verificar si es símbolo
    # ---------------------------------

    def es_simbolo(
        self,
        caracter
    ):

        if caracter == "ε":

            return True


        if caracter.isalpha():

            return True


        if caracter.isdigit():

            return True


        return False


    # ---------------------------------
    # Obtener elementos
    # ---------------------------------

    def obtener_elementos(self):

        elementos = []


        for caracter in self.expresion:

            elementos.append(
                caracter
            )


        return elementos


    # ---------------------------------
    # Obtener símbolos
    # ---------------------------------

    def obtener_simbolos(self):

        simbolos = []


        for caracter in self.expresion:

            if self.es_simbolo(
                caracter
            ):

                if caracter not in simbolos:

                    simbolos.append(
                        caracter
                    )


        return simbolos


    # ---------------------------------
    # Obtener operadores
    # ---------------------------------

    def obtener_operadores(self):

        operadores = []


        for caracter in self.expresion:

            if self.es_operador(
                caracter
            ):

                operadores.append(
                    caracter
                )


        return operadores


    # ---------------------------------
    # Verificar si un elemento puede
    # terminar una expresión
    # ---------------------------------

    def puede_terminar_expresion(
        self,
        caracter
    ):

        if self.es_simbolo(
            caracter
        ):

            return True


        if caracter == ")":

            return True


        if self.es_operador_unario(
            caracter
        ):

            return True


        return False


    # ---------------------------------
    # Verificar si un elemento puede
    # iniciar una expresión
    # ---------------------------------

    def puede_iniciar_expresion(
        self,
        caracter
    ):

        if self.es_simbolo(
            caracter
        ):

            return True


        if caracter == "(":

            return True


        return False


    # ---------------------------------
    # Saber si existe concatenación
    # implícita
    # ---------------------------------

    def necesita_concatenacion(
        self,
        anterior,
        siguiente
    ):

        izquierda_valida = (
            self.puede_terminar_expresion(
                anterior
            )
        )


        derecha_valida = (
            self.puede_iniciar_expresion(
                siguiente
            )
        )


        return (
            izquierda_valida
            and derecha_valida
        )


    # ---------------------------------
    # Detectar concatenaciones
    # ---------------------------------

    def detectar_concatenaciones(self):

        concatenaciones = []


        if len(self.expresion) < 2:

            return concatenaciones


        for posicion in range(
            len(self.expresion) - 1
        ):

            anterior = self.expresion[
                posicion
            ]

            siguiente = self.expresion[
                posicion + 1
            ]


            if self.necesita_concatenacion(
                anterior,
                siguiente
            ):

                concatenaciones.append(
                    (
                        posicion + 1,
                        anterior,
                        siguiente
                    )
                )


        return concatenaciones


    # ---------------------------------
    # Saber si existen concatenaciones
    # ---------------------------------

    def tiene_concatenaciones(self):

        return len(
            self.detectar_concatenaciones()
        ) > 0


    # ---------------------------------
    # Insertar operador de concatenación
    # ---------------------------------

    def insertar_concatenaciones(self):

        if self.esta_vacia():

            return ""


        resultado = ""


        for posicion in range(
            len(self.expresion)
        ):

            actual = self.expresion[
                posicion
            ]


            resultado += actual


            if posicion == len(self.expresion) - 1:

                continue


            siguiente = self.expresion[
                posicion + 1
            ]


            if self.necesita_concatenacion(
                actual,
                siguiente
            ):

                resultado += (
                    self.OPERADOR_CONCATENACION
                )


        return resultado


    # ---------------------------------
    # Obtener expresión preparada
    # ---------------------------------

    def obtener_expresion_concatenada(self):

        return self.insertar_concatenaciones()


    # ---------------------------------
    # Mostrar tabla de precedencia
    # ---------------------------------

    def mostrar_precedencias(self):

        print(
            "\nPrecedencia de operadores:"
        )


        print(
            "*  ->",
            self.obtener_precedencia("*")
        )


        print(
            "+  ->",
            self.obtener_precedencia("+")
        )


        print(
            "?  ->",
            self.obtener_precedencia("?")
        )


        print(
            "·  ->",
            self.obtener_precedencia("·")
        )


        print(
            "|  ->",
            self.obtener_precedencia("|")
        )


    # ---------------------------------
    # Mostrar concatenaciones
    # ---------------------------------

    def mostrar_concatenaciones(self):

        concatenaciones = (
            self.detectar_concatenaciones()
        )


        if not concatenaciones:

            print(
                "No se detectaron "
                "concatenaciones implícitas."
            )

            return


        print(
            "Concatenaciones implícitas:"
        )


        for (
            posicion,
            anterior,
            siguiente
        ) in concatenaciones:

            print(
                "- Entre",
                f"'{anterior}'",
                "y",
                f"'{siguiente}'",
                "después de la posición",
                posicion
            )


    # ---------------------------------
    # Mostrar información
    # ---------------------------------

    def mostrar(self):

        print(
            "\n===== PROCESADOR REGEX ====="
        )


        print(
            "Expresión original:",
            self.expresion_original
        )


        print(
            "Expresión limpia:",
            self.expresion
        )


        print(
            "Longitud:",
            self.longitud()
        )


        print(
            "Elementos:",
            self.obtener_elementos()
        )


        print(
            "Símbolos:",
            self.obtener_simbolos()
        )


        print(
            "Operadores:",
            self.obtener_operadores()
        )


        print()


        self.mostrar_concatenaciones()


        print(
            "Expresión con concatenación:",
            self.obtener_expresion_concatenada()
        )


        self.mostrar_precedencias()