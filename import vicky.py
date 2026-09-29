import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")


def validate_category(category):
    category = category.strip()
    if not category:
        raise ValueError("Category cannot be empty.")
    return category


def validate_amount(amount):
    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return amount


def validate_date(date):
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Invalid date. Please use DD-MM-YYYY format.")
    return date


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [tuple(expense) for expense in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def category_summary(expenses):
    summary = {}
    for category, amount, date in expenses:
        summary[category] = summary.get(category, 0) + amount
    return summary


def daily_summary(expenses):
    summary = {}
    for category, amount, date in expenses:
        summary[date] = summary.get(date, 0) + amount
    return summary


def highest_spending_category(expenses):
    summary = category_summary(expenses)
    return max(summary, key=summary.get) if summary else None


def total_spending(expenses):
    return sum(amount for category, amount, date in expenses)


def format_amount(amount):
    return f"{amount:.2f}"


def print_title(title):
    print("=" * 50)
    print(title.center(50))
    print("=" * 50)


def add_expense(expenses):
    try:
        category = validate_category(input("Enter category: "))
        amount = validate_amount(input("Enter amount: "))
        date = validate_date(input("Enter date (DD-MM-YYYY): "))
        expenses.append((category, amount, date))
        save_expenses(expenses)
        print("\nExpense added successfully!")
    except ValueError as error:
        print(f"\nError: {error}")


def view_expenses(expenses):
    if not expenses:
        print("\nNo expenses found.")
        return
    print("\n----- ALL EXPENSES -----")
    for index, (category, amount, date) in enumerate(expenses, start=1):
        print(f"{index}. {category} | ₹{format_amount(amount)} | {date}")


def search_by_category(expenses):
    category = input("\nEnter category to search: ").strip().lower()
    results = [expense for expense in expenses if expense[0].lower() == category]
    if not results:
        print("\nNo expenses found for this category.")
        return
    print(f"\n----- EXPENSES: {category} -----")
    for category_name, amount, date in results:
        print(f"{category_name} | ₹{format_amount(amount)} | {date}")


def show_category_summary(expenses):
    summary = category_summary(expenses)
    if not summary:
        print("\nNo expenses available.")
        return
    print("\n----- CATEGORY SUMMARY -----")
    for category, amount in summary.items():
        print(f"{category}: ₹{format_amount(amount)}")


def show_daily_summary(expenses):
    summary = daily_summary(expenses)
    if not summary:
        print("\nNo expenses available.")
        return
    print("\n----- DAILY SUMMARY -----")
    for date, amount in summary.items():
        print(f"{date}: ₹{format_amount(amount)}")


def show_highest_category(expenses):
    category = highest_spending_category(expenses)
    if category is None:
        print("\nNo expenses available.")
        return
    summary = category_summary(expenses)
    print(f"\nHighest spending category: {category}")
    print(f"Amount spent: ₹{format_amount(summary[category])}")


def delete_expense(expenses):
    if not expenses:
        print("\nNo expenses available.")
        return
    view_expenses(expenses)
    try:
        number = int(input("\nEnter expense number to delete: "))
        if number < 1 or number > len(expenses):
            raise IndexError("Invalid expense number.")
        deleted = expenses.pop(number - 1)
        save_expenses(expenses)
        print(f"\nDeleted: {deleted[0]} | ₹{format_amount(deleted[1])} | {deleted[2]}")
    except ValueError:
        print("\nPlease enter a valid number.")
    except IndexError as error:
        print(f"\nError: {error}")


def main():
    expenses = load_expenses()
    while True:
        print()
        print_title("SMART DAILY EXPENSE TRACKER")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search by Category")
        print("4. Category-wise Summary")
        print("5. Daily Summary")
        print("6. Show Highest Spending Category")
        print("7. Delete Expense")
        print("8. Show Total Spending")
        print("9. Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            search_by_category(expenses)
        elif choice == "4":
            show_category_summary(expenses)
        elif choice == "5":
            show_daily_summary(expenses)
        elif choice == "6":
            show_highest_category(expenses)
        elif choice == "7":
            delete_expense(expenses)
        elif choice == "8":
            print(f"\nTotal Spending: ₹{format_amount(total_spending(expenses))}")
        elif choice == "9":
            print("\nThank you for using Smart Daily Expense Tracker!")
            break
        else:
            print("\nInvalid choice. Please select 1-9.")


if __name__ == "__main__":
    main()