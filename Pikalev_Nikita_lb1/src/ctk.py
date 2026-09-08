import customtkinter as ctk
import threading
import time

from lb1 import solve_with_backtracking

class VisualizerApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Визуализация: Покрытие квадратами")
        self.app.geometry("800x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.control_frame = ctk.CTkFrame(self.app)
        self.control_frame.pack(pady=20, padx=20, fill="x")

        self.label_n = ctk.CTkLabel(self.control_frame, text="Размер поля (N):", font=("Arial", 14))
        self.label_n.pack(side="left", padx=10)

        self.entry_n = ctk.CTkEntry(self.control_frame, width=80, font=("Arial", 14))
        self.entry_n.pack(side="left", padx=10)
        self.entry_n.insert(0, "6")

        self.btn_start = ctk.CTkButton(self.control_frame, text="Найти решение", command=self.start_calculation, font=("Arial", 14))
        self.btn_start.pack(side="left", padx=20)

        self.status_label = ctk.CTkLabel(self.app, text="Готов к работе", font=("Arial", 14, "bold"), text_color="gray")
        self.status_label.pack(pady=5)

        self.canvas_frame = ctk.CTkFrame(self.app)
        self.canvas_frame.pack(pady=10, padx=20, expand=True, fill="both")

        self.grid_cells = []
        self.is_calculating = False

        self.colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", 
            "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B500", "#00CED1"
        ]

        self.app.mainloop()

    def create_grid(self, n):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.grid_cells = []

        cell_size = min(50, 600 // n)

        for y in range(n):
            row = []
            for x in range(n):
                cell = ctk.CTkFrame(self.canvas_frame, width=cell_size, height=cell_size, fg_color="#2b2b2b", corner_radius=4)

                cell.grid(row=y, column=x, padx=2, pady=2)

                label = ctk.CTkLabel(cell, text=f"{x+1},{y+1}", font=("Arial", 8), text_color="gray50")
                label.place(relx=0.5, rely=0.5, anchor="center")

                row.append(cell)
            self.grid_cells.append(row)

    def start_calculation(self):
        if self.is_calculating:
            return

        try:
            n = int(self.entry_n.get())
            if n < 2 or n > 15:
                self.status_label.configure(text="Ошибка: N должно быть от 2 до 15", text_color="red")
                return

        except ValueError:
            self.status_label.configure(text="Ошибка: введите целое число!", text_color="red")
            return

        self.is_calculating = True
        self.btn_start.configure(state="disabled", text="Вычисление...")
        self.status_label.configure(text="Алгоритм ищет оптимальное решение...", text_color="yellow")

        self.create_grid(n)

        thread = threading.Thread(target=self.run_algorithm, args=(n,))
        thread.daemon = True
        thread.start()

    def run_algorithm(self, n):
        best_solution, operations = solve_with_backtracking(n)
        self.app.after(0, self.on_calculation_finished, best_solution, operations, n)

    def on_calculation_finished(self, solution, operations, n):
        self.is_calculating = False
        self.btn_start.configure(state="normal", text="Найти решение")

        if not solution:
            self.status_label.configure(text="Решение не найдено", text_color="red")
            return

        self.status_label.configure(text=f"Найдено! Квадратов: {len(solution)}, Операций: {operations}", text_color="green")
        self.animate_solution(solution, n)

    def animate_solution(self, solution, n):
        speed = 0.3

        for idx, (x, y, size) in enumerate(solution):
            gui_x = x - 1
            gui_y = y - 1

            color = self.colors[idx % len(self.colors)]
            square_id = idx + 1

            for dy in range(size):
                for dx in range(size):
                    cell = self.grid_cells[gui_y + dy][gui_x + dx]
                    cell.configure(fg_color=color)

                    for child in cell.winfo_children():
                        child.destroy()

                    lbl = ctk.CTkLabel(cell, text=str(square_id), font=("Arial", 12, "bold"), text_color="white")
                    lbl.place(relx=0.5, rely=0.5, anchor="center")

            self.status_label.configure(text=f"Отрисовка: квадрат {square_id} из {len(solution)} (размер {size}x{size} в {x},{y})")
            self.app.update()
            time.sleep(speed)

        self.status_label.configure(text=f"Визуализация завершена! Всего квадратов: {len(solution)}", text_color="green")

if __name__ == "__main__":
    app = VisualizerApp()