import numpy as np
import time
import csv

def determinant(matrice):
    return np.linalg.det(matrice)

def cofacteur(matrice, ligne, colonne):
    sous_matrice = np.delete(np.delete(matrice, ligne, axis=0), colonne, axis=1)
    return ((-1) ** (ligne + colonne)) * determinant(sous_matrice)

def matrice_de_cofacteurs(matrice):
    n = len(matrice)
    cofacteurs = np.zeros_like(matrice, dtype=float)

    for i in range(n):
        for j in range(n):
            cofacteurs[i, j] = cofacteur(matrice, i, j)

    return cofacteurs

def adjoint(matrice):
    return matrice_de_cofacteurs(matrice).T

def inverse_par_laplace(matrice):
    det = determinant(matrice)
    
    if det == 0:
        raise ValueError("La matrice n'est pas inversible (déterminant égal à zéro).")

    n = len(matrice)
    matrice_inverse = np.zeros_like(matrice, dtype=float)

    for i in range(n):
        for j in range(n):
            cof = cofacteur(matrice, j, i)
            matrice_inverse[i, j] = cof / det

    return matrice_inverse

tailles_matrices = [2, 3, 10, 15, 20, 100, 200, 300, 500]

nom_fichier_csv = "resultats_laplace.csv"

with open(nom_fichier_csv, mode='w', newline='') as fichier_csv:

    writer = csv.writer(fichier_csv)

    writer.writerow(["Taille de la matrice", "Matrice", "Matrice Inverse", "Temps d'exécution (secondes)"])

    for n in tailles_matrices:
        matrice = np.random.rand(n, n)

        debut = time.time()

        matrice_inverse = inverse_par_laplace(matrice)

        fin = time.time()

        np.savetxt("temp_matrice.txt", matrice, fmt='%.6f', delimiter=',')
        np.savetxt("temp_matrice_inverse.txt", matrice_inverse, fmt='%.6f', delimiter=',')

        with open("temp_matrice.txt", "r") as f_matrice, open("temp_matrice_inverse.txt", "r") as f_inverse:
            matrice_str = f_matrice.read()
            matrice_inverse_str = f_inverse.read()

        writer.writerow([f"{n}x{n}", matrice_str, matrice_inverse_str, f"Temps d'exécution: {fin - debut:.6f} secondes"])

        writer.writerow(["\n\n\n"])
