

import tkinter as tk
from tkinter import ttk, messagebox
import random

# I NEED TO GO THROUGH AND WORK ON ALL MY COMMENTS TO HAVE PROPER MEANINGS.
class MealTipCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Meal & Tip Calculator")
        self.root.geometry("480x760")
        self.root.resizable(False, True)
        self.root.config(bg="white")

        self.meals = [
            "SELECT A MEAL",
            "Grilled Chicken Salad",
            "Pasta Alfredo",
            "Steak & Chips",
            "Vegetarian Pizza",
            "Seafood Platter",
            "Vegan Bowl",
            "Burger & Fries",
            "Sushi Combo",
        ]

        self.meal_emojis = { 
            "Grilled Chicken Salad": "🥗",
            "Pasta Alfredo": "🍝",
            "Steak & Chips": "🥩🍟",
            "Vegetarian Pizza": "🍕",
            "Seafood Platter": "🦞🐟",
            "Vegan Bowl": "🥦🥕",
            "Burger & Fries": "🍔🍟",
            "Sushi Combo": "🍣"
        }

        self.create_widgets()

    def create_widgets(self):
        # --- Title ---
        tk.Label(self.root, text="🍴 Meal Treat & Tip Calculator 💳",
                 font=("Arial", 16, "bold"), fg="black", bg="white").pack(pady=10)

        # --- Meal Selection ---
        tk.Label(self.root, text="Select a Meal:", font=("Arial", 12), bg="white").pack(pady=5)
        self.meal_choice = tk.StringVar(value="Select a Meal")
        self.meal_dropdown = ttk.Combobox(self.root, textvariable=self.meal_choice,
                                          values=self.meals, state="readonly", font=("Arial", 12))
        self.meal_dropdown.pack(pady=5)
        self.meal_choice.trace("w", self.show_calculator_section)

        # Emoji display for selected meal
        self.emoji_label = tk.Label(self.root, text="", font=("Arial", 26), bg="white")
        self.emoji_label.pack(pady=5)

        # Calculator Frame (hidden initially)
        self.calc_frame = tk.Frame(self.root, bg="white")

        # Bill
        tk.Label(self.calc_frame, text="Bill Amount (£):", font=("Arial", 12), bg="white").pack(pady=5)
        self.entry_bill = tk.Entry(self.calc_frame, font=("Arial", 12))
        self.entry_bill.pack(pady=5)

        # Tip selection
        tk.Label(self.calc_frame, text="Select Tip %:", font=("Arial", 12), bg="white").pack(pady=5)
        self.tip_choice = tk.StringVar(value="10")
        tip_frame = tk.Frame(self.calc_frame, bg="white")
        tip_frame.pack(pady=3)
        tk.Radiobutton(tip_frame, text="10%", variable=self.tip_choice, value="10", bg="white").grid(row=0, column=0, padx=10)
        tk.Radiobutton(tip_frame, text="15%", variable=self.tip_choice, value="15", bg="white").grid(row=0, column=1, padx=10)
        tk.Radiobutton(tip_frame, text="20%", variable=self.tip_choice, value="20", bg="white").grid(row=0, column=2, padx=10)

        custom_frame = tk.Frame(tip_frame, bg="white")
        custom_frame.grid(row=0, column=3, padx=10)
        tk.Radiobutton(custom_frame, text="Custom", variable=self.tip_choice, value="custom", bg="white").pack(side="left")
        self.entry_custom = tk.Entry(custom_frame, font=("Arial", 12), width=6)
        self.entry_custom.pack(side="left", padx=5)

        # People
        tk.Label(self.calc_frame, text="Number of People:", font=("Arial", 12), bg="white").pack(pady=5)
        self.entry_people = tk.Entry(self.calc_frame, font=("Arial", 12))
        self.entry_people.pack(pady=5)

        # Initials
        tk.Label(self.calc_frame, text="Enter Initials (comma-separated):", font=("Arial", 12), bg="white").pack(pady=5)
        self.entry_initials = tk.Entry(self.calc_frame, font=("Arial", 12))
        self.entry_initials.pack(pady=5)
        tk.Label(self.calc_frame, text="Example: AM, FK, JD", font=("Arial", 10, "italic"), fg="gray", bg="white").pack()

        # Payment method
        tk.Label(self.calc_frame, text="Payment Method:", font=("Arial", 12), bg="white").pack(pady=5)
        self.payment_choice = tk.StringVar(value="Cash")
        payment_frame = tk.Frame(self.calc_frame, bg="white")
        payment_frame.pack(pady=3)
        tk.Radiobutton(payment_frame, text="Cash", variable=self.payment_choice, value="Cash", bg="white").grid(row=0, column=0, padx=20)
        tk.Radiobutton(payment_frame, text="Electronic", variable=self.payment_choice, value="Electronic", bg="white").grid(row=0, column=1, padx=20)

        # Buttons
        btn_frame = tk.Frame(self.calc_frame, bg="white")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Calculate", font=("Arial", 13, "bold"), bg="green", fg="white",
                  width=10, command=self.calculate_tip).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Clear", font=("Arial", 13, "bold"), bg="red", fg="white",
                  width=10, command=self.clear_all).grid(row=0, column=1, padx=10)

        # Result section
        tk.Label(self.calc_frame, text="✨ Thank you for patronising us! ✨",
                 font=("Arial", 10, "italic"), fg="green", bg="white").pack(pady=5)
        self.lbl_result = tk.Label(self.calc_frame, text="", font=("Arial", 10), justify="left",
                                   bg="white", relief="groove", padx=10, pady=10, width=50)
        self.lbl_result.pack(pady=10)

        # Bind entry edits to clear result
        for entry in [self.entry_bill, self.entry_people, self.entry_custom, self.entry_initials]:
            entry.bind("<KeyRelease>", self.clear_result_on_edit)

    def show_calculator_section(self, *args):
        selected = self.meal_choice.get()
        if selected != "Select a Meal":
            self.emoji_label.config(text=self.meal_emojis.get(selected, ""))
            self.calc_frame.pack(pady=10, fill="x")
        else:
            self.calc_frame.forget()
            self.emoji_label.config(text="")

    def calculate_tip(self):
        try:
            bill = float(self.entry_bill.get())
            if bill <= 0:
                raise ValueError("Bill must be greater than zero.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid bill amount.")
            return

        try:
            people = int(self.entry_people.get())
            if people <= 0:
                raise ValueError("People must be greater than zero.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of people.")
            return

        if self.tip_choice.get() == "custom":
            try:
                tip_percent = float(self.entry_custom.get())
                if tip_percent < 0:
                    raise ValueError("Tip must be non-negative.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid custom tip percentage.")
                return
        else:
            tip_percent = int(self.tip_choice.get())

        initials_input = self.entry_initials.get().strip()
        initials_list = [i.strip().upper() for i in initials_input.split(",") if i.strip()]
        if len(initials_list) != people:
            messagebox.showerror("Invalid Input",
                                 f"Number of initials ({len(initials_list)}) must match number of people ({people}).")
            return

        tip_amount = bill * tip_percent / 100
        total = bill + tip_amount
        per_person = total / people
        payment_method = self.payment_choice.get()
        selected_meal = self.meal_choice.get()

        # Random payer logic
        if payment_method == "Electronic":
            payer = random.choice(initials_list)
            payer_text = f"\n💳 Selected Payer: {payer}"
            cheer_text = f"\n🎉 Hooray! {payer} is treating everyone to {selected_meal} today! 🥳"
        else:
            payer_text = "\n💵 Everyone is paying their share today!"
            cheer_text = ""

        result_text = (
            f"🍽 Meal: {selected_meal}\n"
            f"Tip: £{tip_amount:.2f}\n"
            f"Total: £{total:.2f}\n"
            f"Per Person: £{per_person:.2f}\n"
            f"Payment Method: {payment_method}"
            f"{payer_text}{cheer_text}"
        )
        self.lbl_result.config(text=result_text, fg="darkblue", bg="#f0f8ff")

    def clear_all(self):
        self.meal_choice.set("Select a Meal")
        self.entry_bill.delete(0, tk.END)
        self.entry_people.delete(0, tk.END)
        self.entry_custom.delete(0, tk.END)
        self.entry_initials.delete(0, tk.END)
        self.tip_choice.set("10")
        self.payment_choice.set("Cash")
        self.lbl_result.config(text="", bg="white")
        self.emoji_label.config(text="")
        self.calc_frame.forget()
        self.show_calculator_section()

    def clear_result_on_edit(self, event):
        self.lbl_result.config(text="", bg="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = MealTipCalculator(root)
    root.mainloop()
