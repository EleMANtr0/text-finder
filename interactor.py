from finder import Searcher
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import os


class Interactor:
    def __init__(self):
        self.searcher = Searcher()
        self.invoke = []
        self.root = tk.Tk()
        self.root.title("Searcher")
        self.root.geometry("300x150")
        self.root.resizable(False, False)

        self.found_count = tk.StringVar(value="0/0")
        self.found_count_label = ttk.Label(textvariable=self.found_count)
        self.found_count_label.place(relx=0, rely=0)

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
        self.ispp = tk.BooleanVar()
        notepad_pp = ttk.Checkbutton(text="open in notepad++", variable=self.ispp)
        notepad_pp.place(relx=0.28, rely=0.83)

        choose_file = ttk.Button(text="choose file", command=self.choose_file)
        choose_dir = ttk.Button(text="choose dir", command=self.choose_dir)
        choose_file.place(relx=0.03, rely=0.15)
        choose_dir.place(relx=0.03, rely=0.45)

    def start(self):
        self.root.mainloop()

    def update_count(self):
        self.found_count.set(f"{self.searcher.match.curr_pos + 1}/{len(self.searcher.match)}")

    def label_update(self, value):
        self.label_text.set(f"{value[0].name}: {value[1]}")

    def open_button_state(self, value):
        if value == "no matches found":
            self.open_button.state(["disabled"])
        else:
            self.open_button.state(["!disabled"])

    def search_button(self):
        self.searcher.search(self.s.get())
        self.searcher.init_direction(1)
        self.invoke = self.searcher.next()
        self.label_update(self.invoke)
        self.update_count()
        self.open_button_state(self.invoke[1])

    def left(self):
        self.invoke = self.searcher.previous()
        self.label_update(self.invoke)
        self.update_count()
        self.open_button_state(self.invoke[1])

    def right(self):
        self.invoke = self.searcher.next()
        self.label_text.set(f"{self.invoke[0].name}: {self.invoke[1]}")
        self.update_count()
        self.open_button_state(self.invoke[1])

    def choose_file(self):
        path = filedialog.askopenfilename()
        self.searcher.update_file(path)

    def choose_dir(self):
        path = filedialog.askdirectory()
        self.searcher.update_dir(path)

    def open_file(self):
        if self.ispp.get():
            subprocess.run(["C:/Program Files/Notepad++/notepad++.exe", f"-n{self.invoke[1]}", self.invoke[0]])
        else:
            os.startfile(self.invoke[0])