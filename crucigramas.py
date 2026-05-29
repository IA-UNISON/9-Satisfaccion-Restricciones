import csps
import time


class Crucigrama(csps.ProblemaCSP):
    def __init__(self, horizontales, verticales, n, m):
        self.X = set(horizontales + verticales)
        self.horizontales = set(horizontales)
        self.verticales = set(verticales)
        self.D = {
    **{palabra: {(fila, col)
        for fila in range(n)
        for col in range(m - len(palabra) + 1)}
       for palabra in horizontales},
    **{palabra: {(fila, col)
        for fila in range(n - len(palabra) + 1)
        for col in range(m)}
    for palabra in verticales}
}
        self.N = {
            palabra: self.X - {palabra}
            for palabra in self.X
        }

    def restriccion_binaria(self, xi, vi, xj, vj):
        if (xi in self.horizontales) == (xj in self.horizontales):
            if xi in self.horizontales:
                if vi[0] == vj[0]:  
                    return not (vi[1] < vj[1] + len(xj) and vj[1] < vi[1] + len(xi))
                return True
            else:
                if vi[1] == vj[1]:  
                    return not (vi[0] < vj[0] + len(xj) and vj[0] < vi[0] + len(xi))
                return True
        
        if xi in self.horizontales:
            fila_h, col_h = vi
            fila_v, col_v = vj
            palabra_h, palabra_v = xi, xj
        else:
            fila_h, col_h = vj
            fila_v, col_v = vi
            palabra_h, palabra_v = xj, xi

        idx_h = col_v - col_h
        idx_v = fila_h - fila_v
        
        if 0 <= idx_h < len(palabra_h) and 0 <= idx_v < len(palabra_v):
            return palabra_h[idx_h] == palabra_v[idx_v]
        return True 
    
def prueba_crucigrama(horizontales, verticales, n, m, consistencia=1):
    
    problema = Crucigrama(horizontales, verticales, n, m)

    print("\n" + "-" * 20 + f"\nPara {horizontales} palabras horizontales y {verticales} palabras verticales")
    print(f"Usando grafo de restricciones con consistencia {consistencia}")
    print("-" * 20)
    
    t0 = time.time()    
    asig = csps.asignacion_completa(problema, consistencia=consistencia, verbose=False)
    t_lapso = time.time() - t0

    print("Se asignaron las siguientes variables:")
    for palabra, pos in asig.items():
        print(f"{palabra}: {pos}")
    print("Se realizaron {} backtrackings".format(problema.backtracking))
    print("Se tardó {:.2f} segundos".format(t_lapso))

if __name__ == "__main__":
    horizontales = ["CARO", "MISA", "TELA", "CARROZA"]
    verticales = ["CASA", "MIRA", "ROSA"]
    prueba_crucigrama(horizontales, verticales, 8, 8)

         
