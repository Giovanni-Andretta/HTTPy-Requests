import requests
import json
from tkinter import messagebox

def send_request(url_entry, method_var, body_text, headers_text, authorization_entry, params_text, response_text, status_code_label):
    url = url_entry.get()
    method = method_var.get()
    body = body_text.get("1.0", "end-1c").strip()
    headers_input = headers_text.get("1.0", "end-1c").strip()
    authorization = authorization_entry.get().strip()
    params_input = params_text.get("1.0", "end-1c").strip()

    if not url:
        messagebox.showerror("Error", "URL is required!")
        return None

    headers = {}
    if headers_input:
        for line in headers_input.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()

    if authorization:
        headers['Authorization'] = authorization

    params = {}
    if params_input:
        for line in params_input.split("\n"):
            if "=" in line:
                key, value = line.split("=", 1)
                params[key.strip()] = value.strip()

    response_text.delete("1.0", "end-1c")

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, verify=False)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=body, params=params, verify=False)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=body, params=params, verify=False)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, data=body, params=params, verify=False)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, params=params, verify=False)

        status_code = response.status_code
        status_code_label.config(text=str(status_code))
        response_text.insert("1.0", json.dumps(response.json(), indent=4))

        return status_code

    except requests.exceptions.RequestException as e:
        response_text.insert("1.0", f"Error: {e}")
        return None
