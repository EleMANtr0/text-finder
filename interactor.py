import finder
from finder import Searcher
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import os

class Interactor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.searcher = Searcher()
        self.found_line = finder.path_line
        self.title("Searcher")
        self.geometry("300x150")
        self.resizable(False, False)

        self.found_count = tk.StringVar(value="0/0")
        found_count_label = ttk.Label(textvariable=self.found_count)
        found_count_label.place(relx=0, rely=0)

        self.s = ttk.Entry(justify="center")
        self.s.place(relx=0.2, rely=0)

        search = ttk.Button(text="search", command=self.search_button)
        search.place(relx=0.65, rely=0)

        self.label_text = tk.StringVar(value="")
        self.text = ttk.Label(textvariable=self.label_text)
        self.text.place(relx=0.5, rely=0.4, anchor="center")

        left = ttk.Button(text="previous", command=self.left)
        right = ttk.Button(text="next", command=self.right)
        left.place(relx=0.03, rely=0.8)
        right.place(relx=0.71, rely=0.8)

        self.open_button = ttk.Button(text="open", command=self.open_file)
        self.open_button.place(relx=0.71, rely=0.2)
        self.have_notepad_pp = tk.BooleanVar()
        notepad_pp = ttk.Checkbutton(text="open in notepad++", variable=self.have_notepad_pp)
        notepad_pp.place(relx=0.28, rely=0.83)

        choose_file = ttk.Button(text="choose file", command=self.choose_file)
        choose_dir = ttk.Button(text="choose dir", command=self.choose_dir)
        choose_file.place(relx=0.03, rely=0.15)
        choose_dir.place(relx=0.03, rely=0.45)

    def start(self):
        self.mainloop()

    def update_count(self):
        self.found_count.set(f"{self.searcher.curr_pos + 1}/{len(self.searcher)}")

    def label_update(self, value):
        if value.line:
            self.label_text.set(f"{value.path.name}: {value.line}")
        else:
            self.label_text.set(f"{value.path.name}: no matches found")

    def set_open_state(self, value):
        if value:
            self.open_button.state(["!disabled"])
        else:
            self.open_button.state(["disabled"])

    def search_button(self):
        self.found_line = self.searcher.search(self.s.get())
        self.label_update(self.found_line)
        self.update_count()
        self.set_open_state(self.found_line.line)

    def left(self):
        self.found_line = self.searcher.previous()
        self.label_update(self.found_line)
        self.update_count()
        self.set_open_state(self.found_line.line)

    def right(self):
        self.found_line = self.searcher.next()
        self.label_update(self.found_line)
        self.update_count()
        self.set_open_state(self.found_line.line)

    def choose_file(self):
        path = filedialog.askopenfilename()
        self.searcher.update_file(path)

    def choose_dir(self):
        path = filedialog.askdirectory()
        self.searcher.update_dir(path)

    def open_file(self):
        if self.have_notepad_pp.get():
            subprocess.run(["C:/Program Files/Notepad++/notepad++.exe", f"-n{self.found_line.line}", self.found_line.path])
        else:
            os.startfile(self.found_line.path)
