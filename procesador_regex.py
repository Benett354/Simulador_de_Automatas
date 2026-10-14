from expresion_regular import ExpresionRegular


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
    # Tipos para Thompson
    # ---------------------------------

    TIPO_SIMBOLO = "SIMBOLO"
    TIPO_EPSILON = "EPSILON"
    TIPO_UNION = "UNION"
    TIPO_CONCATENACION = "CONCATENACION"
    TIPO_KLEENE = "KLEENE"
    TIPO_POSITIVA = "POSITIVA"
    TIPO_OPCIONAL = "OPCIONAL"
    TIPO_DESCONOCIDO = "DESCONOCIDO"


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


    # =================================
    # INTEGRACIÓN CON WILMER
    # =================================

    def crear_validador(self):

        return ExpresionRegular(
            self.expresion
        )


    # ---------------------------------
    # Obtener errores de validación
    # ---------------------------------

    def obtener_errores_validacion(self):

        validador = self.crear_validador()

        return validador.validar()


    # ---------------------------------
    # Saber si la expresión es válida
    # ---------------------------------

    def es_expresion_valida(self):

        return len(
            self.obtener_errores_validacion()
        ) == 0


    # ---------------------------------
    # Validar antes de procesar
    # ---------------------------------

    def validar_antes_de_procesar(self):

        errores = (
            self.obtener_errores_validacion()
        )


        if errores:

            mensaje = (
                "La expresión regular no puede "
                "ser procesada:\n"
            )


            for error in errores:

                mensaje += (
                    "- "
                    + error
                    + "\n"
                )


            raise ValueError(
                mensaje.strip()
            )


        return True


    # ---------------------------------
    # Obtener longitud
    # ---------------------------------

    def longitud(self):

        return len(
            self.expresion
        )


    # ---------------------------------
    # Verificar operador
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
    # Verificar operador de procesamiento
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
    # Verificar símbolo
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
    # Puede terminar una expresión
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
    # Puede iniciar una expresión
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
    # Verificar concatenación implícita
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
    # Insertar concatenaciones
    # ---------------------------------

    def insertar_concatenaciones(self):

        resultado = ""


        if self.esta_vacia():

            return resultado


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
    # Obtener expresión concatenada
    # ---------------------------------

    def obtener_expresion_concatenada(self):

        self.validar_antes_de_procesar()

        return self.insertar_concatenaciones()


    # =================================
    # CONVERSIÓN INFIJA A POSTFIJA
    # =================================

    def convertir_a_postfija(self):

        # Primero se valida con
        # la clase creada por Wilmer
        self.validar_antes_de_procesar()


        # Después se agregan
        # concatenaciones internas
        expresion = (
            self.insertar_concatenaciones()
        )


        salida = []

        pila = []


        # ---------------------------------
        # Recorrer expresión
        # ---------------------------------

        for caracter in expresion:


            # ---------------------------------
            # Símbolo
            # ---------------------------------

            if self.es_simbolo(
                caracter
            ):

                salida.append(
                    caracter
                )

                continue


            # ---------------------------------
            # Paréntesis de apertura
            # ---------------------------------

            if caracter == "(":

                pila.append(
                    caracter
                )

                continue


            # ---------------------------------
            # Paréntesis de cierre
            # ---------------------------------

            if caracter == ")":

                while (
                    pila
                    and pila[-1] != "("
                ):

                    salida.append(
                        pila.pop()
                    )


                if (
                    pila
                    and pila[-1] == "("
                ):

                    pila.pop()


                continue


            # ---------------------------------
            # Operadores
            # ---------------------------------

            if self.es_operador_procesamiento(
                caracter
            ):

                while (
                    pila
                    and pila[-1] != "("
                    and self.tiene_mayor_o_igual_precedencia(
                        pila[-1],
                        caracter
                    )
                ):

                    salida.append(
                        pila.pop()
                    )


                pila.append(
                    caracter
                )


        # ---------------------------------
        # Vaciar pila
        # ---------------------------------

        while pila:

            operador = pila.pop()


            if operador not in {
                "(",
                ")"
            }:

                salida.append(
                    operador
                )


        return "".join(
            salida
        )


    # ---------------------------------
    # Obtener expresión postfija
    # ---------------------------------

    def obtener_postfija(self):

        return self.convertir_a_postfija()


    # =================================
    # TOKENS PARA THOMPSON
    # =================================

    def clasificar_token(
        self,
        token
    ):

        if token == "ε":

            return self.TIPO_EPSILON


        if self.es_simbolo(
            token
        ):

            return self.TIPO_SIMBOLO


        if token == "|":

            return self.TIPO_UNION


        if token == self.OPERADOR_CONCATENACION:

            return self.TIPO_CONCATENACION


        if token == "*":

            return self.TIPO_KLEENE


        if token == "+":

            return self.TIPO_POSITIVA


        if token == "?":

            return self.TIPO_OPCIONAL


        return self.TIPO_DESCONOCIDO


    # ---------------------------------
    # Obtener tokens postfijos
    # ---------------------------------

    def obtener_tokens_postfijos(self):

        postfija = self.obtener_postfija()

        tokens = []


        for caracter in postfija:

            tokens.append(
                caracter
            )


        return tokens


    # ---------------------------------
    # Preparar tokens para Thompson
    # ---------------------------------

    def obtener_tokens_para_thompson(self):

        tokens_procesados = []


        for token in self.obtener_tokens_postfijos():

            tipo = self.clasificar_token(
                token
            )


            tokens_procesados.append(
                (
                    tipo,
                    token
                )
            )


        return tokens_procesados


    # ---------------------------------
    # Contar operadores especiales
    # ---------------------------------

    def contar_operadores_especiales(self):

        conteo = {
            self.TIPO_KLEENE: 0,
            self.TIPO_POSITIVA: 0,
            self.TIPO_OPCIONAL: 0,
            self.TIPO_UNION: 0,
            self.TIPO_CONCATENACION: 0
        }


        for (
            tipo,
            token
        ) in self.obtener_tokens_para_thompson():

            if tipo in conteo:

                conteo[tipo] += 1


        return conteo


    # ---------------------------------
    # Mostrar tokens
    # ---------------------------------

    def mostrar_tokens_thompson(self):

        tokens = (
            self.obtener_tokens_para_thompson()
        )


        print(
            "\nTokens para Thompson:"
        )


        for posicion, (
            tipo,
            token
        ) in enumerate(
            tokens,
            start=1
        ):

            print(
                f"{posicion}.",
                token,
                "->",
                tipo
            )


    # ---------------------------------
    # Mostrar precedencias
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


        # ---------------------------------
        # Primero validar
        # ---------------------------------

        errores = (
            self.obtener_errores_validacion()
        )


        if errores:

            print(
                "Estado: INVÁLIDA"
            )

            print(
                "No se puede procesar."
            )


            for error in errores:

                print(
                    "-",
                    error
                )


            return


        print(
            "Estado: VÁLIDA"
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


        print(
            "Expresión postfija:",
            self.obtener_postfija()
        )


        self.mostrar_precedencias()


        self.mostrar_tokens_thompson()