import json 
import os
import csv

data ={"budget":0, "expenses":[]}# kharcha haru ko lagi dictionary banako cha

if os.path.exists("expenses.json") and os.path.getsize("expenses.json") :#expenses.json list ma kharcha haru store huncha
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Error: The json file is corrupted or empty.") # yo mailya expenses.json file bata data hatauda error aako vayara exception haleko 

    

def save_data():# expenses.json ma kharcha haru save garna ko lagi
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=3)

def set_budget():# budget set garna ko lagi
    try:
        amount = float(input("Enter your monthly budget: "))
        data["budget"] = amount# budget set garna ko lagi
        save_data()
        print(f"Budget set to Rs{amount}.")
    except ValueError:
        print("Invalid amount. Please enter a Number.")


def add_expense():
    category = input("Enter the category: ")
    try:
        amount = float(input("Enter the amount: "))
        if amount > data ["budget"]:
            print("Expense exceeds budget. Please enter a valid amount.")
        data["expenses"].append({"category": category, "amount": amount})
        data["budget"] -= amount # kharcha haru budget bata ghatauna ko lagi
        save_data()
        print("Expense added successfully.")
    except ValueError:
        print("Invalid amount. Please enter a Number.")


def view_transactions():
    if not data["expenses"]:
        print("No expenses found.")
        return
    print("\nTransaction history:")
    for index, exp in enumerate(data["expenses"], start=1):
        print(f"{index}. {exp['category']}: Rs{exp['amount']}")

def view_categories():# category haru herna ko lagi
    if not data["expenses"]:
        print("No categories found. Please add expenses first.")
        return
    categories = set(exp['category'] for exp in data["expenses"])
    print("\nUsed Categories:")
    for index, cat in enumerate(categories, start=1):
        print(f"{index}. {cat}")

def filter_by_category():
    if not data["expenses"]:
        print("No expenses found.")
        return
    category = input("Enter the category to filter: ")
    filtered = [exp for exp in data["expenses"] if exp["category"].lower() == category.lower()]
    if not filtered:
        print(f"No expenses found for category: {category}")
    else:
        print(f"\nExpenses in category '{category}':")
        for index, exp in enumerate(filtered, start=1):
            print(f"{index}. Rs{exp['amount']}")

def total_expenses():
    total = sum(exp['amount'] for exp in data["expenses"])
    print(f"Total expenses: Rs{total}")
    print(f"Remaining budget: Rs{data["budget"]}")

def export_to_csv():
    if not data["expenses"]:
        print("No expenses to export.")
        return
    with open("expenses.csv", "w", newline="") as csvfile:
        fieldnames = ['category', 'amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for expense in data["expenses"]:
            writer.writerow(expense)

        writer.writerow({"category": "Remaining Budget", "amount": data["budget"]})
        writer.writerow({"category": "Total Expenses", "amount": sum(exp['amount'] for exp in data["expenses"])})
        print("Expenses exported to expenses.csv successfully.")
def main():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Set Monthly Budget")
        print("2. Add Expense")
        print("3. View Transaction History")
        print("4. Show Total Expenses and Remaining Budget")
        print("5. View Categories")
        print("6. Filter Expenses by Category")  
        print("7. Exit")

        choice = input("Enter your choice: ")
    
        if choice == "1":
            set_budget()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_transactions()
        elif choice == "4":
            total_expenses()
        elif choice == "5":
            view_categories()
        elif choice == "6":
            filter_by_category()
        elif choice == "7":
            print("Exiting the program.")
            export_to_csv() #directly exit huda csv save garna ko lagi
            break
            
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()# main function call garna ko lagi

    
# yo code ma kharcha haru add garna, dekhna, ra total dekhna ko lagi function haru banako cha.

#still in progress need to add the following features:
#1.Add a feature to export expenses to a CSV file.
#2.Implement a feature to filter expenses by category.
#3.Add a feature to set a budget and track expenses against it.
