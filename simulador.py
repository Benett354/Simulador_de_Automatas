class Simulador:


    def __init__(self, automata):

        self.automata = automata




    # Simulación de AFD


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



        # Verificar estado final

        if estado_actual in self.automata.estados_finales:

            return True, recorrido, "Cadena aceptada"


        else:

            return False, recorrido, "Cadena rechazada"