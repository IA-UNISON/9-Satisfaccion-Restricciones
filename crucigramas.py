import csps
import time


import os

class Crucigrama(csps.ProblemaCSP):
    def __init__(self, pos_ini):
        # pos_ini es una tupla (n, m) que define el tamaño de la retícula
        n, m = pos_ini
        self.n = n
        self.m = m
        
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        try:
            with open(os.path.join(dir_path, 'horizontales.txt'), 'r', encoding='utf-8') as f:
                horizontales = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            horizontales = []
            
        try:
            with open(os.path.join(dir_path, 'verticales.txt'), 'r', encoding='utf-8') as f:
                verticales = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            verticales = []
            
        # Variables (X): tuplas (palabra, direccion)
        self.X = set()
        for w in horizontales:
            self.X.add((w, 'H'))
        for w in verticales:
            self.X.add((w, 'V'))
            
        # Dominios (D): posiciones iniciales (r, c) válidas en la retícula
        self.D = {}
        for var in self.X:
            w, direccion = var
            L = len(w)
            dom = set()
            if direccion == 'H':
                if L <= m:
                    dom = {(r, c) for r in range(n) for c in range(m - L + 1)}
            elif direccion == 'V':
                if L <= n:
                    dom = {(r, c) for r in range(n - L + 1) for c in range(m)}
            self.D[var] = dom
            
        # Vecinos (N): grafo completo (cada palabra se restringe con todas las demás)
        self.N = {x: self.X.difference({x}) for x in self.X}

    def restriccion_binaria(self, xi, vi, xj, vj):
        # TODO: definir la función de restricción binaria entre las variables xi y xj
        pass
    
def prueba_crucigrama(verticales, horizontales, consistencia=1):
    
    # TODO: Probar el CSP del crucigrama con el grafo de restricciones con consistencia dada y medir el tiempo que tarda en resolverlo. Imprimir la asignación resultante, el número de backtrackings realizados y el tiempo que tardó en resolverlo.
    
    raise NotImplementedError("Completa la función prueba_crucigrama para probar tu implementación del CSP del crucigrama")

if __name__ == "__main__":
    
    prueba_crucigrama(...) # TODO: definir los crucigramas a probar

         
