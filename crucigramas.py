import csps
import time


class Crucigrama(csps.ProblemaCSP):
    """
    CSP para construir un crucigrama a partir de dos listas de palabras.

    Variables: cada palabra identificada por (direccion, texto)
    Dominio: posibles posiciones (fila, columna) de inicio en la cuadricula
    Restricciones: H y V deben cruzarse con letra coincidente,
                   palabras del mismo tipo no pueden traslaparse ni pegarse
    """

    def __init__(self, horizontales, verticales, n, m):
        self.horizontales = horizontales
        self.verticales = verticales
        self.n = n
        self.m = m

        self.X = set()
        for w in horizontales:
            self.X.add(('H', w))
        for w in verticales:
            self.X.add(('V', w))

        self.D = {}
        for w in horizontales:
            self.D[('H', w)] = {
                (r, c)
                for r in range(n)
                for c in range(m - len(w) + 1)
            }
        for w in verticales:
            self.D[('V', w)] = {
                (r, c)
                for r in range(n - len(w) + 1)
                for c in range(m)
            }

        self._reducir_dominios()
        self.N = {var: self.X - {var} for var in self.X}

    def _celdas(self, var, pos):
        dir_, word = var
        r, c = pos
        if dir_ == 'H':
            return {(r, c + i): word[i] for i in range(len(word))}
        else:
            return {(r + i, c): word[i] for i in range(len(word))}

    def _reducir_dominios(self):
        vars_h = [v for v in self.X if v[0] == 'H']
        vars_v = [v for v in self.X if v[0] == 'V']

        cambio = True
        while cambio:
            cambio = False
            for var_h in vars_h:
                antes = len(self.D[var_h])
                validas = set()
                for pos_h in self.D[var_h]:
                    celdas_h = self._celdas(var_h, pos_h)
                    puede_cruzar_todos = True
                    for var_v in vars_v:
                        puede = False
                        for pos_v in self.D[var_v]:
                            celdas_v = self._celdas(var_v, pos_v)
                            for celda in set(celdas_h) & set(celdas_v):
                                if celdas_h[celda] == celdas_v[celda]:
                                    puede = True
                                    break
                            if puede:
                                break
                        if not puede:
                            puede_cruzar_todos = False
                            break
                    if puede_cruzar_todos:
                        validas.add(pos_h)
                self.D[var_h] = validas
                if len(validas) != antes:
                    cambio = True

            for var_v in vars_v:
                antes = len(self.D[var_v])
                validas = set()
                for pos_v in self.D[var_v]:
                    celdas_v = self._celdas(var_v, pos_v)
                    puede_cruzar_todos = True
                    for var_h in vars_h:
                        puede = False
                        for pos_h in self.D[var_h]:
                            celdas_h = self._celdas(var_h, pos_h)
                            for celda in set(celdas_h) & set(celdas_v):
                                if celdas_h[celda] == celdas_v[celda]:
                                    puede = True
                                    break
                            if puede:
                                break
                        if not puede:
                            puede_cruzar_todos = False
                            break
                    if puede_cruzar_todos:
                        validas.add(pos_v)
                self.D[var_v] = validas
                if len(validas) != antes:
                    cambio = True

    def restriccion_binaria(self, xi, vi, xj, vj):
        dir_i, word_i = xi
        dir_j, word_j = xj
        ri, ci = vi
        rj, cj = vj

        celdas_i = self._celdas(xi, vi)
        celdas_j = self._celdas(xj, vj)
        comunes = set(celdas_i.keys()) & set(celdas_j.keys())

        if dir_i == dir_j == 'H':
            if comunes:
                return False
            if ri == rj:
                fin_i = ci + len(word_i)
                fin_j = cj + len(word_j)
                if fin_i == cj or fin_j == ci:
                    return False
            if abs(ri - rj) == 1:
                fin_i = ci + len(word_i) - 1
                fin_j = cj + len(word_j) - 1
                if ci <= fin_j and cj <= fin_i:
                    return False

        elif dir_i == dir_j == 'V':
            if comunes:
                return False
            if ci == cj:
                fin_i = ri + len(word_i)
                fin_j = rj + len(word_j)
                if fin_i == rj or fin_j == ri:
                    return False
            if abs(ci - cj) == 1:
                fin_i = ri + len(word_i) - 1
                fin_j = rj + len(word_j) - 1
                if ri <= fin_j and rj <= fin_i:
                    return False

        else:
            if not comunes:
                return False
            for celda in comunes:
                if celdas_i[celda] != celdas_j[celda]:
                    return False

        return True


def _imprime_cuadricula(asign, csp):
    grid = [['.' for _ in range(csp.m)] for _ in range(csp.n)]
    for var, pos in asign.items():
        for (r, c), letra in csp._celdas(var, pos).items():
            grid[r][c] = letra
    print()
    for fila in grid:
        print(' '.join(fila))
    print()


def prueba_crucigrama(horizontales, verticales, n, m, consistencia=1):
    print(f"Crucigrama {n}x{m} | consistencia={consistencia}")
    print(f"Horizontales: {horizontales}")
    print(f"Verticales:   {verticales}")
    print("-" * 45)
    csp = Crucigrama(horizontales, verticales, n, m)
    for var in csp.X:
        if not csp.D[var]:
            print(f"No hay solucion: dominio vacio para {var[0]}_{var[1]}")
            return
    t0 = time.time()
    asign = csps.asignacion_completa(csp, consistencia=consistencia)
    t = time.time() - t0
    if asign is None:
        print(f"No hay solucion para una cuadricula de {n}x{m}")
    else:
        _imprime_cuadricula(asign, csp)
        for var, pos in sorted(asign.items()):
            print(f"  {var[0]}_{var[1]}: fila={pos[0]}, col={pos[1]}")
        print("\nCruces:")
        for var_h in [v for v in asign if v[0] == 'H']:
            celdas_h = csp._celdas(var_h, asign[var_h])
            cruces = []
            for var_v in [v for v in asign if v[0] == 'V']:
                celdas_v = csp._celdas(var_v, asign[var_v])
                inter = set(celdas_h.keys()) & set(celdas_v.keys())
                if inter:
                    celda = list(inter)[0]
                    cruces.append(f"{var_v[1]}('{celdas_h[celda]}')")
            print(f"  {var_h[1]} cruza con: {', '.join(cruces) if cruces else 'NADIE'}")
    print(f"\nBacktrackings: {csp.backtracking}")
    print(f"Tiempo: {t:.3f}s")


if __name__ == "__main__":
    horizontales = ["GATO", "LUNA"]
    verticales = ["GALA", "ORAL"]
    prueba_crucigrama(horizontales, verticales, n=5, m=5)