import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from second_page import SecondPageFrame

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
    entry_frame.pack_forget()

    # Show the next page frame
    next_frame.pack()

    # Update the window size based on the frame's content
    update_window_size()


# Function to update the window size based on the frame's content
def update_window_size():
    window.update_idletasks()  # Update the window's tasks to ensure accurate size calculations
    frame_width = next_frame.winfo_reqwidth()
    frame_height = next_frame.winfo_reqheight()
    window_width = frame_width + window.winfo_rootx() * 2
    window_height = frame_height + window.winfo_rooty() + window.winfo_rootx()
    window.geometry(f"650x550")


# Create a custom Tkinter window
window = tk.Tk()
window.geometry("400x200")
window.title("Entry Page")

# Configure the style for dark mode
style = ttk.Style()
style.theme_use("solar")  # Choose the desired theme for dark mode, e.g., "clam" or "alt"

# Create frames for different pages
entry_frame = ttk.Frame(window)
entry_frame.pack()

next_frame = SecondPageFrame(window)

# Name label and entry field
name_label = ttk.Label(entry_frame, text="Name:")
name_label.pack()

name_entry = ttk.Entry(entry_frame)
name_entry.pack()

# Gender label and radio buttons
gender_label = ttk.Label(entry_frame, text="Gender:")
gender_label.pack()

gender_var = tk.StringVar()

male_radio = ttk.Radiobutton(entry_frame, text="Male", variable=gender_var, value="Male")
male_radio.pack()

female_radio = ttk.Radiobutton(entry_frame, text="Female", variable=gender_var, value="Female")
female_radio.pack()

# Submit button
submit_button = ttk.Button(entry_frame, text="Submit", command=submit)
submit_button.pack()

# Start the Tkinter event loop
window.mainloop()
