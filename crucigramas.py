import csps
import time


import os

class Crucigrama(csps.ProblemaCSP):
    def __init__(self, pos_ini):
        # pos_ini puede ser (n, m) o (n, m, archivo_v, archivo_h)
        if len(pos_ini) == 4:
            n, m, archivo_v, archivo_h = pos_ini
        else:
            n, m = pos_ini
            archivo_v = 'verticales.txt'
            archivo_h = 'horizontales.txt'
            
        self.n = n
        self.m = m
        
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        # Cargar horizontales
        horizontales = []
        for path in [archivo_h, os.path.join(dir_path, archivo_h)]:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    horizontales = [line.strip() for line in f if line.strip()]
                break
            except (FileNotFoundError, OSError):
                continue
                
        # Cargar verticales
        verticales = []
        for path in [archivo_v, os.path.join(dir_path, archivo_v)]:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    verticales = [line.strip() for line in f if line.strip()]
                break
            except (FileNotFoundError, OSError):
                continue
            
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
                
def esta_conectado(asignacion):
    """
    Verifica si todas las palabras colocadas en la asignación forman un único
    componente conectado a través de sus intersecciones.
    """
    if not asignacion:
        return True
        
    # Construir el grafo de intersecciones
    adj = {var: [] for var in asignacion}
    vars_list = list(asignacion.keys())
    n_vars = len(vars_list)
    
    for i in range(n_vars):
        var_i = vars_list[i]
        w_i, dir_i = var_i
        r_i, c_i = asignacion[var_i]
        L_i = len(w_i)
        
        for j in range(i + 1, n_vars):
            var_j = vars_list[j]
            w_j, dir_j = var_j
            r_j, c_j = asignacion[var_j]
            L_j = len(w_j)
            
            # Solo se cruzan si tienen direcciones opuestas
            if dir_i != dir_j:
                if dir_i == 'H':
                    r_h, c_h, L_h = r_i, c_i, L_i
                    r_v, c_v, L_v = r_j, c_j, L_j
                else:
                    r_h, c_h, L_h = r_j, c_j, L_j
                    r_v, c_v, L_v = r_i, c_i, L_i
                    
                # Verificar si hay cruce
                if (r_v <= r_h < r_v + L_v) and (c_h <= c_v < c_h + L_h):
                    adj[var_i].append(var_j)
                    adj[var_j].append(var_i)
                    
    # Hacer BFS/DFS desde la primera variable asignada
    from collections import deque
    visitados = set()
    start_var = vars_list[0]
    
    queue = deque([start_var])
    visitados.add(start_var)
    
    while queue:
        curr = queue.popleft()
        for vecino in adj[curr]:
            if vecino not in visitados:
                visitados.add(vecino)
                queue.append(vecino)
                
    # Si visitamos todas las variables de la asignación, está conectado
    return len(visitados) == n_vars
    
def prueba_crucigrama(verticales, horizontales, consistencia=1, n=15, m=15, max_intentos=100):
    import random
    
    # 1. Instanciar el problema
    problema = Crucigrama((n, m, verticales, horizontales))
    
    # Comprobar si hay variables a colocar
    if not problema.X:
        print("No hay palabras para generar el crucigrama.")
        return None
        
    # Guardar el ordena_valores original de csps
    original_ordena_valores = csps.ordena_valores
    
    # Definir el wrapper para barajar los dominios (domain shuffling)
    def ordena_valores_shuffled(csp, asg, x_i):
        def conflictos(v_i):
            return sum(
                csp.restriccion_binaria(x_i, v_i, x_j, v_j)
                for x_j in csp.N[x_i] if x_j not in asg
                for v_j in csp.D[x_j]
            )
        valores = list(csp.D[x_i])
        random.shuffle(valores)
        return sorted(valores, key=conflictos, reverse=True)
        
    # Reemplazar la función en csps por nuestra versión aleatorizada
    csps.ordena_valores = ordena_valores_shuffled
    
    t0 = time.time()
    asignacion = None
    intentos = 0
    
    # Guardar los dominios originales para poder restaurarlos en cada intento
    original_D = {var: set(dom) for var, dom in problema.D.items()}
    
    while intentos < max_intentos:
        intentos += 1
        
        # Restaurar dominios iniciales
        problema.D = {var: set(dom) for var, dom in original_D.items()}
        
        # Ejecutar la búsqueda CSP
        asignacion = csps.asignacion_completa(problema, consistencia=consistencia, verbose=False)
        
        if asignacion is None:
            # Si el resolvedor determina que no hay solución matemática alguna, no sirve de nada reintentar
            print(f"No hay solución posible en una retícula de {n}x{m} con consistencia {consistencia}.")
            csps.ordena_valores = original_ordena_valores
            return None
            
        # Comprobar si la solución está completamente conectada
        if esta_conectado(asignacion):
            t_lapso = time.time() - t0
            print(f"\n¡Solución conectada encontrada en el intento {intentos}!")
            print(f"Tiempo: {t_lapso:.4f} segundos")
            print(f"Backtrackings en el intento exitoso: {problema.backtracking}")
            
            # Restaurar ordena_valores al original antes de salir
            csps.ordena_valores = original_ordena_valores
            return asignacion
            
    print(f"\nSe alcanzó el límite de {max_intentos} intentos sin encontrar una solución conectada.")
    # Restaurar ordena_valores al original antes de salir
    csps.ordena_valores = original_ordena_valores
    return None

if __name__ == "__main__":
    
    prueba_crucigrama(...) # TODO: definir los crucigramas a probar

         
