
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

    # =================================
    # ESTADOS Y TRANSICIONES
    # =================================

    def crear_estado(self):

        estado = f"q{self.contador_estados}"

        self.contador_estados += 1
        self.estados.add(estado)

        return estado

    def validar_estado(self, estado):

        if estado not in self.estados:

            raise ValueError(
                f"El estado {estado} no existe."
            )

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

    def obtener_transicion(
        self,
        estado,
        simbolo
    ):

        clave = (estado, simbolo)

        return set(
            self.transiciones.get(clave, set())
        )

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
    # COMMIT 2: FRAGMENTOS BÁSICOS
    # =================================

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
    # COMMIT 3: UNIÓN
    # =================================

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

            fragmento_izquierdo = self.pila_fragmentos[-2]
            fragmento_derecho = self.pila_fragmentos[-1]

        elif (
            fragmento_izquierdo is None
            or fragmento_derecho is None
        ):

            raise ValueError(
                "Debe proporcionar ambos fragmentos."
            )

        self.validar_fragmento(fragmento_izquierdo)
        self.validar_fragmento(fragmento_derecho)

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

        self.validar_fragmento(fragmento_izquierdo)
        self.validar_fragmento(fragmento_derecho)

        if fragmento_izquierdo is fragmento_derecho:

            raise ValueError(
                "La concatenación necesita "
                "dos fragmentos diferentes."
            )

        self.retirar_fragmento_de_pila(
            fragmento_izquierdo
        )

        self.retirar_fragmento_de_pila(
            fragmento_derecho
        )

        self.agregar_transicion(
            fragmento_izquierdo.estado_final,
            self.EPSILON,
            fragmento_derecho.estado_inicial
        )

        nuevo_fragmento = FragmentoThompson(
            fragmento_izquierdo.estado_inicial,
            fragmento_derecho.estado_final
        )

        self.pila_fragmentos.append(nuevo_fragmento)

        return nuevo_fragmento

    # =================================
    # COMMIT 5: CERRADURA DE KLEENE
    # =================================

    def construir_cerradura_kleene(self, fragmento=None):

        if fragmento is None:

            if not self.pila_fragmentos:

                raise ValueError(
                    "Se necesita un fragmento "
                    "para construir la cerradura de Kleene."
                )

            fragmento = self.pila_fragmentos[-1]

        self.validar_fragmento(fragmento)

        self.retirar_fragmento_de_pila(fragmento)

        nuevo_inicial = self.crear_estado()
        nuevo_final = self.crear_estado()

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            fragmento.estado_inicial
        )

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            nuevo_final
        )

        self.agregar_transicion(
            fragmento.estado_final,
            self.EPSILON,
            fragmento.estado_inicial
        )

        self.agregar_transicion(
            fragmento.estado_final,
            self.EPSILON,
            nuevo_final
        )

        nuevo_fragmento = FragmentoThompson(
            nuevo_inicial,
            nuevo_final
        )

        self.pila_fragmentos.append(nuevo_fragmento)

        return nuevo_fragmento

    def construir_kleene(self, fragmento=None):

        return self.construir_cerradura_kleene(
            fragmento
        )

    # =================================
    # COMMIT 6: OPERADOR POSITIVO
    # =================================

    def construir_cerradura_positiva(self, fragmento=None):

        if fragmento is None:

            if not self.pila_fragmentos:

                raise ValueError(
                    "Se necesita un fragmento "
                    "para construir la cerradura positiva."
                )

            fragmento = self.pila_fragmentos[-1]

        self.validar_fragmento(fragmento)

        self.retirar_fragmento_de_pila(fragmento)

        nuevo_inicial = self.crear_estado()
        nuevo_final = self.crear_estado()

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            fragmento.estado_inicial
        )

        self.agregar_transicion(
            fragmento.estado_final,
            self.EPSILON,
            fragmento.estado_inicial
        )

        self.agregar_transicion(
            fragmento.estado_final,
            self.EPSILON,
            nuevo_final
        )

        nuevo_fragmento = FragmentoThompson(
            nuevo_inicial,
            nuevo_final
        )

        self.pila_fragmentos.append(nuevo_fragmento)

        return nuevo_fragmento

    def construir_positivo(self, fragmento=None):

        return self.construir_cerradura_positiva(
            fragmento
        )

    # =================================
    # COMMIT 6: OPERADOR OPCIONAL
    # =================================

    def construir_operador_opcional(self, fragmento=None):

        if fragmento is None:

            if not self.pila_fragmentos:

                raise ValueError(
                    "Se necesita un fragmento "
                    "para construir el operador opcional."
                )

            fragmento = self.pila_fragmentos[-1]

        self.validar_fragmento(fragmento)

        self.retirar_fragmento_de_pila(fragmento)

        nuevo_inicial = self.crear_estado()
        nuevo_final = self.crear_estado()

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            fragmento.estado_inicial
        )

        self.agregar_transicion(
            nuevo_inicial,
            self.EPSILON,
            nuevo_final
        )

        self.agregar_transicion(
            fragmento.estado_final,
            self.EPSILON,
            nuevo_final
        )

        nuevo_fragmento = FragmentoThompson(
            nuevo_inicial,
            nuevo_final
        )

        self.pila_fragmentos.append(nuevo_fragmento)

        return nuevo_fragmento

    def construir_opcional(self, fragmento=None):

        return self.construir_operador_opcional(
            fragmento
        )

    # =================================
    # COMMIT 7: INTEGRACIÓN CON REGEX
    # =================================

    def construir_desde_expresion(self, expresion):

        # Paso 1: importar el procesador de Dulce

        from procesador_regex import ProcesadorRegex

        # Paso 2: procesar y validar la expresión

        procesador = ProcesadorRegex(expresion)

        tokens = procesador.obtener_tokens_para_thompson()

        # Paso 3: iniciar una construcción nueva

        self.reiniciar()

        try:

            # Paso 4: recorrer los tokens postfijos

            for tipo, token in tokens:

                # Símbolo del alfabeto

                if tipo == "SIMBOLO":

                    self.construir_fragmento_simbolo(token)

                # Transición epsilon

                elif tipo == "EPSILON":

                    self.construir_fragmento_epsilon()

                # Unión

                elif tipo == "UNION":

                    self.construir_union()

                # Concatenación

                elif tipo == "CONCATENACION":

                    self.construir_concatenacion()

                # Cerradura de Kleene

                elif tipo == "KLEENE":

                    self.construir_cerradura_kleene()

                # Cerradura positiva

                elif tipo == "POSITIVA":

                    self.construir_cerradura_positiva()

                # Operador opcional

                elif tipo == "OPCIONAL":

                    self.construir_operador_opcional()

                else:

                    raise ValueError(
                        f"Tipo de token desconocido: {tipo}"
                    )

            # Paso 5: comprobar que exista
            # un único fragmento resultante

            if len(self.pila_fragmentos) != 1:

                raise ValueError(
                    "La construcción no produjo "
                    "un único fragmento final."
                )

            # Paso 6: devolver el fragmento final

            return self.pila_fragmentos[0]

        except Exception:

            # Evitar conservar una construcción incompleta

            self.reiniciar()

            raise

    # =================================
    # CONVERTIR A AUTOMATA DEL PROYECTO
    # =================================

    def construir_automata(self, expresion):

        # Paso 1: construir el AFN con Thompson

        fragmento = self.construir_desde_expresion(
            expresion
        )

        # Paso 2: importar la clase del proyecto

        from automata import Automata

        # Paso 3: crear un autómata no determinista

        automata = Automata(
            tipo="AFN"
        )

        # Paso 4: registrar los estados

        for estado in self.obtener_estados():

            automata.agregar_estado(estado)

        # Paso 5: registrar el estado inicial

        automata.establecer_estado_inicial(
            fragmento.estado_inicial
        )

        # Paso 6: registrar el estado final

        automata.agregar_estado_final(
            fragmento.estado_final
        )

        # Paso 7: registrar símbolos y transiciones

        for (origen, simbolo), destinos in (
            self.transiciones.items()
        ):

            # Epsilon no forma parte del alfabeto
            # de entrada

            if simbolo != self.EPSILON:

                automata.agregar_simbolo(simbolo)

            for destino in destinos:

                automata.agregar_transicion(
                    origen,
                    simbolo,
                    destino
                )

        return automata

    # =================================
    # CONSULTAS Y REINICIO
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

    def reiniciar(self):

        self.estados.clear()
        self.transiciones.clear()
        self.contador_estados = 0
        self.pila_fragmentos.clear()

    # =================================
    # MOSTRAR INFORMACIÓN
    # =================================

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

        if self.pila_fragmentos:

            print(
                "Fragmento final:",
                self.pila_fragmentos[-1]
            )

        print(
            "Fragmentos en pila:",
            len(self.pila_fragmentos)
        )
