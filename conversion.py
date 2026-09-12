from automata import Automata



class ConversionAFN_AFD:


    def __init__(self, afn):


        self.afn = afn



    # ---------------------------------
    # ε-clausura
    # ---------------------------------

    def epsilon_clausura(self, estados):


        clausura = set(estados)


        pendientes = list(estados)



        while pendientes:


            estado = pendientes.pop()



            transicion = self.afn.obtener_transicion(
                estado,
                "ε"
            )



            if transicion:


                for nuevo_estado in transicion:


                    if nuevo_estado not in clausura:


                        clausura.add(nuevo_estado)

                        pendientes.append(nuevo_estado)



        return clausura



    # ---------------------------------
    # Mover estados
    # ---------------------------------

    def mover(self, estados, simbolo):


        resultado = set()



        for estado in estados:


            transicion = self.afn.obtener_transicion(
                estado,
                simbolo
            )


            if transicion:


                resultado.update(
                    transicion
                )



        return resultado




    # ---------------------------------
    # Conversión AFN → AFD
    # ---------------------------------

    def convertir(self):


        afd = Automata(
            "AFD"
        )



        afd.alfabeto = self.afn.alfabeto.copy()



        estado_inicial = frozenset(
            self.epsilon_clausura(
                {
                    self.afn.estado_inicial
                }
            )
        )



        pendientes = [
            estado_inicial
        ]



        visitados = set()



        nombres = {}



        contador = 0



        nombres[estado_inicial] = (
            "A"
        )



        afd.agregar_estado(
            "A"
        )


        afd.establecer_estado_inicial(
            "A"
        )



        while pendientes:


            actual = pendientes.pop()



            if actual in visitados:

                continue



            visitados.add(
                actual
            )



            nombre_actual = nombres[actual]



            # Verificar estado final

            if any(
                estado in self.afn.estados_finales
                for estado in actual
            ):


                afd.agregar_estado_final(
                    nombre_actual
                )



            for simbolo in self.afn.alfabeto:



                movimiento = self.mover(
                    actual,
                    simbolo
                )



                clausura = frozenset(
                    self.epsilon_clausura(
                        movimiento
                    )
                )



                if len(clausura) == 0:

                    continue



                if clausura not in nombres:


                    contador += 1


                    nuevo_nombre = chr(
                        65 + contador
                    )


                    nombres[clausura] = nuevo_nombre


                    afd.agregar_estado(
                        nuevo_nombre
                    )


                    pendientes.append(
                        clausura
                    )



                afd.agregar_transicion(
                    nombre_actual,
                    simbolo,
                    nombres[clausura]
                )



        return afd