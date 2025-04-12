# HTTP Request Sender and Manager

****************************************************

| Tool     | Version     |
|----------|-------------|
| Python   | 3.10+       |
| Tkinter  | built-in    |
| requests | ^2.31.0     |

****************************************************

## 💡 About the Project

Application to send and manage HTTP requests (GET, POST, PUT, DELETE) using Python and Tkinter. It allows you to easily create, save, and load HTTP requests, view responses, and manage request history.

## Functionalities

- **Send HTTP Requests:** You can send HTTP requests using different methods like GET, POST, PUT, and DELETE.
- **Save and Load Requests:** Requests can be saved with custom names and loaded for future use.
- **Duplicate or Delete Saved Requests:** You can duplicate or remove saved requests from the list.
- **List Requests:** View a list of all saved HTTP requests. You can select a request from the list and load it back into the request fields.
- **View Responses:** The application displays the status code and content of the response from the server.
- **Automatic Load of Last Saved Request:** When the application starts, it automatically loads the last saved request, allowing you to continue where you left off.
- **Undo/Redo History:** You can undo or redo any changes made to the request fields (such as URL, headers, body).

****************************************************

## 🔧 Installation

### 1. Create a Virtual Environment

To create a virtual environment, open your terminal (or command prompt) and run the following:

```
python3 -m venv .venv
```

### 2. Activate the virtual environment:

macOS/Linux:
  ```
  source .venv/bin/activate
  ```

Windows:
  ```
  .venv\Scripts\activate
  ```

Once activated, your terminal prompt will change to show the name of the virtual environment (venv).

### 3. Install Dependencies

After activating the virtual environment, you need to install the required dependencies:

```
pip install -r requirements.txt
```

### 4. Install Tkinter

macOS:
  To install Tkinter on macOS, you can use Homebrew:

  ```
  brew install python-tk
  ```

Windows:
  Tkinter is included with Python by default on Windows, so there is no need to install it separately.

### 5. Run the Application

Once the dependencies are installed and Tkinter is set up, you can run the application with:

```
  python3 main.py
```

### 6. Keyboard Shortcuts

- Ctrl + S / Cmd + S – Save the current request
- Ctrl + Z / Cmd + Z – Undo changes
- Ctrl + Shift + Z / Cmd + Shift + Z – Redo changes

### 7. Creating a Visual Shortcut on macOS using Automator (Optional)

If you want to create a visual shortcut to run the application on your Mac, you can do so using **Automator**:

Steps to Create an Automator Shortcut:

1. Open **Automator** (you can search for it using Spotlight).
2. Choose **Application** when prompted to select a document type.
3. In the search bar on the left, type **Run Shell Script** and double-click it to add it to your workflow.
4. In the **Run Shell Script** box, paste the following command:

    ```
    cd /path/to/your/project
    source .venv/bin/activate
    python3 main.py
    ```

   Replace `/path/to/your/project` with the actual path to your project directory.

5. Save the Automator application with a name like `HTTPy Request.app` to your **Desktop**.
6. Once saved, you can now double-click this application anytime to launch your HTTP Request Sender and Manager app.
7. Optionally, you can drag this new Automator application to your **Dock** for easy access.

Now, you have a convenient visual shortcut to run your app directly from your desktop or Dock!
