class Automata:


    def __init__(self, tipo="AFD"):

        tipo = tipo.upper().strip()

        if tipo not in ("AFD", "AFN"):

            raise ValueError(
                "El tipo de autómata debe ser AFD o AFN."
            )

        # Tipo de autómata
        self.tipo = tipo

        # Q = conjunto de estados
        self.estados = set()

        # Σ = alfabeto
        self.alfabeto = set()

        # δ = función de transición
        self.transiciones = {}

        # q0 = estado inicial
        self.estado_inicial = None

        # F = estados finales
        self.estados_finales = set()



    # ---------------------------------
    # Agregar estado
    # ---------------------------------

    def agregar_estado(self, estado):

        estado = estado.strip()


        if not estado:

            raise ValueError(
                "El nombre del estado no puede estar vacío."
            )


        self.estados.add(
            estado
        )



    # ---------------------------------
    # Establecer estado inicial
    # ---------------------------------

    def establecer_estado_inicial(self, estado):

        estado = estado.strip()


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
    # Agregar estado final
    # ---------------------------------

    def agregar_estado_final(self, estado):

        estado = estado.strip()


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

        simbolo = simbolo.strip()


        if not simbolo:

            raise ValueError(
                "El símbolo no puede estar vacío."
            )


        if simbolo == "ε":

            raise ValueError(
                "ε no pertenece al alfabeto. "
                "Se utiliza únicamente como transición especial de un AFN."
            )


        # Actualmente el simulador procesa
        # la cadena carácter por carácter.
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

        origen = origen.strip()

        simbolo = simbolo.strip()

        destino = destino.strip()



        # Validar origen

        if origen not in self.estados:

            raise ValueError(
                f"El estado origen '{origen}' no existe."
            )



        # Validar destino

        if destino not in self.estados:

            raise ValueError(
                f"El estado destino '{destino}' no existe."
            )



        # Validar epsilon

        if simbolo == "ε":

            if self.tipo != "AFN":

                raise ValueError(
                    "Un AFD no puede contener transiciones ε."
                )



        # Símbolo normal

        elif simbolo not in self.alfabeto:

            raise ValueError(
                f"El símbolo '{simbolo}' no pertenece al alfabeto."
            )



        clave = (
            origen,
            simbolo
        )



        # ---------------------------------
        # AFN
        # ---------------------------------

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



        # ---------------------------------
        # AFD
        # ---------------------------------

        else:

            if clave in self.transiciones:

                destino_actual = self.transiciones[
                    clave
                ]


                # Si es exactamente la misma transición,
                # simplemente no hacemos nada.
                if destino_actual == destino:

                    return


                raise ValueError(
                    f"El AFD ya posee la transición "
                    f"{origen} --{simbolo}--> {destino_actual}. "
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

        clave = (
            origen,
            simbolo
        )


        if clave not in self.transiciones:

            raise ValueError(
                "La transición seleccionada no existe."
            )



        # AFN

        if self.tipo == "AFN":

            if destino is None:

                raise ValueError(
                    "Debe indicar el destino de la transición AFN."
                )


            if destino not in self.transiciones[clave]:

                raise ValueError(
                    "La transición seleccionada no existe."
                )


            self.transiciones[
                clave
            ].remove(
                destino
            )


            # Si ya no existen destinos
            if not self.transiciones[clave]:

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

        clave = (
            estado,
            simbolo
        )


        return self.transiciones.get(
            clave,
            None
        )



    # ---------------------------------
    # Validar autómata completo
    # ---------------------------------

    def validar(self):

        errores = []



        # ---------------------------------
        # Estados
        # ---------------------------------

        if not self.estados:

            errores.append(
                "El autómata no contiene estados."
            )



        # ---------------------------------
        # Estado inicial
        # ---------------------------------

        if self.estado_inicial is None:

            errores.append(
                "No existe estado inicial."
            )


        elif self.estado_inicial not in self.estados:

            errores.append(
                f"El estado inicial '{self.estado_inicial}' "
                "no pertenece al conjunto de estados."
            )



        # ---------------------------------
        # Estados finales
        # ---------------------------------

        for estado in self.estados_finales:

            if estado not in self.estados:

                errores.append(
                    f"El estado final '{estado}' no existe."
                )



        # ---------------------------------
        # Alfabeto
        # ---------------------------------

        if "ε" in self.alfabeto:

            errores.append(
                "ε no debe pertenecer al alfabeto."
            )



        # ---------------------------------
        # Transiciones
        # ---------------------------------

        for (
            origen,
            simbolo
        ), destino in self.transiciones.items():


            if origen not in self.estados:

                errores.append(
                    f"El estado origen '{origen}' no existe."
                )



            # epsilon

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



            # ---------------------------------
            # AFN
            # ---------------------------------

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



            # ---------------------------------
            # AFD
            # ---------------------------------

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
    # Comprobar si el autómata es válido
    # ---------------------------------

    def es_valido(self):

        return len(
            self.validar()
        ) == 0



    # ---------------------------------
    # Mostrar información
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