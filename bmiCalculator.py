import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import matplotlib.pyplot as plt

DATA_FILE = "user_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def calculate_bmi(weight, height):
    return weight / (height ** 2)


def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("500x450")

        self.data = load_data()

        title = tk.Label(root, text="BMI CALCULATOR", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=15)

        tk.Label(frame, text="User Name: ").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(frame, width=25)
        self.name_entry.grid(row=0, column=1)

        tk.Label(frame, text="Weight (kg): ").grid(row=1, column=0, sticky="w")
        self.weight_entry = tk.Entry(frame, width=25)
        self.weight_entry.grid(row=1, column=1)

        tk.Label(frame, text="Height (m): ").grid(row=2, column=0, sticky="w")
        self.height_entry = tk.Entry(frame, width=25)
        self.height_entry.grid(row=2, column=1)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Calculate BMI", width=18, command=self.calculate).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="View History", width=18, command=self.show_history).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Plot Trend", width=18, command=self.plot_trend).grid(row=0, column=2, padx=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


    def calculate(self):
        name = self.name_entry.get().strip()
        weight_text = self.weight_entry.get().strip()
        height_text = self.height_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Enter a valid name.")
            return
        try:
            weight = float(weight_text)
            height = float(height_text)
            if weight <= 0 or height <= 0 or height > 3:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid weight or height value.")
            return

        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)

        if name not in self.data:
            self.data[name] = []

        self.data[name].append({"weight": weight, "height": height, "bmi": round(bmi, 2), "category": category})
        save_data(self.data)

        self.result_label.config(text=f"BMI: {bmi:.2f} ({category})")

    def show_history(self):
        if len(self.data) == 0:
            messagebox.showinfo("Info", "No history available.")
            return

        win = tk.Toplevel(self.root)
        win.title("History of All Users")
        win.geometry("550x350")

        cols = ("User", "Weight", "Height", "BMI", "Category")
        tree = ttk.Treeview(win, columns=cols, show="headings")

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for user, records in self.data.items():
            for r in records:
                tree.insert("", "end", values=(
                    user,
                    r["weight"],
                    r["height"],
                    r["bmi"],
                    r["category"]
                ))

        tree.pack(fill=tk.BOTH, expand=True)
 
    def plot_trend(self):
        if len(self.data) == 0:
            messagebox.showinfo("Info", "No BMI records available to plot.")
            return

        plt.figure(figsize=(8, 5))

        for user, records in self.data.items():
            if len(records) == 0:
                continue
            bmi_values = [entry["bmi"] for entry in records]
            plt.plot(bmi_values, marker='o', label=user)

        plt.title("BMI Trends for All Users")
        plt.xlabel("Record Number")
        plt.ylabel("BMI Value")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    
    def on_close(self):
        messagebox.showinfo("Goodbye", "Thank you for using the BMI Calculator!")
        self.root.destroy()

root = tk.Tk()
app = BMICalculatorApp(root)
root.mainloop()