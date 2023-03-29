import zipfile
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("File Compression Tool")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.file_label = tk.Label(self, text="Select a file or folder:")
        self.file_label.grid(row=0, column=0)

        self.file_path = tk.Entry(self, width=50)
        self.file_path.grid(row=0, column=1)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2)

        self.compress_button = tk.Button(self, text="Compress", command=self.compress_file)
        self.compress_button.grid(row=1, column=1)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path.delete(0, tk.END)
        self.file_path.insert(0, file_path)

    def compress_file(self):
        path = self.file_path.get()
        if os.path.isdir(path):
            file_paths = self.retrieve_file_paths(path)
            self.show_file_list(file_paths)
            self.zip_dir(path, file_paths)
            messagebox.showinfo("Success", "Folder compressed successfully!")
        elif os.path.isfile(path):
            self.zip_file(path)
            messagebox.showinfo("Success", "File compressed successfully!")
        else:
            messagebox.showerror("Error", "Invalid file/folder path.")

    def retrieve_file_paths(self, dir_name):
        file_paths = []
        for root, directories, files in os.walk(dir_name):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_paths.append(file_path)
        return file_paths

    def show_file_list(self, file_paths):
        file_list = ""
        for file in file_paths:
            file_list += file + "\n"
        messagebox.showinfo("File List", file_list)

    def zip_dir(self, dir_path, file_paths):
        compress_dir = zipfile.ZipFile(dir_path + '.zip', 'w')
        with compress_dir:
            for file in file_paths:
                compress_dir.write(file)

    def zip_file(self, file_path):
        compress_file = zipfile.ZipFile(file_path + '.zip', 'w')
        compress_file.write(file_path, compress_type=zipfile.ZIP_DEFLATED)
        compress_file.close()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
