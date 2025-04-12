import os
import json
from tkinter import messagebox

def new_request(request_name_combobox, url_entry, method_var, body_text, headers_text, authorization_entry, params_text, previous_request):
    new_request_name = request_name_combobox.get().strip()

    if not new_request_name:
        messagebox.showerror("Error", "Please enter a request name.")
        return

    file_path = f"requests/{new_request_name}.json"

    if os.path.exists(file_path):
        messagebox.showwarning("Warning", f"Request '{new_request_name}' already exists.")
        return

    clear_fields(url_entry, method_var, body_text, headers_text, authorization_entry, params_text, request_name_combobox, clear_request_name=False)

    new_request = {
        "url": "",
        "method": "GET",
        "body": "",
        "params": "",
        "authorization": "",
        "headers": ""
    }

    try:
        with open(file_path, 'w') as file:
            json.dump(new_request, file, indent=4)

        messagebox.showinfo("Success", f"New request '{new_request_name}' created successfully.")

        list_requests(request_name_combobox)
        request_name_combobox.set(new_request_name)
        previous_request["name"] = new_request_name

    except Exception as e:
        print(f"Error creating JSON file: {e}")
        messagebox.showerror("Error", f"Failed to create the request: {e}")


def save_request(request_name_combobox, url_entry, method_var, body_text, headers_text, authorization_entry, params_text, previous_request, silent=False):
    new_name = request_name_combobox.get().strip()
    old_name = previous_request.get("name")

    if not new_name:
        if not silent:
            messagebox.showerror("Error", "Request name cannot be empty.")
        return

    url = url_entry.get()
    method = method_var.get()
    body = body_text.get("1.0", "end-1c").strip()
    headers = headers_text.get("1.0", "end-1c").strip()
    authorization = authorization_entry.get().strip()
    params = params_text.get("1.0", "end-1c").strip()

    request = {
        'url': url,
        'method': method,
        'body': body,
        'params': params,
        'authorization': authorization,
        'headers': headers
    }

    if old_name and new_name != old_name:
        old_path = f"requests/{old_name}.json"
        new_path = f"requests/{new_name}.json"

        if not os.path.exists(old_path):
            if not silent:
                messagebox.showerror("Error", f"Original request '{old_name}' does not exist.")
            return

        if os.path.exists(new_path):
            if not silent:
                overwrite = messagebox.askyesno("Overwrite", f"Request '{new_name}' already exists. Overwrite?")
                if not overwrite:
                    return
        else:
            os.rename(old_path, new_path)

        previous_request["name"] = new_name
        path_to_save = new_path

    else:
        path_to_save = f"requests/{new_name}.json"
        if not os.path.exists(path_to_save):
            if not silent:
                messagebox.showerror("Error", f"Request '{new_name}' does not exist.")
            return
        previous_request["name"] = new_name

    with open(path_to_save, "w") as file:
        json.dump(request, file, indent=4)

    if not silent:
        messagebox.showinfo("Success", f"Request '{new_name}' saved successfully.")

    list_requests(request_name_combobox)


def load_request(request_name, url_entry, method_var, body_text, headers_text, authorization_entry, params_text):
    request_path = f"requests/{request_name}.json"

    if not os.path.exists(request_path):
        messagebox.showerror("Error", f"Request '{request_name}' not found.")
        return

    with open(request_path, "r") as file:
        request = json.load(file)
        url_entry.delete(0, "end")
        url_entry.insert(0, request['url'])
        method_var.set(request['method'])
        body_text.delete("1.0", "end-1c")
        body_text.insert("end", request['body'])
        params_text.delete("1.0", "end-1c")
        params_text.insert("end", request['params'])
        authorization_entry.delete(0, "end")
        authorization_entry.insert(0, request['authorization'])
        headers_text.delete("1.0", "end-1c")
        headers_text.insert("end", request['headers'])

def load_last_request(request_name_entry, url_entry, method_var, body_text, headers_text, authorization_entry, params_text):
    try:
        request_files = [f for f in os.listdir("requests") if f.endswith(".json")]

        if not request_files:
            return

        latest_file = max(request_files, key=lambda f: os.path.getmtime(os.path.join("requests", f)))

        with open(os.path.join("requests", latest_file), "r") as file:
            last_request = json.load(file)

            request_name = os.path.splitext(latest_file)[0]
            request_name_entry.delete(0, "end")
            request_name_entry.insert(0, request_name)

            url_entry.delete(0, "end")
            url_entry.insert(0, last_request.get("url", ""))

            method_var.set(last_request.get("method", "GET"))

            body_text.delete(1.0, "end")
            body_text.insert(1.0, last_request.get("body", ""))

            headers_text.delete(1.0, "end")
            headers_text.insert(1.0, last_request.get("headers", ""))

            authorization_entry.delete(0, "end")
            authorization_entry.insert(0, last_request.get("authorization", ""))

            params_text.delete(1.0, "end")
            params_text.insert(1.0, last_request.get("params", ""))

    except Exception as e:
        print(f"Error loading last request: {e}")

def list_requests(request_name_combobox):
    try:
        requests_list = [f for f in os.listdir("requests") if f.endswith(".json")]
        requests_list.sort(key=lambda f: os.path.getmtime(os.path.join("requests", f)), reverse=True)
        request_names = [os.path.splitext(r)[0] for r in requests_list]
        request_name_combobox['values'] = request_names
    except FileNotFoundError:
        messagebox.showerror("Error", "No requests folder found.")

def duplicate_request(request_name_combobox, url_entry, method_var, body_text, headers_text, authorization_entry, params_text, previous_request):
    selected_request = request_name_combobox.get()
    if not selected_request:
        messagebox.showerror("Error", "Please select a request to duplicate.")
        return

    new_name = f"{selected_request}_copy"
    request_path = f"requests/{selected_request}.json"
    new_request_path = f"requests/{new_name}.json"

    counter = 1
    while os.path.exists(new_request_path):
        new_name = f"{selected_request}_copy{counter}"
        new_request_path = f"requests/{new_name}.json"
        counter += 1

    with open(request_path, "r") as file:
        request = json.load(file)

    with open(new_request_path, "w") as file:
        json.dump(request, file, indent=4)

    messagebox.showinfo("Success", f"Request duplicated as '{new_name}'.")

    list_requests(request_name_combobox)

    request_name_combobox.set(new_name)
    previous_request["name"] = new_name
    load_request(new_name, url_entry, method_var, body_text, headers_text, authorization_entry, params_text)

def clear_fields(url_entry, method_var, body_text, headers_text, authorization_entry, params_text, request_name_combobox, clear_request_name=True):
    url_entry.delete(0, "end")
    method_var.set("GET")
    body_text.delete("1.0", "end-1c")
    params_text.delete("1.0", "end-1c")
    authorization_entry.delete(0, "end")
    headers_text.delete("1.0", "end-1c")

    if clear_request_name:
        request_name_combobox.set('')

def remove_request(request_name_combobox, url_entry, method_var, body_text, headers_text, authorization_entry, params_text):
    selected_request = request_name_combobox.get()
    if not selected_request:
        messagebox.showerror("Error", "Please select a request to remove.")
        return

    request_path = f"requests/{selected_request}.json"

    if not os.path.exists(request_path):
        messagebox.showerror("Error", f"Request '{selected_request}' not found.")
        return

    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_request}'?")
    if confirm:
        os.remove(request_path)
        messagebox.showinfo("Success", f"Request '{selected_request}' removed successfully.")

        clear_fields(url_entry, method_var, body_text, headers_text, authorization_entry, params_text, request_name_combobox)
        list_requests(request_name_combobox)
