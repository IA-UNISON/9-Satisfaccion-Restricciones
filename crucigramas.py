#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csps
import time


class Crucigrama(csps.ProblemaCSP):

    def __init__(self, verticales, horizontales, n=10, m=10):

        self.verticales = verticales
        self.horizontales = horizontales

        self.n = n
        self.m = m

        self.X = set()

        # Variables horizontales
        for i in range(len(horizontales)):
            self.X.add(f"H{i}")

        # Variables verticales
        for i in range(len(verticales)):
            self.X.add(f"V{i}")

        # Dominios
        self.D = {}

        # Horizontales
        for i, palabra in enumerate(horizontales):

            dominio = set()

            for fila in range(n):
                for col in range(m - len(palabra) + 1):
                    dominio.add((fila, col))

            self.D[f"H{i}"] = dominio

        # Verticales
        for i, palabra in enumerate(verticales):

            dominio = set()

            for fila in range(n - len(palabra) + 1):
                for col in range(m):
                    dominio.add((fila, col))

            self.D[f"V{i}"] = dominio

        # Vecinos
        self.N = {}

        for x in self.X:
            self.N[x] = self.X.difference({x})

    def obtener_celdas(self, var, valor):

        fila, col = valor

        if var[0] == "H":

            palabra = self.horizontales[int(var[1:])]

            return [
                (fila, col + i, palabra[i])
                for i in range(len(palabra))
            ]

        else:

            palabra = self.verticales[int(var[1:])]

            return [
                (fila + i, col, palabra[i])
                for i in range(len(palabra))
            ]

    def restriccion_binaria(self, xi, vi, xj, vj):

        celdas_i = self.obtener_celdas(xi, vi)
        celdas_j = self.obtener_celdas(xj, vj)

        for fi, ci, li in celdas_i:
            for fj, cj, lj in celdas_j:

                # Misma celda
                if fi == fj and ci == cj:

                    # Letras distintas -> conflicto
                    if li != lj:
                        return False

        return True


def imprimir_tablero(csp, solucion):

    tablero = [
        ["." for _ in range(csp.m)]
        for _ in range(csp.n)
    ]

    for var, valor in solucion.items():

        fila, col = valor

        if var[0] == "H":

            palabra = csp.horizontales[int(var[1:])]

            for i, letra in enumerate(palabra):
                tablero[fila][col + i] = letra

        else:

            palabra = csp.verticales[int(var[1:])]

            for i, letra in enumerate(palabra):
                tablero[fila + i][col] = letra

    for fila in tablero:
        print(" ".join(fila))


def prueba_crucigrama(verticales, horizontales, consistencia=1):

    problema = Crucigrama(verticales, horizontales)

    print("\n==========================")
    print("CRUCIGRAMA")
    print("==========================")

    t0 = time.time()

    solucion = csps.asignacion_completa(
        problema,
        consistencia=consistencia,
        verbose=False
    )

    tiempo = time.time() - t0

    if solucion is None:

        print("No hay solución.")
        print("Se necesita una retícula más grande.")

    else:

        print("Solución encontrada:\n")

        imprimir_tablero(problema, solucion)

    print("\nBacktrackings:", problema.backtracking)
    print("Tiempo:", round(tiempo, 4), "segundos")


if __name__ == "__main__":

    verticales = [
        "SOL",
        "LUNA",
        "CASA"
    ]

    horizontales = [
        "SILLA",
        "LAGO",
        "MESA"
    ]

    prueba_crucigrama(
        verticales,
        horizontales,
        consistencia=2
    )