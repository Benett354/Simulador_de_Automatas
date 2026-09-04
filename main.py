from automata import Automata
from simulador import Simulador



def main():


    automata = Automata("AFN")


    # Estados

    automata.agregar_estado("q0")
    automata.agregar_estado("q1")
    automata.agregar_estado("q2")
    automata.agregar_estado("q3")


    # Alfabeto

    automata.agregar_simbolo("0")
    automata.agregar_simbolo("1")


    # Inicial

    automata.establecer_estado_inicial("q0")


    # Final

    automata.agregar_estado_final("q3")



    # Transición epsilon

    automata.agregar_transicion(
        "q0",
        "ε",
        "q1"
    )



    # Transiciones normales

    automata.agregar_transicion(
        "q1",
        "0",
        "q2"
    )


    automata.agregar_transicion(
        "q2",
        "1",
        "q3"
    )



    simulador = Simulador(automata)



    cadena = "01"



    aceptada, recorrido, mensaje = simulador.simular_afn(cadena)



    print("\nCadena:", cadena)


    print("\nRecorrido:")

    for paso in recorrido:

        print(paso)



    print("\nResultado:")

    print(mensaje)




if __name__ == "__main__":

    main()