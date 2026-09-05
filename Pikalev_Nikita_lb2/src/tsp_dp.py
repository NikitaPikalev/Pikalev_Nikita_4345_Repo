def solve_tsp_dp(n, graph):
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    
    dp[1][0] = 0

    print("Итеративное заполнение таблицы ДП:")
    for mask in range(1, 1 << n):
        bin_mask = bin(mask)[2:].zfill(n)
        print(f"\nОбработка маски {bin_mask} (десятичное значение: {mask}):")
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            print(f"  Город {u} достижим, стоимость пути: {dp[mask][u]}")
            for v in range(n):
                if not (mask & (1 << v)) and graph[u][v] > 0:
                    new_mask = mask | (1 << v)
                    new_mask_bin = bin(new_mask)[2:].zfill(n)
                    new_cost = dp[mask][u] + graph[u][v]
                    print(f"    Проверяем переход {u} -> {v} (ребро: {graph[u][v]})")
                    if new_cost < dp[new_mask][v]:
                        print(f"      Обновляем dp[маска={new_mask_bin}][город={v}]: {dp[new_mask][v]} -> {new_cost} через город {u}")
                        dp[new_mask][v] = new_cost
                        parent[new_mask][v] = u
                    else:
                        print(f"      Переход невыгоден (текущая стоимость {dp[new_mask][v]} <= {new_cost})")
                        
    
    full_mask = (1 << n) - 1
    min_cost = INF
    last_city = -1

    print("\nПроверка возврата в стартовый город 0:")
    for u in range(1, n):
        if graph[u][0] > 0 and dp[full_mask][u] != INF:
            cost = dp[full_mask][u] + graph[u][0]
            print(f"  Путь через город {u} -> 0: стоимость {dp[full_mask][u]} + {graph[u][0]} = {cost}")
            if cost < min_cost:
                min_cost = cost
                last_city = u
    
    if min_cost == INF:
        return None, None

    print("\nВосстановление оптимального пути:")
    path = []
    mask = full_mask
    city = last_city
    
    while city != 0:
        path.append(city)
        print(f"  Добавляем город {city} (маска {bin(mask)[2:].zfill(n)})")
        prev_city = parent[mask][city]
        mask = mask ^ (1 << city)
        city = prev_city
    
    path.reverse()
    path = [0] + path + [0]
    
    return min_cost, path


def main():
    graph = []
    with open("matrix.txt", "r") as f:
        lines = f.readlines()
        n = int(lines[0].strip())
        for i in range(1, n + 1):
            graph.append(list(map(int, lines[i].strip().split())))
    
    result, path = solve_tsp_dp(n, graph)

    print("\nРезультат:")
    if result is None:
        print("no path")
    else:
        print(result)
        print(' '.join(map(str, path)))


if __name__ == "__main__":
    main()