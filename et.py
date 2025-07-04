import json 
import os
import csv
import datetime
import numpy as np
import pandas as pd

data ={"budget":0, "expenses":[], "loans":[]}# kharcha haru ko lagi dictionary banako cha

if os.path.exists("expenses.json") and os.path.getsize("expenses.json") :#expenses.json list ma kharcha haru store huncha
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
        if "loans" not in data:
            data["loans"] = []
    except json.JSONDecodeError:
        print("Error: The json file is corrupted or empty.") # yo mailya expenses.json file bata data hatauda error aako vayara exception haleko 


def  expenses_df():
    return pd.DataFrame(data["expenses"]) # expenses haru ko lagi pandas dataframe ma convert garna ko lagi


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
        
        if amount > data["budget"]:  # expenses exceeds vayo vane
            print("Expense exceeds budget!")
            choice = input("Do you want to take a loan from eSewa? (yes/no): ").strip().lower()
            if choice == "yes":
                loan_amount = float(input("Enter loan amount to cover the expense: "))
                
                data["loans"].append({
                    "amount": loan_amount,
                    "source": "eSewa",
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                data["budget"] += loan_amount
                print(f"Loan of Rs{loan_amount} taken from eSewa. New budget: Rs{data['budget']}\nNow again add expense.")
            else:
                print("Loan declined. Expense not added.")
                return
        else:
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data["expenses"].append({"category": category, "amount": amount, "timestamp": timestamp})
            data["budget"] -= amount
            print("Expense added successfully.")
        
        save_data()  # Save data after expense is added or loan is taken
    except ValueError:
        print("Invalid amount. Please enter a number.")


def view_loans():
    if not data["loans"]:
        print("No loans found.")
        return
    print("\nLoan history:")
    for index, loan in enumerate(data["loans"], start=1):
        print(f"{index}. Loan of Rs{loan['amount']} from {loan['source']} on {loan.get('timestamp', 'N/A')}")


def view_transactions():
    if not data["expenses"] and not data.get("loans"):
        print("No transactions found.")
        return
    print("\nTransaction history:")
    if data["expenses"]:
        print("\nExpenses:")
        for index, exp in enumerate(data["expenses"], start=1):
            print(f"{index}. {exp['category']}: Rs{exp['amount']} on {exp.get('timestamp', 'N/A')}")
    else:
        print("No expenses found.")
    if data.get("loans"):
        print("\nLoans:")
        for index, loan in enumerate(data["loans"], start=1):
            print(f"{index}. Loan of Rs{loan['amount']} from {loan['source']} on {loan.get('timestamp', 'N/A')}")
    else:
        print("")

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
    amount = [exp['amount'] for exp in data["expenses"]]
    if not amount:
        print("No expenses found.")
        return
    np_amount = np.array(amount)
    print(f"\nTotal Expenses: Rs{np_amount.sum()}")
    print(f"Average Expense: Rs{np_amount.mean()}")
    print(f"Maximum Expense: Rs{np_amount.max()}")
    print(f"Minimum Expense: Rs{np_amount.min()}")
    print(f"Remaining Budget: Rs{data['budget']}")


def delete_expense():
    if not data["expenses"]:
        print("no expenses found.")
        return
    view_transactions()
    try:
        index= int(input("Enter the index of the expense to delete: ")) - 1
        if 0<=index<len(data["expenses"]):
            deleted_expense = data["expenses"].pop(index)
            data["budget"] += deleted_expense["amount"]
            save_data()
            print("expese deleted successfully.")
        else:
            print("Invalid index. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_all_data():
    confirm = input("Are you sure you want to delete all transactions and loans? (yes/no): ")
    if confirm.lower() == "yes":
        total_returned = sum(exp["amount"] for exp in data["expenses"])
        data["budget"] = 0
        data["expenses"].clear()
        data["loans"] = []  
        save_data()

        if os.path.exists("expenses.csv"):
            os.remove("expenses.csv")
            print("expenses.csv file deleted.")

        print("All transactions and loans have been deleted.")
    else:
        print("Deletion cancelled.")


def edit_expense():
    if not data["expenses"]:
        print("No expenses found.")
        return
    view_transactions()
    try:
        index= int(input("Enter the index of the expense to edit: ")) - 1
        if 0<=index<len(data["expenses"]):
            orginal = data["expenses"][index]
            print(f"Original Expense: {orginal['category']}: Rs{orginal['amount']} on {orginal.get('timestamp', 'N/A')}")
            new_category = input("Enter new category (or press Enter to keep it unchanged): ")
            new_amount = input("Enter new amount (or press Enter to keep it unchanged): ")  

            if new_category:
                orginal["category"] = new_category
            if new_amount:
                new_amount = float(new_amount)
                data["budget"] += orginal["amount"] - new_amount
                data["budget"]-= new_amount
                orginal["amount"] = new_amount
            save_data()
            print("Expense updated successfully.")
        else:
            print("Invalid index. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")



def export_to_csv():
    if not data["expenses"]:
        print("No expenses to export.")
        return
    df= pd.DataFrame(data["expenses"])

    total_expenses = sum(exp['amount'] for exp in data["expenses"])
    remaining_budget = data["budget"]

    all_data = pd.DataFrame([
        {"category": "Total Expenses", "amount": total_expenses, "timestamp": ""},
        {"category": "Remaining Budget", "amount": remaining_budget, "timestamp": ""}
    ])
    final_df = pd.concat([df, all_data], ignore_index=True)
    
    final_df.to_csv("expenses.csv", index=False)
    print("Expenses exported to expenses.csv successfully.")



def main():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Set Monthly Budget")
        print("2. Add Expense")
        print("3. View Transaction History")
        print("4. Total Expenses ")
        print("5. View Categories")
        print("6. Filter Expenses by Category") 
        print("7. Edit Expense")
        print("8. Delete Expense")
        print("9. view loans")
        print("10. Reset All Data")
        print("11. Exit")

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
            edit_expense()
        elif choice == "8":
            delete_expense()
        elif choice == "9":
            view_loans()
        elif choice == "10":
            delete_all_data()
        elif choice == "11":
            print("Exiting the program.")
            export_to_csv() #directly exit huda csv save garna ko lagi
            break
            
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()# main function call garna ko lagi

    
# yo code ma kharcha haru add garna, dekhna, ra total dekhna ko lagi function haru banako cha.

#still in progress need to add the following features:
#1.Add a feature to export expenses to a CSV file. (finished)
#2.Implement a feature to filter expenses by category.(finished)
#3.Add a feature to set a budget and track expenses against it.(finished)
#4.Implement a feature to view total expenses and remaining budget through csv.(finished)

