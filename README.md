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

---

### Modelo CSP para la Construcción de Crucigramas

#### 1. Variables ($X$)
Cada palabra en los conjuntos de palabras a colocar se modela como una variable independiente, entonces para diferenciar la orientación de las palabras (lo que define su comportamiento geométrico y restricciones), representare cada variable como una tupla:
$$X = \{ (w, \text{dir}) \mid w \in H \cup V \}$$
donde:
- $H$ es el conjunto de palabras horizontales.
- $V$ es el conjunto de palabras verticales.
- $\text{dir} \in \{'H', 'V'\}$ indica la orientación de la palabra.

#### 2. Dominios ($D$)
El dominio $D[(w, \text{dir})]$ representa las coordenadas de inicio válidas $(r, c)$ en la retícula de tamaño $n \times m$ (filas indexadas de $0$ a $n-1$, columnas indexadas de $0$ a $m-1$):
- Si la dirección es `'H'` (horizontal), la palabra de longitud $L = \text{len}(w)$ se coloca horizontalmente. Debe caber dentro del límite derecho de la retícula:
  $$D[(w, 'H')] = \{ (r, c) \mid 0 \leq r < n \text{ y } 0 \leq c \leq m - L \}$$
- Si la dirección es `'V'` (vertical), la palabra de longitud $L = \text{len}(w)$ se coloca verticalmente, debe caber dentro del límite inferior de la retícula:
  $$D[(w, 'V')] = \{ (r, c) \mid 0 \leq r \leq n - L \text{ y } 0 \leq c < m \}$$

#### 3. Restricciones Unarias
No se requieren restricciones unarias explícitas, ya que los límites de la retícula y la orientación de cada palabra quedan completamente definidos y filtrados al generar los dominios iniciales.

#### 4. Restricciones Binarias
Definimos la restricción binaria entre dos palabras asignadas $x_i = (w_i, \text{dir}_i)$ con valor $v_i = (r_i, c_i)$ y $x_j = (w_j, \text{dir}_j)$ con valor $v_j = (r_j, c_j)$.
Sean $L_i = \text{len}(w_i)$ y $L_j = \text{len}(w_j)$.

##### Caso A: Misma dirección ($\text{dir}_i == \text{dir}_j$)
- **Orientación Horizontal ($'H'$):**
  - Si sus columnas se traslapan (es decir, $\max(c_i, c_j) \leq \min(c_i + L_i - 1, c_j + L_j - 1)$), deben estar separadas por al menos una fila intermedia para evitar estar pegadas en filas adyacentes:
    $$|r_i - r_j| \geq 2$$
  - Si están en la misma fila ($r_i == r_j$), deben estar separadas por al menos una celda vacía para evitar un traslape o quedar pegadas extremo con extremo:
    $$c_i + L_i < c_j \quad \text{o} \quad c_j + L_j < c_i$$
- **Orientación Vertical ($'V'$):**
  - Si sus filas se traslapan (es decir, $\max(r_i, r_j) \leq \min(r_i + L_i - 1, r_j + L_j - 1)$), deben estar separadas por al menos una columna intermedia:
    $$|c_i - c_j| \geq 2$$
  - Si están en la misma columna ($c_i == c_j$), deben estar separadas por al menos una celda vacía:
    $$r_i + L_i < r_j \quad \text{o} \quad r_j + L_j < r_i$$

##### Caso B: Dirección opuesta (una es $'H'$ y otra $'V'$)
Supongamos sin pérdida de generalidad que $x_i$ es horizontal con valor $(r_h, c_h)$ y $x_j$ es vertical con valor $(r_v, c_v)$.
- **Si se cruzan** (es decir, $r_h \in [r_v, r_v + L_j - 1]$ y $c_v \in [c_h, c_h + L_i - 1]$):
  - El cruce ocurre exactamente en la celda $(r_h, c_v)$. Las letras de ambas palabras en esa celda deben coincidir:
    $$w_i[c_v - c_h] == w_j[r_h - r_v]$$
- **Si no se cruzan**, no deben estar adyacentes (no pueden tocarse en sus extremos o lateralmente):
  - No puede ocurrir que $r_h \in [r_v, r_v + L_j - 1]$ con $c_v \in \{c_h - 1, c_h + L_i\}$.
  - No puede ocurrir que $c_v \in [c_h, c_h + L_i - 1]$ con $r_h \in \{r_v - 1, r_v + L_j\}$.

#### 5. Restricciones Globales y su conversión a restricciones binarias
- **Conectividad**: En un crucigrama válido, todas las palabras deben formar un único componente conexo (todas deben cruzar directa o indirectamente con las demás).
  - *Conversión*: Dado que el resolvedor en `csps.py` solo ejecuta búsquedas basadas en consistencia binaria local, esta restricción global se manejará mediante una verificación a nivel de asignación completa, si la asignación final no es conexa, se barajarán los dominios de forma aleatoria para explorar otra ruta en el árbol de búsqueda.

#### 6. Vecinos ($N$)
Para asegurar que se apliquen todas las restricciones de no colisión, adyacencia e intersección, cada palabra es vecina de todas las demás palabras del problema:
$$N[x] = X \setminus \{x\}$$



