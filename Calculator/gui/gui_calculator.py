import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sys

from math_engine.rpn import infix_to_rpn, rpn
from math_engine.equations import solve_equation, solve_system
from .help_text import help_content


# ------------------- Funkcje GUI -------------------

def evaluate_expression():
    expr = entry_calc.get()
    try:
        expr_rpn = infix_to_rpn(expr)
        result = rpn(expr_rpn)
        result_label_calc.config(text=f"Wynik: {result:.3f}")
    except Exception as e:
        messagebox.showerror("Błąd", str(e))


def plot_expression():
    expr = entry_plot.get().strip()
    if not expr:
        messagebox.showinfo("Info", "Wpisz wyrażenie w polu funkcji (np. sin(x)).")
        return

    try:
        expr_rpn = infix_to_rpn(expr)
        xs = np.linspace(-10, 10, 400)
        ys = []
        for x in xs:
            try:
                ys.append(rpn(expr_rpn, x_val=x))
            except Exception:
                ys.append(float('nan'))

        ax.clear()
        ax.set_facecolor('black')
        ax.spines['left'].set_color('#00bfff')
        ax.spines['bottom'].set_color('#00bfff')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.tick_params(axis='x', colors='#00bfff')
        ax.tick_params(axis='y', colors='#00bfff')
        ax.grid(True, linestyle='--', alpha=0.3, color='#555555')

        ax.plot(xs, ys, color='#00bfff', label=expr, linewidth=2)

        leg = ax.legend(frameon=True)
        if leg is not None:
            leg.get_frame().set_facecolor('black')
            leg.get_frame().set_edgecolor('#00bfff')
            for text in leg.get_texts():
                text.set_color('#00bfff')

        canvas.draw_idle()
    except Exception as e:
        messagebox.showerror("Błąd podczas rysowania", str(e))


def clear_plot():
    ax.clear()
    ax.set_facecolor('black')
    ax.spines['left'].set_color('#00bfff')
    ax.spines['bottom'].set_color('#00bfff')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.tick_params(axis='x', colors='#00bfff')
    ax.tick_params(axis='y', colors='#00bfff')
    ax.grid(True, linestyle='--', alpha=0.3, color='#555555')
    canvas.draw_idle()


def solve_single_equation():
    expr = entry_eq.get()
    if "=" not in expr:
        messagebox.showerror("Błąd", "Równanie musi zawierać znak =")
        return
    try:
        roots = solve_equation(expr)
        if roots == "tożsamość":
            result_label_eq.config(text="Rozwiązanie: nieskończoność (tożsamość)")
        elif roots:
            if isinstance(roots, (list, tuple)):
                roots = [round(r, 3) for r in roots]
            elif isinstance(roots, (int, float)):
                roots = round(roots, 3)
            result_label_eq.config(text=f"Rozwiązania: {roots}")
        else:
            result_label_eq.config(text="Brak rozwiązań w przedziale [-50,50]")
    except Exception as e:
        messagebox.showerror("Błąd", str(e))


def solve_system_equations():
    equations = system_text.get("1.0", "end").strip().split("\n")
    variables = [var.strip() for var in variables_entry.get().split(",")]
    try:
        sol = solve_system(equations, variables)
        if isinstance(sol, dict):
            sol = {k: round(v, 3) for k, v in sol.items()}
        result_label_system.config(text=f"Rozwiązanie: {sol}")
    except Exception as e:
        messagebox.showerror("Błąd", str(e))


# ------------------- GUI główne -------------------

window = tk.Tk()
window.title("MathEW (Extended Workspace) 1.0 Alpha")
window.configure(bg='black')

style = ttk.Style(window)
style.theme_use('default')
style.configure('TNotebook', background='black', borderwidth=0)
style.configure('TNotebook.Tab', background='white', foreground='black', padding=[10, 5])
style.map('TNotebook.Tab', background=[('selected', '#00bfff')], foreground=[('selected', 'white')])

notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True)

# ------------------- Zakładka 1: Kalkulator -------------------
frame_calc = tk.Frame(notebook, bg='black')
notebook.add(frame_calc, text="Kalkulator")

entry_calc = tk.Entry(frame_calc, width=40, font=("Arial", 14, 'bold'), bg='black', fg='white',
                      insertbackground='white', relief='flat', highlightthickness=2, highlightcolor='#00bfff')
entry_calc.pack(pady=10)

btn_eval = tk.Button(frame_calc, text="Oblicz", command=evaluate_expression,
                     bg='black', fg='white', activebackground='#00bfff', activeforeground='black', relief='flat',
                     width=15)
btn_eval.pack(pady=5)

result_label_calc = tk.Label(frame_calc, text="Wynik:", font=("Arial", 14, 'bold'), bg='black', fg='white')
result_label_calc.pack(pady=10)

# ------------------- Zakładka 2: Wykresy -------------------
frame_plot = tk.Frame(notebook, bg='black')
notebook.add(frame_plot, text="Wykresy")

entry_plot = tk.Entry(frame_plot, width=40, font=("Arial", 14, 'bold'), bg='black', fg='white',
                      insertbackground='white', relief='flat', highlightthickness=2, highlightcolor='#00bfff')
entry_plot.pack(pady=10)

btn_plot = tk.Button(frame_plot, text="Rysuj wykres", command=plot_expression,
                     bg='black', fg='white', activebackground='#00bfff', activeforeground='black', relief='flat',
                     width=15)
btn_plot.pack(pady=5)

btn_clear = tk.Button(frame_plot, text="Wyczyść wykres", command=clear_plot,
                      bg='black', fg='white', activebackground='#00bfff', activeforeground='black', relief='flat',
                      width=15)
btn_clear.pack(pady=5)

fig, ax = plt.subplots(figsize=(6, 4), facecolor='black')
ax.set_facecolor('black')
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.draw()
canvas.get_tk_widget().pack()

# ------------------- Zakładka 3: Równania -------------------
frame_eq = tk.Frame(notebook, bg='black')
notebook.add(frame_eq, text="Równania")

entry_eq = tk.Entry(frame_eq, width=40, font=("Arial", 14, 'bold'), bg='black', fg='white',
                    insertbackground='white', relief='flat', highlightthickness=2, highlightcolor='#00bfff')
entry_eq.pack(pady=10)

btn_solve = tk.Button(frame_eq, text="Rozwiąż równanie", command=solve_single_equation,
                      bg='black', fg='white', activebackground='#00bfff', activeforeground='black', relief='flat',
                      width=15)
btn_solve.pack(pady=5)

result_label_eq = tk.Label(frame_eq, text="Rozwiązania:", font=("Arial", 14, 'bold'), bg='black', fg='white')
result_label_eq.pack(pady=10)

# ------------------- Zakładka 4: Układy równań -------------------
frame_system = tk.Frame(notebook, bg='black')
notebook.add(frame_system, text="Układy równań")

tk.Label(frame_system,
         text="Wpisz równania (jedno w wierszu):", bg='black', fg='white', font=("Arial", 12, 'bold')).pack(pady=5)
system_text = tk.Text(frame_system, width=50, height=10, bg='black', fg='white', insertbackground='white',
                      relief='flat')
system_text.pack(pady=5)

tk.Label(frame_system,
         text="Zmienna(y) (oddzielone przecinkiem):", bg='black', fg='white', font=("Arial", 12, 'bold')).pack(pady=5)
variables_entry = tk.Entry(frame_system, width=40, bg='black', fg='white', insertbackground='white', relief='flat')
variables_entry.pack(pady=5)

btn_solve_system = tk.Button(frame_system, text="Rozwiąż układ", command=solve_system_equations,
                             bg='black', fg='white', activebackground='#00bfff', activeforeground='black',
                             relief='flat', width=15)
btn_solve_system.pack(pady=5)

result_label_system = tk.Label(frame_system, text="Rozwiązanie:", font=("Arial", 14, 'bold'), bg='black', fg='white')
result_label_system.pack(pady=10)

# ------------------- Zakładka 5: Pomoc -------------------
frame_help = tk.Frame(notebook, bg='black')
notebook.add(frame_help, text="Pomoc")

scrollbar = tk.Scrollbar(frame_help)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

help_text_widget = tk.Text(frame_help, wrap="word", font=("Consolas", 11, 'bold'),
                           yscrollcommand=scrollbar.set, bg='black', fg='white',
                           padx=15, pady=15, spacing3=5, relief='flat', insertbackground='white')
scrollbar.config(command=help_text_widget.yview)
help_text_widget.insert("1.0", help_content)
help_text_widget.config(state="disabled")
help_text_widget.pack(fill="both", expand=True)


# --- poprawne zamykanie ---
def on_close():
    window.destroy()
    sys.exit(0)


window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()
