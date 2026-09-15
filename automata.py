class Automata:


    def __init__(self, tipo="AFD"):

        tipo = str(tipo).upper().strip()

        if tipo not in ("AFD", "AFN"):

            raise ValueError(
                "El tipo de autómata debe ser AFD o AFN."
            )

        self.tipo = tipo

        # Q
        self.estados = set()

        # Σ
        self.alfabeto = set()

        # δ
        self.transiciones = {}

        # q0
        self.estado_inicial = None

        # F
        self.estados_finales = set()


    # ---------------------------------
    # Agregar estado
    # ---------------------------------

    def agregar_estado(self, estado):

        estado = str(estado).strip()

        if not estado:

            raise ValueError(
                "El nombre del estado no puede estar vacío."
            )

        self.estados.add(
            estado
        )


    # ---------------------------------
    # Estado inicial
    # ---------------------------------

    def establecer_estado_inicial(self, estado):

        estado = str(estado).strip()

        if not estado:

            raise ValueError(
                "Debe indicar un estado inicial."
            )

        if estado not in self.estados:

            raise ValueError(
                f"El estado inicial '{estado}' no existe."
            )

        self.estado_inicial = estado


    # ---------------------------------
    # Estado final
    # ---------------------------------

    def agregar_estado_final(self, estado):

        estado = str(estado).strip()

        if not estado:

            raise ValueError(
                "El estado final no puede estar vacío."
            )

        if estado not in self.estados:

            raise ValueError(
                f"El estado final '{estado}' no existe."
            )

        self.estados_finales.add(
            estado
        )


    # ---------------------------------
    # Agregar símbolo
    # ---------------------------------

    def agregar_simbolo(self, simbolo):

        simbolo = str(simbolo).strip()

        if not simbolo:

            raise ValueError(
                "El símbolo no puede estar vacío."
            )

        if simbolo == "ε":

            raise ValueError(
                "ε no pertenece al alfabeto. "
                "Se utiliza únicamente como transición especial de un AFN."
            )

        if len(simbolo) != 1:

            raise ValueError(
                f"El símbolo '{simbolo}' debe contener un solo carácter."
            )

        self.alfabeto.add(
            simbolo
        )


    # ---------------------------------
    # Agregar transición
    # ---------------------------------

    def agregar_transicion(
        self,
        origen,
        simbolo,
        destino
    ):

        origen = str(origen).strip()
        simbolo = str(simbolo).strip()
        destino = str(destino).strip()

        if origen not in self.estados:

            raise ValueError(
                f"El estado origen '{origen}' no existe."
            )

        if destino not in self.estados:

            raise ValueError(
                f"El estado destino '{destino}' no existe."
            )

        # ε solamente en AFN
        if simbolo == "ε":

            if self.tipo != "AFN":

                raise ValueError(
                    "Un AFD no puede contener transiciones ε."
                )

        elif simbolo not in self.alfabeto:

            raise ValueError(
                f"El símbolo '{simbolo}' no pertenece al alfabeto."
            )

        clave = (
            origen,
            simbolo
        )

        # AFN
        if self.tipo == "AFN":

            if clave not in self.transiciones:

                self.transiciones[
                    clave
                ] = set()

            self.transiciones[
                clave
            ].add(
                destino
            )

        # AFD
        else:

            if clave in self.transiciones:

                destino_actual = self.transiciones[
                    clave
                ]

                # Misma transición:
                # no es necesario duplicarla
                if destino_actual == destino:

                    return

                raise ValueError(
                    f"Ya existe la transición "
                    f"{origen} --{simbolo}--> {destino_actual}.\n"
                    "Un AFD no puede tener dos destinos "
                    "para el mismo estado y símbolo."
                )

            self.transiciones[
                clave
            ] = destino


    # ---------------------------------
    # Eliminar transición
    # ---------------------------------

    def eliminar_transicion(
        self,
        origen,
        simbolo,
        destino=None
    ):

        # IMPORTANTE:
        # Treeview puede devolver 0 y 1 como int.
        # Aquí convertimos TODO nuevamente a str.
        origen = str(origen).strip()
        simbolo = str(simbolo).strip()

        if destino is not None:

            destino = str(
                destino
            ).strip()

        clave = (
            origen,
            simbolo
        )

        if clave not in self.transiciones:

            raise ValueError(
                f"No existe la transición "
                f"({origen}, {simbolo})."
            )

        # AFN
        if self.tipo == "AFN":

            if destino is None:

                raise ValueError(
                    "Debe indicar el destino de la transición AFN."
                )

            destinos = self.transiciones[
                clave
            ]

            if destino not in destinos:

                raise ValueError(
                    f"No existe la transición "
                    f"{origen} --{simbolo}--> {destino}."
                )

            destinos.remove(
                destino
            )

            # Si ya no quedan destinos
            if not destinos:

                del self.transiciones[
                    clave
                ]

        # AFD
        else:

            del self.transiciones[
                clave
            ]


    # ---------------------------------
    # Obtener transición
    # ---------------------------------

    def obtener_transicion(
        self,
        estado,
        simbolo
    ):

        estado = str(estado).strip()
        simbolo = str(simbolo).strip()

        clave = (
            estado,
            simbolo
        )

        return self.transiciones.get(
            clave,
            None
        )


    # ---------------------------------
    # Validar
    # ---------------------------------

    def validar(self):

        errores = []

        if not self.estados:

            errores.append(
                "El autómata no contiene estados."
            )

        # Estado inicial
        if self.estado_inicial is None:

            errores.append(
                "No existe estado inicial."
            )

        elif self.estado_inicial not in self.estados:

            errores.append(
                f"El estado inicial '{self.estado_inicial}' "
                "no pertenece al conjunto de estados."
            )

        # Estados finales
        for estado in self.estados_finales:

            if estado not in self.estados:

                errores.append(
                    f"El estado final '{estado}' no existe."
                )

        # ε jamás pertenece a Σ
        if "ε" in self.alfabeto:

            errores.append(
                "ε no debe pertenecer al alfabeto."
            )

        # Transiciones
        for (
            origen,
            simbolo
        ), destino in self.transiciones.items():

            if origen not in self.estados:

                errores.append(
                    f"El estado origen '{origen}' no existe."
                )

            if simbolo == "ε":

                if self.tipo != "AFN":

                    errores.append(
                        "Un AFD no puede contener transiciones ε."
                    )

            elif simbolo not in self.alfabeto:

                errores.append(
                    f"El símbolo '{simbolo}' "
                    "no pertenece al alfabeto."
                )

            # AFN
            if self.tipo == "AFN":

                if not isinstance(
                    destino,
                    set
                ):

                    errores.append(
                        f"La transición ({origen}, {simbolo}) "
                        "del AFN posee una estructura incorrecta."
                    )

                    continue

                for estado_destino in destino:

                    if estado_destino not in self.estados:

                        errores.append(
                            f"El destino '{estado_destino}' no existe."
                        )

            # AFD
            else:

                if isinstance(
                    destino,
                    set
                ):

                    errores.append(
                        f"La transición ({origen}, {simbolo}) "
                        "tiene múltiples destinos en un AFD."
                    )

                elif destino not in self.estados:

                    errores.append(
                        f"El destino '{destino}' no existe."
                    )

        return errores


    # ---------------------------------
    # Es válido
    # ---------------------------------

    def es_valido(self):

        return len(
            self.validar()
        ) == 0


    # ---------------------------------
    # Mostrar
    # ---------------------------------

    def mostrar(self):

        print(
            "\n===== AUTÓMATA ====="
        )

        print(
            "Tipo:",
            self.tipo
        )

        print(
            "Estados Q:",
            self.estados
        )

        print(
            "Alfabeto Σ:",
            self.alfabeto
        )

        print(
            "Estado inicial:",
            self.estado_inicial
        )

        print(
            "Estados finales:",
            self.estados_finales
        )

        print(
            "Transiciones δ:"
        )

        for transicion, destino in self.transiciones.items():

            print(
                transicion,
                "→",
                destino
            )