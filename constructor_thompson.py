
class FragmentoThompson:

    def __init__(self, estado_inicial, estado_final):

        self.estado_inicial = estado_inicial
        self.estado_final = estado_final

    def __repr__(self):

        return (
            f"FragmentoThompson("
            f"inicial={self.estado_inicial}, "
            f"final={self.estado_final})"
        )


class ConstructorThompson:

    EPSILON = "ε"

    OPERADORES_RESERVADOS = {
        "|", "*", "+", "?", "(", ")", "·"
    }

    def __init__(self):

        self.estados = set()

        self.transiciones = {}

        self.contador_estados = 0

        self.pila_fragmentos = []

    # ---------------------------------
    # Crear un estado nuevo
    # ---------------------------------

    def crear_estado(self):

        estado = f"q{self.contador_estados}"

        self.contador_estados += 1

        self.estados.add(estado)

        return estado

    # ---------------------------------
    # Validar que un estado exista
    # ---------------------------------

    def validar_estado(self, estado):

        if estado not in self.estados:

            raise ValueError(
                f"El estado {estado} no existe."
            )

    # ---------------------------------
    # Agregar una transición
    # ---------------------------------

    def agregar_transicion(
        self,
        origen,
        simbolo,
        destino
    ):

        self.validar_estado(origen)

        self.validar_estado(destino)

        clave = (origen, simbolo)

        if clave not in self.transiciones:

            self.transiciones[clave] = set()

        self.transiciones[clave].add(destino)

    # ---------------------------------
    # Obtener destinos de una transición
    # ---------------------------------

    def obtener_transicion(
        self,
        estado,
        simbolo
    ):

        clave = (estado, simbolo)

        destinos = self.transiciones.get(
            clave,
            set()
        )

        return set(destinos)

    # ---------------------------------
    # Crear fragmento con estados existentes
    # ---------------------------------

    def crear_fragmento(
        self,
        estado_inicial,
        estado_final
    ):

        self.validar_estado(estado_inicial)

        self.validar_estado(estado_final)

        return FragmentoThompson(
            estado_inicial,
            estado_final
        )

    # =================================
    # COMMIT 2: FRAGMENTOS BÁSICOS
    # =================================

    # ---------------------------------
    # Crear fragmento para un símbolo
    # ---------------------------------

    def construir_fragmento_simbolo(
        self,
        simbolo
    ):

        if not isinstance(simbolo, str):

            raise ValueError(
                "El símbolo debe ser texto."
            )

        if len(simbolo) != 1:

            raise ValueError(
                "El símbolo debe contener un carácter."
            )

        if (
            simbolo == self.EPSILON
            or simbolo in self.OPERADORES_RESERVADOS
            or not (
                simbolo.isalpha()
                or simbolo.isdigit()
            )
        ):

            raise ValueError(
                f"Símbolo no válido para un fragmento: {simbolo}"
            )

        # Paso 1: crear estado inicial

        estado_inicial = self.crear_estado()

        # Paso 2: crear estado final

        estado_final = self.crear_estado()

        # Paso 3: conectar ambos estados
        # mediante el símbolo recibido

        self.agregar_transicion(
            estado_inicial,
            simbolo,
            estado_final
        )

        # Paso 4: guardar el fragmento

        fragmento = FragmentoThompson(
            estado_inicial,
            estado_final
        )

        # Paso 5: agregarlo a la pila
        # para utilizarlo posteriormente

        self.pila_fragmentos.append(
            fragmento
        )

        return fragmento

    # ---------------------------------
    # Crear fragmento para epsilon
    # ---------------------------------

    def construir_fragmento_epsilon(self):

        # Paso 1: crear estado inicial

        estado_inicial = self.crear_estado()

        # Paso 2: crear estado final

        estado_final = self.crear_estado()

        # Paso 3: conectar mediante epsilon

        self.agregar_transicion(
            estado_inicial,
            self.EPSILON,
            estado_final
        )

        # Paso 4: guardar el fragmento

        fragmento = FragmentoThompson(
            estado_inicial,
            estado_final
        )

        # Paso 5: agregarlo a la pila

        self.pila_fragmentos.append(
            fragmento
        )

        return fragmento

    # ---------------------------------
    # Obtener estados
    # ---------------------------------

    def obtener_estados(self):

        return sorted(
            self.estados,
            key=lambda estado: int(estado[1:])
        )

    # ---------------------------------
    # Obtener transiciones
    # ---------------------------------

    def obtener_transiciones(self):

        resultado = {}

        for clave, destinos in self.transiciones.items():

            resultado[clave] = set(destinos)

        return resultado

    # ---------------------------------
    # Reiniciar construcción
    # ---------------------------------

    def reiniciar(self):

        self.estados.clear()

        self.transiciones.clear()

        self.contador_estados = 0

        self.pila_fragmentos.clear()

    # ---------------------------------
    # Mostrar información
    # ---------------------------------

    def mostrar(self):

        print("\n===== CONSTRUCTOR DE THOMPSON =====")

        print("Estados:", self.obtener_estados())

        print("Transiciones:")

        for (origen, simbolo), destinos in sorted(
            self.transiciones.items(),
            key=lambda elemento: (
                int(elemento[0][0][1:]),
                elemento[0][1]
            )
        ):

            for destino in sorted(
                destinos,
                key=lambda estado: int(estado[1:])
            ):

                print(
                    f"{origen} --{simbolo}--> {destino}"
                )

        print(
            "Fragmentos en pila:",
            len(self.pila_fragmentos)
        )
