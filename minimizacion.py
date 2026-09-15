from automata import Automata
from collections import deque


class MinimizadorAFD:


    def __init__(self, afd):

        self.afd = afd

        # Guarda las particiones generadas
        self.pasos = []

        # Relación:
        # estado original -> estado minimizado
        self.mapeo_estados = {}

        # Indica si fue necesario crear estado pozo
        self.estado_pozo = None



    # ---------------------------------
    # Generar nombres A, B, C...
    # ---------------------------------

    def generar_nombre(self, numero):

        nombre = ""

        while True:

            numero, residuo = divmod(
                numero,
                26
            )

            nombre = chr(
                65 + residuo
            ) + nombre

            if numero == 0:
                break

            numero -= 1

        return nombre



    # ---------------------------------
    # Obtener estados alcanzables
    # ---------------------------------

    def obtener_alcanzables(self):

        alcanzables = set()

        pendientes = deque()

        pendientes.append(
            self.afd.estado_inicial
        )



        while pendientes:

            estado = pendientes.popleft()


            if estado in alcanzables:
                continue


            alcanzables.add(
                estado
            )



            for simbolo in self.afd.alfabeto:

                destino = self.afd.obtener_transicion(
                    estado,
                    simbolo
                )


                if destino is not None:

                    if destino not in alcanzables:

                        pendientes.append(
                            destino
                        )



        return alcanzables



    # ---------------------------------
    # Preparar AFD completo
    # ---------------------------------

    def preparar_afd(self):

        estados = self.obtener_alcanzables()

        transiciones = {}

        alfabeto = set(
            self.afd.alfabeto
        )



        # Copiar transiciones existentes

        for estado in estados:

            for simbolo in alfabeto:

                destino = self.afd.obtener_transicion(
                    estado,
                    simbolo
                )


                if destino is not None:

                    transiciones[
                        (estado, simbolo)
                    ] = destino



        # ---------------------------------
        # Verificar si faltan transiciones
        # ---------------------------------

        necesita_pozo = False


        for estado in estados:

            for simbolo in alfabeto:

                if (estado, simbolo) not in transiciones:

                    necesita_pozo = True



        # ---------------------------------
        # Crear estado pozo si hace falta
        # ---------------------------------

        if necesita_pozo:

            nombre_pozo = "POZO"

            contador = 1


            while nombre_pozo in estados:

                nombre_pozo = (
                    f"POZO_{contador}"
                )

                contador += 1



            self.estado_pozo = nombre_pozo


            estados.add(
                nombre_pozo
            )



            # Completar transiciones faltantes

            for estado in list(estados):

                for simbolo in alfabeto:

                    if (estado, simbolo) not in transiciones:

                        transiciones[
                            (estado, simbolo)
                        ] = nombre_pozo



            # El pozo siempre vuelve a sí mismo

            for simbolo in alfabeto:

                transiciones[
                    (nombre_pozo, simbolo)
                ] = nombre_pozo



        return (
            estados,
            alfabeto,
            transiciones
        )



    # ---------------------------------
    # Buscar bloque de un estado
    # ---------------------------------

    def indice_bloque(
        self,
        estado,
        particiones
    ):

        for indice, bloque in enumerate(
            particiones
        ):

            if estado in bloque:

                return indice


        return -1



    # ---------------------------------
    # Guardar copia de particiones
    # ---------------------------------

    def guardar_paso(self, particiones):

        copia = []

        for bloque in particiones:

            copia.append(
                set(bloque)
            )

        self.pasos.append(
            copia
        )



    # ---------------------------------
    # Minimizar AFD
    # ---------------------------------

    def minimizar(self):

        # ---------------------------------
        # Validaciones
        # ---------------------------------

        if self.afd.tipo != "AFD":

            raise ValueError(
                "La minimización solamente puede realizarse sobre un AFD."
            )



        errores = self.afd.validar()


        if errores:

            raise ValueError(
                "\n".join(errores)
            )



        if not self.afd.estados:

            raise ValueError(
                "El AFD no contiene estados."
            )



        # ---------------------------------
        # Eliminar estados inalcanzables
        # y completar transición
        # ---------------------------------

        estados, alfabeto, transiciones = (
            self.preparar_afd()
        )



        finales = (
            self.afd.estados_finales
            & estados
        )


        no_finales = (
            estados
            - finales
        )



        # ---------------------------------
        # P0
        # Finales / No finales
        # ---------------------------------

        particiones = []


        if finales:

            particiones.append(
                set(finales)
            )


        if no_finales:

            particiones.append(
                set(no_finales)
            )



        self.pasos = []

        self.guardar_paso(
            particiones
        )



        # ---------------------------------
        # Refinamiento de particiones
        # ---------------------------------

        while True:

            nuevas_particiones = []



            for bloque in particiones:

                grupos = {}



                for estado in bloque:

                    firma = []



                    for simbolo in sorted(
                        alfabeto
                    ):

                        destino = transiciones[
                            (estado, simbolo)
                        ]


                        indice = self.indice_bloque(
                            destino,
                            particiones
                        )


                        firma.append(
                            indice
                        )



                    firma = tuple(
                        firma
                    )



                    if firma not in grupos:

                        grupos[firma] = set()



                    grupos[firma].add(
                        estado
                    )



                for grupo in grupos.values():

                    nuevas_particiones.append(
                        grupo
                    )



            # ---------------------------------
            # Verificar si ya no hubo cambios
            # ---------------------------------

            particiones_anteriores = {
                frozenset(bloque)
                for bloque in particiones
            }


            particiones_nuevas = {
                frozenset(bloque)
                for bloque in nuevas_particiones
            }



            if (
                particiones_anteriores
                ==
                particiones_nuevas
            ):

                break



            particiones = nuevas_particiones


            self.guardar_paso(
                particiones
            )



        # ---------------------------------
        # Crear AFD mínimo
        # ---------------------------------

        afd_minimo = Automata(
            "AFD"
        )



        for simbolo in alfabeto:

            afd_minimo.agregar_simbolo(
                simbolo
            )



        # ---------------------------------
        # Crear nombre para cada bloque
        # ---------------------------------

        nombre_bloques = {}



        for indice, bloque in enumerate(
            particiones
        ):

            nombre = self.generar_nombre(
                indice
            )


            nombre_bloques[
                frozenset(bloque)
            ] = nombre


            afd_minimo.agregar_estado(
                nombre
            )



            for estado in bloque:

                self.mapeo_estados[
                    estado
                ] = nombre



        # ---------------------------------
        # Estado inicial
        # ---------------------------------

        nuevo_inicial = self.mapeo_estados[
            self.afd.estado_inicial
        ]


        afd_minimo.establecer_estado_inicial(
            nuevo_inicial
        )



        # ---------------------------------
        # Estados finales
        # ---------------------------------

        for bloque in particiones:

            if bloque & finales:

                nombre = nombre_bloques[
                    frozenset(bloque)
                ]


                afd_minimo.agregar_estado_final(
                    nombre
                )



        # ---------------------------------
        # Transiciones del AFD mínimo
        # ---------------------------------

        for bloque in particiones:

            representante = next(
                iter(bloque)
            )


            origen_nuevo = nombre_bloques[
                frozenset(bloque)
            ]



            for simbolo in sorted(
                alfabeto
            ):

                destino_original = transiciones[
                    (
                        representante,
                        simbolo
                    )
                ]


                destino_nuevo = self.mapeo_estados[
                    destino_original
                ]



                afd_minimo.agregar_transicion(
                    origen_nuevo,
                    simbolo,
                    destino_nuevo
                )



        return afd_minimo



    # ---------------------------------
    # Obtener pasos
    # ---------------------------------

    def obtener_pasos(self):

        return self.pasos



    # ---------------------------------
    # Obtener equivalencias
    # ---------------------------------

    def obtener_mapeo(self):

        return self.mapeo_estados