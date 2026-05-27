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
        w_i, dir_i = xi
        w_j, dir_j = xj
        r_i, c_i = vi
        r_j, c_j = vj
        L_i = len(w_i)
        L_j = len(w_j)
        
        # Caso A: Misma dirección
        if dir_i == dir_j:
            if dir_i == 'H':
                if r_i == r_j:
                    return c_i + L_i < c_j or c_j + L_j < c_i
                elif abs(r_i - r_j) == 1:
                    return max(c_i, c_j) > min(c_i + L_i - 1, c_j + L_j - 1)
                else:
                    return True
            else:  # dir_i == 'V'
                if c_i == c_j:
                    return r_i + L_i < r_j or r_j + L_j < r_i
                elif abs(c_i - c_j) == 1:
                    return max(r_i, r_j) > min(r_i + L_i - 1, r_j + L_j - 1)
                else:
                    return True
                    
        # Caso B: Direcciones diferentes
        else:
            # Identificar cuál es la horizontal y cuál la vertical
            if dir_i == 'H':
                r_h, c_h, L_h, w_h = r_i, c_i, L_i, w_i
                r_v, c_v, L_v, w_v = r_j, c_j, L_j, w_j
            else:
                r_h, c_h, L_h, w_h = r_j, c_j, L_j, w_j
                r_v, c_v, L_v, w_v = r_i, c_i, L_i, w_i
                
            # ¿Se cruzan?
            se_cruzan = (r_v <= r_h < r_v + L_v) and (c_h <= c_v < c_h + L_h)
            
            if se_cruzan:
                # Comprobar que la letra en el cruce coincida
                return w_h[c_v - c_h] == w_v[r_h - r_v]
            else:
                # Si no se cruzan, comprobar que no se toquen en los bordes (adyacencia ortogonal)
                # 1. La palabra vertical no puede tocar los extremos izquierdo/derecho de la horizontal
                if (r_v <= r_h < r_v + L_v) and (c_v == c_h - 1 or c_v == c_h + L_h):
                    return False
                # 2. La palabra horizontal no puede tocar los extremos superior/inferior de la vertical
                if (c_h <= c_v < c_h + L_h) and (r_h == r_v - 1 or r_h == r_v + L_v):
                    return False
                return True
    
def prueba_crucigrama(verticales, horizontales, consistencia=1):
    
    # TODO: Probar el CSP del crucigrama con el grafo de restricciones con consistencia dada y medir el tiempo que tarda en resolverlo. Imprimir la asignación resultante, el número de backtrackings realizados y el tiempo que tardó en resolverlo.
    
    raise NotImplementedError("Completa la función prueba_crucigrama para probar tu implementación del CSP del crucigrama")

if __name__ == "__main__":
    
    prueba_crucigrama(...) # TODO: definir los crucigramas a probar

         
