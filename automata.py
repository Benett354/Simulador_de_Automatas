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



    # Agregar estados


    def agregar_estado(self, estado):

        self.estados.add(estado)



  
    # Definir estado inicial


    def establecer_estado_inicial(self, estado):

        self.estados.add(estado)

        self.estado_inicial = estado




    # Agregar estado final


    def agregar_estado_final(self, estado):

        self.estados.add(estado)

        self.estados_finales.add(estado)




    # Agregar símbolos al alfabeto


    def agregar_simbolo(self, simbolo):

        self.alfabeto.add(simbolo)




    # Agregar transición


    def agregar_transicion(self, origen, simbolo, destino):

        clave = (origen, simbolo)

        if self.tipo == "AFN":

            if clave not in self.transiciones:

                self.transiciones[clave] = set()

            self.transiciones[clave].add(destino)


        else:

            self.transiciones[clave] = destino



  
    # Obtener transición


    def obtener_transicion(self, estado, simbolo):

        clave = (estado, simbolo)

        return self.transiciones.get(clave, None)




    # Mostrar información


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