import json
import os
from datetime import date

BUDGETS = {
    "Food": 300,
    "Gas": 150, 
    "Rent": 1200,
    "Subscriptions": 100
}

def add_expense(expenses):

    amount = float(input("Amount: "))
    category = input("Category: ").strip().title()
    description = input("Description: ")
    date_input = input("Date (YYYY-MM-DD, leave blank for today): ").strip()

    if date_input == "": 
        date_input = str(date.today())

    expense = {
        "amount": amount,
        "category": category,
        "date": date_input,
        "description": description
    }

    expenses.append(expense)
    print("Congratulations! Expense Added!")

def view_expenses(expenses):
    
    if not expenses:
        print("No responses yet.")
        return

    print("\nYour Expenses:")

    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['date']} | {exp['category']} | ${exp['amount']} | {exp['description']}")

def save_expenses(expenses, filename="expenses.json"):
    with open(filename, "w") as f:
        json.dump(expenses, f, indent=2)

def load_expenses(filename="expenses.json"):
    if not os.path.exists(filename):
        return []
    
    with open(filename, "r") as f:
        return json.load(f)

def monthly_summary(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    year = input("Enter year (YYYY): ").strip()
    month = input("Enter month (MM): ").strip().zfill(2)

    prefix = f"{year}-{month}"

    total = 0.0
    category_totals = {}

    for exp in expenses:
        if exp["date"].startswith(prefix):
            amt = float(exp["amount"])
            total += amt
            cat = exp["category"]
            category_totals[cat] = category_totals.get(cat, 0.0) + amt

    print(f"\nSummary for {prefix}")
    print(f"Total spent: ${total:.2f}")

    for cat, amt in category_totals.items():
        print(f"{cat}: ${amt:.2f}")

    print("\nBudget Check")
    for cat, spent in category_totals.items():
        if cat in BUDGETS and spent > BUDGETS[cat]:
            over = spent - BUDGETS[cat]
            print(f"{cat} over budget by ${over:.2f}")

    if total == 0:
        print("No expenses found for that month.")
        return

    print("\nBy category:")
    for cat in sorted(category_totals):
        print(f"- {cat}: ${category_totals[cat]:.2f}")

def delete_expense(expenses):
    if not expenses:
        print("No expenses to delete")
        return

    view_expenses(expenses)

    choice = input("\nEnter the expense number to delete (or blank to cancel): ").strip()
    if choice == "":
        return
    
    if not choice.isdigit():
        print("Please enter a valid number.")
        return
    
    idx = int(choice) - 1
    if idx < 0 or idx >= len(expenses):
        print("That number is out of range.")
        return
    
    deleted = expenses.pop(idx)
    print(f"Deleted: {deleted['date']} / {deleted['category']} / ${deleted['amount']} / {deleted['description']}")

expenses = load_expenses()

while True: 
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. Expenses List")
    print("3. Monthly Summary")
    print("4. Delete Expense")
    print("5. Exit")

    choice = input("Choose one of the options: ")

    if choice == "1":
        add_expense(expenses)

    elif choice == "2":
        view_expenses(expenses)         

    elif choice == "3":
        monthly_summary(expenses)

    elif choice == "4":
        delete_expense(expenses)

    elif choice == "5":
        save_expenses(expenses)
        print("Saved, Goodbye!")
        break

    else:
        print("Invalid choice, Please try again!")