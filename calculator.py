import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

# Flag to track if the last button pressed was equals
last_button_equals = False


def button_click(value):
    global last_button_equals
    current = entry.get()
    if last_button_equals:
        entry.delete(0, tk.END)
        last_button_equals = False
    entry.insert(tk.END, str(value))


def clear_entry():
    global last_button_equals
    entry.delete(0, tk.END)
    last_button_equals = False


def backspace():
    global last_button_equals
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])
    last_button_equals = False


def evaluate():
    global last_button_equals
    try:
        expression = entry.get()
        # Replace modulus operator with remainder calculation
        if '%' in expression:
            # Split the expression by the modulus operator
            parts = expression.split('%')
            # Evaluate each part and calculate the remainder
            left = eval(parts[0])
            right = eval(parts[1])
            result = left % right
        else:
            # For non-modulus operations, evaluate normally
            result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        last_button_equals = True
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
        last_button_equals = True


# Set up the main window
root = tk.Tk()
root.title("Modern Calculator")
root.geometry("400x600")
root.config(bg="#1e1e1e")

# Configure the style for the buttons
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Segoe UI', 16), borderwidth=0, focuscolor='none')
style.map('TButton', background=[('active', '#3a3a3a')])

# Create and place the entry widget
entry = tk.Entry(root, width=20, font=('Segoe UI', 32), justify=tk.RIGHT, bd=0, bg="#1e1e1e", fg="#ffffff",
                 insertbackground="white")
entry.grid(row=0, column=0, columnspan=4, padx=20, pady=(40, 20), sticky="nsew")

# Define the buttons for the calculator
buttons = [
    'C', '⌫', '%', '/',
    '7', '8', '9', '*',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '0', '.', 'mod', '='
]

# Set up the grid for button placement
row_val = 1
col_val = 0

# Define colors for specific buttons
button_colors = {
    'C': '#ff6b6b', '⌫': '#ff6b6b', '%': '#4ecdc4', '/': '#4ecdc4',
    '*': '#4ecdc4', '-': '#4ecdc4', '+': '#4ecdc4', '=': '#f7b731',
    'mod': '#4ecdc4'
}

# Create and place the buttons
for button in buttons:
    # Set the button color
    bg_color = button_colors.get(button, '#3a3a3a')

    if button == '=':
        btn = ttk.Button(root, text=button, command=evaluate)
        btn.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)
    elif button == 'mod':
        btn = ttk.Button(root, text=button, command=lambda: button_click('%'))
        btn.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)
    else:
        if button == 'C':
            cmd = clear_entry
        elif button == '⌫':
            cmd = backspace
        else:
            cmd = lambda b=button: button_click(b)
        btn = ttk.Button(root, text=button, command=cmd)
        btn.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)

    # Apply the style to the button
    style.configure(f'{button}.TButton', background=bg_color, foreground='white')
    btn.configure(style=f'{button}.TButton')

    # Move to the next grid position
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Configure grid weights for responsive layout
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Start the main event loop
root.mainloop()