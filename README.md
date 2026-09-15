# Simulador de Autómatas

Proyecto desarrollado para el curso de **Autómatas y Lenguajes Formales**.

El sistema permite crear, simular y visualizar **Autómatas Finitos Deterministas (AFD)** y **Autómatas Finitos No Deterministas (AFN)**, incluyendo transiciones epsilon (**ε**).

También incorpora conversión de **AFN a AFD**, minimización de AFD y pruebas automáticas para validar el funcionamiento del sistema.

---

## Funcionalidades principales

La aplicación permite:

- Crear AFD y AFN.
- Definir estados, alfabeto, estado inicial y estados finales.
- Agregar y eliminar transiciones.
- Utilizar transiciones ε en AFN.
- Simular cadenas.
- Mostrar el recorrido paso a paso.
- Determinar si una cadena es aceptada o rechazada.
- Visualizar gráficamente el autómata.
- Representar estados iniciales, finales, bucles y transiciones.
- Convertir AFN a AFD.
- Mostrar la tabla de construcción de subconjuntos.
- Minimizar AFD.
- Mostrar el proceso de minimización.
- Detectar estados inalcanzables.
- Validar entradas incorrectas.
- Ejecutar pruebas automáticas.

---

## Tecnologías utilizadas

- Python 3
- Tkinter
- ttk
- unittest
- Git
- GitHub

No se requieren librerías externas adicionales para ejecutar la versión actual del proyecto.

---

## Estructura del proyecto

```text
SimuladorAutomatas/
│
├── main.py
├── automata.py
├── simulador.py
├── formulario.py
├── transiciones.py
├── interfaz.py
├── dibujador.py
├── conversion.py
├── minimizacion.py
├── test_automatas.py
├── README.md
└── .gitignore
```

### Archivos principales

**main.py**  
Inicia la aplicación.

**automata.py**  
Contiene la estructura principal del autómata:

```text
M = (Q, Σ, δ, q0, F)
```

**simulador.py**  
Realiza la simulación de cadenas en AFD y AFN, incluyendo ε-clausura.

**formulario.py**  
Permite crear nuevos autómatas desde la interfaz.

**transiciones.py**  
Permite agregar, visualizar y eliminar transiciones.

**interfaz.py**  
Contiene la ventana principal y conecta todos los módulos.

**dibujador.py**  
Genera la representación gráfica del autómata.

**conversion.py**  
Realiza la conversión de AFN a AFD mediante construcción de subconjuntos.

**minimizacion.py**  
Realiza la minimización de AFD mediante refinamiento de particiones.

**test_automatas.py**  
Contiene las pruebas automáticas del proyecto.

---

## Ejecución

Para iniciar el programa:

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```

---

## Ejemplo de AFD

Datos:

```text
Estados:
q0,q1,q2

Alfabeto:
0,1

Inicial:
q0

Final:
q2
```

Transiciones:

```text
q0 --0--> q1
q1 --1--> q2
```

Cadena:

```text
01
```

Resultado:

```text
Cadena aceptada
```

---

## AFN y transiciones ε

En un AFN pueden existir varios destinos para un mismo símbolo.

Ejemplo:

```text
q0 --0--> q1
q0 --0--> q2
```

Por lo tanto:

```text
δ(q0,0) = {q1,q2}
```

También se permiten transiciones epsilon:

```text
q0 --ε--> q1
```

Importante:

```text
ε no debe escribirse dentro del alfabeto.
```

El programa lo agrega automáticamente como opción cuando se trabaja con un AFN.

---

## Conversión AFN → AFD

El sistema implementa la **construcción de subconjuntos**.

Ejemplo:

```text
A = {q0}
B = {q0,q1}
C = ∅
```

Durante el proceso se muestra una tabla con los nuevos estados y sus transiciones.

Ejemplo:

| Estado AFD | Subconjunto | 0 | 1 |
|---|---|---|---|
| A | {q0} | B | C |
| B | {q0,q1} | B | D |
| C | ∅ | C | C |

La conversión también considera ε-clausuras.

---

## Minimización de AFD

La minimización se realiza mediante **refinamiento de particiones**.

El procedimiento incluye:

1. Detectar estados alcanzables.
2. Separar estados finales y no finales.
3. Comparar el comportamiento de los estados.
4. Agrupar estados equivalentes.
5. Construir el AFD mínimo.

Ejemplo:

```text
q0 ≡ q1
q2 ≡ q3
```

Entonces:

```text
A = {q0,q1}
B = {q2,q3}
```

El autómata mínimo conserva el mismo lenguaje utilizando menos estados.

---

## Visualización gráfica

El sistema permite visualizar:

- Estado inicial.
- Estados finales.
- Transiciones.
- Bucles.
- Transiciones bidireccionales.
- Múltiples símbolos entre estados.

Los diagramas se centran automáticamente y utilizan barras de desplazamiento cuando son demasiado grandes.

---

## Validaciones

El programa evita errores como:

- Estado inicial inexistente.
- Estado final inexistente.
- ε dentro del alfabeto.
- Transiciones ε en un AFD.
- Dos destinos distintos para la misma transición de un AFD.
- Símbolos que no pertenecen al alfabeto.
- Estados o destinos inexistentes.

---

## Pruebas automáticas

Para ejecutar las pruebas:

```bash
python test_automatas.py
```

Resultado esperado:

```text
Ran 21 tests

OK
```

Las pruebas verifican principalmente:

- AFD.
- AFN.
- ε-clausura.
- Simulación.
- Validaciones.
- Conversión AFN → AFD.
- Minimización.
- Estados inalcanzables.

---

## Control de versiones

El proyecto utiliza Git y GitHub.

Flujo básico:

```bash
git add .
git commit -m "Descripcion del cambio"
git push
```

Esto permite mantener el historial y la trazabilidad del desarrollo.

---

## Estado del proyecto

### Fase 1

```text
COMPLETADA
```

Incluye:

- AFD.
- AFN.
- ε-transiciones.
- Simulación.
- Visualización.
- Conversión AFN → AFD.
- Minimización.
- Validaciones.
- Pruebas automáticas.

### Fase 2

Pendiente.

Se contempla agregar soporte para:

- Expresiones regulares.
- Validación de expresiones.
- Conversión de expresiones regulares a autómatas.
- Integración con las funciones desarrolladas en la Fase 1.

---

## Integrantes

- Benett Isaac Morales Perez 0903-24-7313
- Dulce María Pérez Navarro 0903-23-10366
- Wilmer Adrian Coronado Velasquez 0903-24-7398
- Angel Gabriel Navarro Perez 0903-24-914
```

---

## Curso

**Autómatas y Lenguajes Formales**

---

## Conclusión

El proyecto implementa los principales conceptos de autómatas finitos estudiados en el curso.

La aplicación permite crear, simular, visualizar, convertir y minimizar autómatas, manteniendo una estructura modular que facilita continuar con las siguientes fases del proyecto.

