
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

        return set(
            self.transiciones.get(clave, set())
        )

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
    # Construir fragmento para un símbolo
    # ---------------------------------

    def construir_fragmento_simbolo(self, simbolo):

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

        self.pila_fragmentos.append(fragmento)

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

        self.pila_fragmentos.append(fragmento)

        return fragmento

    # =================================
    # VALIDACIÓN DE FRAGMENTOS
    # =================================

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
    # Retirar un fragmento de la pila
    # ---------------------------------

    def retirar_fragmento_de_pila(self, fragmento):

        for posicion in range(
            len(self.pila_fragmentos) - 1,
            -1,
            -1
        ):

            if self.pila_fragmentos[posicion] is fragmento:

                del self.pila_fragmentos[posicion]

                return

    # =================================
    # COMMIT 3: OPERACIÓN DE UNIÓN
    # =================================

    def construir_union(
        self,
        fragmento_izquierdo=None,
        fragmento_derecho=None
    ):

        # Paso 1: obtener los fragmentos

        if (
            fragmento_izquierdo is None
            and fragmento_derecho is None
        ):

            if len(self.pila_fragmentos) < 2:

                raise ValueError(
                    "Se necesitan dos fragmentos "
                    "para construir una unión."
                )

            fragmento_izquierdo = self.pila_fragmentos[-2]
            fragmento_derecho = self.pila_fragmentos[-1]

        elif (
            fragmento_izquierdo is None
            or fragmento_derecho is None
        ):

            raise ValueError(
                "Debe proporcionar ambos fragmentos."
            )

        # Paso 2: validar los fragmentos

        self.validar_fragmento(fragmento_izquierdo)
        self.validar_fragmento(fragmento_derecho)

        if fragmento_izquierdo is fragmento_derecho:

            raise ValueError(
                "La unión necesita dos fragmentos diferentes."
            )

        # Paso 3: retirar los fragmentos originales

        self.retirar_fragmento_de_pila(
            fragmento_izquierdo
        )

        self.retirar_fragmento_de_pila(
            fragmento_derecho
        )

        # Paso 4: crear nuevos estados

        nuevo_inicial = self.crear_estado()
        nuevo_final = self.crear_estado()

        # Paso 5: conectar el nuevo inicial
        # con los dos fragmentos

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

        # Paso 6: conectar los dos finales
        # con el nuevo estado final

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

        # Paso 7: guardar el resultado

        nuevo_fragmento = FragmentoThompson(
            nuevo_inicial,
            nuevo_final
        )

        self.pila_fragmentos.append(nuevo_fragmento)

        return nuevo_fragmento

    # =================================
    # COMMIT 4: CONCATENACIÓN
    # =================================

    def construir_concatenacion(
        self,
        fragmento_izquierdo=None,
        fragmento_derecho=None
    ):

        # Paso 1: obtener los fragmentos

        if (
            fragmento_izquierdo is None
            and fragmento_derecho is None
        ):

            if len(self.pila_fragmentos) < 2:

                raise ValueError(
                    "Se necesitan dos fragmentos "
                    "para construir una concatenación."
                )

            fragmento_izquierdo = self.pila_fragmentos[-2]
            fragmento_derecho = self.pila_fragmentos[-1]

        elif (
            fragmento_izquierdo is None
            or fragmento_derecho is None
        ):

            raise ValueError(
                "Debe proporcionar ambos fragmentos."
            )

        # Paso 2: validar los fragmentos

        self.validar_fragmento(fragmento_izquierdo)
        self.validar_fragmento(fragmento_derecho)

        if fragmento_izquierdo is fragmento_derecho:

            raise ValueError(
                "La concatenación necesita dos fragmentos diferentes."
            )

        # Paso 3: retirar los fragmentos de la pila

        self.retirar_fragmento_de_pila(
            fragmento_izquierdo
        )

        self.retirar_fragmento_de_pila(
            fragmento_derecho
        )

        # Paso 4: conectar ambos fragmentos con epsilon

        self.agregar_transicion(
            fragmento_izquierdo.estado_final,
            self.EPSILON,
            fragmento_derecho.estado_inicial
        )

        # Paso 5: conservar el inicial del primero
        # y el final del segundo

        nuevo_fragmento = FragmentoThompson(
            fragmento_izquierdo.estado_inicial,
            fragmento_derecho.estado_final
        )

        # Paso 6: guardar el resultado

        self.pila_fragmentos.append(nuevo_fragmento)

        return nuevo_fragmento

    # =================================
    # COMMIT 5: CERRADURA DE KLEENE
    # =================================

    def construir_cerradura_kleene(self, fragmento=None):

        # Paso 1: obtener el fragmento

        if fragmento is None:

            if not self.pila_fragmentos:

                raise ValueError(
                    "Se necesita un fragmento "
                    "para construir la cerradura de Kleene."
                )

            fragmento = self.pila_fragmentos[-1]

        # Paso 2: validar el fragmento

        self.validar_fragmento(fragmento)

        # Paso 3: retirar el fragmento original
        # de la pila

        self.retirar_fragmento_de_pila(fragmento)

        # Paso 4: crear un nuevo estado inicial

        nuevo_inicial = self.crear_estado()

        # Paso 5: crear un nuevo estado final

        nuevo_final = self.crear_estado()

        # Paso 6: permitir entrar al fragmento

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            fragmento.estado_inicial
        )

        # Paso 7: permitir cero repeticiones

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            nuevo_final
        )

        # Paso 8: permitir repetir el fragmento

        self.agregar_transicion(
            fragmento.estado_final,
            self.EPSILON,
            fragmento.estado_inicial
        )

        # Paso 9: permitir salir del fragmento

        self.agregar_transicion(
            fragmento.estado_final,
            self.EPSILON,
            nuevo_final
        )

        # Paso 10: construir el fragmento resultante

        nuevo_fragmento = FragmentoThompson(
            nuevo_inicial,
            nuevo_final
        )

        # Paso 11: guardar el resultado

        self.pila_fragmentos.append(nuevo_fragmento)

        return nuevo_fragmento

    # ---------------------------------
    # Alias para la cerradura de Kleene
    # ---------------------------------

    def construir_kleene(self, fragmento=None):

        return self.construir_cerradura_kleene(
            fragmento
        )

    # =================================
    # CONSULTAS
    # =================================

    def obtener_estados(self):

        return sorted(
            self.estados,
            key=lambda estado: int(estado[1:])
        )

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
