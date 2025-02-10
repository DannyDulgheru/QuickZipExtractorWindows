import os
import zipfile
import sys
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import subprocess

def extract_zip(file_path, progress_bar, progress_label, root):
    if not file_path or not file_path.endswith(".zip"):
        root.destroy()
        return

    # Get directory and filename
    dir_name = os.path.dirname(file_path)
    zip_name = os.path.basename(file_path).replace(".zip", "")
    extract_path = os.path.join(dir_name, zip_name)

    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            total_files = len(zip_ref.namelist())

            # Extract with progress
            for i, file in enumerate(zip_ref.namelist(), 1):
                zip_ref.extract(file, extract_path)
                progress_bar["value"] = (i / total_files) * 100
                progress_label.config(text=f"Extracting... {i}/{total_files}")
                root.update_idletasks()

        # Delete ZIP file
        os.remove(file_path)

        # Open extracted folder
        subprocess.run(["explorer", extract_path], check=False)

    except Exception as e:
        print(f"Error: {e}")

    root.destroy()  # Close window automatically

def start_extraction(file_path):
    root = tk.Tk()
    root.title("Extracting ZIP")
    root.geometry("300x100")
    root.resizable(False, False)
    root.overrideredirect(True)  # Hide window frame

    progress_label = tk.Label(root, text="Starting extraction...", padx=10)
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=250, mode="determinate")
    progress_bar.pack(pady=5)

    threading.Thread(target=extract_zip, args=(file_path, progress_bar, progress_label, root), daemon=True).start()

    root.mainloop()

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]  # Get file path from command-line argument
        start_extraction(file_path)
    else:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        if file_path:
            start_extraction(file_path)

if __name__ == "__main__":
    main()
