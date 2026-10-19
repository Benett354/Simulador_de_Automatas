# Simulador de Autómatas

Proyecto desarrollado para el curso de **Autómatas y Lenguajes Formales**.

El sistema permite crear, simular y visualizar Autómatas Finitos Deterministas (AFD) y Autómatas Finitos No Deterministas (AFN), incluyendo transiciones epsilon (ε).

También incorpora conversión de AFN a AFD, minimización de AFD, procesamiento de expresiones regulares, construcción de autómatas mediante Thompson y registro y análisis de eventos en archivos de texto.

---

## Funcionalidades principales

### Fase 1: Autómatas finitos

- Crear AFD y AFN.
- Definir estados, alfabeto, estado inicial y estados finales.
- Agregar y eliminar transiciones.
- Utilizar transiciones ε en AFN.
- Simular cadenas y mostrar el recorrido paso a paso.
- Determinar si una cadena es aceptada o rechazada.
- Visualizar gráficamente los autómatas.
- Convertir AFN a AFD mediante construcción de subconjuntos.
- Mostrar la tabla de conversión.
- Minimizar AFD mediante refinamiento de particiones.
- Detectar estados inalcanzables.
- Validar entradas y transiciones incorrectas.
- Ejecutar pruebas automáticas.

### Fase 2: Expresiones regulares y Thompson

- Validar y procesar expresiones regulares.
- Detectar errores en las expresiones.
- Procesar operadores de unión, concatenación, clausura de Kleene, repetición positiva y opcional.
- Convertir expresiones regulares a notación postfija.
- Construir automáticamente un AFN con transiciones ε mediante el algoritmo de Thompson.
- Visualizar e integrar el autómata generado con las funciones compatibles del simulador.

### Registro y análisis de eventos

- Registrar eventos en archivos de texto `.txt`.
- Crear automáticamente la carpeta de registros cuando sea necesario.
- Identificar información, advertencias y errores.
- Analizar y validar el formato de los registros.
- Detectar líneas inválidas.
- Filtrar registros por nivel de severidad.
- Consultar los eventos mediante una interfaz gráfica.
- Mostrar resúmenes y detalles de los registros.

---

## Tecnologías utilizadas

- Python 3
- Tkinter y ttk
- Biblioteca estándar `logging`
- `unittest`
- Git y GitHub

No se requieren bibliotecas externas adicionales para las funcionalidades descritas del proyecto.

---

## Estructura del proyecto

```text
Simulador_de_Automatas/
│
├── algoritmos/
│   └── analizador_logs.py
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
│
├── expresion_regular.py
├── procesador_regex.py
├── constructor_thompson.py
├── formulario_regex.py
│
├── registro_logs.py
├── visor_logs.py
│
├── test_automatas.py
├── test_expresiones.py
├── test_procesador_regex.py
├── test_constructor_thompson.py
│
├── README.md
└── .gitignore
```

La carpeta `logs/` y el archivo `simulador.txt` se generan cuando se necesitan para almacenar los registros. Los archivos de registros locales están excluidos del control de versiones.

### Archivos principales

| Archivo | Función |
|---|---|
| `main.py` | Inicia la aplicación. |
| `automata.py` | Define la estructura de los autómatas. |
| `simulador.py` | Simula cadenas en AFD y AFN. |
| `formulario.py` | Permite crear autómatas. |
| `transiciones.py` | Gestiona las transiciones. |
| `interfaz.py` | Integra las herramientas en la interfaz principal. |
| `dibujador.py` | Representa gráficamente los autómatas. |
| `conversion.py` | Convierte AFN a AFD. |
| `minimizacion.py` | Minimiza autómatas deterministas. |
| `expresion_regular.py` | Gestiona las expresiones regulares. |
| `procesador_regex.py` | Valida y procesa expresiones regulares. |
| `constructor_thompson.py` | Construye AFN-ε mediante Thompson. |
| `formulario_regex.py` | Proporciona la interfaz para expresiones regulares y Thompson. |
| `registro_logs.py` | Registra eventos en archivos de texto. |
| `algoritmos/analizador_logs.py` | Analiza y valida los archivos de registros. |
| `visor_logs.py` | Permite consultar y filtrar los registros. |

---

## Ejecución

### Requisitos

- Python 3 instalado.
- Tkinter disponible en la instalación de Python.
- Archivos del proyecto en su estructura correspondiente.

Para iniciar la aplicación desde la carpeta principal:

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```



---

## Ejemplo de AFD

Datos del autómata:

```text
Estados: q0, q1, q2
Alfabeto: 0, 1
Estado inicial: q0
Estado final: q2
```

Transiciones:

```text
q0 --0--> q1
q1 --1--> q2
```

Cadena de entrada:

```text
01
```

Resultado esperado:

```text
Cadena aceptada
```

---

## Expresiones regulares y Thompson

Ejemplo de expresión regular:

```text
(a|b)*abb
```

El sistema procesa la expresión, valida su estructura y permite construir un AFN-ε mediante el algoritmo de Thompson.

El autómata generado puede visualizarse e integrarse con las funcionalidades compatibles del simulador.

---

## Registro de eventos

Los registros se almacenan en archivos de texto dentro de la carpeta `logs`.

Archivo predeterminado:

```text
logs/simulador.txt
```

Formato de ejemplo:

```text
2026-10-18 20:30:15 | INFO | Aplicación iniciada
2026-10-18 20:30:20 | WARNING | Advertencia del sistema
2026-10-18 20:30:25 | ERROR | Error durante una operación
```

El visor permite consultar los registros, filtrarlos por nivel y revisar los errores, advertencias y líneas inválidas.

---

## Pruebas automáticas

El proyecto contiene pruebas para los autómatas, las expresiones regulares y la construcción de Thompson.

Para ejecutar todas las pruebas detectadas por `unittest`:

```bash
python -m unittest discover -v
```

En Windows también puede utilizarse:

```bash
py -m unittest discover -v
```

---

## Control de versiones

El proyecto utiliza Git y GitHub para mantener el historial de cambios y facilitar el trabajo colaborativo.

Los cambios se desarrollan en las ramas correspondientes y posteriormente se integran en `main` siguiendo el flujo de trabajo del equipo.

---

## Estado del proyecto

### Fase 1

**Completada.**

Incluye la creación, simulación, visualización, conversión y minimización de autómatas finitos.

### Fase 2

**Implementación integrada; revisión final pendiente.**

Incluye el procesamiento de expresiones regulares, la construcción de Thompson y el registro y análisis de eventos mediante archivos `.txt`.

---

## Integrantes

- Benett Isaac Morales Perez — 0903-24-7313
- Dulce María Pérez Navarro — 0903-23-10366
- Wilmer Adrian Coronado Velasquez — 0903-24-7398
- Angel Gabriel Navarro Perez — 0903-24-914

---

## Curso

**Autómatas y Lenguajes Formales**

