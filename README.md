![](ia.png)

# Algoritmos de satisfacción de restricciones

## Objetivo

En esta actividad se espera que los estudiantes desarrollen la habilidad para
expresar un problema de satisfacción de restricciones binarias de manera formal,
y que los algoritmos básicos de satisfacción de restricciones puedan utilizarse.


## Para que revisemos juntos

Lo que hay ya desarrollado es lo siguiente:

1. En el archivo `csps.py` se define la clase ProblemaCSP así como los algoritmos de solución vistos en clase.

2. En el archivo `nreinasCSP.py` se desarrolla el problema de las N Reinas y se compara la solución utilizando diferentes valores de N y diferentes tipos de consistencia.

3. En el archivo `sudoku.py` se ofrece una explicación breve del juego del sudoku, se desarrolla como un problema de satisfacción de restricciones y se prueban dos sudokus considerados de nivel *experto* para ver que es realmente un problema muy trivial a resolver.

## Diseñando crucigramas

Con el fin de dar énfasis en el problema del modelado de CSP, más que en los algoritmos de solución, en esta actividad se propone resolver el problema de construcción de crucigramas a partir de un conjunto determinado de palabras. Para esto se va a tener de entrada dos archivos `verticales.txt` y `horizontales.txt`, en los cuales van a venir una lista de palabras que se quieren usar en un crucigrama en forma vertical y horizontal, respectivamente.

El resultado que se busca es como colocar las palabras horizontales y verticales en una retícula de $n \times m$ (es necesario definir $n$ y $m$) de tal manera que cumplan con los requerimientos de un crucigrama, esto es:

- Todas las palabras en horizontal cruzan en una letra común con *al menos* una palabra en forma vertical, y viceversa.
- Una palabra en vertical no puede ir pegada a otra palabra en forma vertical (al menos debe haber una columna entre las dos si se tocan), y respectivamente en forma horizontal.
- No pueden translaparse palabras entre si.
- Si no pude caber en una retícula de $n \times m$ debe de avisar para saber que se necesita otra retícula más grande.

Para hacer el modelo es necesario establecer:

- Variables (como describirlas ¿Por palabras o por estado?)
- Dominios (En funcion de las variables y como se representarían en una retícula)
- Restricciones unarias
- Restricciones binarias
- Restricciones globales y su conversión a restricciones binarias
- Vecinos 

Agrega en este archivo el modelo que vas a usar, y prográmalo en `crucigramas.py`, prueba para un crucigrama con palabras que tu consideres. Recuerda no usar solo palabras cortas o largas, ya que se dificulta la generación del crucigrama.

Modelo CSP:

# Variables:
    Cada variable corresponde a una palabra que debe colocarse en el crucigrama.
# Dominio:
    El dominio de cada palabra son todas las posiciones posibles donde puede ubicarse dentro del crucigrama. Cada posición se representa por fila, columna y horizontal/vertical.

# Restricciones:
    Las palabras deben caber dentro de los límites del tablero.

    Las palabras horizontales deben cruzar con al menos una palabra vertical.

    Las palabras verticales deben cruzar con al menos una palabra horizontal.

    Dos palabras no pueden ocuapr la misma posición, exceoto cuando comparten una letra en un cruce.

    Dos palabras de la misma orientación (horizontal/vertical) no pueden ocupar las mismas posiciones del tablero.

# Vecinos:
    Las palabras serán consideradas vecinas, ya que puede generar problema al colocarse en el tablero.


