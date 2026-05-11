def kmp_search(P, T):
    lenP = len(P)
    Pi = [0] * lenP
    j = 0
    print(f"\nЗначения префикс-функции для {P}\n")

    for i in range(1, lenP):
        while j > 0 and P[i] != P[j]:
            j = Pi[j - 1]
        
        if P[i] == P[j]:
            j += 1
        
        Pi[i] = j

    lenT = len(T)
    result = []
    j = 0

    for i in range(lenT):
        print(f"Символы: t[{i}] = {T[i]} и p[{j}] = {P[j]}")

        while j > 0 and T[i] != P[j]:
            print(f"Символы не совпали, идем назад по префикс-функции, новый j: {Pi[j - 1]}")
            j = Pi[j-1]

        if T[i] == P[j]:
            print(f"Символы совпали: {T[i]} и {P[j]}")
            j += 1
            print(f"Идем вперед, новый j: {j}")

        else:
            print(f"Символы не совпали: {T[i]} и {P[j]}")
        
        if j == lenP:
            pos = i - lenP + 1
            print(f"Найдена полная подстрока {P} на индексе {pos}")
            result.append(str(pos))
            j = Pi[j - 1]
            print(f"Идем назад по префикс-функции, новый j: {j}\n")
        
    return result


P = input("Первая строка: ")
T = input("Вторая строка: ")

result = kmp_search(P, T)

if result:
    print(f"Результат: {','.join(map(str, result))}")

else:
    print(f"Результата нет: {-1}")