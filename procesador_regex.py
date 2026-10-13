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

        # El procesamiento interno
        # se realiza sin espacios
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
    # Verificar si es símbolo
    # ---------------------------------

    def es_simbolo(
        self,
        caracter
    ):

        # Epsilon
        if caracter == "ε":

            return True


        # Letras
        if caracter.isalpha():

            return True


        # Números
        if caracter.isdigit():

            return True


        return False


    # ---------------------------------
    # Convertir expresión a elementos
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

        # Un símbolo puede terminar
        # una parte de la expresión
        if self.es_simbolo(
            caracter
        ):

            return True


        # Un paréntesis cerrado puede
        # terminar un grupo
        if caracter == ")":

            return True


        # *, + y ? actúan sobre
        # la expresión anterior
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

        # Un símbolo puede iniciar
        # una nueva expresión
        if self.es_simbolo(
            caracter
        ):

            return True


        # Un paréntesis abierto inicia
        # un nuevo grupo
        if caracter == "(":

            return True


        return False


    # ---------------------------------
    # Saber si entre dos elementos
    # existe concatenación implícita
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
    # Detectar concatenaciones implícitas
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
    # implícitas
    # ---------------------------------

    def tiene_concatenaciones(self):

        return len(
            self.detectar_concatenaciones()
        ) > 0


    # ---------------------------------
    # Insertar operador de concatenación
    # ---------------------------------

    def insertar_concatenaciones(self):

        # Si está vacía no hay nada
        # que procesar
        if self.esta_vacia():

            return ""


        resultado = ""


        # ---------------------------------
        # Recorrer la expresión
        # ---------------------------------

        for posicion in range(
            len(self.expresion)
        ):

            actual = self.expresion[
                posicion
            ]


            # Agregar carácter actual
            resultado += actual


            # Si estamos en el último
            # carácter terminamos
            if posicion == len(self.expresion) - 1:

                continue


            siguiente = self.expresion[
                posicion + 1
            ]


            # ---------------------------------
            # Verificar concatenación
            # ---------------------------------

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
    # Mostrar concatenaciones detectadas
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