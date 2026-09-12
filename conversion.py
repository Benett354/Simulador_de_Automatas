from automata import Automata
from collections import deque


class ConversionAFN_AFD:


    def __init__(self, afn):

        self.afn = afn

        # Relación:
        # subconjunto AFN -> nombre del estado AFD
        self.nombres = {}

        # Guarda las filas de la tabla de subconjuntos
        self.tabla_subconjuntos = []



    # ---------------------------------
    # ε-clausura
    # ---------------------------------

    def epsilon_clausura(self, estados):

        clausura = set(estados)

        pendientes = list(estados)


        while pendientes:

            estado = pendientes.pop()


            destinos = self.afn.obtener_transicion(
                estado,
                "ε"
            )


            if destinos:

                for nuevo_estado in destinos:

                    if nuevo_estado not in clausura:

                        clausura.add(
                            nuevo_estado
                        )

                        pendientes.append(
                            nuevo_estado
                        )


        return clausura



    # ---------------------------------
    # Función mover
    # ---------------------------------

    def mover(self, estados, simbolo):

        resultado = set()


        for estado in estados:

            destinos = self.afn.obtener_transicion(
                estado,
                simbolo
            )


            if destinos:

                resultado.update(
                    destinos
                )


        return resultado



    # ---------------------------------
    # Generar nombre A, B, C...
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
    # Mostrar conjunto ordenado
    # ---------------------------------

    def formatear_conjunto(self, conjunto):

        if not conjunto:

            return "∅"


        estados = sorted(
            conjunto
        )


        return "{" + ", ".join(estados) + "}"



    # ---------------------------------
    # Obtener nombre para subconjunto
    # ---------------------------------

    def registrar_subconjunto(
        self,
        subconjunto,
        afd,
        pendientes
    ):

        if subconjunto not in self.nombres:

            numero = len(
                self.nombres
            )

            nombre = self.generar_nombre(
                numero
            )


            self.nombres[
                subconjunto
            ] = nombre


            afd.agregar_estado(
                nombre
            )


            pendientes.append(
                subconjunto
            )



    # ---------------------------------
    # Conversión AFN -> AFD
    # ---------------------------------

    def convertir(self):


        if self.afn.tipo != "AFN":

            raise ValueError(
                "La conversión solamente puede realizarse con un AFN."
            )


        errores = self.afn.validar()


        if errores:

            raise ValueError(
                "\n".join(errores)
            )



        # Crear AFD vacío

        afd = Automata(
            "AFD"
        )



        # Copiar alfabeto

        for simbolo in self.afn.alfabeto:

            afd.agregar_simbolo(
                simbolo
            )



        # Limpiar datos de una conversión anterior

        self.nombres = {}

        self.tabla_subconjuntos = []



        # ---------------------------------
        # PASO 1:
        # ε-clausura del estado inicial
        # ---------------------------------

        inicial = frozenset(
            self.epsilon_clausura(
                {
                    self.afn.estado_inicial
                }
            )
        )



        pendientes = deque()



        # Registrar primer subconjunto

        self.registrar_subconjunto(
            inicial,
            afd,
            pendientes
        )



        nombre_inicial = self.nombres[
            inicial
        ]



        afd.establecer_estado_inicial(
            nombre_inicial
        )



        procesados = set()



        # ---------------------------------
        # Construcción de subconjuntos
        # ---------------------------------

        while pendientes:


            actual = pendientes.popleft()



            if actual in procesados:

                continue



            procesados.add(
                actual
            )



            nombre_actual = self.nombres[
                actual
            ]



            # ---------------------------------
            # Revisar si es estado final
            # ---------------------------------

            for estado in actual:


                if estado in self.afn.estados_finales:


                    afd.agregar_estado_final(
                        nombre_actual
                    )


                    break



            # Fila para la tabla

            fila = {
                "estado_afd": nombre_actual,
                "subconjunto": self.formatear_conjunto(
                    actual
                )
            }



            # ---------------------------------
            # Procesar cada símbolo
            # ---------------------------------

            for simbolo in sorted(
                self.afn.alfabeto
            ):


                # PASO 1:
                # mover(actual, simbolo)

                movimiento = self.mover(
                    actual,
                    simbolo
                )



                # PASO 2:
                # ε-clausura del resultado

                cierre = self.epsilon_clausura(
                    movimiento
                )



                destino = frozenset(
                    cierre
                )



                # Registrar nuevo subconjunto

                self.registrar_subconjunto(
                    destino,
                    afd,
                    pendientes
                )



                nombre_destino = self.nombres[
                    destino
                ]



                # Crear transición AFD

                afd.agregar_transicion(
                    nombre_actual,
                    simbolo,
                    nombre_destino
                )



                # Guardar resultado para tabla

                fila[simbolo] = (
                    nombre_destino
                    + " = "
                    + self.formatear_conjunto(
                        destino
                    )
                )



            self.tabla_subconjuntos.append(
                fila
            )



        return afd



    # ---------------------------------
    # Obtener tabla
    # ---------------------------------

    def obtener_tabla(self):

        return self.tabla_subconjuntos