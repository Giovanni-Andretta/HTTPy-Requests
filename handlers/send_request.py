import subprocess
import json
from tkinter import messagebox

def send_request(url_entry, method_var, body_text, headers_text, authorization_entry, params_text, response_text, status_code_label):
    url = url_entry.get().strip()
    method = method_var.get().upper()
    body = body_text.get("1.0", "end-1c").strip()
    headers_input = headers_text.get("1.0", "end-1c").strip()
    auth = authorization_entry.get().strip()
    params_input = params_text.get("1.0", "end-1c").strip()

    if not url:
        messagebox.showerror("Error", "URL is required!")
        return None

    if params_input:
        pairs = []
        for line in params_input.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip().replace(" ", "%20")
                value = value.strip().replace(" ", "%20")
                pairs.append(f"{key}={value}")
        if pairs:
            separator = "&" if "?" in url else "?"
            url += separator + "&".join(pairs)

    headers = []
    if headers_input:
        for line in headers_input.splitlines():
            if ":" in line:
                headers += ["-H", line.strip()]
    if auth:
        headers += ["-H", f"Authorization: {auth}"]

    cmd = ["curl", "-s", "-X", method, "-w", "%{http_code}", url]
    cmd += headers

    if method in ["POST", "PUT", "PATCH"]:
        cmd += ["--data", body if body else ""]

    response_text.config(state="normal")
    response_text.delete("1.0", "end")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        status_code = output[-3:]
        content = output[:-3].strip()

        status_code_label.config(text=status_code)

        try:
            parsed = json.loads(content)
            response_text.insert("1.0", json.dumps(parsed, indent=4))
        except json.JSONDecodeError:
            response_text.insert("1.0", content)

        response_text.config(state="disabled")
        return int(status_code)

    except Exception as e:
        response_text.insert("1.0", f"Error: {e}")
        return None
