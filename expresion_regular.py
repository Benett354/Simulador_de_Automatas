class ExpresionRegular:


    # ---------------------------------
    # Operadores reconocidos
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
    # Constructor
    # ---------------------------------

    def __init__(
        self,
        expresion=""
    ):

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

        # Eliminar espacios
        expresion = expresion.replace(
            " ",
            ""
        )

        self.expresion = expresion


    # ---------------------------------
    # Obtener expresión
    # ---------------------------------

    def obtener_expresion(self):

        return self.expresion


    # ---------------------------------
    # Verificar si está vacía
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
    # Verificar si es símbolo válido
    # ---------------------------------

    def es_simbolo(
        self,
        caracter
    ):

        # Letras
        if caracter.isalpha():

            return True

        # Números
        if caracter.isdigit():

            return True

        # Epsilon
        if caracter == "ε":

            return True

        return False


    # ---------------------------------
    # Obtener símbolos
    # ---------------------------------

    def obtener_simbolos(self):

        simbolos = set()

        for caracter in self.expresion:

            if self.es_simbolo(
                caracter
            ):

                simbolos.add(
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
    # Validación básica
    # ---------------------------------

    def validar_basica(self):

        errores = []

        # Expresión vacía
        if self.esta_vacia():

            errores.append(
                "La expresión regular no puede estar vacía."
            )

            return errores


        # Revisar caracteres
        for caracter in self.expresion:

            if self.es_simbolo(
                caracter
            ):

                continue


            if self.es_operador(
                caracter
            ):

                continue


            errores.append(
                f"El carácter '{caracter}' no está permitido."
            )


        return errores


    # ---------------------------------
    # Validar paréntesis
    # ---------------------------------

    def validar_parentesis(self):

        errores = []

        pila = []


        for posicion, caracter in enumerate(
            self.expresion
        ):

            # Paréntesis de apertura
            if caracter == "(":

                pila.append(
                    posicion
                )


            # Paréntesis de cierre
            elif caracter == ")":

                if not pila:

                    errores.append(
                        "Paréntesis de cierre ')' "
                        f"sin apertura en la posición {posicion + 1}."
                    )

                else:

                    pila.pop()


        # Aperturas que nunca se cerraron
        for posicion in pila:

            errores.append(
                "Paréntesis de apertura '(' "
                f"sin cierre en la posición {posicion + 1}."
            )


        return errores


    # ---------------------------------
    # Validar posición de operadores
    # ---------------------------------

    def validar_posicion_operadores(self):

        errores = []


        if self.esta_vacia():

            return errores


        # ---------------------------------
        # Primer carácter
        # ---------------------------------

        primero = self.expresion[0]


        if primero == "|":

            errores.append(
                "El operador '|' no puede aparecer "
                "al inicio de la expresión."
            )


        if self.es_operador_unario(
            primero
        ):

            errores.append(
                f"El operador '{primero}' no puede aparecer "
                "al inicio de la expresión."
            )


        # ---------------------------------
        # Último carácter
        # ---------------------------------

        ultimo = self.expresion[-1]


        if ultimo == "|":

            errores.append(
                "El operador '|' no puede aparecer "
                "al final de la expresión."
            )


        # ---------------------------------
        # Revisar posiciones internas
        # ---------------------------------

        for posicion, caracter in enumerate(
            self.expresion
        ):


            # ---------------------------------
            # Operador |
            # ---------------------------------

            if caracter == "|":

                if (
                    posicion == 0
                    or posicion == len(self.expresion) - 1
                ):

                    continue


                anterior = self.expresion[
                    posicion - 1
                ]


                siguiente = self.expresion[
                    posicion + 1
                ]


                # Ejemplo:
                # (|a)
                if anterior == "(":

                    errores.append(
                        "El operador '|' no puede aparecer "
                        f"después de '(' en la posición {posicion + 1}."
                    )


                # Ejemplo:
                # (a|)
                if siguiente == ")":

                    errores.append(
                        "El operador '|' no puede aparecer "
                        f"antes de ')' en la posición {posicion + 1}."
                    )


            # ---------------------------------
            # Operadores unarios
            # ---------------------------------

            elif self.es_operador_unario(
                caracter
            ):

                if posicion == 0:

                    continue


                anterior = self.expresion[
                    posicion - 1
                ]


                # Ejemplo:
                # (*a)
                if anterior == "(":

                    errores.append(
                        f"El operador '{caracter}' no puede aparecer "
                        f"después de '(' en la posición {posicion + 1}."
                    )


        return errores


    # ---------------------------------
    # Validar combinaciones
    # incorrectas de operadores
    # ---------------------------------

    def validar_combinaciones_operadores(self):

        errores = []


        if self.esta_vacia():

            return errores


        # Recorremos hasta el penúltimo
        # carácter porque compararemos
        # cada posición con la siguiente.
        for posicion in range(
            len(self.expresion) - 1
        ):

            actual = self.expresion[
                posicion
            ]

            siguiente = self.expresion[
                posicion + 1
            ]


            # ---------------------------------
            # Dos operadores de unión seguidos
            # ---------------------------------

            # Ejemplo:
            # a||b

            if (
                actual == "|"
                and siguiente == "|"
            ):

                errores.append(
                    "No pueden aparecer dos operadores '|' "
                    f"consecutivos en las posiciones "
                    f"{posicion + 1} y {posicion + 2}."
                )


            # ---------------------------------
            # Unión seguida de operador unario
            # ---------------------------------

            # Ejemplos:
            # a|*b
            # a|+b
            # a|?b

            elif (
                actual == "|"
                and self.es_operador_unario(
                    siguiente
                )
            ):

                errores.append(
                    f"El operador '{siguiente}' no puede aparecer "
                    f"inmediatamente después de '|' "
                    f"en la posición {posicion + 2}."
                )


            # ---------------------------------
            # Dos operadores unarios seguidos
            # ---------------------------------

            # Ejemplos:
            # a**
            # a++
            # a??
            # a*+
            # a+?
            # a?*

            elif (
                self.es_operador_unario(
                    actual
                )
                and self.es_operador_unario(
                    siguiente
                )
            ):

                errores.append(
                    f"Los operadores '{actual}' y '{siguiente}' "
                    "no pueden aparecer consecutivamente "
                    f"en las posiciones "
                    f"{posicion + 1} y {posicion + 2}."
                )


        return errores


    # ---------------------------------
    # Saber si los paréntesis son válidos
    # ---------------------------------

    def parentesis_validos(self):

        return len(
            self.validar_parentesis()
        ) == 0


    # ---------------------------------
    # Saber si los operadores
    # están bien posicionados
    # ---------------------------------

    def operadores_bien_posicionados(self):

        return len(
            self.validar_posicion_operadores()
        ) == 0


    # ---------------------------------
    # Saber si las combinaciones
    # de operadores son válidas
    # ---------------------------------

    def combinaciones_operadores_validas(self):

        return len(
            self.validar_combinaciones_operadores()
        ) == 0


    # ---------------------------------
    # Saber si pasa validación básica
    # ---------------------------------

    def es_valida_basica(self):

        return len(
            self.validar_basica()
        ) == 0


    # ---------------------------------
    # Mostrar información
    # ---------------------------------

    def mostrar(self):

        print(
            "\n===== EXPRESIÓN REGULAR ====="
        )


        print(
            "Expresión:",
            self.expresion
        )


        print(
            "Longitud:",
            self.longitud()
        )


        print(
            "Símbolos:",
            self.obtener_simbolos()
        )


        print(
            "Operadores:",
            self.obtener_operadores()
        )


        # ---------------------------------
        # Reunir errores
        # ---------------------------------

        errores = []


        errores.extend(
            self.validar_basica()
        )


        errores.extend(
            self.validar_parentesis()
        )


        errores.extend(
            self.validar_posicion_operadores()
        )


        errores.extend(
            self.validar_combinaciones_operadores()
        )


        # ---------------------------------
        # Mostrar resultado
        # ---------------------------------

        if errores:

            print(
                "Estado: INVÁLIDA"
            )

            print(
                "Errores:"
            )


            for error in errores:

                print(
                    "-",
                    error
                )


        else:

            print(
                "Estado: VÁLIDA"
            )