import tkinter as tk
from tkinter import filedialog

class NFATAnalysisGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NFAT Translocation Analysis Tool")
        self.root.geometry("400x200")

        self.label_input_directory = tk.Label(self.root, text="Input Directory:")
        self.label_input_directory.pack(pady=5)

        self.entry_input_directory = tk.Entry(self.root, width=30)
        self.entry_input_directory.pack(pady=5)

        self.input_directory = None

        self.button_define_directory = tk.Button(self.root, text="Define Input Directory", command=self.define_directory)
        self.button_define_directory.pack(pady=10)

        self.button_cancel = tk.Button(self.root, text="Cancel", command=self.cancel)
        self.button_cancel.pack(side=tk.RIGHT, padx=5)

        self.button_start = tk.Button(self.root, text="Start", command=self.start_analysis)
        self.button_start.pack(side=tk.RIGHT, padx=5)


    def define_directory(self):
        directory = filedialog.askdirectory()
        self.entry_input_directory.delete(0, tk.END)
        self.entry_input_directory.insert(0, directory)
        self.input_directory = directory


    def start_analysis(self):
        input_directory = self.entry_input_directory.get()
        self.root.destroy()

    def run_gui(self):
        self.root.mainloop()

    def cancel(self):
        self.root.destroy()
