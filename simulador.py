class Simulador:


    def __init__(self, automata):

        self.automata = automata



    # ---------------------------------
    # Simulación AFD
    # ---------------------------------

    def simular_afd(self, cadena):

        estado_actual = self.automata.estado_inicial


        recorrido = []

        recorrido.append(estado_actual)



        for simbolo in cadena:


            # Validar símbolo

            if simbolo not in self.automata.alfabeto:

                return False, recorrido, f"Símbolo inválido: {simbolo}"



            transicion = self.automata.obtener_transicion(
                estado_actual,
                simbolo
            )


            # No existe transición

            if transicion is None:

                return False, recorrido, "No existe transición"



            estado_actual = transicion


            recorrido.append(estado_actual)



        # Verificar aceptación

        if estado_actual in self.automata.estados_finales:

            return True, recorrido, "Cadena aceptada"


        else:

            return False, recorrido, "Cadena rechazada"





    # ---------------------------------
    # ε-clausura
    # ---------------------------------

    def epsilon_clausura(self, estados):


        clausura = set(estados)


        pendientes = list(estados)



        while pendientes:


            estado = pendientes.pop()



            transiciones = self.automata.obtener_transicion(
                estado,
                "ε"
            )


            if transiciones:


                for nuevo_estado in transiciones:


                    if nuevo_estado not in clausura:


                        clausura.add(nuevo_estado)

                        pendientes.append(nuevo_estado)



        return clausura





    # ---------------------------------
    # Simulación AFN con ε
    # ---------------------------------

    def simular_afn(self, cadena):


        estados_actuales = self.epsilon_clausura(
            {
                self.automata.estado_inicial
            }
        )



        recorrido = []

        recorrido.append(estados_actuales.copy())



        for simbolo in cadena:



            if simbolo not in self.automata.alfabeto:

                return False, recorrido, f"Símbolo inválido: {simbolo}"



            nuevos_estados = set()



            for estado in estados_actuales:



                transiciones = self.automata.obtener_transicion(
                    estado,
                    simbolo
                )



                if transiciones:


                    nuevos_estados.update(transiciones)



            estados_actuales = self.epsilon_clausura(
                nuevos_estados
            )



            recorrido.append(estados_actuales.copy())



            if not estados_actuales:


                return False, recorrido, "No existen caminos"



        # Revisar estados finales

        for estado in estados_actuales:


            if estado in self.automata.estados_finales:

                return True, recorrido, "Cadena aceptada"



        return False, recorrido, "Cadena rechazada"