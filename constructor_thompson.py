
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

        estado_inicial = self.crear_estado()

        estado_final = self.crear_estado()

        self.agregar_transicion(
            estado_inicial,
            simbolo,
            estado_final
        )

        fragmento = FragmentoThompson(
            estado_inicial,
            estado_final
        )

        self.pila_fragmentos.append(
            fragmento
        )

        return fragmento

    # ---------------------------------
    # Construir fragmento para epsilon
    # ---------------------------------

    def construir_fragmento_epsilon(self):

        estado_inicial = self.crear_estado()

        estado_final = self.crear_estado()

        self.agregar_transicion(
            estado_inicial,
            self.EPSILON,
            estado_final
        )

        fragmento = FragmentoThompson(
            estado_inicial,
            estado_final
        )

        self.pila_fragmentos.append(
            fragmento
        )

        return fragmento

    # =================================
    # COMMIT 3: OPERACIÓN DE UNIÓN
    # =================================

    # ---------------------------------
    # Validar un fragmento
    # ---------------------------------

    def validar_fragmento(self, fragmento):

        if not isinstance(
            fragmento,
            FragmentoThompson
        ):

            raise ValueError(
                "El objeto recibido no es un fragmento Thompson."
            )

        self.validar_estado(
            fragmento.estado_inicial
        )

        self.validar_estado(
            fragmento.estado_final
        )

    # ---------------------------------
    # Retirar fragmento de la pila
    # ---------------------------------

    def retirar_fragmento_de_pila(
        self,
        fragmento
    ):

        for posicion in range(
            len(self.pila_fragmentos) - 1,
            -1,
            -1
        ):

            if self.pila_fragmentos[posicion] is fragmento:

                del self.pila_fragmentos[posicion]

                return

    # ---------------------------------
    # Construir unión
    # ---------------------------------

    def construir_union(
        self,
        fragmento_izquierdo=None,
        fragmento_derecho=None
    ):

        if (
            fragmento_izquierdo is None
            and fragmento_derecho is None
        ):

            if len(self.pila_fragmentos) < 2:

                raise ValueError(
                    "Se necesitan dos fragmentos "
                    "para construir una unión."
                )

            fragmento_izquierdo = (
                self.pila_fragmentos[-2]
            )

            fragmento_derecho = (
                self.pila_fragmentos[-1]
            )

        elif (
            fragmento_izquierdo is None
            or fragmento_derecho is None
        ):

            raise ValueError(
                "Debe proporcionar ambos fragmentos."
            )

        self.validar_fragmento(
            fragmento_izquierdo
        )

        self.validar_fragmento(
            fragmento_derecho
        )

        if fragmento_izquierdo is fragmento_derecho:

            raise ValueError(
                "La unión necesita dos fragmentos diferentes."
            )

        self.retirar_fragmento_de_pila(
            fragmento_izquierdo
        )

        self.retirar_fragmento_de_pila(
            fragmento_derecho
        )

        nuevo_inicial = self.crear_estado()

        nuevo_final = self.crear_estado()

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            fragmento_izquierdo.estado_inicial
        )

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            fragmento_derecho.estado_inicial
        )

        self.agregar_transicion(
            fragmento_izquierdo.estado_final,
            self.EPSILON,
            nuevo_final
        )

        self.agregar_transicion(
            fragmento_derecho.estado_final,
            self.EPSILON,
            nuevo_final
        )

        nuevo_fragmento = FragmentoThompson(
            nuevo_inicial,
            nuevo_final
        )

        self.pila_fragmentos.append(
            nuevo_fragmento
        )

        return nuevo_fragmento

    # =================================
    # COMMIT 4: CONCATENACIÓN
    # =================================

    def construir_concatenacion(
        self,
        fragmento_izquierdo=None,
        fragmento_derecho=None
    ):

        # Paso 1: obtener los dos fragmentos

        if (
            fragmento_izquierdo is None
            and fragmento_derecho is None
        ):

            if len(self.pila_fragmentos) < 2:

                raise ValueError(
                    "Se necesitan dos fragmentos "
                    "para construir una concatenación."
                )

            fragmento_izquierdo = (
                self.pila_fragmentos[-2]
            )

            fragmento_derecho = (
                self.pila_fragmentos[-1]
            )

        elif (
            fragmento_izquierdo is None
            or fragmento_derecho is None
        ):

            raise ValueError(
                "Debe proporcionar ambos fragmentos."
            )

        # Paso 2: validar los fragmentos

        self.validar_fragmento(
            fragmento_izquierdo
        )

        self.validar_fragmento(
            fragmento_derecho
        )

        if fragmento_izquierdo is fragmento_derecho:

            raise ValueError(
                "La concatenación necesita "
                "dos fragmentos diferentes."
            )

        # Paso 3: retirar los fragmentos
        # originales de la pila

        self.retirar_fragmento_de_pila(
            fragmento_izquierdo
        )

        self.retirar_fragmento_de_pila(
            fragmento_derecho
        )

        # Paso 4: conectar el estado final
        # del primer fragmento con el inicial
        # del segundo mediante epsilon

        self.agregar_transicion(
            fragmento_izquierdo.estado_final,
            self.EPSILON,
            fragmento_derecho.estado_inicial
        )

        # Paso 5: conservar el estado inicial
        # del primer fragmento

        nuevo_inicial = (
            fragmento_izquierdo.estado_inicial
        )

        # Paso 6: conservar el estado final
        # del segundo fragmento

        nuevo_final = (
            fragmento_derecho.estado_final
        )

        # Paso 7: crear el fragmento combinado

        nuevo_fragmento = FragmentoThompson(
            nuevo_inicial,
            nuevo_final
        )

        # Paso 8: guardar el resultado en la pila

        self.pila_fragmentos.append(
            nuevo_fragmento
        )

        return nuevo_fragmento

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
