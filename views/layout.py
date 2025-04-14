import tkinter as tk
from tkinter import ttk, scrolledtext
from handlers.request_actions import *
from handlers.send_request import send_request


def enable_undo(widget):
    history = [widget.get("1.0", tk.END).strip() if isinstance(widget, scrolledtext.ScrolledText) else widget.get()]
    history_index = [0]

    def get_current_text():
        return widget.get("1.0", tk.END).strip() if isinstance(widget, scrolledtext.ScrolledText) else widget.get()

    def set_text(value):
        if isinstance(widget, scrolledtext.ScrolledText):
            widget.delete("1.0", tk.END)
            widget.insert("1.0", value)
        else:
            widget.delete(0, tk.END)
            widget.insert(0, value)

    def save_state(event=None):
        current = get_current_text()
        if current != history[-1]:
            history.append(current)
            history_index[0] = len(history) - 1

    def undo(event=None):
        if history_index[0] > 0:
            history_index[0] -= 1
            set_text(history[history_index[0]])
        return "break"

    def redo(event=None):
        if history_index[0] < len(history) - 1:
            history_index[0] += 1
            set_text(history[history_index[0]])
        return "break"

    widget.bind("<KeyPress>", save_state)
    widget.bind("<Command-z>", undo)
    widget.bind("<Control-z>", undo)
    widget.bind("<Command-Shift-Z>", redo)
    widget.bind("<Control-Shift-Z>", redo)


def bind_text_navigation(widget):
    widget.bind("<Tab>", lambda event: (event.widget.insert("insert", "    "), "break")[1])
    widget.bind("<Return>", lambda event: (event.widget.insert("insert", "\n" + get_indent(event)), "break")[1])


def get_indent(event):
    current_line = event.widget.get("insert linestart", "insert")
    return ''.join(char for char in current_line if char == ' ')


def add_labeled_widget(parent, row, label_text, label_color, widget):
    tk.Label(parent, text=label_text, fg=label_color, font=("Source Code Pro", 10)).grid(row=row, column=0, padx=10, pady=5, sticky='w')
    widget.grid(row=row, column=1, padx=10, pady=5, sticky='w')
    enable_undo(widget)
    if isinstance(widget, scrolledtext.ScrolledText):
        bind_text_navigation(widget)


def build_layout(app):
    previous_request = {"name": None}

    frame_buttons = tk.Frame(app)
    frame_buttons.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    frame_content = tk.Frame(app)
    frame_content.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    frame_content.grid_columnconfigure(0, weight=1)
    frame_content.grid_columnconfigure(1, weight=3)

    for row in range(10):
        weight = 0 if row not in [3, 9] else 1
        frame_content.grid_rowconfigure(row, weight=weight)

    for row in range(8):
        frame_buttons.grid_rowconfigure(row, weight=0)

    request_name_combobox = ttk.Combobox(frame_buttons, width=25, font=("Source Code Pro", 10))

    def create_buttons():
        button_data = [
            ("New Request", new_request),
            ("Save Request", save_request),
            ("Duplicate Request", duplicate_request),
        ]

        for i, (label, action) in enumerate(button_data):
            tk.Button(
                frame_buttons, text=label,
                command=lambda act=action: act(
                    request_name_combobox, url_entry, method_var, body_text,
                    headers_text, authorization_entry, params_text, previous_request
                ),
                width=20, font=("Source Code Pro", 10)
            ).grid(row=i, column=0, padx=10, pady=5, sticky='w')

        def remove_and_clear():
            remove_request(
                request_name_combobox, url_entry, method_var, body_text,
                headers_text, authorization_entry, params_text
            )
            previous_request.update({"name": None})

        tk.Button(frame_buttons, text="Remove Request",command=remove_and_clear,width=20, font=("Source Code Pro", 10)).grid(row=len(button_data), column=0, padx=10, pady=5, sticky='w')
        return len(button_data) + 1

    buttons_end_row = create_buttons()

    tk.Label(frame_buttons, text="Select Request:", fg="lightcoral", font=("Source Code Pro", 10)) \
        .grid(row=buttons_end_row, column=0, padx=10, pady=5, sticky='w')
    request_name_combobox.grid(row=buttons_end_row + 1, column=0, padx=10, pady=10, sticky='w')

    url_entry = tk.Entry(frame_content, width=76, font=("Source Code Pro", 10))
    add_labeled_widget(frame_content, 1, "URL:", "mediumseagreen", url_entry)

    method_var = tk.StringVar(value="GET")
    method_menu = ttk.Combobox(frame_content, textvariable=method_var, values=["GET", "POST", "PUT", "DELETE", "PATCH"], width=8, font=("Source Code Pro", 10))
    method_menu.grid(row=2, column=1, padx=10, pady=5, sticky='w')
    tk.Label(frame_content, text="Method:", fg="lightsalmon", font=("Source Code Pro", 10)).grid(row=2, column=0, padx=10, pady=5, sticky='w')

    body_text = scrolledtext.ScrolledText(frame_content, width=74, height=18, font=("Source Code Pro", 10))
    add_labeled_widget(frame_content, 3, "Body:", "orchid", body_text)

    params_text = scrolledtext.ScrolledText(frame_buttons, width=30, height=5, font=("Source Code Pro", 10))
    tk.Label(frame_buttons, text="Params:", fg="lightgoldenrodyellow", font=("Source Code Pro", 10)) \
        .grid(row=buttons_end_row + 2, column=0, padx=10, pady=(5, 0), sticky='w')
    params_text.grid(row=buttons_end_row + 3, column=0, padx=10, pady=5, sticky='w')
    enable_undo(params_text)
    bind_text_navigation(params_text)

    authorization_entry = tk.Entry(frame_buttons, width=30, font=("Source Code Pro", 10))
    tk.Label(frame_buttons, text="Authorization:", fg="lightcoral", font=("Source Code Pro", 10)) \
        .grid(row=buttons_end_row + 4, column=0, padx=10, pady=(5, 0), sticky='w')
    authorization_entry.grid(row=buttons_end_row + 5, column=0, padx=10, pady=5, sticky='w')
    enable_undo(authorization_entry)

    headers_text = scrolledtext.ScrolledText(frame_buttons, width=30, height=5, font=("Source Code Pro", 10))
    tk.Label(frame_buttons, text="Headers:", fg="cadetblue", font=("Source Code Pro", 10)) \
        .grid(row=buttons_end_row + 6, column=0, padx=10, pady=(5, 0), sticky='w')
    headers_text.grid(row=buttons_end_row + 7, column=0, padx=10, pady=5, sticky='w')
    enable_undo(headers_text)
    bind_text_navigation(headers_text)

    send_btn = tk.Button(frame_content, text="Send", width=5, font=("Source Code Pro", 10))
    send_btn.grid(row=7, column=1, padx=10, pady=10, sticky='w')

    tk.Label(frame_content, text="Response:", fg="yellow", font=("Source Code Pro", 10)).grid(row=9, column=0, padx=10, pady=5, sticky='w')

    response_container = tk.Frame(frame_content)
    response_container.grid(row=9, column=1, sticky="w", padx=10, pady=5)

    status_frame = tk.Frame(response_container, bg="black")
    status_frame.pack(side="top", anchor="ne", pady=(0, 5), padx=(0, 30))

    status_canvas = tk.Canvas(status_frame, width=12, height=12, highlightthickness=0, bg="black")
    status_circle_id = status_canvas.create_oval(0, 0, 10, 10, fill="white", outline="white")
    status_canvas.pack(side="left", padx=(0, 5))

    status_code_label = tk.Label(status_frame, text="", width=6, bg="black", fg="white", anchor='center', relief='flat', font=("Source Code Pro", 10, "bold"))
    status_code_label.pack(side="left")

    response_text = scrolledtext.ScrolledText(response_container, width=74, height=21, font=("Source Code Pro", 10), state=tk.DISABLED)
    response_text.pack(fill="both", expand=True)
    enable_undo(response_text)
    bind_text_navigation(response_text)

    blink_job = {"after_id": None}

    def start_blink(color, blink_count=2):
        if blink_job["after_id"]:
            status_canvas.after_cancel(blink_job["after_id"])
            blink_job["after_id"] = None

        def blink(count):
            current_color = status_canvas.itemcget(status_circle_id, "fill")
            new_color = color if current_color == "white" else "white"
            status_canvas.itemconfig(status_circle_id, fill=new_color)

            if new_color == color:
                count -= 1
            if count > 0:
                blink_job["after_id"] = status_canvas.after(400, blink, count)
            else:
                blink_job["after_id"] = None
                status_canvas.itemconfig(status_circle_id, fill=color)

        blink(blink_count)

    def send_request_with_animation():
        save_request(request_name_combobox, url_entry, method_var, body_text, headers_text, authorization_entry, params_text, previous_request, silent=True)

        status_canvas.itemconfig(status_circle_id, fill="white")
        status_code_label.config(text="", fg="white")

        response_text.config(state=tk.NORMAL)
        response_text.delete(1.0, tk.END)

        status_code = send_request(
            url_entry, method_var, body_text, headers_text,
            authorization_entry, params_text,
            response_text, status_code_label
        )

        response_text.config(state=tk.DISABLED)

        if status_code is not None:
            color = "green" if 200 <= status_code <= 299 else "red" if 400 <= status_code <= 599 else "orange"
            status_code_label.config(fg=color)
            start_blink(color)

        status_code_label.config(text=str(status_code))

    send_btn.config(command=send_request_with_animation)

    def handle_save_event(event=None):
        save_request(request_name_combobox, url_entry, method_var, body_text, headers_text, authorization_entry, params_text, previous_request)
        return "break"

    app.bind_all("<Command-s>", handle_save_event)
    app.bind_all("<Control-s>", handle_save_event)

    list_requests(request_name_combobox)
    load_last_request(request_name_combobox, url_entry, method_var, body_text, headers_text, authorization_entry, params_text)
    previous_request["name"] = request_name_combobox.get().strip()

    def on_request_select(event):
        new_request_name = request_name_combobox.get()
        previous_name = previous_request["name"]

        if previous_name and previous_name != new_request_name:
            request_name_combobox.set(previous_name)
            save_request(request_name_combobox, url_entry, method_var, body_text, headers_text, authorization_entry, params_text, previous_request, silent=True)
            request_name_combobox.set(new_request_name)

        previous_request["name"] = new_request_name
        load_request(new_request_name, url_entry, method_var, body_text, headers_text, authorization_entry, params_text)
        status_canvas.itemconfig(status_circle_id, fill="white")
        status_code_label.config(text="", fg="white")

    request_name_combobox.bind("<<ComboboxSelected>>", on_request_select)
