import tkinter as tk
from tkinter import messagebox
import sqlite3
import ttkbootstrap as ttk

# Function to handle the submit button
def submit():
    name = name_entry.get()
    gender = gender_var.get()

    if name == "":
        messagebox.showerror("Error", "Please enter your name!")
        return

    if gender == "":
        messagebox.showerror("Error", "Please select your gender!")
        return

    # Print the name and gender for testing
    print("Name:", name)
    print("Gender:", gender)

    # Hide the entry page frame
    entry_frame.grid_remove()

    # Show the next page frame
    next_frame.grid()

    # Update the window size based on the frame's content
    update_window_size()


# Function to update the window size based on the frame's content
def update_window_size():
    window.update_idletasks()  # Update the window's tasks to ensure accurate size calculations
    frame_width = next_frame.winfo_reqwidth()
    frame_height = next_frame.winfo_reqheight()
    window_width = frame_width + window.winfo_rootx() * 2
    window_height = frame_height + window.winfo_rooty() + window.winfo_rootx()
    window.geometry(f"{window_width}x{window_height}")


# Create a custom Tkinter window
window = tk.Tk()
window.geometry("400x200")
window.title("Entry Page")

# Configure the style for dark mode
style = ttk.Style()
style.theme_use("solar")  # Choose the desired theme for dark mode, e.g., "clam" or "alt"

# Create frames for different pages
entry_frame = ttk.Frame(window)
entry_frame.grid()

next_frame = ttk.Frame(window)
next_frame.grid()

# Name label and entry field
name_label = ttk.Label(entry_frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)

name_entry = ttk.Entry(entry_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

# Gender label and radio buttons
gender_label = ttk.Label(entry_frame, text="Gender:")
gender_label.grid(row=1, column=0, padx=5, pady=5)

gender_var = tk.StringVar()

male_radio = ttk.Radiobutton(entry_frame, text="Male", variable=gender_var, value="Male")
male_radio.grid(row=1, column=1, padx=5, pady=5)

female_radio = ttk.Radiobutton(entry_frame, text="Female", variable=gender_var, value="Female")
female_radio.grid(row=2, column=1, padx=5, pady=5)

# Submit button
submit_button = ttk.Button(entry_frame, text="Submit", command=submit)
submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# SQLite database connection
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("CREATE TABLE IF NOT EXISTS categories (name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS notes (category_id INTEGER, note TEXT)")

# Function to add a new category
def add_category():
    category_name = category_entry.get().strip()

    if category_name == "":
        messagebox.showerror("Error", "Please enter a category name!")
        return

    cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
    conn.commit()

    messagebox.showinfo("Success", "Category added successfully!")
    category_entry.delete(0, tk.END)
    refresh_categories_list()

# Function to add a new note
def add_note():
    selected_category = categories_listbox.get(tk.ACTIVE)
    note_text = note_entry.get("1.0", tk.END).strip()

    if selected_category == "":
        messagebox.showerror("Error", "Please select a category!")
        return

    if note_text == "":
        messagebox.showerror("Error", "Please enter a note!")
        return

    category_id = cursor.execute("SELECT rowid FROM categories WHERE name=?", (selected_category,)).fetchone()[0]
    cursor.execute("INSERT INTO notes (category_id, note) VALUES (?, ?)", (category_id, note_text))
    conn.commit()

    messagebox.showinfo("Success", "Note added successfully!")
    note_entry.delete("1.0", tk.END)
    refresh_notes_list()

# Function to refresh the categories listbox
def refresh_categories_list():
    categories_listbox.delete(0, tk.END)
    categories = cursor.execute("SELECT name FROM categories").fetchall()
    for category in categories:
        categories_listbox.insert(tk.END, category[0])

# Function to refresh the notes listbox based on the selected category
def refresh_notes_list():
    selected_category = categories_listbox.get(tk.ACTIVE)
    if selected_category:
        category_id = cursor.execute("SELECT rowid FROM categories WHERE name=?", (selected_category,)).fetchone()[0]
        notes_listbox.delete(0, tk.END)
        notes = cursor.execute("SELECT note FROM notes WHERE category_id=?", (category_id,)).fetchall()
        for note in notes:
            notes_listbox.insert(tk.END, note[0])

# Category label and entry field
category_label = ttk.Label(next_frame, text="Category:")
category_label.grid(row=0, column=0, padx=5, pady=5)

category_entry = ttk.Entry(next_frame)
category_entry.grid(row=0, column=1, padx=5, pady=5)

# Notes label and entry field
notes_label = ttk.Label(next_frame, text="Notes:")
notes_label.grid(row=1, column=0, padx=5, pady=5)

notes_entry = tk.Text(next_frame, height=5, width=30)
notes_entry.grid(row=1, column=1, padx=5, pady=5)

# Add Category button
add_category_button = ttk.Button(next_frame, text="Add Category", command=add_category)
add_category_button.grid(row=0, column=2, padx=5, pady=5)

# Add Note button
add_note_button = ttk.Button(next_frame, text="Add Note", command=add_note)
add_note_button.grid(row=1, column=2, padx=5, pady=5)

# Categories listbox
categories_listbox = tk.Listbox(next_frame, height=10)
categories_listbox.grid(row=2, column=0, padx=5, pady=5, sticky="we")

# Scrollbar for categories listbox
categories_scrollbar = ttk.Scrollbar(next_frame, orient=tk.VERTICAL)
categories_scrollbar.config(command=categories_listbox.yview)
categories_scrollbar.grid(row=2, column=1, sticky="ns")
categories_listbox.config(yscrollcommand=categories_scrollbar.set)

# Notes listbox
notes_listbox = tk.Listbox(next_frame, height=10)
notes_listbox.grid(row=2, column=2, padx=5, pady=5, sticky="we")

# Scrollbar for notes listbox
notes_scrollbar = ttk.Scrollbar(next_frame, orient=tk.VERTICAL)
notes_scrollbar.config(command=notes_listbox.yview)
notes_scrollbar.grid(row=2, column=3, sticky="ns")
notes_listbox.config(yscrollcommand=notes_scrollbar.set)

# Function to handle category selection event
def on_category_select(event):
    refresh_notes_list()

# Bind category listbox select event
categories_listbox.bind("<<ListboxSelect>>", on_category_select)

# Refresh categories listbox
refresh_categories_list()

# Start the Tkinter event loop
window.mainloop()
