from collections import deque

def solve():
    T = input("Введите текст: ").strip().upper()
    n = int(input("Введите число шаблонов: ").strip())
    patterns = [input().strip().upper() for _ in range(n)]

    alphabet = sorted(list(set(T + ''.join(patterns))))
    char_to_idx = {ch: i for i, ch in enumerate(alphabet)}
    sigma = len(alphabet)

    trie = [[-1] * sigma]
    fail = [0]
    output = [[]]   
    term = [0]  
    node_to_str = [""]   

    print("ПОСТРОЕНИЕ БОРА.")
    for idx, pat in enumerate(patterns):
        print(f"\nДобавляем шаблон '{pat}' (ID: {idx + 1}):")
        node = 0
        for ch in pat:
            c_idx = char_to_idx[ch]
            curr_path = node_to_str[node]
            if trie[node][c_idx] == -1:
                trie[node][c_idx] = len(trie)
                trie.append([-1] * sigma)
                fail.append(0)
                output.append([])
                term.append(0)
                node_to_str.append(curr_path + ch)
                print(f"  Создана вершина: '{curr_path}' --[{ch}]--> '{node_to_str[-1]}'")
            else:
                print(f"  Переход по существующей вершине: '{curr_path}' --[{ch}]--> '{node_to_str[trie[node][c_idx]]}'")
            node = trie[node][c_idx]
        output[node].append(idx + 1)
        print(f"    Шаблон '{pat}' завершён в вершине '{node_to_str[node]}'")

    q = deque()

    print("ПОСТРОЕНИЕ СУФФИКСНЫХ И КОНЕЧНЫХ ССЫЛОК.")
    for c_idx in range(sigma):
        if trie[0][c_idx] != -1:
            s = trie[0][c_idx]
            fail[s] = 0
            term[s] = 0
            q.append(s)
            print(f"  Суффиксная ссылка: '{node_to_str[s]}' -> '' (прямой ребёнок корня)")
        else:
            trie[0][c_idx] = 0

    while q:
        v = q.popleft()
        for c_idx in range(sigma):
            u = trie[v][c_idx]
            if u != -1:
                fail[u] = trie[fail[v]][c_idx]
                print(f"\n  Обработка вершины '{node_to_str[u]}':")
                print(f"    Суффиксная ссылка: '{node_to_str[u]}' -> '{node_to_str[fail[u]]}'")
                
                if output[fail[u]]:
                    term[u] = fail[u]
                    print(f"    Конечная ссылка: '{node_to_str[u]}' -> '{node_to_str[term[u]]}'")
                else:
                    term[u] = term[fail[u]]
                    if term[u] == 0:
                        print(f"    Конечная ссылка: '{node_to_str[u]}' -> ''")
                    else:
                        print(f"    Конечная ссылка: '{node_to_str[u]}' -> '{node_to_str[term[u]]}' (унаследована)")
                
                q.append(u)
            else:
                trie[v][c_idx] = trie[fail[v]][c_idx]

    results = []
    node = 0

    print("ПОИСК В ТЕКСТЕ.")
    for i, ch in enumerate(T):
        c_idx = char_to_idx[ch]
        prev_state = node_to_str[node]
        node = trie[node][c_idx]
        print(f"\nПозиция {i + 1}, символ '{ch}': переход '{prev_state}' -> '{node_to_str[node]}'")

        u = node if output[node] else term[node]
        
        while u != 0:
            for pat_idx in output[u]:
                pos = i + 2 - len(patterns[pat_idx - 1])
                print(f"    Найден шаблон '{patterns[pat_idx - 1]}' (ID: {pat_idx}) в позиции {pos}")
                results.append((pos, pat_idx))
            u = term[u]

    results.sort()

    print("РЕЗУЛЬТАТ.")
    if results:
        for pos, pat_idx in results:
            print(f"{pos} {pat_idx}")
    else:
        print("(Вхождения отсутствуют)")

if __name__ == "__main__":
    solve()