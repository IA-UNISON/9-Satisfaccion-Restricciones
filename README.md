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


# Diseño del Modelo CSP

Para armar el crucigrama en una retícula de `n × m`, lo que hice fue modelar el problema como un CSP (Problema de Satisfacción de Restricciones).

## Variables X

Mis variables van a ser las palabras que queremos acomodar en el tablero. Para organizarme mejor, las dividí en palabras horizontales y verticales.

Si **H** es el conjunto de palabras horizontales y **V** el de las verticales, el conjunto queda así:

X = {H₁, H₂, ..., Hₕ, V₁, V₂, ..., Vᵥ}

En el código les puse un prefijo `H_` o `V_` a cada una. Así no hay problema si por error hay una palabra repetida en ambas listas, el programa las distingue bien.

## Dominios D

El dominio de cada variable son todas las coordenadas **(f, c)** (fila y columna) donde puede empezar una palabra dentro de la cuadrícula sin salirse de los bordes.

**Para una palabra horizontal con longitud L:**
D(Hᵢ) = {(f, c) | 0 ≤ f < n, 0 ≤ c ≤ m - L}

**Para una palabra vertical con longitud L:**
D(Vⱼ) = {(f, c) | 0 ≤ f ≤ n - L, 0 ≤ c < m}

Al limitar las coordenadas restándole la longitud `L`, ya nos aseguramos desde el inicio (en los puros dominios) que ninguna palabra se va a salir del tablero.

## Vecinos N

En este modelo consideré que todas las palabras son vecinas entre sí. Como cualquiera podría cruzarse o estorbarse con otra, lo mejor es que todas se revisen mutuamente.

Por eso, el grafo de restricciones quedó completamente conexo.

## Restricciones Unarias

No hizo falta programar restricciones unarias por separado. Como comenté arriba, las filtramos directamente al momento de armar los dominios para que solo tengan posiciones válidas dentro de la retícula.

## Restricciones Binarias

Estas restricciones sirven para checar si dos palabras pueden estar en el tablero al mismo tiempo sin romperse las reglas del juego.

Si tengo una palabra **xᵢ** en la posición **(f₁, c₁)** y otra **xⱼ** en **(f₂, c₂)**, tienen que cumplir dos condiciones:

### 1. Regla de Intersección

Si los caminos de las dos palabras chocan en la misma celda, la letra en esa coordenada tiene que ser exactamente la misma para ambas. Si no coincide, la asignación se descarta por inválida.

### 2. Regla de Adyacencia Ortogonal

Para que parezca un crucigrama de verdad, las palabras no pueden quedar pegadas de lado ni en los extremos a menos que se estén cruzando bien. O sea, si una celda de la palabra 1 queda a distancia 1 (arriba, abajo, izquierda o derecha) de una celda de la palabra 2 y no es el cruce permitido, la restricción falla.

## Restricciones Globales

La regla general es que todo el crucigrama quede conectado y tenga sentido. En vez de meter una restricción global súper pesada y compleja de programar, decidí aprovechar las restricciones binarias de cruce y de separación. Con esto, el propio algoritmo empaqueta las palabras solas y encuentra una configuración válida dentro del tablero.
