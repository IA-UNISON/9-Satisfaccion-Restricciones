import csps
import time
import os

__author__ = 'Daniel Eduardo Alvarez Terrazas'

class Crucigrama(csps.ProblemaCSP):
    def __init__(self, verticales, horizontales, n, m):
        self.n = n
        self.m = m
        self.horizontales = horizontales
        self.verticales = verticales
        
        # Variables: cada palabra es una variable con prefijo H_ o V_
        self.X = set(['H_' + w for w in horizontales] + ['V_' + w for w in verticales])
        
        # Dominios: posiciones donde puede empezar cada palabra
        self.D = {}
        for w in horizontales:
            L = len(w)
            self.D['H_' + w] = {(r, c) for r in range(n) for c in range(m - L + 1)}
            
        for w in verticales:
            L = len(w)
            self.D['V_' + w] = {(r, c) for r in range(n - L + 1) for c in range(m)}
            
        # Vecinos: todas las palabras son vecinas entre si
        self.N = {x: self.X.difference({x}) for x in self.X}
        
        self.backtracking = 0

    def restriccion_binaria(self, xi, vi, xj, vj):
        
        def get_cells(var, pos):
            word = var[2:] 
            r, c = pos
            if var.startswith('H'):
                return {(r, c + k): word[k] for k in range(len(word))}
            else:
                return {(r + k, c): word[k] for k in range(len(word))}
        
        cells_i = get_cells(xi, vi)
        cells_j = get_cells(xj, vj)
        
        for pos_i, char_i in cells_i.items():
            for pos_j, char_j in cells_j.items():
                if pos_i == pos_j:
                    # si se cruzan, deben tener la misma letra
                    if char_i != char_j:
                        return False
                else:
                    # no pueden estar pegadas ortogonalmente
                    dr = abs(pos_i[0] - pos_j[0])
                    dc = abs(pos_i[1] - pos_j[1])
                    if dr + dc == 1: 
                        return False
        
        return True

def prueba_crucigrama(verticales, horizontales, n, m, consistencia=1):
    print("\n" + "="*50)
    print(f"Crucigrama en cuadricula {n}x{m}")
    print(f"Consistencia: {consistencia}")
    print("="*50)
    
    print("\nPalabras a colocar:")
    print(f"  Horizontales: {', '.join(horizontales)}")
    print(f"  Verticales:   {', '.join(verticales)}")
    
    problema = Crucigrama(verticales, horizontales, n, m)
    t0 = time.time()
    asignacion = csps.asignacion_completa(problema, consistencia=consistencia, verbose=False)
    t_lapso = time.time() - t0
    
    if asignacion is None:
        print("\nNo se encontro solucion.")
        print("El tablero puede ser muy pequeno o las palabras no combinan bien.")
    else:
        
        grid = [[' ' for _ in range(m)] for _ in range(n)]
        
        for var, pos in asignacion.items():
            word = var[2:]
            r, c = pos
            if var.startswith('H'):
                for k in range(len(word)):
                    grid[r][c + k] = word[k]
            else:
                for k in range(len(word)):
                    grid[r + k][c] = word[k]
        
        print("\nSolucion:")
        print("+" + "---+" * m)
        for row in grid:
            line = "|"
            for char in row:
                if char == ' ':
                    line += "   |"
                else:
                    line += f" {char} |"
            print(line)
            print("+" + "---+" * m)
            
    print(f"\nBacktrackings: {problema.backtracking}")
    print(f"Tiempo: {t_lapso:.4f} segundos")

def cargar_palabras(archivo):
    """lee palabras de un archivo de texto."""
    if not os.path.exists(archivo):
        raise FileNotFoundError(f"No se encuentra el archivo: {archivo}")
    
    with open(archivo, 'r', encoding='utf-8') as f:
        palabras = [linea.strip().upper() for linea in f if linea.strip()]
    return palabras

if __name__ == "__main__":
    
    horizontales = cargar_palabras("horizontales.txt")
    verticales = cargar_palabras("verticales.txt")
    
    prueba_crucigrama(verticales, horizontales, 15, 15, consistencia=1)

    prueba_crucigrama(verticales, horizontales, 15, 15, consistencia=2)
