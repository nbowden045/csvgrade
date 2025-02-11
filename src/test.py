import tkinter as tk

# Sample dictionary
data = {
    "1": {"1_1": "fail", "2_1": "ish", "3_1": "pass"},
    "2": {"1_3": "fail", "2_2": "ish", "3_2": "pass"}
}

# Create the main application window
root = tk.Tk()
root.title("Dynamic Menu")

# Dictionary to store selected values
selected_values = {}

# Function to print selected values
def show_selection():
    for key, var in selected_values.items():
        print(f"Selection for {key}: {var.get()}")

# Create UI elements
for row, (outer_key, inner_dict) in enumerate(data.items()):
    tk.Label(root, text=f"Category {outer_key}:").grid(row=row, column=0, sticky="w")

    # Variable to store selected option for this category
    selected_values[outer_key] = tk.StringVar(value="")  

    for col, (inner_key, value) in enumerate(inner_dict.items(), start=1):
        rb = tk.Radiobutton(root, text=value, variable=selected_values[outer_key], value=inner_key)
        rb.grid(row=row, column=col, sticky="w")

# Button to show selections
tk.Button(root, text="Submit", command=show_selection).grid(row=len(data), column=0, columnspan=3)

# Run the main loop
root.mainloop()
