import tkinter as tk
from tkinter import messagebox
import random


class LuckyDrawApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.load_names_from_file()

    def create_widgets(self):
        # Create label and entry for number of names
        self.num_label = tk.Label(self.master, text="Number of Names to Select")
        self.num_entry = tk.Entry(self.master)
        self.draw_button = tk.Button(self.master, text="Draw", command=self.draw_names)

        # Place number entering box and draw button
        self.num_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="EW")
        self.num_entry.grid(row=1, column=0, columnspan=1, padx=5, pady=0, sticky="EW")
        self.draw_button.grid(row=2, column=0, columnspan=1, padx=5, pady=0, sticky="EW")

        # Create label and listbox for selected names
        self.selected_label = tk.Label(self.master, text="Selected Names")
        self.selected_listbox = tk.Listbox(self.master, height=10)
        self.selected_scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.selected_listbox.yview)
        self.selected_listbox.config(yscrollcommand=self.selected_scrollbar.set)

        # Place selected names listbox
        self.selected_label.grid(row=3, column=0, columnspan=3, padx=5, pady=10, sticky="W")
        self.selected_listbox.grid(row=4, column=0, rowspan=2, columnspan=2, padx=5, pady=5, sticky="NEW")
        self.selected_scrollbar.grid(row=4, column=1, rowspan=2, padx=0, pady=0, sticky="NS")

        # Create label and listbox for all names, with a scrollbar
        self.all_label = tk.Label(self.master, text="Name List")
        self.all_listbox = tk.Listbox(self.master, height=15)
        self.all_scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.all_listbox.yview)
        self.all_listbox.config(yscrollcommand=self.all_scrollbar.set)

        # Place name list listbox
        self.all_label.grid(row=0, column=3, columnspan=3, padx=10, pady=5, sticky="W")
        self.all_listbox.grid(row=1, column=3, columnspan=2, rowspan=4, padx=10, pady=0, sticky="NSEW")
        self.all_scrollbar.grid(row=1, column=5, rowspan=4, padx=0, pady=0, sticky="NS")

        # Create button to add a new name
        self.add_button = tk.Button(self.master, text="Add", command=self.add_name, width=10)

        # Create button to remove a selected name
        self.remove_button = tk.Button(self.master, text="Remove", command=self.remove_selected_name, width=10)
        self.remove_button.config(state="disabled")

        # Place add and remove button
        self.add_button.grid(row=5, column=3, padx=10, pady=5, sticky="W")
        self.remove_button.grid(row=5, column=4, padx=10, pady=5, sticky="W")

    def draw_names(self):
        # Check if number of names to select is valid
        if not self.num_entry.get().isdigit():
            messagebox.showerror("Error", "Number of names to select must be an integer.")
            return

        # Get number of names to select
        num_names = int(self.num_entry.get())

        # Get all names from listbox
        all_names = self.all_listbox.get(0, tk.END)

        # Check if the number of names to select is greater than the number of names in the list
        if num_names > len(all_names):
            messagebox.showerror("Error", "Number of names to select is greater than the names in the list.")
            return

        # Select random names
        selected_names = random.sample(all_names, num_names)

        # Display selected names in listbox
        self.selected_listbox.delete(0, tk.END)
        for name in selected_names:
            self.selected_listbox.insert(tk.END, name)

    def add_name(self):
        # Create a popup window to input new name
        popup = tk.Toplevel()
        popup.title("Add a new name")
        popup.geometry("200x100")

        label = tk.Label(popup, text="Enter a new name:")
        label.pack()

        entry = tk.Entry(popup)
        entry.pack()

        button = tk.Button(popup, text="Add", command=lambda: self.add_name_helper(entry.get(), popup))
        button.pack()

    def add_name_helper(self, new_name, popup):
        # Add new name to listbox and save to file
        self.add_name_to_listbox(new_name)
        self.save_names_to_file()
        popup.destroy()

    def remove_selected_name(self):
        # Get selected name from listbox
        selected_name = self.all_listbox.get(tk.ACTIVE)

        # Remove selected name from listbox and save to file
        self.all_listbox.delete(tk.ACTIVE)
        self.save_names_to_file()

        # Disable remove button if no name is selected
        if self.all_listbox.size() == 0:
            self.remove_button.config(state="disabled")

    def add_name_to_listbox(self, name):
        # Add name to listbox
        self.all_listbox.insert(tk.END, name)

        # Enable remove button
        self.remove_button.config(state="normal")

    def load_names_from_file(self):
        try:
            with open("names.txt", "r") as f:
                names = f.read().splitlines()
                for name in names:
                    self.add_name_to_listbox(name)
        except FileNotFoundError:
            pass

    def save_names_to_file(self):
        # Save names in listbox to file
        with open("names.txt", "w") as f:
            for name in self.all_listbox.get(0, tk.END):
                f.write(name + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Lucky Draw')
    app = LuckyDrawApplication(master=root)
    app.mainloop()