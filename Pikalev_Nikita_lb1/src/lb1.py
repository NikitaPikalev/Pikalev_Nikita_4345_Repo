def solve_with_backtracking(N):
    grid = [[0] * N for _ in range(N)]

    best_solution = None
    operations_counter = [0]
    best_count = float('inf')

    def can_place(x, y, size):
        if x + size > N or y + size > N:
            return False
        
        for i in range(size):
            for j in range(size):
                if grid[y + i][x + j] != 0:
                    return False
        return True
    
    def place_square(x, y, size, square_id):
        print(f"Размещаем в клетке {x, y} квадрат размером {size}")
        for i in range(size):
            for j in range(size):
                grid[y + i][x + j] = square_id
        operations_counter[0] += 1
    
    def remove_square(x, y, size):
        print(f"Удаляем из клетки {x, y} квадрат размером {size}")
        for i in range(size):
            for j in range(size):
                grid[y + i][x + j] = 0
        operations_counter[0] += 1

    def find_empty_cell():
        for y in range(N):
            for x in range(N):
                if grid[y][x] == 0:
                    return(x, y)
        return None
    
    def get_max_possible_size(x, y):
        if grid[y][x] != 0:
            return 0
        
        max_size = 1
        while (x + max_size <= N and y + max_size <= N):
            can_expand = True

            for i in range(max_size):
                if grid[y + max_size - 1][x + i] != 0:
                    can_expand = False
                    break
                if grid[y + i][x + max_size - 1] != 0:
                    can_expand = False
                    break
            
            if not can_expand:
                break

            max_size += 1

        return max_size - 1
    
    def backtrack(squares):
        nonlocal best_solution, best_count

        if N % 2 == 0:
            if can_place(0, 0, N//2):
                size = N//2

                place_square(0, 0, size, 1)
                squares.append((1, 1, size))
                print(f"Размещаем в клетке {1, 1} квадрат размером {size}")

                place_square(N//2, 0, size, 2)
                squares.append((N//2+1, 1, size))
                print(f"Размещаем в клетке {N//2+1, 1} квадрат размером {size}")

                place_square(0, N//2, size, 3)
                squares.append((1, N//2+1, size))
                print(f"Размещаем в клетке {1, N//2+1} квадрат размером {size}")

                place_square(N//2, N//2, size, 4)
                squares.append((N//2+1, N//2+1, size))
                print(f"Размещаем в клетке {N//2+1, N//2+1} квадрат размером {size}")

        if N % 2 == 1 and N > 1 and N != 9 and N != 15:
            if can_place(0, 0, N//2 + 1):
                big_size = N//2 + 1
                small_size = N//2
                
                place_square(0, 0, big_size, 1)
                squares.append((1, 1, big_size))
                print(f"Размещаем в клетке {1, 1} квадрат размером {big_size}")

                place_square(0, big_size, small_size, 2)
                squares.append((1, big_size+1, small_size))
                print(f"Размещаем в клетке {1, big_size+1} квадрат размером {big_size}")

                place_square(big_size, 0, small_size, 3)
                squares.append((big_size+1, 1, small_size))
                print(f"Размещаем в клетке {big_size+1, 1} квадрат размером {big_size}")

        if N == 9 or N == 15:
            if can_place(0, 0, N//2 + 1):
                small_size = N//3
                big_size = small_size * 2

                place_square(0, 0, big_size, 1)
                squares.append((1, 1, big_size))
                print(f"Размещаем в клетке {1, 1} квадрат размером {big_size}")

                place_square(0, big_size, small_size, 2)
                squares.append((1, big_size+1, small_size))
                print(f"Размещаем в клетке {1, big_size+1} квадрат размером {big_size}")

                place_square(big_size, 0, small_size, 3)
                squares.append((big_size+1, 1, small_size))
                print(f"Размещаем в клетке {big_size+1, 1} квадрат размером {big_size}")

        empty = find_empty_cell()

        if empty is None:
            if len(squares) < best_count:
                best_count = len(squares)
                best_solution = squares.copy()
            return
        
        x, y = empty

        if len(squares) >= best_count:
            return
        
        max_size = get_max_possible_size(x, y)
        max_size = min(max_size, N - 1)

        print(f"Количество элементов: {len(squares)}")

        for size in range(max_size, 0, -1):
            if can_place(x, y, size):
                square_id = len(squares) + 1
                place_square(x, y, size, square_id)
                squares.append((x + 1, y + 1, size))

                backtrack(squares)

                squares.pop()
                remove_square(x, y, size)
    
    backtrack([])
    return best_solution, operations_counter[0]

if __name__ == "__main__":
    N = int(input())

    squares, count_operations = solve_with_backtracking(N)

    if squares:
        print(len(squares))
        for x, y, size in squares:
            print(x, y, size)
        print(f"Количество операций: {count_operations}")
    else:
        print("Решение не найдено")