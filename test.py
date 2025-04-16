import json 
import os

expenses = [] 
if os.path.exists("expenses.json") :#expenses.json list ma kharcha haru store huncha
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except json.JSONDecodeError:
        print("Error: The json file is corrupted or empty.") # yo mailya expenses.json file bata data hatauda error aako vayara exception haleko 

    

def save_expenses():# expenses.json ma kharcha haru save garna ko lagi
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=3)

def add_expense(expense):# kharcha haru add garna ko lagi
    category = input("Enter the category: ")# category ko lagi input lincha
    try:
        amount = float(input("Enter the amount: "))
    except ValueError:
        print("Invalid amount. Please enter a Number.")
        return
    expense.append({"category": category, "amount": amount})
    save_expenses()
    print("Expense added successfully!")# kharcha haru add vayo.

def view_transactions():# kharcha haru dekhna ko lagi
    if not expenses:
        print("No expenses found.")
        return
    print("\nTransaction history:")
    for index, exp in enumerate(expenses, start=1):
        print(f"{index}. {exp['category']}: Rs{exp['amount']}")

def total_expenses():# kharcha haru ko total dekhna ko lagi
    total = sum(exp['amount'] for exp in expenses)
    print(f"Total expenses: Rs{total}")

def main():# main function ko lagi
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Transaction History")
        print("3. Show Total Expenses")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            total_expenses()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()# main function call garna ko lagi
# yo code ma kharcha haru add garna, dekhna, ra total dekhna ko lagi function haru banako cha.

#still in progress nedd to add the following features:
# 1. Add a feature to delete an expense.
# 2. Add a feature to edit an expense.
# 3. Add a feature to filter expenses by category.
# 4. Excepltion handling for file operations.
