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
    # Obtener operadores utilizados
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


        # ---------------------------------
        # Expresión vacía
        # ---------------------------------

        if self.esta_vacia():

            errores.append(
                "La expresión regular no puede estar vacía."
            )

            return errores


        # ---------------------------------
        # Revisar cada carácter
        # ---------------------------------

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


        errores = self.validar_basica()


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