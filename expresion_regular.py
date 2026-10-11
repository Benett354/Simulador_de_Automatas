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

        # Aquí guardaremos las posiciones
        # de los paréntesis de apertura
        pila = []

        for posicion, caracter in enumerate(
            self.expresion
        ):

            # ---------------------------------
            # Paréntesis de apertura
            # ---------------------------------

            if caracter == "(":

                pila.append(
                    posicion
                )

            # ---------------------------------
            # Paréntesis de cierre
            # ---------------------------------

            elif caracter == ")":

                # No existe apertura correspondiente
                if not pila:

                    errores.append(
                        "Paréntesis de cierre ')' "
                        f"sin apertura en la posición {posicion + 1}."
                    )

                else:

                    pila.pop()

        # ---------------------------------
        # Aperturas que nunca se cerraron
        # ---------------------------------

        for posicion in pila:

            errores.append(
                "Paréntesis de apertura '(' "
                f"sin cierre en la posición {posicion + 1}."
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
        # Reunir errores actuales
        # ---------------------------------

        errores = []

        errores.extend(
            self.validar_basica()
        )

        errores.extend(
            self.validar_parentesis()
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