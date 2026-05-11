def kmp_search(A, B):
    lenA = len(A)

    if lenA != len(B):
        return -1
    
    if lenA == 0:
        return 0
    
    pi = [0] * lenA
    j = 0
    print(f"\nПостроение префикс-функции для {A}\n")

    for i in range(1, lenA):
        print(f"Шаг i={i}: A[{i}]='{A[i]}', A[{j}]='{A[j]}'")
        while j > 0 and B[i] != B[j]:
            j = pi[j - 1]
            print(f"Символы не совпали, идем назад по префикс-функции, новый j={j}")

        if B[i] == B[j]:
            j += 1
            print(f"Символы совпали, идем вперед, новый j={j}")

        pi[i] = j
        print(f"pi[{i}]={j}\n")
    
    j = 0

    for i in range(2 * lenA - 1):
        while j > 0 and A[i % lenA] != B[j]:
            j = pi[j - 1]
            print(f"Идем назад по префикс-функции, новый j={j}")

        if A[i % lenA] != B[j]:
            print(f"A[{i % lenA}]='{A[i % lenA]}' и B[{j}]='{B[j]}' не совпали")

        if A[i % lenA] == B[j]:
            print(f"A[{i % lenA}]='{A[i % lenA]}' и B[{j}]='{B[j]}' совпали")
            j += 1
            print(f"Идем вперед по префикс-функции, новый j={j}\n")

        if j == lenA:
            return i - lenA + 1
        
    return -1


A = input("Первая строка: ")
B = input("Вторая строка: ")

result = kmp_search(A, B)
print(f"Результат: {result}")