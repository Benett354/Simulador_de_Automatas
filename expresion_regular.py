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
    # Obtener símbolos de la expresión
    # ---------------------------------

    def obtener_simbolos(self):

        simbolos = set()

        for caracter in self.expresion:

            if caracter not in self.OPERADORES:

                simbolos.add(
                    caracter
                )

        return simbolos


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