import csps
import time

def posiciones_ocupadas(palabra, inicio, orientacion):
    r, c = inicio
    if orientacion == 'H':
        return [(r, c + k) for k in range(len(palabra))]
    return [(r + k, c) for k in range(len(palabra))]


def letra_en_celda(palabra, inicio, orientacion, celda):
    r, c = inicio
    if orientacion == 'H':
        return palabra[celda[1] - c]
    return palabra[celda[0] - r]

class CrucigramaCSP(csps.ProblemaCSP):
    def __init__(self, palabras_h, palabras_v, n=20, m=20):
        self.n, self.m = n, m

        self.catalog = {}
        for p in palabras_h:
            self.catalog[('H', p)] = p
        for p in palabras_v:
            self.catalog[('V', p)] = p

        self.orientacion = {x: x[0] for x in self.catalog}
        self.X = set(self.catalog.keys())

        self.D = {}
        for x, pal in self.catalog.items():
            L = len(pal)
            if self.orientacion[x] == 'H':
                self.D[x] = {(r, c) for r in range(n) for c in range(m - L + 1)}
            else:
                self.D[x] = {(r, c) for r in range(n - L + 1) for c in range(m)}
            if not self.D[x]:
                raise ValueError(f"'{pal}' no cabe en una retícula {n}×{m}")

        self.N = {x: self.X - {x} for x in self.X}

        self._podar_dominios()

    def _podar_dominios(self):
        hs = [x for x in self.X if self.orientacion[x] == 'H']
        vs = [x for x in self.X if self.orientacion[x] == 'V']

        cambio = True
        while cambio:
            cambio = False

            for xh in hs:
                antes = len(self.D[xh])
                self.D[xh] = {
                    ph for ph in self.D[xh]
                    if self._cruce_valido_existe(xh, ph, vs)
                }
                if len(self.D[xh]) != antes:
                    cambio = True

            for xv in vs:
                antes = len(self.D[xv])
                self.D[xv] = {
                    pv for pv in self.D[xv]
                    if self._cruce_valido_existe(xv, pv, hs)
                }
                if len(self.D[xv]) != antes:
                    cambio = True

    def _cruce_valido_existe(self, xi, vi, contrarias):
        celdas_i = set(posiciones_ocupadas(self.catalog[xi], vi, self.orientacion[xi]))
        for xj in contrarias:
            for vj in self.D[xj]:
                celdas_j = set(posiciones_ocupadas(self.catalog[xj], vj, self.orientacion[xj]))
                comunes = celdas_i & celdas_j
                if comunes:
                    celda = next(iter(comunes))
                    li = letra_en_celda(self.catalog[xi], vi, self.orientacion[xi], celda)
                    lj = letra_en_celda(self.catalog[xj], vj, self.orientacion[xj], celda)
                    if li == lj:
                        return True
        return False

    def restriccion_binaria(self, xi, vi, xj, vj):
        pal_i = self.catalog[xi]
        pal_j = self.catalog[xj]
        ori_i = self.orientacion[xi]
        ori_j = self.orientacion[xj]

        celdas_i = set(posiciones_ocupadas(pal_i, vi, ori_i))
        celdas_j = set(posiciones_ocupadas(pal_j, vj, ori_j))
        comunes = celdas_i & celdas_j

        if ori_i == ori_j:
            if comunes:
                return False

            if ori_i == 'H':
                ri, rj = vi[0], vj[0]
                cols_i = {c for _, c in celdas_i}
                cols_j = {c for _, c in celdas_j}
                if ri == rj:
                    if min(cols_j) - max(cols_i) == 1 or min(cols_i) - max(cols_j) == 1:
                        return False
                if abs(ri - rj) == 1 and cols_i & cols_j:
                    return False
            else:
                ci, cj = vi[1], vj[1]
                rows_i = {r for r, _ in celdas_i}
                rows_j = {r for r, _ in celdas_j}
                if ci == cj:
                    if min(rows_j) - max(rows_i) == 1 or min(rows_i) - max(rows_j) == 1:
                        return False
                if abs(ci - cj) == 1 and rows_i & rows_j:
                    return False
            return True

        if len(comunes) > 1:
            return False
        if len(comunes) == 1:
            celda = next(iter(comunes))
            li = letra_en_celda(pal_i, vi, ori_i, celda)
            lj = letra_en_celda(pal_j, vj, ori_j, celda)
            return li == lj

        return True

    def primera_palabra_aislada(asignacion, csp):
        for xi, vi in asignacion.items():
            ori_i = csp.orientacion[xi]
            celdas_i = set(posiciones_ocupadas(csp.catalog[xi], vi, ori_i))
            tiene_cruce = False
            for xj, vj in asignacion.items():
                if xj == xi or csp.orientacion[xj] == ori_i:
                    continue
                celdas_j = set(posiciones_ocupadas(csp.catalog[xj], vj, csp.orientacion[xj]))
                if celdas_i & celdas_j:
                    tiene_cruce = True
                    break
            if not tiene_cruce:
                return xi
        return None


def prueba_crucigrama(verticales, horizontales, consistencia=1):
    n, m = 6, 6
    csp = CrucigramaCSP(horizontales, verticales, n, m)

    start_time = time.time()
    solution = csps.asignacion_completa(csp, consistencia=consistencia)
    end_time = time.time()

    if solution is not None:
        imprimir_crucigrama(solution, csp)
        print("Número de backtrackings realizados:", csp.backtracking)
    else:
        print("No se encontró solución.")

    print("Tiempo total:", end_time - start_time, "segundos")

def imprimir_crucigrama(asignacion, csp):
    max_row = csp.n
    max_col = csp.m

    filas_totales    = max_row
    columnas_totales = max_col
    matriz = [['.' for _ in range(columnas_totales)] for _ in range(filas_totales)]

    for x, inicio in asignacion.items():
        pal = csp.catalog[x]
        for celda in posiciones_ocupadas(pal, inicio, csp.orientacion[x]):
            matriz[celda[0]][celda[1]] = letra_en_celda(pal, inicio, csp.orientacion[x], celda)

    for fila in matriz:
        print(" ".join(fila))

def leer_palabras(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    palabras_h = leer_palabras('horizontales.txt')
    palabras_v = leer_palabras('verticales.txt')
    prueba_crucigrama(palabras_v, palabras_h)


         
