import csps
import time

class Crucigrama(csps.ProblemaCSP):
    def __init__(self, pos_ini):

        verticales = pos_ini["verticales"]
        horizontales = pos_ini["horizontales"]
        n = pos_ini["filas"]
        m = pos_ini["columnas"]

        self.X = set()

        for w in horizontales:
            self.X.add((w,"H"))
        for w in verticales:
            self.X.add((w,"V"))

        self.D={}

        for var in self.X:
            w, direccion=var
            L=len(w)
            dominio = set()

            if direccion == "H":
                if L <=m:
                    dominio ={
                        (r,c)
                        for r in range(n)
                        for c in range(m-L+1)
                    }

            elif direccion == "V":
                if L <= n:
                    dominio ={
                        (r,c)
                        for r in range(n-L+1)
                        for c in range(m)
                    }

            self.D[var] = dominio

        self.N={
            x: self.X.difference({x})
            for x in self.X
        }

    def casillas_ocupadas(self, palabra, direccion, fila, columna):
        casillas =[]
        for i in range(len(palabra)):
            if direccion =="H":
                casillas.append((fila, columna + i, palabra[i]))
            else:
                casillas.append((fila + i, columna, palabra[i]))
        return casillas
    
    def restriccion_binaria(self, xi, vi, xj, vj):
        palabra1, dir1 = xi
        palabra2, dir2 = xj
        fila1,col1 = vi
        fila2,col2 = vj
        casillas1 = {}
        casillas2 = {}

        for i, letra in enumerate(palabra1):
            if dir1 == "H":
                casillas1[(fila1, col1 + i)] = letra
            else:
                casillas1[(fila1 + i, col1)] = letra

        for i, letra in enumerate(palabra2):
            if dir2 == "H":
                casillas2[(fila2, col2 + i)] = letra
            else:
                casillas2[(fila2 + i, col2)] = letra

        comunes = set(casillas1.keys()) & set(casillas2.keys())
        
        if dir1 == dir2:
            return len(comunes) == 0
        
        if len(comunes) == 0:
            return True
        
        for pos in comunes:
            if casillas1[pos] != casillas2[pos]:
                return False
            
        return True
    
    def esta_conectado(self, asig):
        cruces ={var: 0 for var in asig}
        for xi, vi in asig.items():
            for xj, vj in asig.items():
                if xi == xj:
                    continue
                palabra1, dir1 = xi
                palabra2, dir2 = xj

                if dir1 == dir2:
                    continue

                fila1,col1=vi
                fila2,col2=vj

                for i, letra1 in enumerate(palabra1):
                    if dir1 == "H":
                        pos1 = (fila1, col1 + i)
                    else:
                        pos1 = (fila1 + i, col1)

                    for j, letra2 in enumerate(palabra2):
                        if dir2 == "H":
                            pos2 = (fila2, col2 + j)
                        else:
                            pos2 = (fila2 + j, col2)

                        if pos1 == pos2:
                            cruces[xi] += 1
                            cruces[xj] += 1
        return all(cruces[var] > 0 for var in cruces)
               

def imprimir_crucigrama(solucion, filas, columnas):
    tablero = [["." for _ in range(columnas)] for _ in range(filas)]

    for variable, posicion in solucion.items():
        palabra, direccion = variable
        fila, columna = posicion

        for i, letra in enumerate(palabra):
            if direccion == "H":
                tablero[fila][columna + i] = letra.lower()
            else:
                tablero[fila + i][columna] = letra.lower()
    for fila in tablero:
        print(" ".join(fila))


def prueba_crucigrama(consistencia=1):
    with open("vertical.txt", "r", encoding="utf-8") as f:
        verticales = [line.strip() for line in f if line.strip()]

    with open("horizontal.txt", "r", encoding="utf-8") as f:
        horizontales = [line.strip() for line in f if line.strip()]

    for filas, columnas in [(10,10), (15,15),(20,20)]:
        print("\n"+"="*60)
        print(f"Prueba: Crucigrama de {filas}x{columnas}")
        print("="*60)
        pos_ini = {
            "filas": filas,
            "columnas": columnas,
            "verticales": verticales,
            "horizontales": horizontales
        }

        programa = Crucigrama(pos_ini)
        t0 = time.time()
        asig =csps.asignacion_completa(programa, consistencia=consistencia)
        t_lapso=time.time() - t0

        if asig is None:
            print("No se puede colocar el crucigrama")
        else:
            print("Solución encontrada:")
            print(f"Tiempo: {t_lapso:.4f} segundos")
            print(f"Backtrackings: {programa.backtracking}")
            print("Crucigrama:")
            imprimir_crucigrama(asig, filas, columnas)

        

if __name__ == "__main__":
    
    prueba_crucigrama(consistencia=1) 
