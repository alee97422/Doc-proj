import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

class PlaceholderText(tk.Text):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_active = True
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)
        self.add_placeholder()

    def remove_placeholder(self, event=None):
        if self.placeholder_active:
            self.delete("1.0", tk.END)
            self.placeholder_active = False

    def add_placeholder(self, event=None):
        if not self.get("1.0", tk.END).strip():
            self.insert("1.0", self.placeholder)
            self.placeholder_active = True


class SecondPageFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a list of categories
        categories = ["Anger", "Anxiety", "Depression", "Fear", "Grief", "Happiness", "Hope", "Loneliness", "Love",
                      "Sadness", "Shame", "Stress"]

        # Create a listbox for categories
        categories_listbox = tk.Listbox(self, height=15)
        for category in categories:
            categories_listbox.insert(tk.END, category)
        categories_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.config(command=categories_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Configure the listbox to use the scrollbar
        categories_listbox.config(yscrollcommand=scrollbar.set)

        # Create a placeholder for the first text box
        text_box1 = PlaceholderText(self, height=10, width=60, placeholder="Notes")
        text_box1.grid(row=1, column=2, padx=0, pady=0)

        # Create a placeholder for the second text box
        text_box2 = PlaceholderText(self, height=10, width=60, placeholder="End/Add Notes")
        text_box2.grid(row=3, column=2, padx=0, pady=0)

        # Create two buttons below the last text boxes
        copy_button = ttk.Button(self, text="Copy Notes", command=lambda: self.copy_notes(text_box2))
        copy_button.grid(row=6, column=1, padx=5, pady=5)

        add_button = ttk.Button(self, text="Add Note to Category Here")
        add_button.grid(row=6, column=2, padx=5, pady=5)

    def copy_notes(self, text_box):
        notes = text_box.get("1.0", tk.END).strip()
        if notes:
            self.clipboard_clear()
            self.clipboard_append(notes)
            messagebox.showinfo("Notes Copied", "Notes copied to clipboard!")
        else:
            messagebox.showwarning("Empty Notes", "No notes to copy!")
