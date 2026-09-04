class Simulador:


    def __init__(self, automata):

        self.automata = automata



    # ---------------------------------
    # Simulación AFD
    # ---------------------------------

    def simular_afd(self, cadena):


        errores = self.automata.validar()


        if errores:

            return False, [], "\n".join(errores)



        estado_actual = self.automata.estado_inicial



        recorrido = []


        recorrido.append(
            f"Inicio: {estado_actual}"
        )



        for simbolo in cadena:



            if simbolo not in self.automata.alfabeto:


                return (
                    False,
                    recorrido,
                    f"Símbolo inválido: {simbolo}"
                )



            recorrido.append(
                f"Leer símbolo: {simbolo}"
            )



            estado_actual = self.automata.obtener_transicion(
                estado_actual,
                simbolo
            )



            if estado_actual is None:


                recorrido.append(
                    "No existe transición"
                )


                return (
                    False,
                    recorrido,
                    "Cadena rechazada"
                )



            recorrido.append(
                f"Nuevo estado: {estado_actual}"
            )



        if estado_actual in self.automata.estados_finales:



            recorrido.append(
                "Estado final encontrado"
            )


            return (
                True,
                recorrido,
                "Cadena aceptada"
            )



        recorrido.append(
            "No es estado final"
        )


        return (
            False,
            recorrido,
            "Cadena rechazada"
        )





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


        errores = self.automata.validar()


        if errores:


            return False, [], "\n".join(errores)



        estados_actuales = self.epsilon_clausura(
            {
                self.automata.estado_inicial
            }
        )



        recorrido = []



        recorrido.append(
            f"Inicio: {estados_actuales}"
        )



        for simbolo in cadena:



            if simbolo not in self.automata.alfabeto:



                return (
                    False,
                    recorrido,
                    f"Símbolo inválido: {simbolo}"
                )



            recorrido.append(
                f"Leer símbolo: {simbolo}"
            )



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



            recorrido.append(
                f"Estados actuales: {estados_actuales}"
            )



            if not estados_actuales:


                recorrido.append(
                    "No existen caminos posibles"
                )


                return (
                    False,
                    recorrido,
                    "Cadena rechazada"
                )



        for estado in estados_actuales:



            if estado in self.automata.estados_finales:



                recorrido.append(
                    "Estado final encontrado"
                )


                return (
                    True,
                    recorrido,
                    "Cadena aceptada"
                )



        recorrido.append(
            "No hay estados finales"
        )



        return (
            False,
            recorrido,
            "Cadena rechazada"
        )