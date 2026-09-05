import random

def generate_matrix(n, symmetric=False):
    matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                if symmetric:
                    if j > i:
                        if random.random() > 0.1:
                            val = random.randint(1, 50)
                            matrix[i][j] = val
                            matrix[j][i] = val
                else:
                    if random.random() > 0.1:
                        matrix[i][j] = random.randint(1, 50)
    
    with open("matrix.txt", "w") as f:
        f.write(str(n) + "\n")
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")
    
    print(f"Матрица {n}x{n} ({'симметричная' if symmetric else 'асимметричная'}) сохранена в matrix.txt")

if __name__ == "__main__":
    n = int(input("Введите количество городов (5-15): "))
    sym = input("Матрица симметричная? (y/n): ").strip().lower() == 'y'
    generate_matrix(n, symmetric=sym)