from collections import deque

def solve():
    T = input("Введите текст: ").strip().upper()
    P = input("Введите шаблон: ").strip().upper()
    wildcard_input = input().strip().upper()

    wildcard_char = wildcard_input[0]
    forbidden_char = wildcard_input[1]

    parts = []
    positions = []
    wildcard_positions = []
    current_part = ""

    print("РАЗБОР ШАБЛОНА НА ЧАСТИ")
    i = 0
    while i < len(P):
        if P[i] == wildcard_char:
            if current_part:
                parts.append(current_part)
                positions.append(i - len(current_part))
                print(f"  Завершена часть '{current_part}' на позиции {i - len(current_part)}")
                current_part = ""
            wildcard_positions.append(i)
            print(f"  Символ джокера '{wildcard_char}' на позиции {i}")
            i += 1
        else:
            current_part += P[i]
            i += 1

    if current_part:
        parts.append(current_part)
        positions.append(len(P) - len(current_part))
        print(f"  Завершена часть '{current_part}' на позиции {len(P) - len(current_part)}")

    print(f"\nИтого частей: {len(parts)}")
    print(f"Позиции диких символов: {wildcard_positions}")

    if not parts and not wildcard_positions:
        print("Шаблон пуст")
        return

    alphabet = sorted(list(set(T + ''.join(parts))))
    char_to_idx = {ch: i for i, ch in enumerate(alphabet)}
    sigma = len(alphabet)

    trie = [[-1] * sigma]
    fail = [0]
    output = [[]]   
    term = [0]   
    node_to_str = [""]  

    print("ПОСТРОЕНИЕ БОРА.")
    for idx, part in enumerate(parts):
        print(f"\nДобавляем часть '{part}' (ID: {idx}):")
        node = 0
        for ch in part:
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
        output[node].append(idx)
        print(f"    Часть '{part}' завершена в вершине '{node_to_str[node]}'")

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

    print("ПОИСК ЧАСТЕЙ В ТЕКСТЕ.")
    found_parts = [[] for _ in range(len(T))]

    node = 0
    for i, ch in enumerate(T):
        c_idx = char_to_idx[ch]
        node = trie[node][c_idx]
        prev_state = node_to_str[node]
        print(f"\nПозиция {i}, символ '{ch}': переход '{prev_state}' -> '{node_to_str[node]}'")

        u = node if output[node] else term[node]

        while u != 0:
            for part_idx in output[u]:
                start_pos_in_pattern = positions[part_idx]
                end_pos_in_text = i
                start_pos_in_text = end_pos_in_text - len(parts[part_idx]) + 1
                pattern_start = start_pos_in_text - start_pos_in_pattern
                print(f"    Найдена часть '{parts[part_idx]}' (ID: {part_idx}) в тексте на позиции {start_pos_in_text}")
                if pattern_start >= 0 and pattern_start + len(P) <= len(T):
                    found_parts[pattern_start].append((part_idx, start_pos_in_text))
                    print(f"      Кандидат на начало шаблона: позиция {pattern_start}")
                else:
                    print(f"      Кандидат {pattern_start} отброшен")
            u = term[u]

    print("ПРОВЕРКА КОНДИДАТОВ")
    results = []
    pattern_len = len(P)

    for pos in range(len(T) - pattern_len + 1):
        print(f"\nКандидат на позицию {pos}:")
        print(f"  Найдено частей в этой позиции: {len(found_parts[pos])} из {len(parts)}")

        if len(found_parts[pos]) == len(parts):
            valid = True
            part_found = [False] * len(parts)

            for part_idx, part_start_in_text in found_parts[pos]:
                expected_start = pos + positions[part_idx]
                print(f"  Часть {part_idx} '{parts[part_idx]}': найдена на {part_start_in_text}, ожидается {expected_start}")
                if part_start_in_text == expected_start:
                    part_found[part_idx] = True
                    print("  Позиция совподает.")
                else:
                    valid = False
                    print("  Позиция не совподает")
                    break

            if not (valid and all(part_found)):
                print(f"    Кандидат {pos} отброшен: не все части на своих местах")
                continue

            wildcard_valid = True
            for w_pos in wildcard_positions:
                text_pos = pos + w_pos
                print(f"  Проверка символа джокера: позиция {text_pos} в тексте = '{T[text_pos]}'")
                if T[text_pos] == forbidden_char:
                    wildcard_valid = False
                    print(f"  Запретный символ - '{forbidden_char}'")
                    break

            if wildcard_valid:
                print(f"    Кандидат {pos} ПРИНЯТ")
                results.append(pos + 1)  

    print("РЕЗУЛЬТАТ.")
    if results:
            for pos in results:
                print(pos)
    else:
        print("(Совпадений не найдено)")

if __name__ == "__main__":
    solve()