"""
Crucigramas como CSP. Variables = palabras; valor = posicion (r, c) de inicio.
La retricula es n x m. Cada palabra horizontal ocupa celdas (r, c..c+L-1) y
cada vertical (r..r+L-1, c).

"""

import csps
import time


def celdas(palabra, pos, orientacion):
    # devuelve la lista de celdas (r, c) que ocupa la palabra
    r, c = pos
    if orientacion == 'H':
        return [(r, c + k) for k in range(len(palabra))]
    return [(r + k, c) for k in range(len(palabra))]


def letra_en(palabra, pos, orientacion, celda):
    # letra de la palabra colocada en pos/orientacion sobre la celda dada
    r, c = pos
    if orientacion == 'H':
        return palabra[celda[1] - c]
    return palabra[celda[0] - r]


class Crucigrama(csps.ProblemaCSP):
    def __init__(self, horizontales, verticales, n, m):
        # cada variable es la palabra etiquetada con su orientacion
        # X = {('H', palabra), ('V', palabra), ...}
        self.palabras = {('H', p): p for p in horizontales}
        self.palabras.update({('V', p): p for p in verticales})
        self.orientacion = {x: x[0] for x in self.palabras}
        self.X = set(self.palabras.keys())
        self.n, self.m = n, m

        # dominio: todas las posiciones (r, c) donde la palabra cabe
        self.D = {}
        for x, pal in self.palabras.items():
            L = len(pal)
            if self.orientacion[x] == 'H':
                self.D[x] = {(r, c) for r in range(n) for c in range(m - L + 1)}
            else:
                self.D[x] = {(r, c) for r in range(n - L + 1) for c in range(m)}
            if not self.D[x]:
                raise ValueError(f"La palabra '{pal}' no cabe en {n}x{m}")

        # vecinos: todas las demas (potencialmente todas se restringen entre si)
        self.N = {x: self.X - {x} for x in self.X}

    def restriccion_binaria(self, xi, vi, xj, vj):
        pal_i, pal_j = self.palabras[xi], self.palabras[xj]
        ori_i, ori_j = self.orientacion[xi], self.orientacion[xj]
        celdas_i = set(celdas(pal_i, vi, ori_i))
        celdas_j = set(celdas(pal_j, vj, ori_j))
        comunes = celdas_i & celdas_j

        if ori_i == ori_j:
            # paralelas: no se solapan ni se tocan
            if comunes:
                return False
            if ori_i == 'H':
                # misma fila: requieren al menos una columna vacia entre ellas
                if vi[0] == vj[0]:
                    cols_i = {c for (_, c) in celdas_i}
                    cols_j = {c for (_, c) in celdas_j}
                    if min(cols_j) - max(cols_i) == 1 or min(cols_i) - max(cols_j) == 1:
                        return False
                # filas contiguas: no pueden compartir columna (quedarian pegadas)
                if abs(vi[0] - vj[0]) == 1:
                    cols_i = {c for (_, c) in celdas_i}
                    cols_j = {c for (_, c) in celdas_j}
                    if cols_i & cols_j:
                        return False
            else:
                # misma columna: requieren al menos una fila vacia entre ellas
                if vi[1] == vj[1]:
                    rows_i = {r for (r, _) in celdas_i}
                    rows_j = {r for (r, _) in celdas_j}
                    if min(rows_j) - max(rows_i) == 1 or min(rows_i) - max(rows_j) == 1:
                        return False
                # columnas contiguas: no pueden compartir fila
                if abs(vi[1] - vj[1]) == 1:
                    rows_i = {r for (r, _) in celdas_i}
                    rows_j = {r for (r, _) in celdas_j}
                    if rows_i & rows_j:
                        return False
            return True

        # cruzadas (una H, una V): comparten 0 o 1 celdas, y si comparten, letras coinciden
        if len(comunes) > 1:
            return False
        if len(comunes) == 1:
            celda = next(iter(comunes))
            return letra_en(pal_i, vi, ori_i, celda) == letra_en(pal_j, vj, ori_j, celda)
        return True


def imprime_crucigrama(asignacion, palabras_map, n, m):
    # arma una matriz n x m con las letras colocadas
    grid = [['.' for _ in range(m)] for _ in range(n)]
    for x, pos in asignacion.items():
        pal = palabras_map[x]
        for celda in celdas(pal, pos, x[0]):
            grid[celda[0]][celda[1]] = pal[celdas(pal, pos, x[0]).index(celda)]
    print()
    for fila in grid:
        print('  ' + ' '.join(fila))
    print()


def prueba_crucigrama(verticales, horizontales, n=8, m=8, consistencia=1,
                      max_intentos=2000):
    print(f"--- Crucigrama: H={horizontales}  V={verticales}  retícula {n}x{m} "
          f"consistencia={consistencia} ---")
    try:
        cru = Crucigrama(horizontales, verticales, n, m)
    except ValueError as e:
        print("ERROR:", e, "-> intenta una retícula más grande.")
        return

    # pre-filtrar dominios: eliminar posiciones que no pueden cruzar con ninguna
    # posicion posible de palabras del otro tipo (poda barata para la global)
    for x in list(cru.X):
        ori_x = cru.orientacion[x]
        otras = [y for y in cru.X if cru.orientacion[y] != ori_x]
        if not otras:
            continue
        validas = set()
        for pos in cru.D[x]:
            celdas_x = set(celdas(cru.palabras[x], pos, ori_x))
            for y in otras:
                if any(celdas_x & set(celdas(cru.palabras[y], py, cru.orientacion[y]))
                       for py in cru.D[y]):
                    validas.add(pos)
                    break
        cru.D[x] = validas

    # buscar solucion que cumpla la restriccion global; si la primera no cumple,
    # se prohibe la posicion de la palabra que no cruza y se reintenta
    dominios_base = {x: set(cru.D[x]) for x in cru.X}
    t0 = time.time()
    sol = None
    backtracks_totales = 0
    for _ in range(max_intentos):
        # restaurar dominios para cada intento
        cru.D = {x: set(dominios_base[x]) for x in cru.X}
        candidata = csps.asignacion_completa(cru, consistencia=consistencia)
        backtracks_totales += cru.backtracking
        if candidata is None:
            break
        mala = palabra_aislada(candidata, cru)
        if mala is None:
            sol = candidata
            break
        # prohibe esa posicion para la palabra aislada y reintenta
        dominios_base[mala].discard(candidata[mala])
        if not dominios_base[mala]:
            break

    dt = time.time() - t0
    if sol is None:
        print("No hay solución que cumpla la restricción global en esta retícula.")
        return

    print(f"Backtrackings totales: {backtracks_totales}    Tiempo: {dt:.3f}s")
    imprime_crucigrama(sol, cru.palabras, n, m)


def palabra_aislada(asignacion, cru):
    # devuelve la primera palabra que NO cruza ninguna del otro tipo, o None
    for x in asignacion:
        ori_x = cru.orientacion[x]
        celdas_x = set(celdas(cru.palabras[x], asignacion[x], ori_x))
        cruza = False
        for y in asignacion:
            if y == x or cru.orientacion[y] == ori_x:
                continue
            celdas_y = set(celdas(cru.palabras[y], asignacion[y], cru.orientacion[y]))
            if celdas_x & celdas_y:
                cruza = True
                break
        if not cruza:
            return x
    return None


if __name__ == "__main__":

    # Caso 1: 2 horizontales + 2 verticales, longitudes mezcladas (3, 4 y 5)
    print("=" * 60)
    print("CASO 1: longitudes 3 y 5")
    print("=" * 60)
    prueba_crucigrama(verticales=["MAR", "ARO"],
                      horizontales=["CASA", "MARZO"],
                      n=5, m=6, consistencia=2)

    # Caso 2: longitudes 4 y 5, mas palabras
    print("=" * 60)
    print("CASO 2: longitudes 4 y 5")
    print("=" * 60)
    prueba_crucigrama(verticales=["LUNA", "RAMA"],
                      horizontales=["CASA", "LARGO"],
                      n=6, m=6, consistencia=2)

    # Caso 3: muestra que avisa cuando una palabra no cabe
    print("=" * 60)
    print("CASO 3: retícula muy chica (debe avisar)")
    print("=" * 60)
    prueba_crucigrama(verticales=["LUNA"],
                      horizontales=["MURCIELAGO"],
                      n=4, m=4, consistencia=1)


# MODELO CSP DEL CRUCIGRAMA

# 1) VARIABLES
#    Una variable por cada palabra a colocar, etiquetada con su orientacion:
#       X = { ('H', palabra_h1), ('H', palabra_h2), ...,
#             ('V', palabra_v1), ('V', palabra_v2), ... }
#    Se eligio "por palabra" en vez de "por casilla" porque por palabra hay
#    pocas variables (una por palabra) con dominios manejables, mientras que
#    por casilla habria n*m variables con dominio = alfabeto y restricciones
#    globales feisimas (cada palabra completa seria una restriccion n-aria).
#
# 2) DOMINIOS
#    Cada variable toma como valor la posicion (r, c) de su PRIMERA letra en
#    la reticula n x m. Para una palabra horizontal de longitud L:
#       D = { (r, c) : 0 <= r < n  y  0 <= c <= m - L }
#    Para una vertical:
#       D = { (r, c) : 0 <= r <= n - L  y  0 <= c < m }
#    El dominio es discreto y finito.
#
# 3) RESTRICCIONES UNARIAS
#    "La palabra debe caber en la reticula". Ya esta absorbida en el dominio
#    por construccion (solo se generan posiciones donde la palabra cabe). Si
#    una palabra no cabe en la reticula, el constructor avisa con ValueError.
#
# 4) RESTRICCIONES BINARIAS
#    Para cada par de variables (xi, xj) con valores (vi, vj):
#    a) Misma orientacion (paralelas):
#         - No se solapan (sus celdas no comparten ninguna).
#         - Si estan en la misma fila/columna: al menos una celda vacia entre
#           ellas (no quedan pegadas extremo con extremo).
#         - Si estan en filas/columnas contiguas: sus rangos no se solapan en
#           la otra dimension (no quedan pegadas lado a lado).
#    b) Distinta orientacion (una H y una V):
#         - Comparten 0 o 1 celdas. Si comparten 1, las letras en esa celda
#           deben coincidir.
#
# 5) RESTRICCIONES GLOBALES Y SU CONVERSION
#    "Toda palabra cruza al menos una palabra de la otra direccion".
#    Esta restriccion es n-aria por naturaleza (involucra una palabra contra
#    TODAS las del otro tipo a la vez) y NO se convierte limpiamente a binaria
#    sin introducir variables auxiliares. Aqui se maneja con dos mecanismos:
#       (i)  Pre-filtrado de dominios: se eliminan posiciones que no cruzan
#            con ninguna posicion posible de palabras del otro tipo. Esto
#            reduce el espacio pero no garantiza el cruce efectivo.
#       (ii) Filtrado post-solucion: si el CSP devuelve una solucion donde
#            alguna palabra queda aislada, se prohibe esa posicion y se
#            reintenta hasta encontrar una solucion donde todas crucen.
#
# 6) VECINOS
#    En principio, toda variable es vecina de las demas: dos palabras
#    cualesquiera pueden chocar (solaparse, pegarse o cruzarse mal). Por eso
#    N[x] = X - {x} para toda variable x. El grafo de restriccion es completo.