class Automata:


    def __init__(self, tipo="AFD"):

        # Tipo de automata: AFN o AFD
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
    # Agregar estados
    # ---------------------------------

    def agregar_estado(self, estado):

        self.estados.add(estado)



    # ---------------------------------
    # Definir estado inicial
    # ---------------------------------

    def establecer_estado_inicial(self, estado):

        self.estados.add(estado)

        self.estado_inicial = estado



    # ---------------------------------
    # Agregar estado final
    # ---------------------------------

    def agregar_estado_final(self, estado):

        self.estados_finales.add(estado)



    # ---------------------------------
    # Agregar símbolos al alfabeto
    # ---------------------------------

    def agregar_simbolo(self, simbolo):

        self.alfabeto.add(simbolo)



    # ---------------------------------
    # Agregar transición
    # ---------------------------------

    def agregar_transicion(self, origen, simbolo, destino):

        clave = (origen, simbolo)



        # AFN permite múltiples destinos

        if self.tipo == "AFN":


            if clave not in self.transiciones:

                self.transiciones[clave] = set()



            self.transiciones[clave].add(destino)



        # AFD solamente un destino

        else:


            if clave in self.transiciones:

                raise ValueError(
                    "Un AFD no puede tener múltiples destinos para la misma transición"
                )


            self.transiciones[clave] = destino





    # ---------------------------------
    # Obtener transición
    # ---------------------------------

    def obtener_transicion(self, estado, simbolo):

        clave = (estado, simbolo)

        return self.transiciones.get(clave, None)




    # ---------------------------------
    # Validar automata
    # ---------------------------------

    def validar(self):


        errores = []



        # Verificar estado inicial

        if self.estado_inicial is None:

            errores.append(
                "No existe estado inicial"
            )



        elif self.estado_inicial not in self.estados:

            errores.append(
                "El estado inicial no pertenece al conjunto de estados"
            )



        # Verificar estados finales

        for estado in self.estados_finales:


            if estado not in self.estados:

                errores.append(
                    f"El estado final {estado} no existe"
                )



        # Verificar transiciones

        for (origen, simbolo), destino in self.transiciones.items():



            # Verificar origen

            if origen not in self.estados:

                errores.append(
                    f"El estado origen {origen} no existe"
                )



            # Verificar símbolo

            if simbolo != "ε" and simbolo not in self.alfabeto:

                errores.append(
                    f"El símbolo {simbolo} no pertenece al alfabeto"
                )



            # AFN

            if self.tipo == "AFN":


                for estado_destino in destino:


                    if estado_destino not in self.estados:

                        errores.append(
                            f"El destino {estado_destino} no existe"
                        )



            # AFD

            else:


                if destino not in self.estados:

                    errores.append(
                        f"El destino {destino} no existe"
                    )



        return errores



    # ---------------------------------
    # Comprobar si es válido
    # ---------------------------------

    def es_valido(self):

        return len(self.validar()) == 0




    # ---------------------------------
    # Mostrar información
    # ---------------------------------

    def mostrar(self):

        print("\n===== AUTOMATA =====")

        print("Tipo:", self.tipo)

        print("Estados Q:", self.estados)

        print("Alfabeto Σ:", self.alfabeto)

        print("Estado inicial:", self.estado_inicial)

        print("Estados finales:", self.estados_finales)

        print("Transiciones δ:")



        for transicion, destino in self.transiciones.items():

            print(transicion, "→", destino)