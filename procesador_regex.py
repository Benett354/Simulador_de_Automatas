class ProcesadorRegex:


    # ---------------------------------
    # Operadores de expresiones regulares
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
        # se realizará sin espacios
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