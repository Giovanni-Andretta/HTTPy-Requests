import tkinter as tk
from views.layout import build_layout

def create_window():
    app = tk.Tk()
    app.title("HTTPy Requests")

    window_width = 1150
    window_height = 850
    screen_width = app.winfo_screenwidth()
    position_top = 0
    position_right = int(screen_width / 2 - window_width / 2)
    app.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    build_layout(app)

    return app
