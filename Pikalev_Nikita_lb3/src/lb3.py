cost_replace, cost_insert, cost_delete, cost_insert2 = map(int, input("Стоимость операций: ").split())

S = input("Первая строка: ").strip()
T = input("Вторая строка: ").strip()

lenS, lenT = len(S), len(T)

prev = [j * cost_insert for j in range(lenT + 1)]

for i in range(1, lenS + 1):
    curr = [i * cost_delete] + [0] * lenT

    for j in range(1, lenT + 1):
        print(f"Символ из первой строки: {S[i-1]}")
        print(f"Символ из второй строки: {T[j-1]}")

        if S[i-1] == T[j-1]:
            print(f"Символы совпадают.")
            curr[j] = prev[j-1]
        
        else:
            replace_val = prev[j-1] + cost_replace
            delete_val = prev[j] + cost_delete
            insert_val = curr[j-1] + cost_insert
            insert2_val = float('inf')

            print(f"Символы не совпадают.")
            print(f"Стоимость замены: {replace_val}")
            print(f"Стоимость удаления: {delete_val}")
            print(f"Стоимость вставки: {insert_val}")

            if j >= 2 and T[j-2] == T[j-1]:
                insert2_val = curr[j-2] + cost_insert2
                print(f"Стоимость двойной вставки: {insert2_val}")
            
            else:
                print(f"Двойная вставка невозможна")

            curr[j] = min(replace_val, delete_val, insert_val, insert2_val)
            print(f"Минимальная стоимость: {curr[j]}")
  
        print(f"Текущая строка: {curr}\n")

    prev = curr

print(f"Расстояние Левенштейна: {prev[lenT]}")

