from automata import Automata
from simulador import Simulador



def main():


    automata = Automata("AFD")


    # Estados

    automata.agregar_estado("q0")
    automata.agregar_estado("q1")
    automata.agregar_estado("q2")



    # Alfabeto

    automata.agregar_simbolo("0")
    automata.agregar_simbolo("1")



    # Inicial

    automata.establecer_estado_inicial("q0")



    # Final

    automata.agregar_estado_final("q2")



    # Transiciones

    automata.agregar_transicion("q0","0","q1")

    automata.agregar_transicion("q1","1","q2")



    simulador = Simulador(automata)



    cadena = "01"


    aceptada, recorrido, mensaje = simulador.simular_afd(cadena)



    print("\nCadena:", cadena)

    print("Recorrido:", recorrido)

    print("Resultado:", mensaje)




if __name__ == "__main__":

    main()